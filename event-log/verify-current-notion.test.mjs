import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
import {verifyCurrent,sha256,META} from './verify-current-notion.mjs';

function fixture(t){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'notion-sync-test-'));
 t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
 const write=(p,s)=>{fs.mkdirSync(path.dirname(path.join(root,p)),{recursive:true});fs.writeFileSync(path.join(root,p),s);};
 const read=p=>fs.readFileSync(path.join(root,p),'utf8');
 const doc='event-log/01-service/sample.md',id='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',blankId='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';
 const a='11111111-1111-1111-1111-111111111111',b='22222222-2222-2222-2222-222222222222';
 const image=id=>'<image source="notion-file-block://00000000-0000-0000-0000-000000000000/'+id+'?name=image.png" />';
 const md=id=>'![참고사진](../../assets/'+id+'.png)';
 const source='<toggle>\n과거 로깅\n- event_label: old\n- value: 예전\n'+image(a)+'\n</toggle>\n<toggle>\n새 로깅\n- event_label: service__screen__target__click\n- value: 새 값\n'+image(b)+'\n</toggle>';
 const properties={platform:['ANDROID'],상태:'로깅 필요',url:'https://app.notion.com/p/'+id};
 const tick=String.fromCharCode(96),body='## 과거 로깅\n- event_label: old\n- value: 예전\n'+md(a)+'\n## 새 로깅\n- event_label: service__screen__target__click\n- value: 새 값\n'+md(b);
 const output='# Sample\n\n플랫폼: ANDROID\n[Notion 기준 명세]('+properties.url+')\n원본 ID: '+tick+id+tick+'\n\n<!-- notion-body:start -->\n'+body+'\n<!-- notion-body:end -->\n<details>\n<summary>Notion 원문 속성 전체</summary>\n\n'+tick.repeat(3)+'json\n'+JSON.stringify(properties)+'\n'+tick.repeat(3)+'\n</details>\n';
 write(doc,output);
 const images=[a,b].map((id,i)=>{const bytes=Buffer.from('image-'+i),asset='assets/'+id+'.png';write(asset,bytes);return {id,asset,bytes:bytes.length,sha256:sha256(bytes),git_blob_sha:crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex')};});
 const sourcePages=[{id,title:'Sample',service:'주변상점',url:properties.url,original_body:source,platforms:['ANDROID'],properties},{id:blankId,service:'주변상점',original_body:'',url:'https://app.notion.com/p/'+blankId}];
 const gz=zlib.gzipSync(JSON.stringify(sourcePages));write(META+'/source-pages.json.gz',gz);
 const entry={notion_id:id,title:'Sample',service:'주변상점',path:doc,notion_url:properties.url,source_body_sha256:sha256(source),output_sha256:sha256(output),platforms:['ANDROID'],image_ids:[a,b]};
 const manifest={service:'주변상점',pages:[entry],blank_pages:[{notion_id:blankId,service:'주변상점',url:'https://app.notion.com/p/'+blankId}]};
 write(META+'/services/01.json',JSON.stringify(manifest));
 write(META+'/images/01.json',JSON.stringify(images));
 write(META+'/summary.json',JSON.stringify({notion_rows:2,nonblank_pages:1,blank_pages:1,source_snapshot:{path:META+'/source-pages.json.gz',sha256:sha256(gz),records:2},services:[{path:'services/01.json'}],images:{unique_files:2,occurrences:2},previous_exports:[]}));
 write('event-log/01-service/README.md','[Sample](sample.md)\n[Blank](https://app.notion.com/p/'+blankId+')\n');
 const active=['주변상점','복덕방','사장님','식단','버스','게시판','배너','홈화면 리디자인','콜밴팟','학교 부서 정보','팀원 모집','로그인/회원가입/정보수정 V2','시간표','모의수강신청','강제 업데이트','다국어 지원'];
 write('README.md',active.map(n=>'['+n+'](event-log/01-service/README.md)').join('\n')+'\n## 레거시 서비스\n');
 const mutate=fn=>{const changed=fn(read(doc));write(doc,changed);manifest.pages[0].output_sha256=sha256(changed);write(META+'/services/01.json',JSON.stringify(manifest));};
 return {root,write,read,doc,mutate,a,b,md,manifest};
}
test('current source snapshot, metadata, references and image bytes all pass',t=>{const f=fixture(t);assert.deepEqual(verifyCurrent(f.root).errors,[]);});
test('changed current value fails even after refreshing output hash',t=>{const f=fixture(t);f.mutate(s=>s.replace('- value: 새 값','- value: 다른 값'));assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Source prose')));});
test('changed past value is rejected',t=>{const f=fixture(t);f.mutate(s=>s.replace('- value: 예전','- value: 손실'));assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Source prose')));});
test('moving a photo into the wrong section fails with its page sequence intact',t=>{const f=fixture(t);f.mutate(s=>s.replace(f.md(f.a)+'\n## 새 로깅','## 새 로깅\n'+f.md(f.a)));assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Source prose')));});
test('changed image bytes are rejected',t=>{const f=fixture(t);f.write('assets/'+f.a+'.png','corrupted');assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Image bytes')));});
test('changed platform property is rejected despite a new output hash',t=>{const f=fixture(t);f.mutate(s=>s.replace('"platform":["ANDROID"]','"platform":["WEB"]'));assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Properties')));});
test('unlisted reader documents are rejected',t=>{const f=fixture(t);f.write('event-log/01-service/extra.md','# Unexpected');assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Unmapped')));});
test('missing service-list entry is rejected',t=>{const f=fixture(t);f.write('event-log/01-service/README.md','[Blank](https://app.notion.com/p/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb)');assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Service index')));});
test('logging fields inserted outside the source body are rejected',t=>{const f=fixture(t);f.mutate(s=>s+'\n## 새 로깅\n- value: injected\n');assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('outside source body')));});
test('duplicate body markers are rejected',t=>{const f=fixture(t);f.mutate(s=>s+'\n<!-- notion-body:start -->\n<!-- notion-body:end -->\n');assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('marker uniqueness')));});
test('changed Notion source snapshot is rejected',t=>{const f=fixture(t);f.write(META+'/source-pages.json.gz',zlib.gzipSync('[]'));assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Source snapshot file hash')));});
test('percent-encoded parentheses in a valid service-list filename are accepted',t=>{const f=fixture(t);const renamed='event-log/01-service/(sample).md';f.write(renamed,f.read(f.doc));fs.unlinkSync(path.join(f.root,f.doc));f.manifest.pages[0].path=renamed;f.write(META+'/services/01.json',JSON.stringify(f.manifest));f.write('event-log/01-service/README.md',f.read('event-log/01-service/README.md').replace('sample.md','%28sample%29.md'));assert.deepEqual(verifyCurrent(f.root).errors,[]);});


test('confirmed blank retirement permits removing only the blank link',t=>{
 const f=fixture(t),id=f.manifest.blank_pages[0].notion_id;
 f.write('docs/current/removed-blank-pages.json',JSON.stringify({pages:[{notion_id:id,status:'in_trash',source_body_empty:true}]}));
 f.write('event-log/01-service/README.md','[Sample](sample.md)\n');
 const result=verifyCurrent(f.root);assert.deepEqual(result.errors,[]);assert.equal(result.activeBlankPages,0);assert.equal(result.retiredBlankPages,1);
});
test('unrecorded removal of a blank link fails',t=>{
 const f=fixture(t);f.write('event-log/01-service/README.md','[Sample](sample.md)\n');
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Blank page link')));
});
test('a nonblank page cannot be retired as blank',t=>{
 const f=fixture(t);
 f.write('docs/current/removed-blank-pages.json',JSON.stringify({pages:[{notion_id:f.manifest.pages[0].notion_id,status:'in_trash',source_body_empty:true}]}));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('known blank source')));
});
test('retired blank links must disappear from current indexes',t=>{
 const f=fixture(t),id=f.manifest.blank_pages[0].notion_id;
 f.write('docs/current/removed-blank-pages.json',JSON.stringify({pages:[{notion_id:id,status:'in_trash',source_body_empty:true}]}));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Retired blank still linked')));
});

function supplementalFixture(f){
 const id='cccccccccccccccccccccccccccccccc',doc='event-log/01-service/legacy-notice.md',url='https://app.notion.com/p/'+id;
 const properties={title:'Legacy notice'},source={id,title:'Legacy notice',service:'주변상점',url,platforms:[],properties,original_body:'레거시 보존 안내'};
 const tick=String.fromCharCode(96),output='# Legacy notice\n\n플랫폼: \n[Notion 기준 명세]('+url+')\n원본 ID: '+tick+id+tick+'\n\n<!-- notion-body:start -->\n레거시 보존 안내\n<!-- notion-body:end -->\n'+tick.repeat(3)+'json\n'+JSON.stringify(properties)+'\n'+tick.repeat(3)+'\n';
 const manifest={notion_id:id,title:source.title,service:source.service,path:doc,notion_url:url,platforms:[],source_body_sha256:sha256(source.original_body),output_sha256:sha256(output),image_ids:[]};
 const item={source,manifest};f.write(doc,output);f.write('docs/current/additional-notion-pages.json',JSON.stringify({pages:[item]}));f.write('event-log/01-service/README.md',f.read('event-log/01-service/README.md')+'[Legacy notice](legacy-notice.md)\n');return {doc,item};
}
test('additional source uses all normal page checks without rewriting the initial snapshot',t=>{
 const f=fixture(t);supplementalFixture(f);const r=verifyCurrent(f.root);assert.deepEqual(r.errors,[]);assert.equal(r.pages,2);assert.equal(r.sourceRows,3);
});

function newServiceFixture(f){
 const extra=supplementalFixture(f),group={service:'동아리',path:'event-log/23-club'};
 const doc=group.path+'/legacy-notice.md';
 extra.item.source.service=group.service;extra.item.manifest.service=group.service;extra.item.manifest.path=doc;
 f.write(doc,f.read(extra.doc));fs.unlinkSync(path.join(f.root,extra.doc));
 f.write(group.path+'/README.md','[Legacy notice](legacy-notice.md)\n');
 f.write('README.md',f.read('README.md').replace('## 레거시 서비스','[동아리]('+group.path+'/README.md)\n## 레거시 서비스'));
 const state={services:[group],pages:[extra.item]};
 f.write('docs/current/additional-notion-pages.json',JSON.stringify(state));return state;
}
test('registered new service is validated without rewriting the archived service snapshot',t=>{
 const f=fixture(t),snapshot=f.read(META+'/summary.json');newServiceFixture(f);
 const result=verifyCurrent(f.root);assert.deepEqual(result.errors,[]);assert.equal(result.services,2);
 assert.equal(f.read(META+'/summary.json'),snapshot);
});
test('unregistered new service is rejected',t=>{
 const f=fixture(t),state=newServiceFixture(f);delete state.services;
 f.write('docs/current/additional-notion-pages.json',JSON.stringify(state));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Additional source service')));
});
test('new service cannot shadow a historical service or use another service directory',t=>{
 const f=fixture(t),state=newServiceFixture(f);state.services[0].service='주변상점';
 f.write('docs/current/additional-notion-pages.json',JSON.stringify(state));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Invalid additional service')));
 state.services[0].service='동아리';state.services[0].path='event-log/another';f.write('event-log/another/README.md','');
 f.write('docs/current/additional-notion-pages.json',JSON.stringify(state));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Additional service page path')));
});
test('additional source text cannot change even after refreshing its output hash',t=>{
 const f=fixture(t),s=supplementalFixture(f),changed=f.read(s.doc).replace('레거시 보존 안내','원문과 다른 내용');
 f.write(s.doc,changed);s.item.manifest.output_sha256=sha256(changed);f.write('docs/current/additional-notion-pages.json',JSON.stringify({pages:[s.item]}));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Source prose')));
});


test('current platform update preserves archived snapshot and validates reader against new source',t=>{
 const f=fixture(t),snapshot=f.read(META+'/source-pages.json.gz');
 const sources=JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(f.root,META+'/source-pages.json.gz'))));
 const old=sources[0],source={...old,platforms:['ANDROID','IOS'],properties:{...old.properties,platform:['ANDROID','IOS']}};
 const body=f.read(f.doc).replace('플랫폼: ANDROID','플랫폼: ANDROID, IOS').replace(JSON.stringify(old.properties),JSON.stringify(source.properties));
 f.write(f.doc,body);
 const manifest={...f.manifest.pages[0],platforms:source.platforms,output_sha256:sha256(body)};
 f.write('docs/current/notion-page-updates.json',JSON.stringify({pages:[{source,manifest}]}));
 assert.deepEqual(verifyCurrent(f.root).errors,[]);
 assert.equal(f.read(META+'/source-pages.json.gz'),snapshot);
 f.write(f.doc,body.replace('새 값','오류 값'));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Output body hash')||e.includes('Source prose')));
});
test('unknown current page update is rejected',t=>{
 const f=fixture(t);f.write('docs/current/notion-page-updates.json',JSON.stringify({pages:[{source:{id:'unknown'},manifest:{notion_id:'unknown',path:f.doc}}]}));
 assert.ok(verifyCurrent(f.root).errors.some(e=>e.includes('Invalid current page update identity')));
});

test('current update may remove a misplaced photo without changing the archived snapshot',t=>{
 const f=fixture(t),snapshot=fs.readFileSync(path.join(f.root,META+'/source-pages.json.gz'));
 const old=JSON.parse(zlib.gunzipSync(snapshot))[0];
 const source={...old,original_body:old.original_body.replace(/<image[^>]*22222222-2222-2222-2222-222222222222[^>]*\/>/,'')};
 const output=f.read(f.doc).replace(f.md(f.b),'');
 f.write(f.doc,output);
 const manifest={...f.manifest.pages[0],image_ids:[f.a],source_body_sha256:sha256(source.original_body),output_sha256:sha256(output)};
 f.write('docs/current/notion-page-updates.json',JSON.stringify({pages:[{source,manifest}]}));
 assert.deepEqual(verifyCurrent(f.root).errors,[]);
 assert.deepEqual(fs.readFileSync(path.join(f.root,META+'/source-pages.json.gz')),snapshot);
});
