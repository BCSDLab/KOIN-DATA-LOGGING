import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from koin_weekly_audit.version_scope import targets_for, select_scope, VersionScopeError
from koin_weekly_audit.notify import slack_text, detail_markdown
from run import audit
from test_runner import Collector


def row(platform, version, count=1, day='20261118'):
    return dict(platform=platform, app_version=version, event_count=count, event_date=day,
                event_name='DA1', event_label='unregistered_' + str(version), value='private@example.com',
                screen_view='screen', event_category='click')


class VersionScopeTest(unittest.TestCase):
    def test_mobile_exact_targets_and_web_unchanged(self):
        rows = [row('IOS','5.2.6'), row('IOS','5.2.5',2), row('IOS','5.3.0',3),
                row('ANDROID','5.2.4'), row('ANDROID','4.9.9',4), row('WEB',None,5)]
        selected, scope = select_scope(rows, {'IOS':'5.2.6','ANDROID':'5.2.4'})
        self.assertEqual([(r['platform'],r['app_version']) for r in selected], [('IOS','5.2.6'),('ANDROID','5.2.4'),('WEB',None)])
        self.assertEqual(scope['excluded_events'],9)
        self.assertEqual({r['classification'] for r in scope['reference']},{'older','newer_or_other'})
        self.assertNotIn('private@example.com',json.dumps(scope))

    def test_unknown_and_semantic_versions_are_reference_only(self):
        selected, scope = select_scope([row('IOS','5.2.9'),row('IOS',None),row('IOS','SECRET')], {'IOS':'5.2.10','ANDROID':'5.2.4'})
        self.assertEqual(selected,[])
        self.assertEqual(scope['reference'][1]['classification'],'older')
        self.assertEqual(scope['excluded_events'],3)
        self.assertNotIn('SECRET',json.dumps(scope))

    def test_missing_targets_fail_closed(self):
        with self.assertRaises(VersionScopeError): select_scope([], {'IOS':'5.2.6'})
        with tempfile.TemporaryDirectory() as folder:
            policy=Path(folder)/'policy.json';policy.write_text('{}')
            with self.assertRaises(VersionScopeError): targets_for('stage',policy)

    def test_runner_filters_rules_investigation_and_previous_period(self):
        seen=[]
        def investigator(catalog, report, rows):
            seen.append((report['environment'],rows))
            return dict(status='completed')
        rows=[row('IOS','5.2.6'),row('IOS','5.2.5',2),row('IOS','5.3.0',3),
              row('ANDROID','5.2.4',4),row('ANDROID','5.2.3',5),row('WEB',None,6),
              row('IOS','4.7.0',7,'20261114')]
        with tempfile.TemporaryDirectory() as folder:
            reports=audit(date(2026,11,16),folder,folder+'/state',collector=Collector(),
                          query=lambda *a,**kw:dict(rows=rows,complete=True,missing_daily_tables=[]),investigator=investigator)
        self.assertEqual(reports['stage']['events'],11)
        self.assertEqual(reports['production']['events'],12)
        self.assertEqual(reports['stage']['previous_period_recheck']['events'],0)
        for environment, selected in seen:
            target=reports[environment]['version_scope']['targets']
            self.assertTrue(all(r['platform']=='WEB' or r['app_version']==target[r['platform']] for r in selected))
            self.assertEqual(len(selected),3)
        stage=reports['stage']
        text=slack_text('stage',stage['start'],stage['end'],stage)
        self.assertIn('iOS 5.2.6:',text)
        self.assertNotIn('5.3.0',text)
        self.assertIn('5.3.0',detail_markdown(reports))
        self.assertNotIn('private@example.com',detail_markdown(reports))

    def test_no_target_events_is_not_healthy(self):
        with tempfile.TemporaryDirectory() as folder:
            reports=audit(date(2026,11,16),folder,folder+'/state',collector=Collector(),
                query=lambda *a,**kw:dict(rows=[row('IOS','4.7.0')],complete=True,missing_daily_tables=[]),
                investigator=lambda *a:dict(status='completed'))
        text=slack_text('stage','2026-11-16','2026-11-22',reports['stage'])
        self.assertIn('iOS 5.2.6: 수집 0건',text)
        self.assertNotIn('이상 없음',text)
