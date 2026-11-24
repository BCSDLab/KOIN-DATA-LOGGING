import json
import html
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def slack_text(environment, start, end, report):
    title = '[Stage]' if environment == 'stage' else '[Prod]'
    lines = [f'{title} 주간 로깅 검수 · {start[5:]}~{end[5:]}']
    if not report.get('complete'):
        lines.append('⚠️ 검수 불완전 · 로그 집계 불가')
        diagnostic = report.get('source_diagnostics') or {}
        if diagnostic.get('http_status') == 404:
            reason = 'Notion 원본 페이지 접근 실패 (404)'
        elif diagnostic.get('code') == 'root_not_unique':
            reason = '연결된 Event Log 원본을 하나로 지정해야 합니다'
        elif report.get('failure_type') == 'IncompleteSource':
            reason = 'Notion 명세 전체 수집 실패'
        else:
            reason = report.get('failure_type', '수집 범위 미확인')
        lines += ['원인: ' + html.escape(reason), 'iOS·Android·Web 모두 판정 미확인']
    else:
        lines += ['✅ 비교 완료 | DA1·DA2 + CAMPUS·BUSINESS·USER',
                  '문제 label 수', '```', '             미등록 / 과거 / 명세 불일치']
        for platform, name in (('IOS', 'iOS'), ('ANDROID', 'Android'), ('WEB', 'Web')):
            stats = report.get('platform_summary', {}).get(platform)
            if stats is None:
                lines.append(name + ': 판정 미확인')
                continue
            groups = stats['categories']
            counts = [groups.get(c, {}).get('labels', 0) for c in
                      ('unregistered', 'legacy_logging', 'current_mismatch')]
            lines.append(f"{name:<12} {counts[0]:>6} / {counts[1]:>4} / {counts[2]:>11}")
        lines.append('```')
        zero = [name for p, name in (('IOS', 'iOS'), ('ANDROID', 'Android'), ('WEB', 'Web'))
                if report.get('platform_summary', {}).get(p, {}).get('events') == 0]
        if zero:
            lines.append('수집 0건: ' + '·'.join(zero))
        agent = report.get('agent', {})
        ai = 'AI 조사 완료' if agent.get('status') == 'completed' else 'AI 추가 조사 미확인'
        lines.append(f"전체 수집 {report.get('events', 0):,}건 · {ai}")
        findings = sorted(report.get('findings', []), key=lambda x: -x.get('count', 0))
        examples = list(dict.fromkeys(x['label'] for x in findings))[:3]
        if examples:
            lines.append('문제 label 예시: ' + ', '.join(html.escape(x.replace('`', '')[:110]) for x in examples))
        revision = report.get('source_revision')
        if revision:
            lines.append('기준: GitHub main · ' + revision[:7])
    if report.get('detail_url'):
        lines.append('상세 결과: ' + report['detail_url'])
    return '\n'.join(lines)


def slack_payload(environment, start, end, report):
    """Native Slack table avoids Korean/Latin monospace alignment differences."""
    text = slack_text(environment, start, end, report)
    blocks = [dict(type='header', text=dict(type='plain_text', text=('[Stage]' if environment == 'stage' else '[Prod]') + ' 주간 로깅 검수')),
              dict(type='context', elements=[dict(type='mrkdwn', text=f'{start} ~ {end} · KST')])]
    def section(value):
        blocks.append(dict(type='section', text=dict(type='mrkdwn', text=value)))
    if report.get('complete'):
        section('*규칙 비교 완료* · DA1·DA2 / CAMPUS·BUSINESS·USER')
        rows = [[dict(type='raw_text', text=x) for x in ('플랫폼', '미등록', '과거', '명세 불일치')]]
        for platform, name in (('IOS', 'iOS'), ('ANDROID', 'Android'), ('WEB', 'Web')):
            stats = report.get('platform_summary', {}).get(platform)
            counts = [str(stats['categories'].get(c, {}).get('labels', 0)) if stats else '미확인'
                      for c in ('unregistered', 'legacy_logging', 'current_mismatch')]
            rows.append([dict(type='raw_text', text=x) for x in [name] + counts])
        blocks.append(dict(type='table', column_settings=[dict(align='left')] + [dict(align='right') for _ in range(3)], rows=rows))
        agent = report.get('agent', {})
        ai = 'AI 조사 완료' if agent.get('status') == 'completed' else 'AI 조사 실패: ' + agent.get('failure_code', agent.get('failure_type', '미확인'))
        section(f"수집 *{report.get('events', 0):,}건* · {html.escape(ai)}\n숫자는 문제 label 수이며, 항목 간 중복될 수 있습니다.")
        examples = []
        for category, name in (('unregistered', '미등록'), ('legacy_logging', '과거'), ('current_mismatch', '명세 불일치')):
            items = [x for x in report.get('findings', []) if x.get('category') == category]
            items.sort(key=lambda x: -x.get('count', 0))
            if items:
                label = html.escape(items[0]['label'].replace('`', '')[:120])
                examples.append(f'• {name}: `{label}`')
        if examples:
            section('*확인할 label 예시*\n' + '\n'.join(examples))
    else:
        missing = report.get('missing_daily_tables', [])
        if missing:
            dates = [x.removeprefix('events_') for x in missing]
            reason = f"일별 데이터 {len(dates)}일 누락: " + ', '.join(dates[:10])
        elif report.get('failure_type') == 'IncompleteSource':
            reason = 'GitHub 명세 전체 수집 실패'
        else:
            reason = report.get('failure_type') or '조회 범위 확인 필요'
        section('*검수 불완전*\n' + html.escape(reason))
        observed = report.get('events')
        section((f'현재 조회 {observed:,}건 · ' if observed is not None else '') + 'iOS·Android·Web 최종 판정 보류')
    revision = report.get('source_revision')
    if revision:
        blocks.append(dict(type='context', elements=[dict(type='mrkdwn', text='기준: GitHub main · `' + revision[:7] + '`')]))
    if report.get('detail_url'):
        section('<' + report['detail_url'] + '|상세 결과 보기>')
    return dict(text=text, blocks=blocks, unfurl_links=False, unfurl_media=False)


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
