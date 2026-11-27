import json
import unittest
from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.environment_evidence import value_collections
from koin_weekly_audit.handoff import developer_handoff
from koin_weekly_audit.notify import detail_markdown
from test_weekly_audit import SPEC, OBS, page


class DeveloperHandoffTest(unittest.TestCase):
    def test_all_wrong_fields_are_reported_even_with_legacy_event_name(self):
        cat=build_catalog([page(SPEC)])
        report=compare(cat,[dict(OBS,event_name='CAMPUS',screen_view='wrong',event_category='swipe',value='스와이프')])
        self.assertEqual({f['field'] for f in report['findings']},{'event_name','screen_view','event_category','value'})
        report.update(complete=True,start='2026-11-16',end='2026-11-22',source_revision='a'*40,query_job_id='verified-query')
        result=developer_handoff({'production':report})
        for field in ('event_name','screen_view','event_category','value'):
            self.assertIn('다른 필드: '+field,result)
        for value in ('뒤로가기','스와이프','wrong','20261122','5.2.6','verified-query'):
            self.assertIn(value,result)

    def test_typo_event_name_is_not_silently_excluded(self):
        cat=build_catalog([page(SPEC)])
        result=compare(cat,[dict(OBS,event_name='DA3')])
        self.assertEqual(result['events'],3)
        self.assertEqual(result['findings'][0]['reason'],'event_name_mismatch')
        bad=compare(cat,[dict(OBS,event_name='DA3',event_label='unregistered',duplicate_param_keys=1)])
        self.assertEqual({f['reason'] for f in bad['findings']},{'unexpected_event_name','unregistered_label','duplicate_parameter_key'})
        self.assertEqual(compare(cat,[dict(OBS,event_name='session_start',event_label=None)])['events'],0)

    def test_unspecified_value_has_actual_collection_without_false_error(self):
        cat=build_catalog([page(SPEC.replace('value: 뒤로가기','value: 기존 미기재 유지'))])
        rows=[dict(OBS,value=None,value_parameter_present=False,event_count=45)]
        report=compare(cat,rows)
        self.assertEqual(report['findings'],[])
        report.update(complete=True,start='2026-11-16',end='2026-11-22',value_collection=value_collections(cat,rows))
        output=detail_markdown({'production':report})
        self.assertIn('value 미지정 · 명세: 기존 미기재 유지',output)
        self.assertIn('파라미터 없음 (45건)',output)
        self.assertIn(OBS['event_label'],output)

    def test_collection_separates_null_empty_string_and_string_null(self):
        cat=build_catalog([page(SPEC)])
        rows=[dict(OBS,value=None,value_parameter_present=True),dict(OBS,value=''),dict(OBS,value='null'),dict(OBS,value='private@example.com')]
        collection=value_collections(cat,rows)
        self.assertEqual(collection[0]['actual']['NULL (값 없음)'],3)
        self.assertEqual(collection[0]['actual']['"null"'],3)
        self.assertEqual(collection[0]['actual']['"" (빈 문자열)'],3)
        self.assertNotIn('private@example.com',json.dumps(collection))

class ReadableDetailTest(unittest.TestCase):
    def test_one_card_per_label_and_field_counts_are_not_added(self):
        report = compare(build_catalog([page(SPEC)]), [dict(OBS, event_name='CAMPUS', screen_view='wrong', event_category='swipe', value='스와이프')])
        report.update(complete=True, start='2026-11-16', end='2026-11-22', platform_summary={'IOS': {'events': 3}})
        output = detail_markdown({'stage': report})
        self.assertEqual(output.count('#### ' + OBS['event_label'] + '\n'), 1)
        for field in ('event_name', 'screen_view', 'event_category', 'value'):
            self.assertIn('| **' + field + '**', output)
        self.assertIn('필드별 건수는 중복될 수 있습니다', output)
        self.assertLess(output.index('## 플랫폼별 요약'), output.index('# 개발자 전달용 상세'))
        self.assertLess(output.index('# 개발자 전달용 상세'), output.index('## 전체 분석 근거'))
        self.assertEqual(output.count('<a name="audit-stage-ios"></a>'), 1)
        self.assertEqual(output.count('<details>'), output.count('</details>'))
        self.assertIn('명세 바로가기', output)

    def test_zero_and_incomplete_are_visible_in_overview(self):
        report = dict(complete=False, start='2026-11-16', end='2026-11-22', findings=[])
        self.assertIn('조회 불완전 · 판정 불가', detail_markdown({'stage': report}))
        report['complete'] = True
        self.assertIn('수집 없음 · 판정 없음', detail_markdown({'stage': report}))


class SpecificationLocationTest(unittest.TestCase):
    def test_handoff_labels_source_with_decoded_service_and_page(self):
        from koin_weekly_audit.handoff import specification_link
        url = 'https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/sha/event-log/16-%EB%8B%A4%EA%B5%AD%EC%96%B4/%EC%96%B8%EC%96%B4-%EB%B3%80%EA%B2%BD.md'
        result = specification_link(url)
        self.assertIn('[16-다국어/언어-변경.md]', result)
        self.assertIn('](' + url + ')', result)
