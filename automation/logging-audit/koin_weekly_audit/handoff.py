"""Developer-ready, reproducible issue notes generated from deterministic findings."""
import hashlib
import html


def text(value):
    return html.escape(str(value)).replace('\n',' ').replace('`','')


def developer_handoff(reports, reasons=None):
    lines = ['<a name="developer-handoff"></a>', '', '# 개발자 전달용 상세', '',
             '실제 수집 근거에 따른 필드별 확인 목록입니다. 같은 로그의 여러 필드 오류는 각각 기록하며 건수를 중복 합산하지 않습니다. 명세 미확정은 SDK 오류 확정과 구분합니다.', '']
    for env, report in reports.items():
        lines += ['## ' + ('Stage' if env == 'stage' else 'Prod'), '',
            '기간: ' + report['start'] + ' ~ ' + report['end'],
            '명세 커밋: ' + text(report.get('source_revision') or '미확인'),
            'BigQuery 조회 job: ' + text(report.get('query_job_id') or '미확인'), '']
        if not report.get('complete'):
            lines += ['조회/명세 수집 불완전 — 정상 판정 불가', '']
        for platform, name in (('IOS','iOS'),('ANDROID','Android'),('WEB','Web')):
            target = report.get('version_scope', {}).get('targets', {}).get(platform)
            lines += ['### ' + name + (' ' + target if target else ''), '']
            findings = [f for f in report.get('findings', []) if platform in f.get('platforms', [])]
            if not findings:
                stats = report.get('platform_summary', {}).get(platform, {})
                lines += ['관측 범위에서 이상 없음' if report.get('complete') and stats.get('events') else '판정 대상 로그 없음 또는 조회 불완전', '']
            for f in findings:
                issue_id = hashlib.sha256('|'.join((env, platform, f['label'], f['reason'])).encode()).hexdigest()[:10]
                values = f.get('platform_value_counts', {}).get(platform, {})
                actual = '; '.join(str(v) + ' (' + str(n) + '건)' for v,n in sorted(values.items())) or ', '.join(f.get('platform_observed_values', {}).get(platform, [])) or '근거 확인 필요'
                lines += ['#### [' + issue_id + '] ' + text(f['label']), '',
                    '- 구분: ' + ('명세 담당자 확인 필요' if f['reason']=='specification_conflict' else text((reasons or {}).get(f['reason'],f['reason']))),
                    '- 다른 필드: ' + text(f.get('field') or f['reason']),
                    ('- 자동 판정 기준: ' if f.get('field')=='value' else '- 명세 값: ') + text(', '.join(f.get('platform_expected_values', {}).get(platform, f.get('expected_values', []))) or '현행 계약 확인 필요'),
                    '- 실제 수집: ' + text(actual),
                    '- 해당 오류 발생: ' + str(f.get('platform_counts', {}).get(platform,0)) + '건',
                    '- 앱 버전: ' + text(', '.join(f.get('platform_versions', {}).get(platform, []))),
                    '- 관측 날짜(event_date): ' + text(', '.join(f.get('platform_dates', {}).get(platform, [])) or '미확인')]
                value_source = f.get('platform_value_source', {}).get(platform)
                if value_source:
                    lines += ['- GitHub 원문 value 표기: ' + text('; '.join(s['raw_text'] for s in value_source['sources']) or ('현행 계약 연결 없음' if value_source['status']=='no_current_contract' else '원문 추출 미확인'))]
                    lines += ['- value 원문 출처: [원문 ' + str(s['line']) + '행](' + s['url'] + ')' for s in value_source['sources'] if s['url'].startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/')]
                for source in (f.get('expectation_sources', []) if f.get('field') == 'event_name' else []):
                    if source.get('platforms') and platform not in source['platforms']:
                        continue
                    if source['url'].startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/'):
                        lines += ['- event_name 원문 근거: ' + text(', '.join(source['event_names']) or '미기재') + ' · [해당 명세](' + source['url'] + ')']
                urls = [u for u in f.get('specification_urls', []) if u.startswith('https://github.com/BCSDLab/KOIN-DATA-LOGGING/')]
                lines += ['- 명세: ' + (' · '.join('[원문 명세](' + u + ')' for u in urls) or '등록된 명세 없음 — 계약 등록 또는 SDK label 확인 필요'), '']
    return '\n'.join(lines)
