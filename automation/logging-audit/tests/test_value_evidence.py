import json
import unittest
from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.environment_evidence import observations, compare_environments
from koin_weekly_audit.notify import detail_markdown
from test_weekly_audit import SPEC, OBS, page


class ValueEvidenceTest(unittest.TestCase):
    def test_expected_actual_and_counts_are_actionable(self):
        cat=build_catalog([page(SPEC)])
        report=compare(cat,[dict(OBS,value='잘못된 버튼',event_count=2),dict(OBS,value='이전 버튼',event_count=4)])
        issue=report['findings'][0]
        self.assertEqual(issue['expected_values'],['"뒤로가기"'])
        self.assertEqual(issue['platform_value_counts']['IOS'],{'"잘못된 버튼"':2,'"이전 버튼"':4})
        report.update(complete=True,start='2026-11-16',end='2026-11-22')
        markdown=detail_markdown({'stage':report})
        self.assertIn('잘못된 버튼',markdown);self.assertIn('(2건)',markdown)

    def test_missing_null_empty_are_distinct(self):
        cat=build_catalog([page(SPEC)])
        report=compare(cat,[dict(OBS,value=None,value_parameter_present=False),
                            dict(OBS,value=None,value_parameter_present=True),dict(OBS,value='',value_parameter_present=True)])
        actual=report['findings'][0]['platform_value_counts']['IOS']
        self.assertEqual(set(actual),{'파라미터 없음','NULL (값 없음)','"" (빈 문자열)'})
        self.assertEqual(report['findings'][0]['expected_values'],['"뒤로가기"'])

    def test_explicit_choices_are_not_false_mismatches(self):
        for choices,values in [('위로 또는 아래로',['위로','아래로']),('로그인 완료 또는 로그인 실패',['로그인 완료','로그인 실패'])]:
            cat=build_catalog([page(SPEC.replace('value: 뒤로가기','value: '+choices))])
            self.assertEqual(compare(cat,[dict(OBS,value=v) for v in values])['findings'],[])
            bad=compare(cat,[dict(OBS,value='오류')])['findings'][0]
            self.assertEqual(bad['reason'],'enum_value_mismatch')
            self.assertEqual(set(bad['expected_values']),{'"'+v+'"' for v in values})

    def test_sensitive_fixed_values_masked_and_dynamic_never_exported(self):
        cat=build_catalog([page(SPEC)])
        for value in ('private@example.com','010-1234-5678','https://secret.example/key','sk-proj-secret'):
            result=compare(cat,[dict(OBS,value=value)])
            self.assertNotIn(value,json.dumps(result,ensure_ascii=False))
        dynamic=build_catalog([page(SPEC.replace('value: 뒤로가기','value: 선택한 게시글 ID'))])
        evidence=observations(dynamic,[dict(OBS,value='PRIVATE')])
        self.assertNotIn('PRIVATE',json.dumps(evidence))
        self.assertNotIn('value',evidence[0]['fields'])

    def test_environment_comparison_uses_observed_sets_not_traffic(self):
        cat=build_catalog([page(SPEC)])
        def env(rows):
            return dict(complete=True,start='2026-11-16',end='2026-11-22',snapshot_sha256='same',observed_evidence=observations(cat,rows))
        a=env([OBS]);b=env([dict(OBS,event_count=99)])
        result=compare_environments({'stage':a,'production':b})
        self.assertEqual(result['same_observed_labels'],1);self.assertEqual(result['differences'],[])
        b=env([dict(OBS,value='다른 값',event_count=7)])
        diff=compare_environments({'stage':a,'production':b})['differences'][0]
        self.assertEqual(diff['field'],'value');self.assertEqual(diff['production'],{'"다른 값"':7})
        self.assertEqual(diff['expected'],['"뒤로가기"'])
        b['complete']=False
        self.assertFalse(compare_environments({'stage':a,'production':b})['complete'])
        b['complete']=True;b['start']='2026-11-09'
        self.assertFalse(compare_environments({'stage':a,'production':b})['complete'])

    def test_masking_does_not_claim_identical_values(self):
        cat=build_catalog([page(SPEC)])
        def env(value):
            return dict(complete=True,start='2026-11-16',end='2026-11-22',snapshot_sha256='same',observed_evidence=observations(cat,[dict(OBS,value=value)]))
        result=compare_environments({'stage':env('first@example.com'),'production':env('second@example.com')})
        self.assertEqual(result['same_observed_labels'],0)
        self.assertEqual(result['masked_fields'],1)
