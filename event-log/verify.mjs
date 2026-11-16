import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>JSON.parse(read(p));
const manifest=json('_archive/navigation-map.json'),preservation=json('_archive/preservation-manifest.json');
const corrections=json('_archive/live-notion-corrections.json').pages;
manifest.pages=manifest.pages.map(p=>{const correction=corrections.find(c=>c.id===p.id);return correction?{...p,fields:correction.fields,sections:correction.sections}:p;});
const names=['주변상점','복덕방','사장님','새 주변상점 - 레거시','미래의 주변상점 - 레거시','식단','버스','게시판','배너','홈화면 리디자인','콜밴팟','학교 부서 정보','팀원 모집','로그인/회원가입/정보수정 - 레거시','로그인/회원가입/정보수정 V2','시간표','모의수강신청','강제 업데이트','졸업학점 계산기 - 레거시','동아리 - 레거시'];
const errors=[];
const normalize=s=>String(s||'').replace(/<[^>]*>/g,'').replace(/\\([_.*~{}<>\[\]])/g,'$1').replaceAll('&amp;','&').replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[`*]/g,'').replace(/\s+/g,' ').trim();
function extract(s){const fields=[];for(const line of s.split('\n')){const m=normalize(line).match(/^[-•]?\s*(설명|screen_view|event_name|event_label|value|event_category)\s*[:：]\s*(.*)$/i);if(m&&m[2])fields.push({key:m[1].toLowerCase(),value:m[2]});}return{fields,images:[...s.matchAll(/!\[[^\]]*\]\([^)]*?assets\/(?:multilingual\/)?([a-f0-9-]+)\.(?:png|jpe?g)\)/gi)].map(m=>m[1])};}
const main=read('README.md');let last=-1;
// The archived import keeps its historical order; the reader README groups legacy services below current services.
for(let i=0;i<names.length;i++){const s=manifest.services[i];if(s?.name!==names[i]||s?.number!==i+1)errors.push('Archived service identity: '+names[i]);}
const additions=json('event-log/21-다국어-지원/manifest.json');
const readerNames=[...names.filter(n=>!n.includes('레거시')),'다국어 지원',...names.filter(n=>n.includes('레거시'))];
for(const name of readerNames){const pos=main.indexOf('['+name+']');if(pos<=last)errors.push('Service name/order: '+name);last=pos;}
if(main.indexOf('## 레거시 서비스')<main.indexOf('[다국어 지원]'))errors.push('Legacy section must follow current services');
let links=0,images=0,sections=0;
const documents=['README.md','_archive/README.md',...manifest.services.map(s=>s.folder+'/README.md'),...manifest.pages.map(p=>p.file),additions.folder+'/README.md',...additions.pages.map(p=>p.path)];
for(const file of documents){const md=read(file);if(/https?:\/\/(?:app\.)?notion\.(?:com|so)/i.test(md))errors.push('External Notion link: '+file);if(/<image\b/i.test(md))errors.push('Unsupported image: '+file);
 for(const m of md.matchAll(/(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)){const target=m[2];if(/^[a-z]+:/i.test(target)||target.startsWith('#'))continue;const resolved=path.resolve(root,path.dirname(file),decodeURIComponent(target.split('#')[0]));if(path.relative(root,resolved).startsWith('..')||!fs.existsSync(resolved))errors.push('Broken link: '+file+' -> '+target);links++;if(m[1])images++;}
}
for(const page of manifest.pages){const md=read(page.file),parsed=extract(md),available=new Set(parsed.fields.map(f=>f.key+'\0'+normalize(f.value)));for(const f of page.fields)if(!available.has(f.key+'\0'+normalize(f.value)))errors.push('Field loss: '+page.id+' '+f.key+'='+f.value);
 if(JSON.stringify(parsed.images)!==JSON.stringify(page.images))errors.push('Image order/association: '+page.id);
 const found=[...md.matchAll(/<!-- logging-section:(past|new):start -->([\s\S]*?)<!-- logging-section:\1:end -->/g)];
 if(found.length!==page.sections.length)errors.push('Section count: '+page.id);
 for(let i=0;i<page.sections.length;i++){sections++;const expected=page.sections[i],actual=found[i];if(!actual||actual[1]!==expected.kind){errors.push('Section kind: '+page.id);continue;}const data=extract(actual[2]),set=new Set(data.fields.map(f=>f.key+'\0'+normalize(f.value)));if(expected.fields.some(f=>!set.has(f.key+'\0'+normalize(f.value)))||JSON.stringify(expected.images)!==JSON.stringify(data.images))errors.push('Past/new definition or photo association: '+page.id+' '+expected.title);}
}
for(const file of preservation.files){const b=fs.readFileSync(path.join(root,'_archive/original',file.path));const sha=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');if(sha!==file.sha)errors.push('Original changed: '+file.path);}
const assetManifest=json('_archive/original/notion/assets-manifest.json'),imageMap=json('_archive/original/notion/zip-image-map.json');let checkedImages=0;
for(const asset of assetManifest){const b=fs.readFileSync(path.join(root,asset.file));if(b.length!==asset.bytes||crypto.createHash('sha256').update(b).digest('hex')!==asset.sha256)errors.push('Image integrity: '+asset.file);checkedImages++;}
for(const image of imageMap){const a=assetManifest.find(a=>a.file===image.archiveFile);if(!a||a.sha256!==image.sha256||a.bytes!==image.bytes)errors.push('Notion ZIP image mismatch: '+image.exportFile);}

for(const page of additions.pages){const md=read(page.path),parsed=extract(md);const expected=page.fields.map(f=>({key:f.key,value:normalize(f.value)}));if(JSON.stringify(parsed.fields)!==JSON.stringify(expected))errors.push('Additional field mismatch: '+page.title);if(JSON.stringify(parsed.images)!==JSON.stringify(page.images))errors.push('Additional image association: '+page.title);if(!page.fields.some(f=>f.key==='event_name'&&f.value==='DA1'))errors.push('Additional event_name: '+page.title);}
for(const image of additions.images){const b=fs.readFileSync(path.join(root,image.path));if(b.length!==image.bytes||crypto.createHash('sha256').update(b).digest('hex')!==image.sha256)errors.push('Additional image integrity: '+image.path);}
const result={additionalServices:1,additionalReaderPages:additions.pages.length,additionalImages:additions.images.length,services:manifest.services.length,readerPages:manifest.pages.length,pastAndNewSections:sections,links,imageReferences:images,originalFilesPreserved:preservation.files.length,imagesChecked:checkedImages,notionZipImagesMapped:imageMap.length,errors};
console.log(JSON.stringify(result,null,2));
if(process.argv.includes('--report'))fs.writeFileSync(path.join(root,'_archive/reader-validation.json'),JSON.stringify({...result,scope:'제공된 Notion ZIP·보존 원문 기준의 파일, 정의, 페이지별 이미지 순서, 과거/새 구간 대응 검사. 모든 현재 Notion 페이지의 실시간·육안 전수 검수는 별도.'},null,2)+'\n');
if(errors.length)process.exitCode=1;
