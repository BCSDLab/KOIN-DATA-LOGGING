import unittest

from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.notify import slack_text
from koin_weekly_audit.bigquery_source import build_query
from test_weekly_audit import page, SPEC, OBS


PAST = '''- 과거 로깅
 - event_name: CAMPUS
 - event_label: “old_back”
 - value: 뒤로가기
 - event_category: click
'''


class AlertCategoriesTest(unittest.TestCase):
    def test_legacy_name_does_not_hide_unobserved_current_contract(self):
        report = compare(build_catalog([page(SPEC)]), [dict(OBS, event_name='CAMPUS')])
        self.assertIn(OBS['event_label'], report['unobserved_labels'])
        self.assertIn(dict(label=OBS['event_label'], platform='IOS'), report['unobserved_platform_contracts'])

    def test_past_section_after_new_does_not_overwrite_current(self):
        cat = build_catalog([page(SPEC + '\n' + PAST)])
        self.assertIn(OBS['event_label'], cat['by_label'])
        self.assertIn('old_back', cat['legacy_by_label'])
        self.assertNotIn('old_back', cat['by_label'])
        self.assertEqual(compare(cat, [OBS])['findings'], [])

    def test_three_categories_disjoint_and_linked(self):
        cat = build_catalog([page(PAST + SPEC)])
        result = compare(cat, [dict(OBS, event_label='unknown', event_count=2),
                               dict(OBS, event_label='old_back', event_count=4),
                               dict(OBS, screen_view='wrong', value=None, event_count=6)])
        stats = result['platform_summary']['IOS']['categories']
        self.assertEqual({k: x['events'] for k, x in stats.items()},
                         dict(unregistered=2, legacy_logging=4, current_mismatch=6))
        # Two field errors in six events must not be counted as twelve events.
        self.assertEqual(len([x for x in result['findings'] if x['category'] == 'current_mismatch']), 2)
        legacy = next(x for x in result['findings'] if x['category'] == 'legacy_logging')
        self.assertEqual(legacy['reason'], 'historical_label_still_collected')
        self.assertEqual(legacy['specification_urls'], [page('')['url']])

    def test_current_label_wins_over_past_label(self):
        past = PAST.replace('old_back', OBS['event_label'])
        result = compare(build_catalog([page(past + SPEC)]), [OBS])
        self.assertEqual(result['findings'], [])

    def test_legacy_page_and_plain_old_fields_are_indexed(self):
        old_page = page('- event_label: plain_old\n- event_category: click')
        retired = page(SPEC); retired['lifecycle_status'] = '레거시'
        cat = build_catalog([old_page, retired])
        self.assertIn('plain_old', cat['legacy_by_label'])
        self.assertNotIn(OBS['event_label'], cat['by_label'])
        self.assertIn(OBS['event_label'], cat['legacy_by_label'])

    def test_no_past_label_inferred_from_description(self):
        p = page('- 과거 로깅\n참고 old_back 같은 이름은 추정하지 않는다.\n' + SPEC)
        self.assertEqual(build_catalog([p])['legacy_by_label'], {})

    def test_old_event_names_always_alert_even_with_current_label(self):
        cat = build_catalog([page(SPEC)])
        for name in ('CAMPUS', 'BUSINESS', 'USER', 'campus', 'business', 'user'):
            with self.subTest(name=name):
                finding = compare(cat, [dict(OBS, event_name=name)])['findings'][0]
                self.assertEqual(finding['category'], 'legacy_logging')
                self.assertEqual(finding['reason'], 'legacy_event_name')
                self.assertEqual(finding['event_names'], [name])

    def test_other_event_names_are_excluded(self):
        result = compare(build_catalog([page(SPEC)]), [dict(OBS, event_name='screen_view'),
                                                      dict(OBS, event_name='CAMPUS_debug')])
        self.assertEqual(result['events'], 0)
        self.assertEqual(result['findings'], [])

    def test_platform_counts_and_names_not_crossed(self):
        cat = build_catalog([page(PAST + SPEC)])
        result = compare(cat, [dict(OBS, event_label='old_back', event_name='CAMPUS', event_count=3),
                               dict(OBS, event_label='old_back', event_name='USER', platform='WEB', event_count=7)])
        finding = result['findings'][0]
        self.assertEqual(finding['platform_counts'], {'IOS': 3, 'WEB': 7})
        self.assertEqual(finding['platform_event_names'], {'IOS': ['CAMPUS'], 'WEB': ['USER']})
        self.assertEqual(result['platform_summary']['ANDROID']['events'], 0)

    def test_every_platform_and_every_category_always_visible(self):
        report = compare(build_catalog([page(SPEC)]), [])
        report['complete'] = True
        text = slack_text('production', '2026-11-16', '2026-11-22', report)
        for p in ('IOS', 'ANDROID', 'WEB'):
            self.assertIn({'IOS': 'iOS', 'ANDROID': 'Android', 'WEB': 'Web'}[p], text)
        self.assertIn('미등록 / 과거 / 명세 불일치', text)
        self.assertLessEqual(len(text.splitlines()), 12)
        self.assertIn('수집 0건: iOS·Android·Web', text)
        self.assertIn('```', text)
        rows = [line for line in text.splitlines() if line.startswith(('iOS ', 'Android ', 'Web '))]
        self.assertEqual(len({line.index('/') for line in rows}), 1)

    def test_source_failure_is_not_zero_traffic(self):
        text = slack_text('stage', 'a', 'b', {'complete': False})
        self.assertIn('iOS·Android·Web 모두 판정 미확인', text)
        self.assertIn('로그 집계 불가', text)
        self.assertNotIn('수집 0건 —', text)

    def test_query_scope(self):
        sql = build_query('kap-chat', 'analytics_432041405')
        self.assertIn("event_name IN ('DA1','DA2') OR UPPER(event_name) IN ('CAMPUS','BUSINESS','USER')", sql)


if __name__ == '__main__':
    unittest.main()
