import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';

export function validateArchive(root, {inventory} = {}) {
  root = path.resolve(root);
  const exists = file => fs.existsSync(file) || inventory?.has(path.relative(root, file).split(path.sep).join('/'));
  const index = JSON.parse(fs.readFileSync(path.join(root, 'notion/index.json'), 'utf8'));
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'notion/assets-manifest.json'), 'utf8'));
  const errors = [], ids = new Set(), assetNames = new Set();
  let links = 0, images = 0;
  function checkTarget(file, target) {
    if (/^(?:[a-z][a-z0-9+.-]*:|#)/i.test(target)) return;
    const resolved = path.resolve(path.dirname(file), decodeURIComponent(target.split('#')[0]));
    if (path.relative(root, resolved).startsWith('..') || !exists(resolved)) errors.push(`Missing/unsafe link: ${path.relative(root,file)} -> ${target}`);
    links++;
  }
  const files = ['README.md', 'notion/README.md', 'notion/recovery-review.md', ...index.map(e=>'notion/'+e.file)];
  for (const file of new Set(files)) {
    const absolute = path.join(root, file);
    if (!fs.existsSync(absolute)) {errors.push('Missing document: '+file); continue;}
    const text = fs.readFileSync(absolute, 'utf8');
    if (/<\/?image\b/i.test(text)) errors.push('Unsupported image tag: '+file);
    if (/https?:\/\/(?:app\.)?notion\.(?:com|so)\b/i.test(text)) errors.push('External Notion URL: '+file);
    for (const m of text.matchAll(/(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)) {checkTarget(absolute,m[2]); if(m[1]) images++;}
    for (const m of text.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi)) {checkTarget(absolute,m[1]);images++;}
  }
  for (const e of index) {if(ids.has(e.id)) errors.push('Duplicate source ID: '+e.id);ids.add(e.id);}
  for (const asset of manifest) {
    if(assetNames.has(asset.file))errors.push('Duplicate asset: '+asset.file);assetNames.add(asset.file);
    const file = path.join(root,'notion',asset.file);
    if(!exists(file)){errors.push('Missing asset: '+asset.file);continue;}
    if(fs.existsSync(file)) {
      const bytes=fs.readFileSync(file);
      if(bytes.length!==asset.bytes||crypto.createHash('sha256').update(bytes).digest('hex')!==asset.sha256) errors.push('Asset integrity: '+asset.file);
    }
  }
  const recovery = JSON.parse(fs.readFileSync(path.join(root,'notion/recovery-manifest.json'),'utf8'));
  for(const r of recovery.pages) if(!ids.has(r.id))errors.push('Recovered source absent from index: '+r.id);
  return {documents:index.length,assets:manifest.length,recoveredPages:recovery.pages.length,links,images,errors};
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const result = validateArchive(process.cwd());
  console.log(JSON.stringify(result,null,2));
  if(result.errors.length) process.exitCode=1;
}
