import copy
import unittest

from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.environment_evidence import observations, value_collections
from koin_weekly_audit.normalization import normalize_observation, normalization_summary
from test_weekly_audit import SPEC, OBS, page


class AndroidDebugTest(unittest.TestCase):
    def setUp(self):
        self.catalog = build_catalog([page(SPEC, ['ANDROID', 'IOS', 'WEB'])])
        self.row = dict(OBS, platform='ANDROID', event_name='DA1_debug',
                        event_label=OBS['event_label'] + ' (debug)', event_category='click_debug')

    def test_normal_debug_matches_and_keeps_raw_input(self):
        before = copy.deepcopy(self.row)
        report = compare(self.catalog, [self.row])
        self.assertEqual(report['findings'], [])
        self.assertEqual(report['events'], 3)
        self.assertNotIn(OBS['event_label'], report['unobserved_labels'])
        self.assertEqual(report['platform_summary']['ANDROID']['event_names'], {'DA1': 3})
        self.assertEqual(self.row, before)
        normalized = normalize_observation(self.row)
        self.assertEqual(normalized['raw_identifiers']['event_label'], self.row['event_label'])
        self.assertEqual(normalize_observation(normalized), normalized)

    def test_label_underscore_debug_supported(self):
        self.row['event_label'] = OBS['event_label'] + '_debug'
        self.assertEqual(compare(self.catalog, [self.row])['findings'], [])

    def test_true_mismatches_survive_normalization(self):
        self.row.update(event_name='DA2_debug', screen_view='wrong', event_category='swipe_debug')
        reasons = {f['reason'] for f in compare(self.catalog, [self.row])['findings']}
        self.assertEqual(reasons, {'event_name_mismatch', 'screen_view_mismatch', 'event_category_mismatch'})

    def test_unregistered_debug_label_still_alerts(self):
        self.row['event_label'] = 'unknown__screen__button__click (debug)'
        report = compare(self.catalog, [self.row])
        self.assertEqual([f['reason'] for f in report['findings']], ['unregistered_label'])
        self.assertEqual(report['findings'][0]['label'], 'unknown__screen__button__click')

    def test_legacy_debug_remains_legacy(self):
        self.row['event_name'] = 'CAMPUS_debug'
        self.assertIn('legacy_event_name', [f['reason'] for f in compare(self.catalog, [self.row])['findings']])

    def test_other_platforms_are_not_normalized(self):
        for platform in ('IOS', 'WEB'):
            row = dict(self.row, platform=platform)
            self.assertEqual(normalize_observation(row), row)
            self.assertIn('unexpected_event_name', [f['reason'] for f in compare(self.catalog, [row])['findings']])

    def test_screen_and_value_are_never_stripped(self):
        row = dict(self.row, screen_view='room_debug', value='뒤로가기_debug')
        normalized = normalize_observation(row)
        self.assertEqual(normalized['screen_view'], 'room_debug')
        self.assertEqual(normalized['value'], '뒤로가기_debug')
        self.assertIn('fixed_value_mismatch', [f['reason'] for f in compare(self.catalog, [row])['findings']])

    def test_strip_one_terminal_marker_only(self):
        row = dict(self.row, event_name='DA1_debug_debug')
        self.assertEqual(normalize_observation(row)['event_name'], 'DA1_debug')
        self.assertIn('event_name_mismatch', [f['reason'] for f in compare(self.catalog, [row])['findings']])
        row = dict(self.row, event_label='real_debug__screen__button__click')
        self.assertEqual(normalize_observation(row)['event_label'], row['event_label'])

    def test_missing_label_still_alerts(self):
        self.assertIn('event_label_missing', [f['reason'] for f in compare(self.catalog, [dict(self.row, event_label=None)])['findings']])

    def test_detail_evidence_uses_same_contract_keys(self):
        result = observations(self.catalog, [self.row])[0]
        self.assertEqual(result['label'], OBS['event_label'])
        self.assertEqual(result['fields']['event_name'], {'DA1': 3})
        self.assertEqual(value_collections(self.catalog, [self.row])[0]['label'], OBS['event_label'])
        self.assertEqual(normalization_summary([self.row])['android_debug_events'], 3)


if __name__ == '__main__':
    unittest.main()
