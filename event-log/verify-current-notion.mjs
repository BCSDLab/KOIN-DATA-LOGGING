import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {fileURLToPath} from 'node:url';

export const META='_archive/updates/2026-11-27/notion-sync';
const ACTIVE=['주변상점','복덕방','사장님','식단','버스','게시판','배너','홈화면 리디자인','콜밴팟','학교 부서 정보','팀원 모집','로그인/회원가입/정보수정 V2','시간표','모의수강신청','강제 업데이트','다국어 지원'];
export const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const blobSha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const canonical=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
const same=(a,b)=>canonical(a)===canonical(b);
const decode=s=>s.replace(/&#(?:x([0-9a-f]+)|(\d+));/gi,(_,h,d)=>String.fromCodePoint(parseInt(h||d,h?16:10))).replace(/&(lt|gt|amp|quot|apos|nbsp);/g,(_,n)=>({lt:'<',gt:'>',amp:'&',quot:'"',apos:"'",nbsp:' '}[n]));

export function prose(text,{source,images,docPath}){
 text=text.replaceAll('\\<','&lt;').replaceAll('\\>','&gt;');
 if(source){
  text=text.replace(/<image\b([^>]*?)(?:\/\s*>|>([\s\S]*?)<\/image>)/g,(_,attrs,caption)=>{
   const ref=attrs.match(/source="([^"]+)"/)?.[1],id=ref?.match(/notion-file-block:\/\/[^/]+\/([a-f0-9-]{36})/i)?.[1];
   if(!images.has(id))throw new Error('Unresolved source image '+id);
   return ' IMAGE'+images.get(id).git_blob_sha+' '+(caption||'')+' ';
  });
  text=text.replace(/<date\b[^>]*start="([^"]+)"[^>]*\/>/g,'$1');
 }else{
  const byAsset=new Map([...images.values()].map(i=>[i.asset,i]));
  text=text.replace(/!\[[^\n]*?\]\(([^\n]+)\)/g,(_,link)=>{
   const asset=path.posix.normalize(path.posix.join(path.posix.dirname(docPath),decodeURIComponent(link)));
   if(!byAsset.has(asset))throw new Error('Unregistered image asset '+asset);
   return ' IMAGE'+byAsset.get(asset).git_blob_sha+' ';
  });
 }
 text=text.replace(/\[([^\n]*?)\]\([^\n]+?\)/g,(_,label)=>label==='Notion 원문'?'':label);
 return decode(text.replace(/<[^>]*>/g,'')).replace(/[^A-Za-z0-9가-힣]/g,'');
}
function referenceLinks(text){
 return [...text.matchAll(/<(?:page|mention)\b[^>]*url="([^"]+)"|(?<!!)\[[^\n]*?\]\(([^)\n]+)\)/g)].map(m=>decode(m[1]||m[2]));
}

export function verifyCurrent(root,{imageCache}={}){
 root=path.resolve(root);
 const errors=[];
 const check=(ok,msg)=>{if(!ok)errors.push(msg);};
 const safe=rel=>{const full=path.resolve(root,rel);if(path.relative(root,full).startsWith('..')||path.isAbsolute(path.relative(root,full)))throw new Error('Path escapes repository: '+rel);return full;};
 const read=rel=>fs.readFileSync(safe(rel));
 const json=rel=>JSON.parse(read(rel));
 const summary=json(META+'/summary.json');
 const compressed=read(summary.source_snapshot.path);
 check(sha256(compressed)===summary.source_snapshot.sha256,'Source snapshot file hash');
 const sources=JSON.parse(zlib.gunzipSync(compressed));
 const sourceMap=new Map(sources.map(s=>[s.id,s]));
 check(sourceMap.size===sources.length,'Duplicate source IDs');
 check(sources.length===summary.notion_rows&&sources.length===summary.source_snapshot.records,'Source row count');
 const manifests=summary.services.map(s=>json(META+'/'+s.path));
 const pages=manifests.flatMap(s=>s.pages),blankPages=manifests.flatMap(s=>s.blank_pages);
 check(pages.length===summary.nonblank_pages,'Page count');
 check(blankPages.length===summary.blank_pages,'Blank page count');
 const additionalPath='docs/current/additional-notion-pages.json';
 const additionalState=fs.existsSync(safe(additionalPath))?json(additionalPath):{pages:[]};
 const additional=additionalState.pages;
 const extraServices=new Map(),servicePaths=new Set();
 for(const group of additionalState.services||[]){
  const valid=typeof group.service==='string'&&group.service.length>0&&
   !manifests.some(s=>s.service===group.service)&&!extraServices.has(group.service)&&
   typeof group.path==='string'&&/^event-log\/[^/]+$/.test(group.path)&&
   group.path!=='event-log/..'&&!servicePaths.has(group.path)&&
   !pages.some(p=>path.posix.dirname(p.path)===group.path);
  check(valid,'Invalid additional service registration '+group.service);
  if(!valid)continue;
  safe(group.path);extraServices.set(group.service,group);servicePaths.add(group.path);
  check(fs.existsSync(safe(group.path+'/README.md')),'Additional service index '+group.service);
 }
 for(const item of additional){
  const s=item.source,m=item.manifest;
  check(!sourceMap.has(s.id),'Duplicate additional source ID '+s.id);
  check(s.id===m.notion_id&&Boolean(s.original_body),'Additional source must be a nonblank page '+s.id);
  const extraService=extraServices.get(s.service);
  check(manifests.some(group=>group.service===s.service)||Boolean(extraService),'Additional source service '+s.id);
  if(extraService)check(path.posix.dirname(m.path)===extraService.path,'Additional service page path '+s.id);
  sources.push(s);sourceMap.set(s.id,s);pages.push(m);
 }

 const updatesPath='docs/current/notion-page-updates.json';
 const updatedIds=new Set();
 let updatedImageReferences=0;
 if(fs.existsSync(safe(updatesPath))){
  for(const item of json(updatesPath).pages){
   const s=item.source,m=item.manifest,previous=sourceMap.get(s.id);
   const at=pages.findIndex(p=>p.notion_id===s.id);
   const valid=Boolean(previous&&at>=0&&m.notion_id===s.id&&m.path===pages[at].path&&
    s.title===previous.title&&s.service===previous.service&&s.url===previous.url&&
    s.original_body&&!updatedIds.has(s.id));
   check(valid,'Invalid current page update identity '+s.id);
   if(!valid)continue;
   updatedImageReferences+=m.image_ids.length-pages[at].image_ids.length;
   updatedIds.add(s.id);sourceMap.set(s.id,s);
   sources[sources.findIndex(p=>p.id===s.id)]=s;pages[at]=m;
  }
 }

 check(new Set(manifests.map(s=>s.service)).size===summary.services.length,'Service uniqueness');
 const ids=new Set(),files=new Set(),images=new Map();
 for(const name of fs.readdirSync(safe(META+'/images')).filter(n=>n.endsWith('.json'))){
  for(const image of json(META+'/images/'+name)){
   check(!images.has(image.id),'Duplicate image ID '+image.id);images.set(image.id,image);
  }
 }
 check(images.size===summary.images.unique_files,'Unique image count');
 for(const image of additionalState.images||[]){
  const previous=images.get(image.id);
  check(!previous||(previous.git_blob_sha===image.git_blob_sha&&previous.sha256===image.sha256),'Additional image identity '+image.id);
  if(!previous)images.set(image.id,image);
 }

 let references=0,notionLinks=0;
 for(const m of pages){
  check(!ids.has(m.notion_id),'Duplicate page ID '+m.notion_id);ids.add(m.notion_id);
  check(!files.has(m.path),'Duplicate page path '+m.path);files.add(m.path);
  const s=sourceMap.get(m.notion_id);if(!s){errors.push('Missing source '+m.notion_id);continue;}
  check(Boolean(s.original_body),'Nonblank source required '+m.path);
  check(s.title===m.title&&s.service===m.service&&s.url===m.notion_url,'Source identity '+m.path);
  check(sha256(s.original_body)===m.source_body_sha256,'Source body hash '+m.path);
  const bytes=read(m.path),text=bytes.toString('utf8');
  check(sha256(bytes)===m.output_sha256,'Output body hash '+m.path);
  const sourceBody=text.match(/<!-- notion-body:start -->\n([\s\S]*?)\n<!-- notion-body:end -->/);
  if(!sourceBody){errors.push('Missing body markers '+m.path);continue;}
  check((text.match(/<!-- notion-body:start -->/g)||[]).length===1&&(text.match(/<!-- notion-body:end -->/g)||[]).length===1,'Body marker uniqueness '+m.path);
  const outside=text.slice(0,sourceBody.index)+text.slice(sourceBody.index+sourceBody[0].length);
  check(!/^(?:#{1,6}\s*(?:새|과거|이전)\s*로깅|\s*[-*]?\s*(?:event_label|event_name|event_category|screen_view|value|설명)\s*:)/m.test(outside),'Logging fields outside source body '+m.path);
  const body=sourceBody[1];
  check(text.startsWith('# '+m.title+'\n'),'Title '+m.path);
  check(text.includes('[Notion 기준 명세]('+m.notion_url+')'),'Canonical source link '+m.path);
  check(text.includes('원본 ID: '+String.fromCharCode(96)+m.notion_id+String.fromCharCode(96)),'Canonical source ID '+m.path);
  check(/^https:\/\/app\.notion\.com\/p\/[a-f0-9]{32}$/.test(m.notion_url),'Invalid Notion URL '+m.path);
  const fence=String.fromCharCode(96).repeat(3),at=text.indexOf(fence+'json\n');
  const end=at<0?-1:text.indexOf('\n'+fence,at+fence.length+5);
  try{
   const properties=at<0||end<0?null:JSON.parse(text.slice(at+fence.length+5,end));
   check(same(properties,s.properties),'Properties '+m.path);
  }catch{errors.push('Properties JSON '+m.path);}
  check(same(m.platforms,s.platforms),'Platform metadata '+m.path);
  check(text.includes('플랫폼: '+s.platforms.join(', ')),'Platform header '+m.path);
  try{check(prose(s.original_body,{source:true,images,docPath:m.path})===prose(body,{source:false,images,docPath:m.path}),'Source prose/section/image placement '+m.path);}catch(e){errors.push(m.path+': '+e.message);}
  check(same(referenceLinks(s.original_body),referenceLinks(body)),'Reference link sequence '+m.path);
  const sourceIds=[...s.original_body.matchAll(/<image[^>]+source="notion-file-block:\/\/[^/]+\/([a-f0-9-]{36})/gi)].map(x=>x[1]);
  check(same(sourceIds,m.image_ids),'Source image sequence '+m.path);
  const actualImages=[...body.matchAll(/!\[[^\n]*?\]\(([^\n]+)\)/g)].map(x=>path.posix.normalize(path.posix.join(path.posix.dirname(m.path),decodeURIComponent(x[1]))));
  const hashes=actualImages.map(asset=>{const i=[...images.values()].find(i=>i.asset===asset);return i?.git_blob_sha;});
  check(same(hashes,sourceIds.map(id=>images.get(id)?.git_blob_sha)),'Image hash sequence '+m.path);
  references+=sourceIds.length;
  const index=read(path.posix.dirname(m.path)+'/README.md').toString();
  const indexTargets=[...index.matchAll(/\]\(([^)\s]+)\)/g)].map(link=>decodeURIComponent(link[1]));
  check(indexTargets.includes(path.posix.basename(m.path)),'Service index entry '+m.path);
  for(const link of text.matchAll(/(!?)\[[^\n]*?\]\(([^\n]+)\)/g)){
   const target=link[2];
   if(/^[a-z]+:|^#/i.test(target)){if(target.startsWith('https://app.notion.com/p/'))notionLinks++;continue;}
   try{
    const rel=path.posix.normalize(path.posix.join(path.posix.dirname(m.path),decodeURIComponent(target.split('#')[0])));
    let exists=fs.existsSync(safe(rel));
    if(!exists&&imageCache&&link[1]){const image=[...images.values()].find(i=>i.asset===rel);exists=Boolean(image&&fs.existsSync(path.join(imageCache,image.id+'.bin')));}
    check(exists,'Broken relative link '+m.path+' -> '+target);
   }catch(e){errors.push(e.message);}
  }
  check(!/X-Amz-(?:Signature|Credential)=|[?&]sig=/i.test(text),'Signed URL '+m.path);
 }
 const retirementPath='docs/current/removed-blank-pages.json';
 const retirements=fs.existsSync(safe(retirementPath))?json(retirementPath).pages:[];
 const retired=new Set();
 for(const item of retirements){
  const known=blankPages.find(b=>b.notion_id===item.notion_id);
  check(!retired.has(item.notion_id),'Duplicate retired blank source '+item.notion_id);
  check(Boolean(known)&&sourceMap.get(item.notion_id)?.original_body==='','Retirement must reference a known blank source '+item.notion_id);
  check(item.status==='in_trash'&&item.source_body_empty===true,'Retirement confirmation '+item.notion_id);
  retired.add(item.notion_id);
 }
 for(const b of blankPages){
  check(!ids.has(b.notion_id),'Duplicate blank source ID '+b.notion_id);ids.add(b.notion_id);
  const s=sourceMap.get(b.notion_id);check(s?.original_body==='','Blank source '+b.notion_id);
  const m=pages.find(m=>m.service===b.service);
  check(Boolean(m),'Blank source service '+b.notion_id);
  if(m){
   const listed=read(path.posix.dirname(m.path)+'/README.md').toString().includes(b.url);
   check(retired.has(b.notion_id)?!listed:listed,(retired.has(b.notion_id)?'Retired blank still linked ':'Blank page link ')+b.notion_id);
  }
 }
 check(ids.size===sources.length,'All source pages accounted for');
 check(references===summary.images.occurrences+additional.reduce((n,x)=>n+x.manifest.image_ids.length,0)+updatedImageReferences,'Image reference count');
 let imagesChecked=0;
 for(const image of images.values()){
  try{
   let full=safe(image.asset);
   if(!fs.existsSync(full)&&imageCache)full=path.join(imageCache,image.id+'.bin');
   const b=fs.readFileSync(full);
   check(b.length===image.bytes&&sha256(b)===image.sha256&&blobSha(b)===image.git_blob_sha,'Image bytes '+image.asset);
   imagesChecked++;
  }catch(e){errors.push('Missing image '+image.asset+': '+e.message);}
 }
 const readme=read('README.md').toString();let last=-1;
 for(const service of ACTIVE){const at=readme.indexOf('['+service+']');check(at>last,'Active service order '+service);last=at;}
 check(readme.indexOf('## 레거시 서비스')>last,'Legacy section placement');
 for(const group of extraServices.values()){
  const beforeLegacy=readme.slice(0,readme.indexOf('## 레거시 서비스'));
  const targets=[...beforeLegacy.matchAll(/\]\(([^)]+)\)/g)].map(m=>decodeURIComponent(m[1]));
  check(targets.includes(group.path+'/README.md'),'Additional active service link '+group.service);
  check(additional.some(p=>p.source.service===group.service),'Empty additional service '+group.service);
 }
 for(const old of summary.previous_exports){
  const stub=read(old.previous_path).toString();
  check(!/새\s*로깅|event[_\\]*label\s*:/.test(stub),'Prior export is still active '+old.previous_path);
  const rel=path.posix.relative(path.posix.dirname(old.previous_path),old.archive_path);
  check(stub.includes(']('+encodeURI(rel).replaceAll('(', '%28').replaceAll(')', '%29')+')')||stub.includes(']('+rel.split('/').map(encodeURIComponent).join('/')+')'),'Previous export archive link '+old.previous_path);
  check(fs.existsSync(safe(old.archive_path)),'Missing previous export archive '+old.archive_path);
 }
 const known=new Set([...files,...summary.previous_exports.map(p=>p.previous_path)]);
 function walk(dir){for(const name of fs.readdirSync(safe(dir))){const rel=path.posix.join(dir,name);if(fs.statSync(safe(rel)).isDirectory())walk(rel);else if(rel.endsWith('.md')&&name!=='README.md')check(known.has(rel),'Unmapped reader document '+rel);}}
 walk('event-log');
 return {pages:pages.length,blankPages:blankPages.length,activeBlankPages:blankPages.length-retired.size,retiredBlankPages:retired.size,sourceRows:sources.length,services:manifests.length+extraServices.size,imageReferences:references,imagesChecked,notionLinks,errors};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const root=process.argv[2]||path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
 const index=process.argv.indexOf('--image-cache'),imageCache=index<0?undefined:process.argv[index+1];
 try{const result=verifyCurrent(root,{imageCache});console.log(JSON.stringify(result,null,2));if(result.errors.length)process.exitCode=1;}catch(error){console.error(error);process.exitCode=1;}
}


