"""Validate the pinned checkout against current specification examples without network."""
import json
import socket
from pathlib import Path
from unittest.mock import patch

from koin_weekly_audit.github_source import GitHubSource
from koin_weekly_audit.contracts import build_catalog, compare


def check_current_specs(collector=None):
    source = (collector or GitHubSource()).collect()
    if not source.get('canonical_index_used'):
        raise AssertionError('Current canonical document index is required')
    catalog = build_catalog(source['pages'])
    by_id = {p['notion_id']: p for p in source['pages']}
    examples = json.loads((Path(__file__).parent / 'current-value-cases.json').read_text(encoding='utf8'))
    checks = dict(value_contracts=0, valid_platform_examples=0, missing_value_examples=0,
                  wrong_value_examples=0, unsupported_platform_examples=0, android_debug_examples=0)
    page_ids = set()

    def observation(c, platform, value):
        return dict(event_date='20261118', event_name=c['names'][0], event_label=c['label'],
                    event_category=c['categories'][0], screen_view=c['screens'][0],
                    platform=platform, value=value, value_parameter_present=True, event_count=1,
                    app_version='synthetic-only')

    def require(report, expected_reason=None):
        reasons = {f['reason'] for f in report['findings']}
        if expected_reason is None:
            if reasons:
                raise AssertionError('Valid current contract rejected: ' + ','.join(sorted(reasons)))
        elif expected_reason not in reasons:
            raise AssertionError('Missing expected mismatch: ' + expected_reason)

    for case in examples['contracts']:
        page_ids.add(case['notion_id'])
        page = by_id[case['notion_id']]
        matches = [c for c in catalog['by_label'].get(case['label'], []) if c['url'] == page['url']]
        if len(matches) != 1:
            raise AssertionError('Expected one declared contract: ' + case['label'])
        c = matches[0]
        if (c['status'] != 'current' or c['label'] in catalog['conflicts'] or
                c['fixed_value'] != case['value'] or not c['value_required'] or
                sorted(c['platforms']) != sorted(case['platforms'])):
            raise AssertionError('Approved current value/platform contract changed: ' + case['label'])
        checks['value_contracts'] += 1
        for platform in case['platforms']:
            good = observation(c, platform, case['value'])
            require(compare(catalog, [good])); checks['valid_platform_examples'] += 1
            missing = dict(good, value=None, value_parameter_present=False)
            require(compare(catalog, [missing]), 'value_missing'); checks['missing_value_examples'] += 1
            wrong = dict(good, value='synthetic-wrong-value')
            require(compare(catalog, [wrong]), 'fixed_value_mismatch'); checks['wrong_value_examples'] += 1
            if platform == 'ANDROID':
                debug = dict(good, event_name=good['event_name'] + '_debug',
                             event_category=good['event_category'] + '_debug',
                             event_label=good['event_label'] + ' (debug)')
                require(compare(catalog, [debug])); checks['android_debug_examples'] += 1
        unsupported = next(p for p in ('IOS', 'ANDROID', 'WEB') if p not in case['platforms'])
        require(compare(catalog, [observation(c, unsupported, case['value'])]), 'platform_mismatch')
        checks['unsupported_platform_examples'] += 1
    if len(page_ids) != examples['pages']:
        raise AssertionError('Approved value example pages are missing')

    normal_examples = []
    for label, contracts in catalog['by_label'].items():
        if label in catalog['conflicts']:
            continue
        for c in contracts:
            if c['status'] != 'current':
                continue
            value = c['fixed_value'] or (c['allowed_values'][0] if c['allowed_values'] else 'synthetic-value')
            for platform in c['platforms']:
                normal_examples.append(observation(c, platform, value))
    require(compare(catalog, normal_examples))
    return dict(source_revision=source['source_revision'], documents=source['row_count'],
                services=len(source['databases']), ignored_reference_documents=source['ignored_reference_documents'],
                labels=len(catalog['by_label']), contracts=sum(map(len, catalog['by_label'].values())),
                all_resolved_platform_examples=len(normal_examples), approved_value_pages=len(page_ids),
                checks=checks, unresolved_labels=catalog['conflicts'],
                unresolved_details=[dict(label=label, sources=[dict(url=c['url'], title=c['title'],
                    missing_fields=[k for k in ('event_name', 'screen_view', 'event_category') if not c['raw_fields'].get(k)],
                    source_review_pending=c['status'] == 'unresolved') for c in catalog['by_label'][label]])
                    for label in catalog['conflicts']],
                external_data_queried=False, external_ai_called=False, slack_sent=False)


def main():
    with patch('urllib.request.urlopen', side_effect=AssertionError('Network disabled')) as http, \
         patch('socket.socket', side_effect=AssertionError('Network disabled')) as sockets:
        result = check_current_specs()
        http.assert_not_called()
        sockets.assert_not_called()
    output = Path('reports/current-spec-check.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

