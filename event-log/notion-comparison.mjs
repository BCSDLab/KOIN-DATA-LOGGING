export function normalize(s){return String(s||'').replace(/<[^>]*>/g,'').replace(/\\([_.*~{}<>\[\]])/g,'$1').replaceAll('&amp;','&').replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[`*]/g,'').replace(/\s+/g,' ').trim();}
export function fields(s){const out=[];for(const line of s.split('\n')){const m=normalize(line).match(/^[-•]?\s*(설명|screen_view|event_name|event_label|value|event_category)\s*[:：]\s*(.*)$/i);if(m&&m[2])out.push({key:m[1].toLowerCase(),value:m[2]});}return out;}
const kind=s=>/^(과거|이전)\s*로깅/.test(normalize(s))?'past':/^(새|신규|현재)\s*로깅/.test(normalize(s))?'new':null;
export function parseSource(s){
 const images=[];for(const m of s.matchAll(/<image\b[^>]*\bsource="([^"]+)"[^>]*>/gi))images.push({index:m.index,reference:m[1].replaceAll('&amp;','&')});
 for(const m of s.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g))images.push({index:m.index,reference:m[1]});images.sort((a,b)=>a.index-b.index);
 for(const i of images){i.fileId=i.reference.match(/notion-file-block:\/\/[a-f0-9-]+\/([a-f0-9-]+)/i)?.[1]??null;}
 const parts=[],stack=[];for(const m of s.matchAll(/<toggle>|<\/toggle>/g)){if(m[0]==='<toggle>'){const title=s.slice(m.index+8).match(/^\s*([^\n]+)/)?.[1]||'';stack.push({start:m.index,end:0,contentStart:m.index+8,title:normalize(title),kind:kind(title)});}else{const p=stack.pop();if(p?.kind){p.end=m.index;parts.push(p);}}}
 for(const m of s.matchAll(/^(#{1,6})\s+([^\n]+)$/gm)){if(!kind(m[2])||parts.some(p=>m.index>=p.start&&m.index<p.end))continue;const next=[...s.slice(m.index+m[0].length).matchAll(/^(#{1,6})\s+[^\n]+$/gm)].find(n=>n[1].length<=m[1].length);parts.push({start:m.index,contentStart:m.index+m[0].length,end:next?m.index+m[0].length+next.index:s.length,title:normalize(m[2]),kind:kind(m[2])});}
 parts.sort((a,b)=>a.start-b.start);return {images,fields:fields(s),sections:parts.map(p=>({...p,fields:fields(s.slice(p.contentStart,p.end)),images:images.filter(i=>i.index>=p.start&&i.index<p.end)})),unassignedImages:images.filter(i=>!parts.some(p=>i.index>=p.start&&i.index<p.end))};
}
export function parseReader(s){const images=[...s.matchAll(/!\[[^\]]*\]\([^)]*?assets\/([a-f0-9-]+)\.(?:png|jpe?g)\)/gi)].map(m=>({index:m.index,fileId:m[1]})),parts=[];
 for(const m of s.matchAll(/<!-- logging-section:(past|new):start -->([\s\S]*?)<!-- logging-section:\1:end -->/g))parts.push({start:m.index,end:m.index+m[0].length,kind:m[1],content:m[2],title:m[2].match(/^## ([^\n]+)/m)?.[1]||m[1]});
 for(const m of s.matchAll(/^(#{1,6})\s+([^\n]+)$/gm)){if(!kind(m[2])||parts.some(p=>m.index>=p.start&&m.index<p.end))continue;const next=[...s.slice(m.index+m[0].length).matchAll(/^(#{1,6})\s+[^\n]+$/gm)].find(n=>n[1].length<=m[1].length);const end=next?m.index+m[0].length+next.index:s.length;parts.push({start:m.index,end,kind:kind(m[2]),title:normalize(m[2]),content:s.slice(m.index,end)});}
 parts.sort((a,b)=>a.start-b.start);return {images,fields:fields(s),sections:parts.map(p=>({...p,fields:fields(p.content),images:images.filter(i=>i.index>=p.start&&i.index<p.end)})),unassignedImages:images.filter(i=>!parts.some(p=>i.index>=p.start&&i.index<p.end))};
}

export function compare(source, reader, canonicalId=id=>id) {
  const issues=[];
  const ids=a=>a.map(x=>canonicalId(x.fileId));
  if(JSON.stringify(ids(source.images))!==JSON.stringify(reader.images.map(x=>x.fileId)))issues.push('page_image_sequence');
  if(source.sections.length!==reader.sections.length)issues.push('section_count');
  for(let i=0;i<source.sections.length;i++){
    const a=source.sections[i],b=reader.sections[i];
    if(!b||a.kind!==b.kind)issues.push('section_kind:'+i);
    else {if(JSON.stringify(ids(a.images))!==JSON.stringify(b.images.map(x=>x.fileId)))issues.push('section_images:'+i+':'+a.kind);const x=new Set(a.fields.map(f=>f.key+'\0'+f.value)),y=new Set(b.fields.map(f=>f.key+'\0'+f.value));if([...x].some(f=>!y.has(f))||[...y].some(f=>!x.has(f)))issues.push('section_definition:'+i+':'+a.kind);}
  }
  const set=a=>new Set(a.map(f=>f.key+'\0'+f.value)),a=set(source.fields),b=set(reader.fields);
  if(source.fields.some(f=>!b.has(f.key+'\0'+f.value))||reader.fields.some(f=>!a.has(f.key+'\0'+f.value)))issues.push('definition_difference');
  if(source.images.some(i=>!i.fileId))issues.push('unsupported_image_reference');
  return issues;
}
