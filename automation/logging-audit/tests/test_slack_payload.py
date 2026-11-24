import unittest
from koin_weekly_audit.notify import slack_payload


class SlackPayloadTest(unittest.TestCase):
    def test_native_table_preserves_platform_category_cells(self):
        categories = ('unregistered', 'legacy_logging', 'current_mismatch')
        summary = {p: dict(events=100, categories={c: dict(labels=i*3+j) for j, c in enumerate(categories)})
                   for i, p in enumerate(('IOS', 'ANDROID', 'WEB'))}
        report = dict(complete=True, events=300, platform_summary=summary,
                      agent=dict(status='failed', failure_type='PermissionDeniedError'),
                      detail_url='https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1')
        payload = slack_payload('production', '2026-11-16', '2026-11-22', report)
        table = next(b for b in payload['blocks'] if b['type'] == 'table')
        self.assertEqual([[c['text'] for c in row] for row in table['rows'][1:]],
                         [['iOS', '0', '1', '2'], ['Android', '3', '4', '5'], ['Web', '6', '7', '8']])
        self.assertEqual([c['align'] for c in table['column_settings']], ['left', 'right', 'right', 'right'])
        self.assertIn('PermissionDeniedError', str(payload['blocks']))

    def test_partial_collection_explains_dates_without_zero_success(self):
        payload = slack_payload('stage', '2026-11-16', '2026-11-22',
                                dict(complete=False, events=201, missing_daily_tables=['events_20261117']))
        content = str(payload['blocks'])
        self.assertIn('20261117', content)
        self.assertIn('201', content)
        self.assertIn('최종 판정 보류', content)
        self.assertFalse(any(b['type'] == 'table' for b in payload['blocks']))

    def test_examples_are_separate_by_category_and_do_not_leak_values(self):
        findings = [dict(category=c, label='example__label__click', count=1, raw_value='PRIVATE')
                    for c in ('unregistered', 'legacy_logging', 'current_mismatch')]
        payload = slack_payload('stage', '2026-11-16', '2026-11-22',
                                dict(complete=True, events=3, findings=findings))
        content = str(payload['blocks'])
        self.assertIn('• 미등록:', content)
        self.assertIn('• 과거:', content)
        self.assertIn('• 명세 불일치:', content)
        self.assertNotIn('PRIVATE', content)


if __name__ == '__main__':
    unittest.main()
