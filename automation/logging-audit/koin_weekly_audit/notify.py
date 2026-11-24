import json
import html
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


REASONS = {
    'event_label_missing': 'event_label 누락', 'unregistered_label': '명세에 없는 label',
    'historical_label_still_collected': '과거 명세 label 수집', 'legacy_event_name': '과거 event_name 수집',
    'specification_conflict': '명세 충돌·미확정 — 담당자 확인 필요',
    'event_name_mismatch': 'event_name 불일치', 'screen_view_mismatch': 'screen_view 불일치',
    'event_category_mismatch': 'event_category 불일치', 'platform_mismatch': '지원 플랫폼 불일치',
    'value_missing': '필수 value 누락', 'fixed_value_mismatch': '고정 value 불일치',
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


def slack_text(environment, start, end, report):
    title = '[Stage]' if environment == 'stage' else '[Prod]'
    lines = [f'{title} 주간 로깅 검수 · {start[5:]}~{end[5:]}'] + notification_sections(report)
    if report.get('detail_url'):
        lines.append('상세보기: ' + report['detail_url'])
    return '\n'.join(lines)


def slack_payload(environment, start, end, report):
    blocks = [dict(type='header', text=dict(type='plain_text', text=('[Stage]' if environment == 'stage' else '[Prod]') + ' 주간 로깅 검수')),
              dict(type='context', elements=[dict(type='mrkdwn', text=f'{start} ~ {end} · KST')])]
    for section in notification_sections(report):
        # Each platform is independent; never show AI failure as an event error.
        blocks.append(dict(type='section', text=dict(type='mrkdwn', text=section[:2900])))
    if report.get('detail_url'):
        blocks.append(dict(type='section', text=dict(type='mrkdwn', text='<' + report['detail_url'] + '|상세보기>')))
    return dict(text=slack_text(environment, start, end, report), blocks=blocks, unfurl_links=False, unfurl_media=False)


def detail_markdown(reports):
    lines = ['# 주간 로깅 검수', '', '기준: GitHub main의 전체 현행·과거 명세. DA1·DA2 및 CAMPUS·BUSINESS·USER를 플랫폼별 대조합니다.',
             '미관측 명세는 오류로 판정하지 않습니다. 동적 value는 존재 여부만 검사합니다. 구버전 적용 시점과 명세 충돌은 담당자 확인 대상입니다.', '']
    lines += ['## 문제 로그 바로가기', '']
    for env, report in reports.items():
        title = 'Stage' if env == 'stage' else 'Prod'
        links = ['[' + name + ' (' + str(len(platform_findings(report, platform))) + '개 항목)](#audit-' + env + '-' + platform.lower() + ')' for platform, name in PLATFORM_NAMES]
        lines += ['**' + title + '**: ' + ' · '.join(links), '']
    for env, report in reports.items():
        lines += ['## ' + env, '', '기간: ' + report['start'] + ' ~ ' + report['end'],
                  '명세 커밋: `' + report.get('source_revision', '미확인') + '`', '']
        if not report.get('complete'):
            lines += notification_sections(report) + ['']
        for platform, name in PLATFORM_NAMES:
            findings = platform_findings(report, platform)
            lines += ['<a name="audit-' + env + '-' + platform.lower() + '"></a>', '', '### ' + ('Stage' if env == 'stage' else 'Prod') + ' · ' + name, '']
            if not findings:
                stats = report.get('platform_summary', {}).get(platform)
                lines += [('이상 없음' if report.get('complete') and stats and stats['events'] else '판정 대상 없음 또는 조회 불완전'), '']
                continue
            lines += ['**아래는 실제 수집에서 확인된 전체 문제 목록입니다.** 같은 label의 필드별 문제는 각각 표시합니다.', '', '| event_label | 확인 사항 | 명세 기준 | 실제 수집 | 수집 건수 | 앱 버전 | 명세 |', '| --- | --- | --- | --- | ---: | --- | --- |']
            for f in findings:
                refs = ' · '.join('[명세](' + u + ')' for u in f.get('specification_urls', []) if u.startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/')) or '등록된 명세 없음'
                versions = ', '.join(f.get('platform_versions', {}).get(platform, []))
                expected = ', '.join(f.get('expected_values', [])) or '등록된 현행 계약 없음 또는 명세 확인 필요'
                actual = ', '.join(f.get('platform_observed_values', {}).get(platform, [])) or '확인 필요'
                cells = [safe(f['label']), safe(REASONS.get(f['reason'], f['reason'])), safe(expected), safe(actual), str(f.get('platform_counts', {}).get(platform, 0)), safe(versions), refs]
                lines.append('| ' + ' | '.join(c.replace('|', '&#124;') for c in cells) + ' |')
            lines += ['']
        previous = report.get('previous_period_recheck', {})
        lines += ['이전 기간 재검사: ' + ('완료' if previous.get('complete') else '불완전') + ' · 누락 ' + ', '.join(previous.get('missing_daily_tables', [])),
                  'AI 추가 조사: ' + report.get('agent', {}).get('status', '미확인') + ' · ' + report.get('agent', {}).get('failure_type', ''), '']
    return '\n'.join(lines)


def send_once(webhook, text, receipt):
    parsed = urllib.parse.urlparse(webhook)
    if parsed.scheme != 'https' or parsed.hostname != 'hooks.slack.com' or not parsed.path.startswith('/services/') or parsed.query:
        raise ValueError('Invalid Slack webhook destination')
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(receipt, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return json.loads(receipt.read_text(encoding='utf8'))
    with os.fdopen(fd, 'w', encoding='utf8') as f:
        json.dump({'status': 'delivery_unknown', 'reason': 'attempt_reserved'}, f)
    req = urllib.request.Request(webhook, data=json.dumps(text if isinstance(text, dict) else {'text': text}, ensure_ascii=False).encode('utf8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    result = {'status': 'delivery_unknown'}
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read(128).decode()
            if response.status == 200 and body.strip() == 'ok':
                result = {'status': 'sent'}
    except urllib.error.HTTPError as exc:
        result = {'status': 'rejected' if exc.code < 500 else 'delivery_unknown', 'http_status': exc.code}
    except OSError:
        pass
    # Never persist the webhook, raw exception text, IDs or event values.
    tmp = receipt.with_suffix('.tmp')
    tmp.write_text(json.dumps(result), encoding='utf8')
    tmp.replace(receipt)
    return result
