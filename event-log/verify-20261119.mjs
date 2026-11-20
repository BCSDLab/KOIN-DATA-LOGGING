import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p));
const manifest=JSON.parse(read('_archive/updates/2026-11-19/manifest.json'));
const sources=JSON.parse(read('_archive/updates/2026-11-19/source-pages.json'));
const gitsha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const errors=[];let references=0,links=0;
for(const removed of manifest.removedReaderPages||[])if(fs.existsSync(path.join(root,removed)))errors.push('Removed reader still exists: '+removed);
const normalize=s=>s.replace(/<code>(.*?)<\/code>/g,'$1').replace(/<[^>]*>/g,'').replace(/\\([_{}()[\].])/g,'$1').replace(/[*`]/g,'').replace(/\s+/g,' ').trim();
function current(t){const lines=t.split('\n');const start=lines.findIndex(l=>/^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?새\s*로깅(?:\s|$|\()/.test(l));return start<0?'':lines.slice(start).join('\n');}
function fieldLines(t){const result=[];for(const line of t.split('\n')){if(/^\s*(?:[-*]\s*)?(?:설명|screen_view|event_name|event_label|value|event_category)\s*[:：]/.test(line))result.push(normalize(line));}return result;}
for(const p of manifest.pages){const md=read(p.path).toString(),source=sources.find(s=>s.path===p.path);if(!source){errors.push('Missing source: '+p.path);continue;}
 if(gitsha(Buffer.from(source.body))!==p.sourceSha)errors.push('Source snapshot hash: '+p.path);
 // The transfer must preserve every logging field line, including old/new contracts and multiline headers.
 if(JSON.stringify(fieldLines(source.body))!==JSON.stringify(fieldLines(md)))errors.push('Logging field line difference: '+p.path);
 const images=[...md.matchAll(/!\[[^\n]*\]\(([^\n]+)\)/g)].map(m=>path.posix.normalize(path.posix.join(path.posix.dirname(p.path),decodeURIComponent(m[1]))));
 const actual=images.map(i=>{references++;try{return gitsha(read(i));}catch{errors.push('Missing image: '+i);return null;}});
 if(JSON.stringify(actual)!==JSON.stringify(p.images))errors.push('Image bytes/order: '+p.path);
 const platform=md.match(/^platform:\s*(.*)$/m)?.[1]?.split(',').map(s=>s.trim().replace(/WEB\s*\(/g,'WEB(')).sort()||[];
 if(JSON.stringify(platform)!==JSON.stringify(p.platform))errors.push('Platform changed: '+p.path);
 if(/https?:\/\/(?:app\.)?notion\.(?:so|com)/i.test(md))errors.push('External Notion link: '+p.path);
 for(const m of md.matchAll(/(?<!!)\[[^\]]*\]\(([^\s)]+)\)/g)){if(/^[a-z]+:|^#/.test(m[1]))continue;links++;const file=path.resolve(root,path.dirname(p.path),decodeURIComponent(m[1]));if(path.relative(root,file).startsWith('..')||!fs.existsSync(file))errors.push('Broken link: '+p.path+' -> '+m[1]);}
 if(p.legacy&&!md.includes('레거시 참고 명세'))errors.push('Legacy notice missing: '+p.path);
 const index=read(path.posix.dirname(p.path)+'/README.md').toString();const targets=[...index.matchAll(/\]\(([^\s)]+)\)/g)].map(m=>decodeURIComponent(m[1]));if(!targets.includes(path.posix.basename(p.path)))errors.push('Page not in service index: '+p.path);
}
for(const p of manifest.replacedFiles)if(gitsha(read(p.beforePath))!==p.beforeSha)errors.push('Previous GitHub document changed: '+p.path);
for(const image of manifest.images){const b=read(image.path);if(gitsha(b)!==image.sha||b.length!==image.bytes)errors.push('Asset integrity: '+image.path);}
const back=manifest.pages.filter(p=>!p.legacy&&p.fields.event_label.some(l=>l.includes('__navigation__back__')));
const click=back.find(p=>p.fields.event_category.includes('click')),swipe=back.find(p=>p.fields.event_category.includes('swipe'));
if(!click||!swipe)errors.push('Missing separate back click/swipe pages');
else {for(const k of ['screen_view','event_name','value'])if(JSON.stringify(click.fields[k])!==JSON.stringify(swipe.fields[k]))errors.push('Back contract mismatch: '+k);if(click.fields.event_label[0].replace(/__click$/,'__swipe')!==swipe.fields.event_label[0])errors.push('Back label prefix mismatch');if(JSON.stringify(swipe.platform)!==JSON.stringify(['IOS']))errors.push('Unconfirmed swipe platform');}
console.log(JSON.stringify({pages:manifest.pages.length,sourceSnapshots:sources.length,newAssets:manifest.images.length,previousDocumentsPreserved:manifest.replacedFiles.length,imageReferences:references,links,reviewItems:manifest.reviewItems,errors},null,2));
if(errors.length)process.exitCode=1;
