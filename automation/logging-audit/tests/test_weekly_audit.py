import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.notion_source import IncompleteSource, NotionSource
from koin_weekly_audit.notify import send_once, slack_text
from koin_weekly_audit.bigquery_source import build_query


def page(text, platforms=None):
    return dict(url='https://www.notion.so/test', title='test', service='복덕방', text=text,
                platforms=platforms or ['IOS'])


SPEC = '''- 새 로깅
 - 설명: 뒤로가기를 클릭한다.
 - screen_view: `room_common`
 - event_name: `DA1`
 - event_label: `real_estate__room_common__navigation__back__click`
 - value: 뒤로가기
 - event_category: `click`'''
OBS = dict(event_date='20261122', event_name='DA1', platform='IOS', app_version='5.2.6',
           event_label='real_estate__room_common__navigation__back__click',
           screen_view='room_common', event_category='click', value='뒤로가기', event_count=3)


class ContractsTest(unittest.TestCase):
    def test_web_mobile_platform_and_per_platform_coverage(self):
        cat = build_catalog([page(SPEC, ['WEB (모바일)', 'IOS'])])
        result = compare(cat, [dict(OBS, platform='WEB')])
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['unobserved_platform_contracts'], [dict(label=OBS['event_label'], platform='IOS')])

    def test_multiline_labels_and_matching_screens(self):
        text = '''- 새 로깅
 - screen_view:
   - 분실: `lost_item_edit`
   - 습득: `found_item_edit`
 - event_name: DA2
 - event_label:
   - 분실: board__lost_item_edit__form__submit
   - 습득: board__found_item_edit__form__submit
 - value: 분실물 / 습득물
 - event_category: submit'''
        cat = build_catalog([page(text)])
        self.assertEqual(len(cat['by_label']), 2)
        self.assertEqual(cat['by_label']['board__lost_item_edit__form__submit'][0]['screens'], ['lost_item_edit'])

    def test_no_swipe_support_inferred_from_web_metadata(self):
        p = page(SPEC.replace('event_label: `real_estate__room_common__navigation__back__click`',
                              'event_label: 모바일 `real_estate__room_common__navigation__back__swipe`').replace('category: `click`', 'category: `swipe`'), ['WEB'])
        cat = build_catalog([p])
        self.assertIn('real_estate__room_common__navigation__back__swipe', cat['conflicts'])

    def test_valid_and_wrong_contract(self):
        catalog = build_catalog([page(SPEC)])
        self.assertEqual(compare(catalog, [OBS])['findings'], [])
        bad = compare(catalog, [dict(OBS, event_name='DA2', screen_view=None, value=None)])
        self.assertEqual({x['reason'] for x in bad['findings']}, {'event_name_mismatch', 'screen_view_mismatch', 'value_missing'})

    def test_unresolved_not_treated_as_correct(self):
        p = page(SPEC); p['unresolved'] = True
        result = compare(build_catalog([p]), [OBS])
        self.assertEqual(result['findings'][0]['reason'], 'specification_conflict')

    def test_conflicting_same_label(self):
        cat = build_catalog([page(SPEC), page(SPEC.replace('room_common`', 'room_detail`'))])
        self.assertIn(OBS['event_label'], cat['conflicts'])

    def test_platform_variants_not_false_conflict(self):
        cat = build_catalog([page(SPEC, ['IOS']), page(SPEC, ['ANDROID'])])
        self.assertEqual(cat['conflicts'], [])
        self.assertEqual(compare(cat, [dict(OBS, platform='ANDROID')])['findings'], [])

    def test_dynamic_value_not_compared_to_placeholder(self):
        cat = build_catalog([page(SPEC.replace('value: 뒤로가기', 'value: {매물명}'))])
        self.assertEqual(compare(cat, [dict(OBS, value='미래빌리지')])['findings'], [])
        self.assertTrue(compare(cat, [dict(OBS, value=None)])['findings'])

    def test_missing_and_unregistered_label(self):
        cat = build_catalog([page(SPEC)])
        self.assertEqual(compare(cat, [dict(OBS, event_label=None)])['findings'][0]['reason'], 'event_label_missing')
        self.assertEqual(compare(cat, [dict(OBS, event_label='old_label')])['findings'][0]['reason'], 'unregistered_label')

    def test_swipe_separate_category(self):
        swipe = SPEC.replace('__click', '__swipe').replace('category: `click`', 'category: `swipe`')
        cat = build_catalog([page(SPEC), page(swipe)])
        result = compare(cat, [dict(OBS, event_label=OBS['event_label'].replace('__click', '__swipe'), event_category='swipe')])
        self.assertEqual(result['findings'], [])

    def test_query_daily_only_and_bounded(self):
        sql = build_query('kap-chat', 'analytics_432041405')
        self.assertIn("event_name IN ('DA1','DA2')", sql)
        self.assertIn('_TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix', sql)
        self.assertNotIn('user_pseudo_id', sql)
        with self.assertRaises(ValueError): build_query('kap-chat` UNION', 'dataset')


class SourceTest(unittest.TestCase):
    def test_paginates_no_filter(self):
        calls = []
        def request(path, payload):
            calls.append(payload)
            return dict(results=[{'id': 'a' if len(calls) == 1 else 'b'}], has_more=len(calls) == 1, next_cursor='next')
        source = NotionSource('not-printed', 'root', request=request)
        self.assertEqual(len(list(source.all_results('query', post=True))), 2)
        self.assertNotIn('filter', calls[0])
        self.assertEqual(calls[1]['start_cursor'], 'next')

    def test_broken_pagination_fails(self):
        source = NotionSource('x', 'root', request=lambda *_: dict(results=[], has_more=True, next_cursor=None))
        with self.assertRaises(IncompleteSource): list(source.all_results('query', post=True))

    def test_unsupported_blocks_fail(self):
        source = NotionSource('x', 'root', request=lambda *_: dict(results=[{'id': 'x', 'type': 'unsupported'}], has_more=False))
        with self.assertRaises(IncompleteSource): source.blocks('root')


class NotifyTest(unittest.TestCase):
    def test_no_raw_value_or_secret_in_message(self):
        result = compare(build_catalog([page(SPEC)]), [dict(OBS, value='personal secret')])
        result['complete'] = True
        text = slack_text('production', '2026-11-16', '2026-11-22', result)
        self.assertIn('[Prod]', text)
        self.assertNotIn('personal secret', text)

    def test_existing_unknown_receipt_not_reposted(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'receipt.json'
            path.write_text('{"status":"delivery_unknown"}')
            with patch('urllib.request.urlopen') as request:
                result = send_once('https://hooks.slack.com/services/test/redacted/example', 'text', path)
                request.assert_not_called()
                self.assertEqual(result['status'], 'delivery_unknown')

    def test_failed_source_cannot_render_success(self):
        text = slack_text('stage', 'a', 'b', dict(complete=False, failure_type='IncompleteSource'))
        self.assertIn('검수 불완전', text)
        self.assertNotIn('비교 완료', text)


if __name__ == '__main__':
    unittest.main()
