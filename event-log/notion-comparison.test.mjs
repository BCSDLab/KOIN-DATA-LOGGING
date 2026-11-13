import test from 'node:test';
import assert from 'node:assert/strict';
import {parseSource,parseReader,compare} from './notion-comparison.mjs';
const a='11111111-1111-1111-1111-111111111111',b='22222222-2222-2222-2222-222222222222';
const image=id=>'<image source="notion-file-block://aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/'+id+'?name=test.png" />';
const md=id=>'![screen](../../assets/'+id+'.png)';
const source='<toggle>\n과거 로깅\n- event_label: old\n'+image(a)+'\n</toggle>\n<toggle>\n새 로깅\n- event_label: current\n'+image(b)+'\n</toggle>';
const past='<!-- logging-section:past:start -->\n## 과거 로깅\n- event_label: old\n'+md(a)+'\n<!-- logging-section:past:end -->';
const current='<!-- logging-section:new:start -->\n## 새 로깅\n- event_label: current\n'+md(b)+'\n<!-- logging-section:new:end -->';
test('Notion past/current definitions and their pictures remain paired',()=>assert.deepEqual(compare(parseSource(source),parseReader(past+'\n'+current)),[]));
test('moving a picture outside its section fails even when page image order is unchanged',()=>{
 const changed=past.replace(md(a),'')+'\n'+md(a)+'\n'+current;
 assert.deepEqual(parseSource(source).images.map(i=>i.fileId),parseReader(changed).images.map(i=>i.fileId));
 assert.ok(compare(parseSource(source),parseReader(changed)).includes('section_images:0:past'));
});
test('missing images and changed event labels are rejected',()=>{
 const issues=compare(parseSource(source),parseReader((past+'\n'+current).replace(md(b),'').replace('event_label: current','event_label: wrong')));
 assert.ok(issues.includes('page_image_sequence'));assert.ok(issues.includes('definition_difference'));
});
