import unittest
from daily_report import summary_text,publish,probe_write,MARKER,PAGE


def reports():
    return {e:dict(start='2026-11-23',end='2026-11-28',as_of_kst='2026-11-28T14:00:00+09:00',
                  complete=False,value_collection=[dict(label='club__club_list__filter__recruiting__click',platform='WEB')],
                  findings=[dict(label='club__club_list__filter__recruiting__click',platforms=['WEB'],reason=r,platform_counts={'WEB':2}) for r in ('value_missing','event_name_mismatch')]) for e in ('stage','production')}


class DailyTests(unittest.TestCase):
    def test_write_probe_keeps_the_existing_text_and_does_not_collect(self):
        calls=[];paragraph={'id':'managed','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':MARKER+'\n기존 요약'},'plain_text':MARKER+'\n기존 요약'}]}}
        def request(method,path,payload=None):
            calls.append((method,path,payload))
            return {'results':[paragraph]} if '/children' in path else paragraph
        result=probe_write('test',request)
        self.assertTrue(result['content_unchanged']);self.assertFalse(result['bigquery_queried'])
        self.assertEqual(sum(c[0]=='PATCH' for c in calls),1)

    def test_overlapping_failures_count_one_label(self):
        catalog={'by_label':{'club__club_list__filter__recruiting__click':[{'platforms':['WEB']}]}}
        text=summary_text(reports(),catalog)
        self.assertIn('Stage Web : 불일치 1 · 미관측 0 · 명세 밖 0 · 정상 0',text)
        self.assertIn('입력 대기·잠정',text)
        self.assertEqual(text.count('• stage/WEB'),1)

    def test_missing_is_not_normal_or_implementation_failure(self):
        r=reports()
        for x in r.values():x['value_collection']=[];x['findings']=[]
        text=summary_text(r,{'by_label':{'new':[{'platforms':['WEB']}]}})
        self.assertIn('불일치 0 · 미관측 1 · 명세 밖 0 · 정상 0',text);self.assertIn('미관측 ≠ 미구현',text)

    def test_requires_both_environments_and_same_period(self):
        r=reports();del r['production']
        with self.assertRaises(ValueError):summary_text(r,{'by_label':{}})

    def test_only_managed_paragraph_is_updated_and_read_back(self):
        calls=[];state={'text':MARKER+'\nprevious'}
        def paragraph(id,text):return {'id':id,'type':'paragraph','paragraph':{'rich_text':[{'text':{'content':text}}]}}
        def request(method,path,payload=None):
            calls.append((method,path,payload))
            if path.startswith('blocks/'+PAGE+'/children'):
                return {'results':[paragraph('managed',state['text']),{'id':'manual','type':'to_do','to_do':{'checked':True}}]}
            if method=='PATCH':
                self.assertEqual(path,'blocks/managed');state['text']=''.join(x['text']['content'] for x in payload['paragraph']['rich_text'])
                return paragraph('managed',state['text'])
            return paragraph('managed',state['text'])
        result=publish('test',MARKER+'\n새 요약','https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1',request)
        self.assertTrue(result['readback_verified']);self.assertEqual(sum(c[0]=='PATCH' for c in calls),1)
        self.assertTrue(all(c[1]!='blocks/manual' for c in calls))

    def test_missing_or_duplicate_marker_does_not_write(self):
        for n in (0,2):
            calls=[]
            def request(method,path,payload=None):
                calls.append(method)
                return {'results':[{'id':str(i),'type':'paragraph','paragraph':{'rich_text':[{'text':{'content':MARKER}}]}} for i in range(n)]}
            with self.assertRaises(RuntimeError):publish('test',MARKER+'\nnew','https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1',request)
            self.assertNotIn('PATCH',calls)

    def test_invalid_link_or_missing_token_does_not_request(self):
        def fail(*a):self.fail('No network call allowed')
        with self.assertRaises(ValueError):publish('test',MARKER+'\nnew','https://evil.invalid',fail)
        with self.assertRaises(RuntimeError):publish('',MARKER+'\nnew','https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1',fail)

    def test_readback_failure_is_not_success(self):
        def request(method,path,payload=None):
            if '/children' in path:return {'results':[{'id':'managed','type':'paragraph','paragraph':{'rich_text':[{'text':{'content':MARKER}}]}}]}
            return {'type':'paragraph','paragraph':{'rich_text':[]}}
        with self.assertRaises(RuntimeError):publish('test',MARKER+'\nnew','https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1',request)

    def test_failure_does_not_show_zero_as_success(self):
        r=reports();r['stage']['failure_type']='PermissionDenied'
        self.assertIn('조회 실패',summary_text(r,{'by_label':{}}))
