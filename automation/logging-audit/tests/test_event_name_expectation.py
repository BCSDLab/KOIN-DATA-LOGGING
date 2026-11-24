import unittest
from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.handoff import developer_handoff
from test_weekly_audit import SPEC, OBS, page


class EventNameExpectationTest(unittest.TestCase):
    def test_current_label_legacy_or_typo_uses_only_exact_declared_name(self):
        for expected in ('DA1','DA2'):
            catalog=build_catalog([page(SPEC.replace('`DA1`','`'+expected+'`'))])
            for actual in ('CAMPUS','DA3'):
                report=compare(catalog,[dict(OBS,event_name=actual)])
                issue=next(f for f in report['findings'] if f['field']=='event_name')
                self.assertEqual(issue['expected_values'],[expected])
                self.assertEqual(issue['platform_expected_values'],{'IOS':[expected]})

    def test_no_current_contract_does_not_invent_expected_name(self):
        catalog=build_catalog([page(SPEC)])
        report=compare(catalog,[dict(OBS,event_name='CAMPUS',event_label='old_label')])
        issue=next(f for f in report['findings'] if f['field']=='event_name')
        self.assertIn('정답 미확정',issue['expected_values'][0])
        self.assertNotEqual(issue['expected_values'],['DA1','DA2'])

    def test_conflicting_names_are_marked_as_conflict_not_jointly_allowed(self):
        catalog=build_catalog([page(SPEC),page(SPEC.replace('`DA1`','`DA2`'))])
        report=compare(catalog,[dict(OBS,event_name='CAMPUS')])
        issue=next(f for f in report['findings'] if f['field']=='event_name')
        self.assertIn('충돌',issue['expected_values'][0])
        mixed=build_catalog([page(SPEC.replace('`DA1`','`DA1` 또는 `DA2`'))])
        self.assertIn(OBS['event_label'],mixed['conflicts'])

    def test_platform_source_is_used_and_handoff_preserves_provenance(self):
        a=page(SPEC,['IOS']);b=page(SPEC.replace('`DA1`','`DA2`'),['ANDROID'])
        a['url']='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/revision/ios.md'
        b['url']='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/revision/android.md'
        report=compare(build_catalog([a,b]),[dict(OBS,event_name='CAMPUS'),dict(OBS,event_name='CAMPUS',platform='ANDROID')])
        issue=next(f for f in report['findings'] if f['field']=='event_name')
        self.assertEqual(issue['platform_expected_values'],{'IOS':['DA1'],'ANDROID':['DA2']})
        report.update(complete=True,start='2026-11-16',end='2026-11-22')
        output=developer_handoff({'stage':report})
        self.assertIn('명세 값: DA1',output)
        self.assertIn('명세 값: DA2',output)
        self.assertNotIn('명세 값: DA1, DA2',output)
        self.assertIn('/ios.md',output);self.assertIn('/android.md',output)
