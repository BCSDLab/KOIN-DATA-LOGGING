import unittest

from koin_weekly_audit.contracts import build_catalog, compare
from test_weekly_audit import page, SPEC, OBS


class MultiContractTest(unittest.TestCase):
    def test_full_contracts_keep_their_own_fields(self):
        second = SPEC.replace('room_common', 'room_detail').replace('DA1', 'DA2').replace('__click', '__swipe').replace('category: `click`', 'category: `swipe`')
        cat = build_catalog([page(SPEC + '\n### 두 번째 동작\n' + second)])
        self.assertEqual(len(cat['by_label']), 2)
        first = cat['by_label'][OBS['event_label']][0]
        self.assertEqual(first['names'], ['DA1'])
        self.assertEqual(first['categories'], ['click'])
        second_label = 'real_estate__room_detail__navigation__back__swipe'
        result = compare(cat, [OBS, dict(OBS, event_label=second_label, screen_view='room_detail', event_name='DA2', event_category='swipe')])
        self.assertEqual(result['findings'], [])

    def test_shared_tail_fields_keep_both_screen_contracts(self):
        text = '''- 새 로깅
 - 설명: 분류 화면에서 검색한다.
 - screen_view: department_main
 - event_label: department__department_main__search__click
 목록 화면
 - 설명: 목록 화면에서 검색한다.
 - screen_view: department_list
 - event_label: department__department_list__search__click
 - event_name: DA2
 - value: {검색어}
 - event_category: click'''
        cat = build_catalog([page(text)])
        self.assertEqual(len(cat['by_label']), 2)
        for screen in ('department_main', 'department_list'):
            label = 'department__' + screen + '__search__click'
            result = compare(cat, [dict(OBS, event_name='DA2', event_label=label, screen_view=screen, value='검색어')])
            self.assertEqual(result['findings'], [])

    def test_select_category_is_validated(self):
        text = SPEC.replace('__click', '__select').replace('category: `click`', 'category: `select`')
        cat = build_catalog([page(text)])
        result = compare(cat, [dict(OBS, event_label=OBS['event_label'].replace('__click', '__select'))])
        self.assertEqual([r['reason'] for r in result['findings']], ['event_category_mismatch'])

    def test_sibling_note_does_not_become_allowed_category(self):
        cat = build_catalog([page(SPEC + '\n - 설명 외 참고: select 동작과 혼동하지 않는다.')])
        contract = cat['by_label'][OBS['event_label']][0]
        self.assertEqual(contract['categories'], ['click'])

    def test_missing_required_contract_field_is_review_not_unregistered(self):
        cat = build_catalog([page(SPEC.replace(' - event_name: `DA1`\n', ''))])
        result = compare(cat, [OBS])
        self.assertEqual(result['findings'][0]['reason'], 'specification_conflict')


if __name__ == '__main__':
    unittest.main()
