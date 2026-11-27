import json
import hashlib
import html
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from .environment_evidence import compare_environments
from .handoff import developer_handoff


REASONS = {
    'event_label_missing': 'event_label 누락', 'unregistered_label': '명세에 없는 label',
    'historical_label_still_collected': '과거 명세 label 수집', 'legacy_event_name': '과거 event_name 수집',
    'specification_conflict': '명세 충돌·미확정 — 담당자 확인 필요',
    'event_name_mismatch': 'event_name 불일치', 'unexpected_event_name':'예상하지 않은 event_name', 'screen_view_mismatch': 'screen_view 불일치',
    'event_category_mismatch': 'event_category 불일치', 'platform_mismatch': '지원 플랫폼 불일치',
    'value_missing': '필수 value 누락', 'fixed_value_mismatch': '고정 value 불일치', 'enum_value_mismatch': '허용 value 불일치',
    'duplicate_parameter_key': '파라미터 키 중복',
}
PLATFORM_NAMES = (('IOS', 'iOS'), ('ANDROID', 'Android'), ('WEB', 'Web'))


def safe(value):
    return html.escape(str(value).replace('`', '').replace('\n', ' ')[:160])


def platform_findings(report, platform):
    return sorted((f for f in report.get('findings', []) if platform in f.get('platforms', [])),
                  key=lambda f: (-f.get('platform_counts', {}).get(platform, 0), f['label'], f['reason']))


def notification_sections(report):
    if not report.get('complete'):
        missing = report.get('missing_daily_tables', [])
        reason = ('일별 데이터 누락: ' + ', '.join(x.removeprefix('events_') for x in missing)) if missing else (
            'GitHub 명세 수집 실패' if report.get('failure_type') == 'IncompleteSource' else report.get('failure_type') or '조회 범위 미확인')
        return ['⚠️ 검수 불완전 · ' + safe(reason), 'iOS·Android·Web: 판정 불가']
    lines = []
    for platform, name in PLATFORM_NAMES:
        target = report.get('version_scope', {}).get('targets', {}).get(platform)
        name = name + (' ' + target if target else '')
        stats = report.get('platform_summary', {}).get(platform)
        findings = platform_findings(report, platform)
        if stats is None:
            lines.append(name + ': 판정 불가')
        elif not stats['events']:
            lines.append(name + ': 수집 0건 · 판정 대상 없음')
        elif not findings:
            lines.append(name + ': 이상 없음')
        else:
            labels = list(dict.fromkeys(f['label'] for f in findings))
            lines.append(f'{name}: 이상·확인 필요 {len(labels)}개 label')
    return lines


def audit_context(report):
    source = {'notion': 'Notion', 'github': 'GitHub main'}.get(report.get('source_kind'), '미확인')
    lines = ['명세 기준: ' + source]
    if source == 'GitHub main':
        lines[-1] += ' · Notion 직접 대조 미실행'
    status = report.get('agent', {}).get('status')
    lines.append('AI 추가 조사: ' + ('완료' if status == 'completed' else '미완료 · 규칙 검수 결과와 별도'))
    if status != 'completed' and report.get('agent', {}).get('failure_diagnostics', {}).get('category') == 'quota':
        lines.append('AI API: 사용량·결제 한도 확인 필요')
    debug = report.get('normalization', {}).get('android_debug_events', 0)
    if debug:
        lines.append('Android 디버그 ' + str(debug) + '건: 접미사 제외 후 명세 대조')
    return lines


def slack_text(environment, start, end, report):
    title = '[Stage]' if environment == 'stage' else '[Prod]'
    lines = [f'{title} 주간 로깅 검수 · {start[5:]}~{end[5:]}'] + notification_sections(report) + audit_context(report)
    if report.get('detail_url'):
        lines.append('상세보기: ' + report['detail_url'])
    return '\n'.join(lines)


def slack_payload(environment, start, end, report):
    blocks = [dict(type='header', text=dict(type='plain_text', text=('[Stage]' if environment == 'stage' else '[Prod]') + ' 주간 로깅 검수')),
              dict(type='context', elements=[dict(type='mrkdwn', text=f'{start} ~ {end} · KST')])]
    for section in notification_sections(report):
        # Each platform is independent; never show AI failure as an event error.
        blocks.append(dict(type='section', text=dict(type='mrkdwn', text=section[:2900])))
    blocks.append(dict(type='context', elements=[dict(type='mrkdwn', text='\n'.join(audit_context(report)))]))
    if report.get('detail_url'):
        blocks.append(dict(type='section', text=dict(type='mrkdwn', text='<' + report['detail_url'] + '|상세보기>')))
    return dict(text=slack_text(environment, start, end, report), blocks=blocks, unfurl_links=False, unfurl_media=False)


def detail_markdown(reports):
    lines = ['# 주간 로깅 검수', '', '기준: GitHub main의 전체 현행·과거 명세. DA1·DA2 및 CAMPUS·BUSINESS·USER를 플랫폼별 대조합니다.',
             '미관측 명세는 오류로 판정하지 않습니다. 동적 value는 존재 여부만 검사합니다. 구버전 적용 시점과 명세 충돌은 담당자 확인 대상입니다.', '']
    lines += ['## 문제 로그 바로가기', '', '[Stage · Prod 실제 수집 비교](#user-content-audit-environments) · [개발자 전달용 상세](#user-content-developer-handoff)', '']
    for env, report in reports.items():
        title = 'Stage' if env == 'stage' else 'Prod'
        links = ['[' + name + ' (' + str(len(platform_findings(report, platform))) + '개 항목)](#user-content-audit-' + env + '-' + platform.lower() + ')' for platform, name in PLATFORM_NAMES]
        lines += ['**' + title + '**: ' + ' · '.join(links) + ' · [실제 value 수집 현황](#user-content-values-' + env + ')', '']
    for env, report in reports.items():
        lines += ['## ' + env, '', '기간: ' + report['start'] + ' ~ ' + report['end'],
                  '명세 커밋: `' + (report.get('source_revision') or '미확인') + '`',
                  'BigQuery 조회 job: `' + str(report.get('query_job_id') or '미확인') + '`', '']
        lines += audit_context(report) + ['']
        agent = report.get('agent', {})
        if agent.get('failure_diagnostics'):
            diagnostic = agent['failure_diagnostics']
            lines += ['AI 진단: ' + safe(diagnostic.get('category')) +
                      ' · HTTP ' + safe(diagnostic.get('http_status')) +
                      ' · API code ' + safe(diagnostic.get('api_code')), '']
        if agent.get('status') == 'completed':
            lines += ['### AI 추가 조사 (원인 가설)', '']
            for note in agent.get('analysis', {}).get('investigations', []):
                for key, title in (('observation', '관측'), ('hypothesis', '원인 가설'), ('next_action', '확인할 사항')):
                    lines.append('- ' + title + ': ' + html.escape(str(note.get(key, ''))).replace('\n', ' '))
                lines.append('- 근거: ' + ', '.join(safe(ref) for ref in note.get('evidence_ids', [])))
            for limitation in agent.get('analysis', {}).get('limitations', []):
                lines.append('- 조사 한계: ' + html.escape(str(limitation)).replace('\n', ' '))
            lines += ['근거별 집계는 해당 환경의 agent.json 및 report.json에 보존됩니다.', '']
        if not report.get('complete'):
            lines += notification_sections(report) + ['']
        for platform, name in PLATFORM_NAMES:
            findings = platform_findings(report, platform)
            target = report.get('version_scope', {}).get('targets', {}).get(platform)
            name = name + (' ' + target if target else '')
            lines += ['<a name="audit-' + env + '-' + platform.lower() + '"></a>', '', '### ' + ('Stage' if env == 'stage' else 'Prod') + ' · ' + name, '']
            if not findings:
                stats = report.get('platform_summary', {}).get(platform)
                lines += [('이상 없음' if report.get('complete') and stats and stats['events'] else '판정 대상 없음 또는 조회 불완전'), '']
                continue
            lines += ['**아래는 실제 수집에서 확인된 전체 문제 목록입니다.** 같은 label의 필드별 문제는 각각 표시합니다.', '', '| event_label | 확인 사항 | 명세 기준 | 실제 수집 | 수집 건수 | 앱 버전 | 명세 |', '| --- | --- | --- | --- | ---: | --- | --- |']
            for f in findings:
                refs = ' · '.join('[명세](' + u + ')' for u in f.get('specification_urls', []) if u.startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/')) or '등록된 명세 없음'
                versions = ', '.join(f.get('platform_versions', {}).get(platform, []))
                expected = ', '.join(f.get('platform_expected_values', {}).get(platform, f.get('expected_values', []))) or '등록된 현행 계약 없음 또는 명세 확인 필요'
                source = f.get('platform_value_source', {}).get(platform)
                if source:
                    raw = '; '.join(x['raw_text'] for x in source['sources']) or ('해당 label·플랫폼의 현행 계약 연결 없음' if source['status']=='no_current_contract' else '원문 value 추출 미확인 — 명세 확인 필요')
                    expected = 'GitHub 원문: ' + raw + ' / 자동 판정 기준: ' + expected
                actual_counts = f.get('platform_value_counts', {}).get(platform, {})
                actual = '; '.join(str(v) + ' (' + str(n) + '건)' for v, n in sorted(actual_counts.items())) if actual_counts else ', '.join(f.get('platform_observed_values', {}).get(platform, [])) or '확인 필요'
                cells = [safe(f['label']), safe(REASONS.get(f['reason'], f['reason'])), html.escape(expected).replace('\n',' '), html.escape(actual).replace('\n',' '), str(f.get('platform_counts', {}).get(platform, 0)), safe(versions), refs]
                lines.append('| ' + ' | '.join(c.replace('|', '&#124;') for c in cells) + ' |')
            lines += ['']
        lines += ['<a name="values-' + env + '"></a>', '', '### 실제 value 수집 현황 (이상 여부와 별도)', '', '검수 범위에 실제 수집된 모든 label의 value 상태와 값별 건수입니다. value 미지정은 오류가 아니며, 파라미터 없음·NULL·빈 문자열·문자열 null을 구분합니다. 민감정보 가능 패턴은 가립니다. 가로 스크롤 없이 label별로 명세와 실제 값을 읽을 수 있습니다.', '']
        for row in report.get('value_collection', []):
            values = '; '.join(str(v) + ' (' + str(n) + '건)' for v,n in sorted(row['actual'].items()))
            escape = lambda v: html.escape(str(v)).replace('\n',' ')
            source = row.get('source', {})
            raw = '; '.join(x['raw_text'] for x in source.get('sources', [])) or ('해당 label·플랫폼의 현행 계약 연결 없음' if source.get('status')=='no_current_contract' else '원문 value 추출 미확인 — 명세 확인 필요')
            source_links = ' · '.join('[원문 ' + str(x['line']) + '행](' + x['url'] + ')' for x in source.get('sources', []) if x['url'].startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/'))
            lines += ['#### [' + escape(row['platform']) + '] ' + escape(row['label']), '', '- GitHub 원문 value 표기: ' + escape(raw), '- 원문 출처: ' + (source_links or '현행 계약·원문 구조 확인 필요'), '- 자동 판정 기준: ' + escape(', '.join(row['expected'])), '- 실제 value: ' + escape(values), '- 총 수집: ' + str(row['events']) + '건 · 앱 버전: ' + escape(', '.join(row['versions'])), '']
        if not report.get('value_collection'):
            lines += ['관측 없음 또는 조회 불완전']
        lines += ['']
        scope = report.get('version_scope', {})
        lines += ['### 구버전·기타 버전 참고 (이상 판정 제외)', '', '모바일 검수 기준은 담당자가 확인한 버전입니다. Web은 전체 수집을 검사합니다. 구버전 및 기준 외 버전은 아래 집계로만 보존하며 AI 조사와 이상 알림에서 제외합니다.', '', '| 플랫폼 | 버전 | 구분 | 수집 건수 | label 수 |', '| --- | --- | --- | ---: | ---: |']
        for row in scope.get('reference', []):
            kind = {'older':'구버전', 'newer_or_other':'기준보다 높은 버전·기타 빌드', 'unknown':'버전 미확인'}[row['classification']]
            lines.append('| ' + ' | '.join([safe(row['platform']), safe(row['app_version']), kind, str(row['events']), str(row['labels'])]) + ' |')
        if not scope.get('reference'):
            lines += ['| — | — | 참고 집계 없음 | 0 | 0 |']
        lines += ['']
        previous = report.get('previous_period_recheck', {})
        lines += ['이전 기간 재검사: ' + ('완료' if previous.get('complete') else '불완전') + ' · 누락 ' + ', '.join(previous.get('missing_daily_tables', [])),
                  'AI 추가 조사: ' + report.get('agent', {}).get('status', '미확인') + ' · ' + report.get('agent', {}).get('failure_type', ''), '']
    comparison = compare_environments(reports)
    lines += ['<a name="audit-environments"></a>', '', '## Stage · Prod 실제 수집 비교', '']
    if not comparison['complete']:
        lines += ['비교 불완전: ' + comparison['reason']]
    else:
        lines += ['동일 기간·동일 명세의 같은 label·플랫폼에서 관측한 값 집합을 비교합니다. 건수 차이는 오류로 판정하지 않습니다. 값 차이는 사용 동작·기준 버전 차이 때문일 수 있어 검토 대상이며, 양쪽 값이 같아도 명세에 맞는지는 위 환경별 검수로 판단합니다. 동적 value는 제외합니다.', '',
            '양쪽 관측 ' + str(comparison['common_labels']) + '개 · 비교 대상 필드의 관측 값 동일 ' + str(comparison['same_observed_labels']) + '개 · Stage만 관측 ' + str(comparison['stage_only']) + '개 · Prod만 관측 ' + str(comparison['production_only']) + '개 · 민감정보 가림으로 값 비교 제외 ' + str(comparison['masked_fields']) + '개 필드 (label·플랫폼 조합)', '',
            '| 플랫폼 | event_label | 필드 | 명세 | Stage 실제 값 (건수) | Prod 실제 값 (건수) |', '| --- | --- | --- | --- | --- | --- |']
        for row in comparison['differences']:
            values = lambda counts: '; '.join(str(v) + ' (' + str(n) + '건)' for v,n in sorted(counts.items()))
            cells = [row['platform'], row['label'], row['field'], ', '.join(row['expected']) or '현행 명세 없음', values(row['stage']), values(row['production'])]
            lines += ['| ' + ' | '.join(html.escape(str(c)).replace('\n',' ').replace('|','&#124;') for c in cells) + ' |']
        if not comparison['differences']:
            lines += ['| — | — | — | ' + ('관측한 비교 대상 필드에서 값 차이 없음' if comparison['common_labels'] else '양쪽 공통 관측 없어 비교 대상 없음') + ' | — | — |']
    lines += ['', developer_handoff(reports, REASONS)]
    return '\n'.join(lines)


def send_once(webhook, text, receipt):
    parsed = urllib.parse.urlparse(webhook)
    if parsed.scheme != 'https' or parsed.hostname != 'hooks.slack.com' or not parsed.path.startswith('/services/') or parsed.query:
        raise ValueError('Invalid Slack webhook destination')
    receipt = Path(receipt)
    payload = json.dumps(text if isinstance(text, dict) else {'text': text}, ensure_ascii=False, sort_keys=True).encode('utf8')
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(receipt, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        result = json.loads(receipt.read_text(encoding='utf8'))
        return dict(result, reused=True, payload_matches=result.get('payload_sha256') == payload_sha256)
    with os.fdopen(fd, 'w', encoding='utf8') as f:
        json.dump({'status': 'delivery_unknown', 'reason': 'attempt_reserved'}, f)
    req = urllib.request.Request(webhook, data=payload,
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    result = {'status': 'delivery_unknown', 'payload_sha256': payload_sha256}
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read(128).decode()
            if response.status == 200 and body.strip() == 'ok':
                result.update(status='sent', sent_at=datetime.now(timezone.utc).isoformat())
    except urllib.error.HTTPError as exc:
        result.update(status='rejected' if exc.code < 500 else 'delivery_unknown', http_status=exc.code)
    except OSError:
        pass
    # Never persist the webhook, raw exception text, IDs or event values.
    tmp = receipt.with_suffix('.tmp')
    tmp.write_text(json.dumps(result), encoding='utf8')
    tmp.replace(receipt)
    return result

