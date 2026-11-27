import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from run import audit, custom_range
from test_runner import Collector
from koin_weekly_audit.bigquery_source import fetch, build_query
from koin_weekly_audit.notify import slack_payload, detail_markdown


class CustomRangeTest(unittest.TestCase):
    def test_range_validation(self):
        self.assertEqual(custom_range('2026-11-23','2026-11-27', date(2026,11,27)), (date(2026,11,23),date(2026,11,27)))
        for start,end in [('2026-11-28','2026-11-27'),('2026-11-23','2026-11-28'),('2026-11-23',None)]:
            with self.assertRaises(ValueError): custom_range(start,end,date(2026,11,27))

    def test_requested_end_and_live_flag_reach_query_and_report(self):
        calls=[]
        def query(project,dataset,start,end,**kwargs):
            calls.append((start,end,kwargs))
            return dict(rows=[],complete=True,missing_daily_tables=[])
        with tempfile.TemporaryDirectory() as folder:
            reports=audit(date(2026,11,23),folder,folder+'/state',collector=Collector(),query=query,
                          investigator=lambda *a: {'status':'completed'},end=date(2026,11,27),include_intraday=True)
            self.assertEqual(len(calls),2)
            self.assertTrue(all(c[:2]==('2026-11-20','2026-11-27') and c[2]['include_intraday'] for c in calls))
            for r in reports.values():
                self.assertEqual(r['end'],'2026-11-27');self.assertTrue(r['custom_range'])
            from pathlib import Path
            self.assertTrue((Path(folder)/'2026-11-23_to_2026-11-27'/'stage-report.json').is_file())

    def test_live_notice_visible_without_removed_metadata(self):
        r=dict(complete=True,start='2026-11-23',end='2026-11-27',custom_range=True,provisional=True,
               as_of_kst='2026-11-27T15:00:00+09:00',findings=[])
        message=json.dumps(slack_payload('stage',r['start'],r['end'],r),ensure_ascii=False)
        self.assertIn('기간 지정 로깅 검수',message);self.assertIn('당일 수집 진행 중',message)
        for removed in ('명세 기준:', '상세 분석:', 'AI API:'):self.assertNotIn(removed,message)
        details=detail_markdown({'stage':r})
        self.assertLess(details.index('당일 수집 진행 중'),details.index('## 플랫폼별 요약'))

    def test_intraday_query_date_is_validated(self):
        with self.assertRaises(ValueError):build_query('project-id','dataset',"20261127' OR TRUE")

    def test_live_table_fallback_and_daily_priority(self):
        today=datetime.now(timezone(timedelta(hours=9))).date()
        suffix=today.strftime('%Y%m%d')
        for daily,live,include,expected_live,missing in [
            (False,True,True,True,False),(True,True,True,False,False),
            (False,True,False,False,True),(False,False,True,False,True)]:
            tables=([SimpleNamespace(table_id='events_'+suffix)] if daily else [])+([SimpleNamespace(table_id='events_intraday_'+suffix)] if live else [])
            queries=[]
            job=SimpleNamespace(result=lambda timeout: [],job_id='mock-job',total_bytes_processed=0)
            def query(sql,**kwargs):queries.append(sql);return job
            client=SimpleNamespace(list_tables=lambda *a:tables,query=query)
            bq=SimpleNamespace(Client=lambda **kw:client,QueryJobConfig=lambda **kw:kw,ScalarQueryParameter=lambda *a:a)
            with patch.dict(sys.modules,{'google':SimpleNamespace(cloud=SimpleNamespace(bigquery=bq)), 'google.cloud':SimpleNamespace(bigquery=bq),'google.cloud.bigquery':bq}):
                result=fetch('project-id','dataset',today.isoformat(),today.isoformat(),include_intraday=include)
            self.assertEqual('intraday_'+suffix in queries[0],expected_live)
            self.assertEqual(result['missing_daily_tables'],['events_'+suffix] if missing else [])
            self.assertEqual(result['complete'],not missing)
