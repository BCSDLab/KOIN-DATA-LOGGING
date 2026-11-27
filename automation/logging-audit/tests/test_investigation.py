import copy
import json
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.investigation import investigate, breakdown
from koin_weekly_audit.notify import detail_markdown, slack_text
from test_weekly_audit import SPEC, OBS, page
from offline_check import SyntheticSource, synthetic_query
from run import audit


def fixture(rows=None):
    catalog = build_catalog([page(SPEC, ['ANDROID', 'IOS', 'WEB'])])
    rows = rows if rows is not None else [dict(OBS, platform='ANDROID', event_name='DA2_debug',
        event_label=OBS['event_label'] + ' (debug)', event_category='click_debug', app_version='5.2.4')]
    report = compare(catalog, rows)
    report.update(complete=True, environment='stage', start='2026-11-16', end='2026-11-22',
                  source_revision='a'*40, query_job_id='query_123')
    return catalog, report, rows


class InvestigationTest(unittest.TestCase):
    def test_normalized_evidence_exact_counts_and_sources(self):
        catalog, report, rows = fixture()
        before = copy.deepcopy((catalog, report, rows))
        result = investigate(catalog, report, rows)
        item = result['investigations'][0]
        self.assertFalse(result['external_ai_called'])
        self.assertEqual(item['label'], OBS['event_label'])
        self.assertEqual(item['observed_events'], 3)
        self.assertEqual(item['breakdowns']['event_name']['groups'], [{'key': 'DA2', 'events': 3}])
        self.assertEqual(item['contracts'][0]['names'], ['DA1'])
        self.assertEqual(item['query_job_id'], 'query_123')
        self.assertEqual(item['first_observed_date'], '20261122')
        self.assertEqual((catalog, report, rows), before)

    def test_multiple_errors_do_not_double_observed_count(self):
        catalog, report, rows = fixture([dict(OBS, event_name='DA2', screen_view='wrong', event_count=7)])
        item = investigate(catalog, report, rows)['investigations'][0]
        self.assertEqual(len(item['reasons']), 2)
        self.assertEqual(item['observed_events'], 7)
        self.assertEqual(item['largest_single_rule_events'], 7)
        self.assertTrue(all(r['events'] == 7 for r in item['reasons']))

    def test_platform_coverage_precedes_extra_labels_from_busy_platform(self):
        rows = [dict(OBS, platform='ANDROID', event_name='DA2', event_label='unknown_' + str(i), event_count=100-i) for i in range(8)]
        rows.extend([dict(OBS, platform='IOS', event_name='DA2', event_count=1),
                     dict(OBS, platform='WEB', event_name='DA2', event_count=2)])
        result = investigate(*fixture(rows))
        self.assertEqual(len(result['investigations']), 4)
        self.assertEqual({i['platform'] for i in result['investigations']}, {'ANDROID', 'IOS', 'WEB'})
        self.assertEqual(result['total_label_platform_findings'], 10)

    def test_order_is_deterministic_and_no_raw_values_or_ids_exported(self):
        rows = [dict(OBS, event_name='DA2', event_count=4, event_date=day,
                     value='private@example.com', user_id='PRIVATE USER', user_pseudo_id='PRIVATE PSEUDO')
                for day in ('20261119', '20261120')]
        catalog, report, rows = fixture(rows)
        first = investigate(catalog, report, rows)
        self.assertEqual(first, investigate(catalog, report, list(reversed(rows))))
        serialized = json.dumps(first)
        for private in ('private@example.com', 'PRIVATE USER', 'PRIVATE PSEUDO'):
            self.assertNotIn(private, serialized)

    def test_bounded_groups_preserve_omitted_counts(self):
        rows = [dict(event_count=i+1, app_version='1.0.'+str(i)) for i in range(35)]
        result = breakdown(rows, 'app_version')
        self.assertEqual(len(result['groups']), 30)
        self.assertEqual(result['omitted_groups'], 5)
        self.assertEqual(result['omitted_events'], 15)
        self.assertEqual(result['total_events'], 630)

    def test_incomplete_and_no_findings_not_invented(self):
        catalog, report, rows = fixture([OBS])
        self.assertEqual(investigate(catalog, report, rows)['investigations'], [])
        report['complete'] = False
        self.assertEqual(investigate(catalog, report, rows)['status'], 'skipped')

    def test_sensitive_identifier_is_masked(self):
        catalog, report, rows = fixture([dict(OBS, event_label='person@example.com', event_name='DA2')])
        text = json.dumps(investigate(catalog, report, rows))
        self.assertNotIn('person@example.com', text)
        self.assertIn('(invalid identifier)', text)

    def test_missing_label_rows_are_counted(self):
        result = investigate(*fixture([dict(OBS, event_label=None, event_count=6)]))
        self.assertEqual(result['investigations'][0]['observed_events'], 6)

    def test_invalid_limit_rejected(self):
        for limit in (0, -1, 21, True):
            with self.assertRaises(ValueError):
                investigate(*fixture(), limit=limit)

    def test_whole_runner_and_details_work_without_network_even_if_key_present(self):
        with tempfile.TemporaryDirectory() as folder, patch('run.summary_url', return_value=None), \
             patch.dict('os.environ', {'OPENAI_API_KEY': 'fake-not-used'}), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network')) as http, \
             patch('socket.socket', side_effect=AssertionError('network')) as sockets:
            reports = audit(date(2026, 11, 16), folder, folder+'/state',
                            collector=SyntheticSource(), query=synthetic_query)
            http.assert_not_called()
            sockets.assert_not_called()
            for report in reports.values():
                self.assertEqual(report['investigation']['status'], 'completed')
                self.assertNotIn('agent', report)
                self.assertNotIn('AI API: 사용 안 함', slack_text('stage', report['start'], report['end'], report))
            details = detail_markdown(reports)
            self.assertIn('규칙 기반 상세 분석', details)
            self.assertIn('event_name 불일치 2건', details)
            self.assertIn('필수 value 누락 3건', details)
            self.assertNotIn('fake-not-used', details)


if __name__ == '__main__':
    unittest.main()
