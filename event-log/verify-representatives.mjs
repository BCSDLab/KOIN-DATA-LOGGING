import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>JSON.parse(read(p));
const nav=json('_archive/navigation-map.json'),registry=json('_archive/representatives.json');
const presentation=json('_archive/presentation-cleanup.json').changes;
const pages=new Map(nav.pages.map(p=>[p.id,p])),errors=[];
const listed=[];
for(const service of nav.services){
 const file=service.folder+'/README.md';
 for(const m of read(file).matchAll(/\[[^\]]+\]\(([^)]+)\)/g))listed.push(path.posix.normalize(path.posix.join(service.folder,decodeURIComponent(m[1]))));
}
for(const p of nav.pages){
 const canonical=pages.get(p.representativeId);
 if(!canonical||canonical.service!==p.service||canonical.representativeId!==canonical.id)errors.push('Invalid representative: '+p.id);
 const count=listed.filter(f=>f===p.file).length;
 if(p.readerRole==='preserved_alias'&&count)errors.push('Alias exposed in service list: '+p.file);
 if(p.readerRole==='representative'&&count!==1)errors.push('Representative listed count '+count+': '+p.file);
}
const fingerprint=p=>JSON.stringify(p.sections.filter(s=>s.kind==='new').flatMap(s=>s.fields));
for(const group of registry.groups){
 const canonical=pages.get(group.representativeId);
 const text=read(canonical.file);
 if(!text.includes('<!-- representative-related:start -->'))errors.push('Missing source links: '+canonical.id);
 for(const id of group.aliasIds){
  const alias=pages.get(id);if(alias?.representativeId!==canonical.id)errors.push('Lost alias: '+id);
  const aliasRelative=path.posix.relative(path.posix.dirname(canonical.file),alias.file);
  const links=[...text.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)].map(m=>decodeURIComponent(m[1]));
  if(!links.includes(aliasRelative))errors.push('Alias not reachable: '+id);
  if(group.definitionState==='same_current_definition'&&fingerprint(canonical)!==fingerprint(alias))errors.push('Definitions were not identical: '+id);
 }
 if(group.definitionState==='conflicting_originals_transition_draft'&&(!text.includes('원문 충돌')||!text.includes('전환 초안')))errors.push('Conflict not disclosed: '+canonical.id);
}
for(const p of registry.originalReaders){
 const current=read(p.file).replace(/<!-- representative-note:start -->[\s\S]*?<!-- representative-note:end -->\n?/g,'').replace(/<!-- representative-related:start -->[\s\S]*?<!-- representative-related:end -->\n?/g,'');
 const bytes=Buffer.from(current),hash=crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
 const adjusted=presentation.find(c=>c.file===p.file);
 if(adjusted?.representativeBodyAfterSha){if(adjusted.representativeBodyBeforeSha!==p.sha||hash!==adjusted.representativeBodyAfterSha)errors.push('Presentation provenance mismatch: '+p.file);}else if(hash!==p.sha)errors.push('Original reader content changed: '+p.file);
}
const allFiles=['README.md','_archive/README.md',...registry.originalReaders.map(p=>p.file)];
for(const p of allFiles){for(const m of read(p).matchAll(/\[[^\]]+\]\(([^)\s]+)\)/g)){
 if(/^[a-z]+:|^#/i.test(m[1]))continue;
 const f=path.resolve(root,path.dirname(p),decodeURIComponent(m[1].split('#')[0]));
 if(path.relative(root,f).startsWith('..')||!fs.existsSync(f))errors.push('Broken source link: '+p+' -> '+m[1]);
}}
const result={groups:registry.groups.length,listedDocuments:nav.pages.filter(p=>p.readerRole==='representative').length,preservedAliasDocuments:nav.pages.filter(p=>p.readerRole==='preserved_alias').length,readerBodiesValidated:registry.originalReaders.length,presentationAdjustedBodies:presentation.filter(c=>c.representativeBodyAfterSha).length,conflictingGroups:registry.groups.filter(g=>g.definitionState==='conflicting_originals_transition_draft').length,errors};
console.log(JSON.stringify(result,null,2));
if(process.argv.includes('--report'))fs.writeFileSync(path.join(root,'_archive/representative-validation.json'),JSON.stringify(result,null,2)+'\n');
if(errors.length)process.exitCode=1;
