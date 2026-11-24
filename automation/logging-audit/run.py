"""Standalone weekly audit. No Airflow, Docker or Tailscale dependency."""
import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from koin_weekly_audit.bigquery_source import fetch
from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.notion_source import NotionSource, IncompleteSource
from koin_weekly_audit.notify import send_once, slack_text

ROOT = 'f820221954bc82cfbe7e813b975c5be1'
SOURCES = {'stage': ('koin-stage-438512', 'analytics_427218788'),
           'production': ('kap-chat', 'analytics_432041405')}
KST = timezone(timedelta(hours=9))


class NotionTokenMissing(RuntimeError):
    pass


def week_start(value=None, today=None):
    today = today or datetime.now(KST).date()
    if value:
        start = date.fromisoformat(value)
        if start.weekday() != 0 or start + timedelta(days=6) >= today:
            raise ValueError('Use a completed calendar week starting on Monday')
        return start
    return today - timedelta(days=today.weekday() + 7)


def audit(start, output, state, send=False, collector=None, query=fetch, sender=send_once):
    end = start + timedelta(days=6)
    output, state = Path(output) / start.isoformat(), Path(state) / start.isoformat()
    output.mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True)
    catalog, source_error, source = None, None, None
    try:
        if collector is None:
            token = os.getenv('NOTION_LOGGING_READ_TOKEN')
            if not token:
                raise NotionTokenMissing()
            collector = NotionSource(token, os.getenv('NOTION_EVENT_LOG_ROOT', ROOT))
        source = collector.collect()
        if not source.get('complete') or len(source['databases']) < 22 or source['row_count'] < 700:
            raise IncompleteSource('Source completeness check failed')
        catalog = build_catalog(source['pages'])
        if not catalog['by_label']:
            raise IncompleteSource('No current DA1/DA2 contracts found')
        # Keep a reproducible specification snapshot, without tokens or raw events.
        (output / 'contract-snapshot.json').write_text(json.dumps(catalog, ensure_ascii=False), encoding='utf8')
    except Exception as exc:
        source_error = type(exc).__name__
    reports = {}
    for environment, (project, dataset) in SOURCES.items():
        report = dict(complete=False, failure_type=source_error or 'UnknownFailure')
        if source_error is None:
            try:
                fetched = query(project, dataset, (start - timedelta(days=3)).isoformat(), end.isoformat(),
                                max_bytes=int(os.getenv('AUDIT_MAX_BYTES', str(5 * 1024**3))))
                primary = [r for r in fetched['rows'] if start.strftime('%Y%m%d') <= r['event_date'] <= end.strftime('%Y%m%d')]
                late = [r for r in fetched['rows'] if r['event_date'] < start.strftime('%Y%m%d')]
                report = compare(catalog, primary)
                report['previous_period_recheck'] = compare(catalog, late)
                report.update(complete=fetched['complete'], missing_daily_tables=fetched['missing_daily_tables'],
                              query_job_id=fetched.get('job_id'), bytes_processed=fetched.get('bytes_processed'),
                              coverage=dict(rows=source['row_count'], databases=len(source['databases']),
                                            parsed_pages=sum(r['status'] == 'parsed' for r in catalog['coverage']),
                                            unparsed_pages=sum(r['status'] != 'parsed' for r in catalog['coverage'])))
            except Exception as exc:
                report = dict(complete=False, failure_type=type(exc).__name__, snapshot_sha256=catalog['snapshot_sha256'])
        report.update(environment=environment, start=start.isoformat(), end=end.isoformat())
        server, repo, run_id = (os.getenv(k) for k in ('GITHUB_SERVER_URL', 'GITHUB_REPOSITORY', 'GITHUB_RUN_ID'))
        if server and repo and run_id:
            report['detail_url'] = f'{server}/{repo}/actions/runs/{run_id}'
        message = slack_text(environment, start.isoformat(), end.isoformat(), report)
        (output / f'{environment}-slack.txt').write_text(message, encoding='utf8')
        if send:
            webhook = os.getenv('SLACK_LOGGING_AUDIT_WEBHOOK')
            if webhook:
                try:
                    receipt = sender(webhook, message, state / f'{environment}-delivery.json')
                    report['delivery_status'] = receipt['status']
                except Exception as exc:
                    report['delivery_status'] = 'failed'
                    report['delivery_error_type'] = type(exc).__name__
            else:
                report['delivery_status'] = 'secret_missing'
        else:
            report['delivery_status'] = 'not_requested'
        # Only sanitized summaries are uploaded as GitHub artifacts.
        (output / f'{environment}-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
        reports[environment] = report
    return reports


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--week-start')
    parser.add_argument('--print-week-start', action='store_true')
    parser.add_argument('--output', default='reports')
    parser.add_argument('--state', default='.audit-state')
    parser.add_argument('--send', action='store_true')
    args = parser.parse_args(argv)
    start = week_start(args.week_start)
    if args.print_week_start:
        print(start.isoformat())
        return 0
    reports = audit(start, args.output, args.state, send=args.send)
    summary = {k: {field: r.get(field) for field in ('complete', 'events', 'observed_labels', 'failure_type', 'delivery_status')} for k, r in reports.items()}
    print(json.dumps(summary, ensure_ascii=False))
    if os.getenv('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(
            '# 주간 로깅 검수\n\n```json\n' + json.dumps(summary, ensure_ascii=False, indent=2) + '\n```\n\n'
            + '상세 결과는 이 실행의 logging-audit-results artifact에 있습니다. 불일치는 배포 버전 확인이 필요한 후보입니다.\n', encoding='utf8')
    return 0 if all(r.get('complete') and (not args.send or r.get('delivery_status') == 'sent') for r in reports.values()) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('Audit setup failed: ' + type(exc).__name__, file=sys.stderr)
        sys.exit(2)
