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
from koin_weekly_audit.notify import send_once, slack_text, slack_payload, detail_markdown
from koin_weekly_audit.agent import investigate
from koin_weekly_audit.github_source import GitHubSource
from koin_weekly_audit.actions import summary_url
from koin_weekly_audit.version_scope import targets_for, select_scope

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


def audit(start, output, state, send=False, collector=None, query=fetch, sender=send_once, investigator=investigate):
    end = start + timedelta(days=6)
    output, state = Path(output) / start.isoformat(), Path(state) / start.isoformat()
    output.mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True)
    catalog, source_error, source, source_diagnostics = None, None, None, None
    try:
        if collector is None:
            collector = GitHubSource()
        source = collector.collect()
        if not source.get('complete') or len(source['databases']) < 21 or source['row_count'] < 700:
            raise IncompleteSource('Source completeness check failed')
        catalog = build_catalog(source['pages'])
        if not catalog['by_label']:
            raise IncompleteSource('No current DA1/DA2 contracts found')
        # Keep a reproducible specification snapshot, without tokens or raw events.
        (output / 'contract-snapshot.json').write_text(json.dumps(catalog, ensure_ascii=False), encoding='utf8')
    except Exception as exc:
        source_error = type(exc).__name__
        if isinstance(exc, IncompleteSource):
            source_diagnostics = exc.diagnostics
        if isinstance(collector, NotionSource):
            source_diagnostics = dict(source_diagnostics or {}, root=collector.root,
                discovered_data_sources=len(collector.databases), discovered_rows=len(collector.rows),
                visited_pages=len(collector.visited))
    reports = {}
    detail_url = summary_url()
    for environment, (project, dataset) in SOURCES.items():
        primary = []
        report = dict(complete=False, failure_type=source_error or 'UnknownFailure')
        if source_diagnostics:
            report['source_diagnostics'] = source_diagnostics
        if source_error is None:
            try:
                targets = targets_for(environment)
                fetched = query(project, dataset, (start - timedelta(days=3)).isoformat(), end.isoformat(),
                                max_bytes=int(os.getenv('AUDIT_MAX_BYTES', str(5 * 1024**3))))
                primary = [r for r in fetched['rows'] if start.strftime('%Y%m%d') <= r['event_date'] <= end.strftime('%Y%m%d')]
                late = [r for r in fetched['rows'] if r['event_date'] < start.strftime('%Y%m%d')]
                primary, version_scope = select_scope(primary, targets)
                late, previous_scope = select_scope(late, targets)
                report = compare(catalog, primary)
                report['version_scope'] = version_scope
                report['previous_period_recheck'] = compare(catalog, late)
                report['previous_period_recheck']['version_scope'] = previous_scope
                missing = fetched['missing_daily_tables']
                primary_missing = [t for t in missing if start.strftime('%Y%m%d') <= t.removeprefix('events_') <= end.strftime('%Y%m%d')]
                previous_missing = [t for t in missing if t.removeprefix('events_') < start.strftime('%Y%m%d')]
                report['previous_period_recheck'].update(complete=not previous_missing, missing_daily_tables=previous_missing)
                report.update(complete=not primary_missing and (fetched['complete'] or bool(missing)), missing_daily_tables=primary_missing,
                              query_job_id=fetched.get('job_id'), bytes_processed=fetched.get('bytes_processed'),
                              coverage=dict(rows=source['row_count'], databases=len(source['databases']),
                                            parsed_pages=sum(r['status'] == 'parsed' for r in catalog['coverage']),
                                            unparsed_pages=sum(r['status'] != 'parsed' for r in catalog['coverage']),
                                            historical_labels=len(catalog['legacy_by_label'])))
            except Exception as exc:
                report = dict(complete=False, failure_type=type(exc).__name__, snapshot_sha256=catalog['snapshot_sha256'])
        report.update(environment=environment, start=start.isoformat(), end=end.isoformat())
        if source:
            report.update(source_kind=source.get('source_kind'), source_revision=source.get('source_revision'))
        try:
            if investigator is investigate:
                checkpoint = lambda result: (output / f'{environment}-agent.json').write_text(
                    json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
                report['agent'] = investigator(catalog, report, primary, checkpoint=checkpoint)
            else:
                report['agent'] = investigator(catalog, report, primary)
        except Exception as exc:
            report['agent'] = dict(status='failed', failure_type=type(exc).__name__)
        if detail_url:
            report['detail_url'] = detail_url
        message = slack_text(environment, start.isoformat(), end.isoformat(), report)
        (output / f'{environment}-slack.txt').write_text(message, encoding='utf8')
        payload = slack_payload(environment, start.isoformat(), end.isoformat(), report)
        (output / f'{environment}-slack.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf8')
        if send:
            webhook = os.getenv('SLACK_LOGGING_AUDIT_STAGE_WEBHOOK')
            if webhook:
                try:
                    phase = 'complete' if report.get('complete') else 'incomplete'
                    import hashlib
                    destination = hashlib.sha256(webhook.encode()).hexdigest()[:12]
                    scope_key = hashlib.sha256(json.dumps(report.get('version_scope', {}).get('targets', {}), sort_keys=True).encode()).hexdigest()[:10]
                    receipt = sender(webhook, payload, state / f'{environment}-{phase}-{destination}-{scope_key}-platform-audit-v5-delivery.json')
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
    summary = {k: {**{field: r.get(field) for field in ('complete', 'events', 'observed_labels', 'failure_type', 'delivery_status', 'source_diagnostics', 'version_scope')},
                   'agent_status': r.get('agent', {}).get('status'),
                   'agent_failure_type': r.get('agent', {}).get('failure_type'),
                   'agent_failure_code': r.get('agent', {}).get('failure_code'),
                   'missing_daily_tables': r.get('missing_daily_tables'),
                   'coverage': r.get('coverage')} for k, r in reports.items()}
    print(json.dumps(summary, ensure_ascii=False))
    if os.getenv('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(
            detail_markdown(reports), encoding='utf8')
    for environment, report in reports.items():
        if report.get('agent', {}).get('status') != 'completed':
            print(f'::warning title=AI 추가 조사 미완료::{environment}: 규칙 검수 결과와 별도로 AI 추가 조사를 완료하지 못했습니다. 상세 보고서를 확인하세요.')
    # Findings are audit results, not execution failures. Optional AI is separate.
    return 0 if reports and all(r.get('complete') and
                   (not args.send or r.get('delivery_status') == 'sent') for r in reports.values()) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('Audit setup failed: ' + type(exc).__name__, file=sys.stderr)
        sys.exit(2)
