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
