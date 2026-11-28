"""Daily, read-only collection; update one managed Notion summary, never Slack."""
import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

from run import audit, KST
from koin_weekly_audit.notify import detail_markdown

PAGE = '4230221954bc815fa3e0e2323d99ff8c'
MARKER = '오늘의 로깅 검수'
REASONS = {'value_missing':'value 누락', 'fixed_value_mismatch':'고정 value 불일치',
           'enum_value_mismatch':'허용 value 불일치', 'event_name_mismatch':'event_name 불일치',
           'event_category_mismatch':'category 불일치', 'screen_view_mismatch':'화면 불일치',
           'previous_naming_label':'이전 네이밍', 'historical_label_still_collected':'과거 로그 지속',
           'legacy_event_name':'과거 event_name', 'unregistered_label':'명세 밖 라벨',
           'specification_conflict':'명세 확인 필요', 'platform_mismatch':'미지원 플랫폼'}


def summary_text(reports, catalog):
    """Count unique labels; never add overlapping field-failure counts."""
    periods = {(r['start'],r['end']) for r in reports.values()}
    if len(periods)!=1 or set(reports)!={'stage','production'}:
        raise ValueError('Both environments and one period are required')
    start,end=next(iter(periods))
    lines=[MARKER, (f'{end} 하루 기준' if start==end else f'{start} ~ {end}')+' · 오늘 수집은 잠정',
           '갱신: '+max(r['as_of_kst'] for r in reports.values()),
           '플랫폼별 수집 상태']
    priorities=[]
    for env,name in [('stage','Stage'),('production','Production')]:
        r=reports[env]
        status='입력 대기·잠정' if not r.get('complete') else '관측 범위 검수'
        for platform,short in [('IOS','iOS'),('ANDROID','Android'),('WEB','Web')]:
            supported={label for label,cs in catalog['by_label'].items() if any(platform in c['platforms'] for c in cs)}
            seen={row['label'] for row in r.get('value_collection',[]) if row['platform']==platform}
            findings=[f for f in r.get('findings',[]) if platform in f.get('platforms',[])]
            bad={f['label'] for f in findings}&supported&seen
            counts=[len((seen&supported)-bad),len(bad),len(supported-seen),len(seen-supported)]
            version=r.get('version_scope',{}).get('targets',{}).get(platform,'')
            if r.get('failure_type'):
                lines.append(f'{name} {short} {version}: 조회 실패 · 기존 상세를 정상으로 간주하지 않음')
                continue
            lines.append(f'{name} {short} {version}: 불일치 {counts[1]} · 미관측 {counts[2]} · 명세 밖 {counts[3]} · 정상 {counts[0]} · '+status)
            for f in findings:
                label=f.get('label') or '(라벨 없음)'
                if not re.fullmatch(r'[A-Za-z0-9_ ()-]{1,180}',label):label='라벨 형식 확인 필요'
                contracts=catalog['by_label'].get(label,[])
                title=contracts[0].get('title',label) if contracts else label
                title=re.sub(r'^[\d\s.,·-]+','',title).replace('_',' ')
                expected=f.get('platform_expected_values',{}).get(platform,f.get('expected_values',[]))
                target=' / '.join(str(v).strip(' "“”') for v in expected[:2])
                if f['reason']=='value_missing':action='value 누락 → '+target
                elif f['reason']=='specification_conflict':action='명세 담당자가 기준을 먼저 확인'
                elif label.startswith('cafeteria__dining__'):action='동결 범위 확인 필요 · 수정 보류'
                else:
                    actual=f.get('platform_observed_values',{}).get(platform,[])
                    shown=' / '.join(str(v) for v in actual[:2]) if f.get('field') in ('event_name','screen_view','event_category','platform') else ''
                    action=REASONS.get(f['reason'],'파라미터 확인')+(' '+shown if shown else '')+(' → '+target if target else '')
                tier=0 if f['reason'] in ('value_missing','fixed_value_mismatch','enum_value_mismatch','event_name_mismatch','event_category_mismatch','screen_view_mismatch') and not label.startswith('cafeteria__dining__') else 1
                priorities.append((tier,f.get('platform_counts',{}).get(platform,0),env,platform,label,action,title))
    lines+=['','우선 확인']
    used=set()
    for tier,count,env,p,label,reason,title in sorted(priorities,key=lambda x:(x[0],-x[1],x[2:])):
        key=(env,p,label)
        if key in used:continue
        used.add(key);lines.append(f'• {env}/{p} {title}: {reason}')
        if len(used)==3:break
    if not used:lines.append('• 확인된 오류 없음. 미관측·입력 대기는 정상 수집과 구분합니다.')
    lines+=['','미관측 ≠ 미구현. 담당자 실행 체크와 과거 기록은 아래 상세에 보존합니다.']
    return '\n'.join(lines)


def notion_request(token,method,path,payload=None):
    req=urllib.request.Request('https://api.notion.com/v1/'+path,method=method,
        headers={'Authorization':'Bearer '+token,'Notion-Version':'2025-09-03','Content-Type':'application/json'},
        data=None if payload is None else json.dumps(payload).encode('utf8'))
    try:
        with urllib.request.urlopen(req,timeout=40) as response:return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError('Notion HTTP '+str(exc.code)+'; report page access/write capability required') from None
    except (OSError,ValueError):raise RuntimeError('Notion request failed; check report before retrying') from None


def plain(block):
    return ''.join(t.get('plain_text',t.get('text',{}).get('content','')) for t in block.get('paragraph',{}).get('rich_text',[]))


def probe_write(token,request=None):
    if not token:raise RuntimeError('Notion report token missing')
    call=request or (lambda method,path,payload=None:notion_request(token,method,path,payload))
    page=call('GET','blocks/'+PAGE+'/children?page_size=100')
    if page.get('has_more'):raise RuntimeError('Probe requires a bounded report header')
    matches=[b for b in page['results'] if b.get('type')=='paragraph' and plain(b).splitlines()[0:1]==[MARKER]]
    if len(matches)!=1:raise RuntimeError('Expected exactly one managed summary paragraph')
    block=matches[0];rich=[]
    for item in block['paragraph']['rich_text']:
        if item['type']!='text':raise RuntimeError('Probe only supports existing plain-text report summary')
        rich.append({k:item[k] for k in ('type','text','annotations') if k in item})
    call('PATCH','blocks/'+block['id'],{'paragraph':{'rich_text':rich}})
    final=call('GET','blocks/'+block['id'])
    if plain(final)!=plain(block):raise RuntimeError('Notion probe readback mismatch')
    return {'notion_write_verified':True,'content_unchanged':True,'bigquery_queried':False,'slack_sent':False}


def publish(token,text,detail_url,request=None):
    """Never recurse, append/delete blocks, or touch checklists and history."""
    if not token:raise RuntimeError('Notion report token missing')
    if not text.startswith(MARKER+'\n'):raise ValueError('Summary marker missing')
    if not re.fullmatch(r'https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/\d+(?:#summary-\d+)?',detail_url):
        raise ValueError('Invalid detail URL')
    call=request or (lambda method,path,payload=None:notion_request(token,method,path,payload))
    blocks=[];cursor=None;seen=set()
    while True:
        path='blocks/'+PAGE+'/children?page_size=100'
        if cursor:path+='&start_cursor='+urllib.parse.quote(cursor,safe='')
        page=call('GET',path);blocks.extend(page['results'])
        if not page.get('has_more'):break
        cursor=page.get('next_cursor')
        if not cursor or cursor in seen:raise RuntimeError('Notion pagination incomplete')
        seen.add(cursor)
    matches=[b for b in blocks if b.get('type')=='paragraph' and plain(b).splitlines()[0:1]==[MARKER]]
    if len(matches)!=1:raise RuntimeError('Expected exactly one managed summary paragraph')
    rich=[{'type':'text','text':{'content':text[i:i+1800]}} for i in range(0,len(text),1800)]
    rich.append({'type':'text','text':{'content':'\n상세 결과 보기','link':{'url':detail_url}}})
    payload={'paragraph':{'rich_text':rich}}
    block_id=matches[0]['id'];call('PATCH','blocks/'+block_id,payload)
    final=call('GET','blocks/'+block_id)
    if plain(final)!=text+'\n상세 결과 보기':raise RuntimeError('Notion summary readback mismatch')
    return {'page_id':PAGE,'block_id':block_id,'readback_verified':True}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='reports/daily');parser.add_argument('--publish',action='store_true')
    parser.add_argument('--probe-notion',action='store_true')
    parser.add_argument('--probe-notion-write',action='store_true')
    args=parser.parse_args();today=datetime.now(KST).date();start=today
    if args.probe_notion_write:
        print(json.dumps(probe_write(os.getenv('NOTION_REPORT_TOKEN',''))));return
    if args.probe_notion:
        token=os.getenv('NOTION_REPORT_TOKEN','')
        if not token:raise RuntimeError('Notion report token missing')
        # A read-only connection probe: publishing is independently verified after deployment.
        page=notion_request(token,'GET','pages/'+PAGE)
        if page.get('id','').replace('-','')!=PAGE:raise RuntimeError('Unexpected report page')
        print(json.dumps({'notion_report_access':True,'writes':False,'slack_sent':False}));return
    # send is explicitly false and no webhook is needed by this entry point.
    reports=audit(start,args.output,'.audit-state/daily',send=False,end=today,include_intraday=True)
    if os.getenv('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(detail_markdown(reports),encoding='utf8')
    folder=Path(args.output)/(start.isoformat()+'_to_'+today.isoformat())
    catalog=json.loads((folder/'contract-snapshot.json').read_text(encoding='utf8')) if (folder/'contract-snapshot.json').is_file() else {'by_label':{}}
    text=summary_text(reports,catalog);(folder/'notion-summary.txt').write_text(text,encoding='utf8')
    detail=next((r.get('detail_url') for r in reports.values() if r.get('detail_url')),'')
    if args.publish:
        receipt=publish(os.getenv('NOTION_REPORT_TOKEN',''),text,detail)
        (folder/'notion-publish.json').write_text(json.dumps(receipt),encoding='utf8')
    print(json.dumps({'daily_summary_written':True,'notion_published':args.publish,'slack_sent':False}))
    if any(r.get('failure_type') for r in reports.values()):raise SystemExit(1)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        # Neither a credential nor an HTTP request/response is printed.
        print('Daily report failed: '+str(exc) if type(exc) in (RuntimeError,ValueError) else 'Daily report failed: '+type(exc).__name__)
        raise SystemExit(2)
