import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {parseSource,parseReader,compare} from './notion-comparison.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),read=p=>fs.readFileSync(path.join(root,p));
const nav=JSON.parse(read('_archive/navigation-map.json')),images=JSON.parse(read('_archive/live-notion-images.json')).images;
const snapshots=zlib.gunzipSync(read('_archive/live-notion-snapshots.jsonl.gz')).toString('utf8').trim().split('\n').map(JSON.parse),sources=new Map(snapshots.map(s=>[s.id,s]));
const errors=[],byId=new Map(images.map(i=>[i.id,i]));let references=0,sections=0;
if(sources.size!==snapshots.length||sources.size!==nav.pages.length)errors.push('Source coverage/duplicate mismatch');
for(const page of nav.pages){const source=sources.get(page.id);if(!source){errors.push('Missing source: '+page.id);continue;}if(source.truncated||source.unknownBlocks)errors.push('Incomplete source: '+page.id);
 const parsed=parseSource(source.body),reader=parseReader(read(page.file).toString('utf8'));
 const canonical=id=>{const asset=byId.get(id)?.assetFile;return asset?path.basename(asset).split('.')[0]:id;};
 for(const issue of compare(parsed,reader,canonical))errors.push(page.id+': '+issue);
 references+=parsed.images.length;sections+=parsed.sections.length;
 if(crypto.createHash('sha256').update(source.body).digest('hex')!==source.normalizedBodySha256)errors.push('Snapshot body hash: '+page.id);
}
for(const image of images){if(!image.assetFile){errors.push('Unresolved image: '+image.id);continue;}const b=read(image.assetFile);if(b.length!==image.bytes||crypto.createHash('sha256').update(b).digest('hex')!==image.sha256)errors.push('Live image bytes: '+image.id);}
console.log(JSON.stringify({pagesCompared:nav.pages.length,imageReferences:references,pastAndNewSections:sections,uniqueImageBytesChecked:images.length,errors},null,2));if(errors.length)process.exitCode=1;
