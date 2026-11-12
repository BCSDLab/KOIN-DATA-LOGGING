import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import ts from 'typescript';
import { load, validate, generate, read } from '../cli/core.mjs';

const root = path.resolve(import.meta.dirname,'..');
const model = load(root);
const copy = () => structuredClone(model);
const first = m => m.specs[0].data.events[0];
test('source contracts follow confirmed naming and DA1 forced-update override',()=>{
  assert.deepEqual(validate(model),[]);
  const forced = model.specs.find(s=>s.data.screen_view==='forced_update');
  assert.equal(forced.data.events.length,5);
  assert.ok(forced.data.events.every(e=>e.event_name==='DA1'));
  assert.equal(model.vocabulary.services.main,'DA2');
});
for (const [name, mutate, message] of [
  ['duplicate label',m=>m.specs[0].data.events.push(structuredClone(first(m))),'중복'],
  ['screen mismatch',m=>m.specs[0].data.screen_view='wrong','불일치'],
  ['wrong DA',m=>{first(m).event_name='DA2';},'DA 배정'],
  ['unknown platform',m=>{first(m).platforms=['mobile'];},'platforms'],
  ['category mismatch',m=>{first(m).event_category='submit';},'접미'],
  ['reserved params',m=>{first(m).params.event_label={type:'string',required:true,description:'bad'};},'예약'],
  ['typo field',m=>{first(m).platfroms=['WEB'];},'알 수 없는'],
  ['value type',m=>{first(m).value.const=123;},'타입 불일치'],
]) test(`reject ${name}`,()=>{const m=copy();mutate(m);assert.match(validate(m).join('\n'),new RegExp(message));});
test('draft, legacy and frozen contracts cannot enter production generation',()=>{
  for(const status of ['draft','legacy','frozen']) {
    const m=copy();first(m).status=status;
    assert.ok(!generate(m)['logging.ts'].includes(JSON.stringify(first(m).event_label)+':'));
  }
  const m=copy();first(m).status='draft';
  assert.ok(generate(m,{preview:true})['logging.ts'].includes('PREVIEW'));
});
test('YAML duplicate keys fail instead of silently overwriting',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'koin-yaml-'));
  try { const f=path.join(dir,'bad.yaml');fs.writeFileSync(f,'value: 1\nvalue: 2\n');assert.throws(()=>read(f)); }
  finally {fs.rmSync(dir,{recursive:true,force:true});}
});
test('generation is deterministic and platform-specific',()=>{
  const a=generate(model);assert.deepEqual(a,generate(model));
  assert.equal(JSON.parse(a['manifest.json']).event_count,9);
  assert.equal(JSON.parse(a['manifest.json']).web_count,4);
  assert.equal(JSON.parse(a['manifest.json']).android_count,5);
  assert.ok(!a['logging.ts'].includes('main__forced_update'));
  assert.ok(!a['KoinEvents.kt'].includes('cafeteria__main_category'));
});
test('generated TypeScript compiles, rejects bad calls and validates runtime payloads',async()=>{
  const m=copy(), e=first(m);
  e.value={type:'string',required:true,description:'test dynamic value'};
  e.params={count:{type:'number',required:true,description:'count'},direction:{type:'string',required:false,enum:['up','down'],description:'direction'}};
  const source=generate(m)['logging.ts'];
  const label=JSON.stringify(e.event_label);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'koin-ts-'));
  try {
    fs.writeFileSync(path.join(dir,'logging.ts'),source);
    fs.writeFileSync(path.join(dir,'calls.ts'),`import {createEvent} from './logging';\ncreateEvent(${label},{value:'v1',count:1});\n// @ts-expect-error unknown label\ncreateEvent('missing',{});\n// @ts-expect-error missing count\ncreateEvent(${label},{value:'v1'});\n// @ts-expect-error wrong value type\ncreateEvent(${label},{value:1,count:1});\n// @ts-expect-error invalid enum\ncreateEvent(${label},{value:'v1',count:1,direction:'left'});\n`);
    fs.appendFileSync(path.join(dir,'calls.ts'),"// @ts-expect-error fixed value cannot be overwritten\ncreateEvent('cafeteria__main_category__category_navigation__cafeteria_entry__click',{value:'override'});\n");
    const result=spawnSync(process.execPath,[path.join(root,'node_modules/typescript/bin/tsc'),'--strict','--noEmit','--target','ES2022','--moduleResolution','node',path.join(dir,'calls.ts')],{encoding:'utf8'});
    assert.equal(result.status,0,result.stdout+result.stderr);
    const js=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ES2022}}).outputText;
    const {createEvent}=await import('data:text/javascript;base64,'+Buffer.from(js).toString('base64'));
    const payload=createEvent(e.event_label,{value:'v1',count:2});
    assert.equal(payload.event_name,'DA1');assert.equal(payload.params.value,'v1');assert.equal(payload.params.count,2);
    assert.ok(!Object.hasOwn(payload.params,'direction'));
    assert.throws(()=>createEvent(e.event_label,{value:'v1',count:NaN}));
    assert.throws(()=>createEvent(e.event_label,{value:'v1',count:2,event_label:'override'}));
    assert.throws(()=>createEvent(e.event_label,{value:'v1',count:2,toString:1}));
    assert.throws(()=>createEvent('missing',{}));
  } finally {fs.rmSync(dir,{recursive:true,force:true});}
});
test('fixed wire values are supplied by generated code',async()=>{
  const source=generate(model)['logging.ts'];
  const js=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ES2022}}).outputText;
  const {createEvent}=await import('data:text/javascript;base64,'+Buffer.from(js).toString('base64'));
  const label='cafeteria__main_category__category_navigation__cafeteria_entry__click';
  assert.equal(createEvent(label,{}).params.value,'식단');
  assert.throws(()=>createEvent(label,{value:'overwritten'}));
});

for(const state of ['unknown','unsupported']) test('block platform '+state,()=>{const m=copy();const e=m.specs.find(s=>s.data.screen_view==='forced_update').data.events[0];e.platform_support.ANDROID.state=state;assert.match(validate(m).join('\n'),/생성 플랫폼의 지원 확인 필요/);assert.ok(!generate(m)['KoinEvents.kt'].includes('class Event_'+e.event_label+'('));});
