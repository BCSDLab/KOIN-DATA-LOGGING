import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def slack_text(environment, start, end, report):
    title = '[Stage]' if environment == 'stage' else '[Prod]'
    lines = [f'{title} 주간 로깅 검수 · DA1/DA2', f'기간: {start} ~ {end} (KST)',
             '명세: 최신 Notion Event Log · WEB/ANDROID/IOS',
             '상태: ' + ('검수 불완전' if not report.get('complete') else '비교 완료 · 최신 명세 기준'),
             f"수집 {report.get('events', 0):,}건 / {report.get('observed_labels', 0)}개 label",
             f"불일치·검토 항목 {len(report.get('findings', []))}개 / 미관측 {len(report.get('unobserved_labels', []))}개"]
    if report.get('failure_type'):
        lines.append('실행 오류: ' + report['failure_type'])
    if report.get('missing_daily_tables'):
        lines.append('일별 테이블 누락: ' + ', '.join(report['missing_daily_tables']))
    if report.get('coverage'):
        coverage = report['coverage']
        lines.append(f"명세 {coverage['rows']}행 수집 / DA1·DA2 해석 {coverage['parsed_pages']}페이지 / 과거·참조·미해석 {coverage['unparsed_pages']}페이지")
    if 'unobserved_platform_contracts' in report:
        lines.append(f"플랫폼별 미관측 계약: {len(report['unobserved_platform_contracts'])}개")
    if report.get('previous_period_recheck'):
        previous = report['previous_period_recheck']
        lines.append(f"이전 기간 말일 3일 재검사: {previous['events']:,}건 / 불일치·검토 {len(previous['findings'])}개")
    translations = dict(event_label_missing='event_label 누락', unregistered_label_or_old_version='미등록 label·구버전 확인',
                        specification_conflict='명세 충돌·미확정', event_name_mismatch='event_name 불일치',
                        screen_view_mismatch='screen_view 불일치', event_category_mismatch='category 불일치',
                        platform_mismatch='플랫폼 확인 필요', value_missing='value 누락',
                        fixed_value_mismatch='고정 value 불일치', duplicate_parameter_key='중복 파라미터 키')
    for item in sorted(report.get('findings', []), key=lambda x: -x['count'])[:12]:
        lines.append(f"• {item['label']} | {translations.get(item['reason'], item['reason'])} {item['count']:,}건 | {'/'.join(item['platforms'])} {'/'.join(item['versions'])}")
        if item.get('specification_urls'):
            lines.append('  ' + item['specification_urls'][0])
    lines += ['최근 날짜는 지연 수집으로 잠정 집계하며 다음 주에 재검사합니다.',
              '미관측은 구현 누락을 의미하지 않습니다. 동적 value는 존재 여부만 검사합니다.',
              '버전 적용 시점이 미확정인 불일치는 담당자 확인이 필요합니다.',
              '명세 snapshot: ' + report.get('snapshot_sha256', '(unavailable)')[:12]]
    if report.get('detail_url'):
        lines.append('전체 결과: ' + report['detail_url'])
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
    req = urllib.request.Request(webhook, data=json.dumps({'text': text}, ensure_ascii=False).encode('utf8'),
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
