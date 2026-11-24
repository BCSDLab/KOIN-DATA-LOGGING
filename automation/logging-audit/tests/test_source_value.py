import unittest
from koin_weekly_audit.source_value import source_values, contract_value_sources, audit_markdown
from koin_weekly_audit.contracts import build_catalog
from koin_weekly_audit.environment_evidence import value_collections
from koin_weekly_audit.notify import detail_markdown
from test_weekly_audit import page, SPEC, OBS


class SourceValueTest(unittest.TestCase):
    def test_source_fragment_preserves_child_note_not_rule_interpretation(self):
        text=SPEC.replace('value: 뒤로가기','value: 설정 아이콘 or 새 키워드 추가\n  - 클릭하는 진입점에 따라 달리 해주세요')
        p=page(text);p['url']='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/sha/spec.md'
        cat=build_catalog([p])
        contract=cat['by_label'][OBS['event_label']][0]
        self.assertEqual(contract['allowed_values'],['새 키워드 추가','설정 아이콘'])
        evidence=contract['value_source'][0]
        self.assertIn('클릭하는 진입점에 따라 달리 해주세요',evidence['raw_text'])
        self.assertEqual(evidence['url'],p['url']+'#L6')

    def test_past_value_is_not_used_as_current(self):
        p=page('- 과거 로깅\n- value: 예전값\n'+SPEC)
        evidence=source_values(p)
        self.assertEqual(len(evidence),1)
        self.assertIn('뒤로가기',evidence[0]['raw_text'])
        self.assertNotIn('예전값',evidence[0]['raw_text'])

    def test_no_contract_is_not_same_as_empty_value_in_source(self):
        cat=build_catalog([page(SPEC.replace('value: 뒤로가기','value:'))])
        evidence=contract_value_sources(cat,OBS['event_label'],'IOS')
        self.assertEqual(evidence['status'],'source_present')
        self.assertEqual(evidence['sources'][0]['declared_text'],'')
        self.assertEqual(contract_value_sources(cat,'unknown','IOS')['status'],'no_current_contract')

    def test_report_keeps_source_and_interpretation_separate_and_audits_all_pages(self):
        a=page(SPEC.replace('value: 뒤로가기','value: 기존 미기재 유지'))
        b=page('# 참고 문서');b['title']='참고';b['url']='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/sha/ref.md'
        cat=build_catalog([a,b])
        report=dict(complete=True,start='2026-11-16',end='2026-11-22',value_collection=value_collections(cat,[dict(OBS,value=None,value_parameter_present=False)]))
        result=detail_markdown({'production':report})
        self.assertIn('GitHub 원문 value 표기:  - value: 기존 미기재 유지',result)
        self.assertIn('자동 판정 기준:',result)
        audit=audit_markdown(cat['coverage'])
        self.assertIn('참고',audit);self.assertIn('기존 미기재 유지',audit)
