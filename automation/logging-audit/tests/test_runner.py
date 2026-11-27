import tempfile
import json
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from run import audit, week_start, main


class Collector:
    def collect(self):
        return dict(complete=True, databases={str(i): 1 for i in range(22)}, row_count=836,
                    pages=[dict(title='테스트', service='테스트', url='https://www.notion.so/test', platforms=['IOS'],
                                text='- 새 로깅\n- event_name: DA1\n- event_label: test__screen__button__click\n- screen_view: screen\n- event_category: click\n- value: 확인')])


class RunnerTest(unittest.TestCase):
    def test_previous_period_missing_table_does_not_invalidate_primary_week(self):
        with tempfile.TemporaryDirectory() as folder:
            reports = audit(date(2026, 11, 16), folder, folder + '/state', collector=Collector(),
                            query=lambda *a, **kw: dict(rows=[], complete=False, missing_daily_tables=['events_20261114']),
                            investigator=lambda *a: dict(status='skipped'))
            for report in reports.values():
                self.assertTrue(report['complete'])
                self.assertEqual(report['missing_daily_tables'], [])
                self.assertFalse(report['previous_period_recheck']['complete'])
                self.assertEqual(report['previous_period_recheck']['missing_daily_tables'], ['events_20261114'])

    def test_stage_trial_never_falls_back_to_existing_channel(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict('os.environ',
                {'SLACK_LOGGING_AUDIT_WEBHOOK': 'OLD-CHANNEL'}, clear=True), patch('run.send_once') as sender:
            reports = audit(date(2026, 11, 16), folder, folder + '/state', send=True,
                            collector=Collector(), sender=sender,
                            query=lambda *a, **kw: dict(rows=[], complete=True, missing_daily_tables=[]),
                            investigator=lambda *a: dict(status='skipped'))
            sender.assert_not_called()
            self.assertTrue(all(r['delivery_status'] == 'secret_missing' for r in reports.values()))

    def test_exit_status_preserves_failures_but_optional_ai_is_warning(self):
        cases = [
            (dict(complete=True, delivery_status='sent', agent=dict(status='failed')), True, 0),
            (dict(complete=True, delivery_status='sent', delivery_current_confirmed=False, agent=dict(status='completed')), True, 1),
            (dict(complete=True, delivery_status='not_requested', agent=dict(status='failed')), False, 0),
            (dict(complete=False, delivery_status='sent', agent=dict(status='completed')), True, 1),
            (dict(complete=True, delivery_status='failed', agent=dict(status='completed')), True, 1),
            (dict(complete=True, delivery_status='secret_missing', agent=dict(status='completed')), True, 1),
        ]
        for report, send, expected in cases:
            with self.subTest(report=report), patch('run.audit', return_value={'stage':report}), patch.dict('os.environ', {}, clear=True):
                self.assertEqual(main(['--send'] if send else []), expected)

    def test_completed_calendar_week(self):
        self.assertEqual(week_start(today=date(2026, 11, 24)), date(2026, 11, 16))
        self.assertEqual(week_start(today=date(2026, 11, 30)), date(2026, 11, 23))
        with self.assertRaises(ValueError): week_start('2026-11-17', today=date(2026, 11, 24))
        with self.assertRaises(ValueError): week_start('2026-11-23', today=date(2026, 11, 24))

    def test_environment_failure_isolated_and_reported(self):
        calls, messages = [], []
        def query(project, dataset, start, end, **kwargs):
            calls.append((project, start, end))
            if project == 'koin-stage-438512': raise PermissionError('DO NOT PRINT SECRET')
            return dict(rows=[], complete=True, missing_daily_tables=[])
        def sender(webhook, message, receipt):
            messages.append(message)
            return {'status': 'sent'}
        with tempfile.TemporaryDirectory() as folder, patch.dict('os.environ', {'SLACK_LOGGING_AUDIT_STAGE_WEBHOOK': 'dummy'}):
            reports = audit(date(2026, 11, 16), folder + '/reports', folder + '/state', True,
                            Collector(), query, sender)
            self.assertFalse(reports['stage']['complete'])
            self.assertTrue(reports['production']['complete'])
            self.assertEqual(len(messages), 2)
            self.assertNotIn('DO NOT PRINT SECRET', json.dumps(messages))
            self.assertTrue(all('blocks' in message for message in messages))
            self.assertEqual(calls[0][1:], ('2026-11-13', '2026-11-22'))

    def test_source_failure_cannot_query_or_claim_success(self):
        class Broken:
            def collect(self): raise PermissionError('secret')
        with tempfile.TemporaryDirectory() as folder, patch('run.fetch') as query:
            results = audit(date(2026, 11, 16), folder, folder + '/state', collector=Broken(), query=query)
            query.assert_not_called()
            self.assertFalse(any(r['complete'] for r in results.values()))
            self.assertTrue(all(r['failure_type'] == 'PermissionError' for r in results.values()))

    def test_incomplete_inventory_rejected(self):
        class Small:
            def collect(self): return dict(complete=True, databases={}, row_count=0, pages=[])
        with tempfile.TemporaryDirectory() as folder:
            results = audit(date(2026, 11, 16), folder, folder + '/state', collector=Small())
            self.assertTrue(all(r['failure_type'] == 'IncompleteSource' for r in results.values()))


if __name__ == '__main__':
    unittest.main()
