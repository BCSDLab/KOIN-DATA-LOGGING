import fs from 'node:fs';
import path from 'node:path';
import { parseDocument } from 'yaml';

export function files(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory()
    ? files(path.join(dir, e.name)) : [path.join(dir, e.name)]).sort();
}
export function read(file) {
  const doc = parseDocument(fs.readFileSync(file, 'utf8'), { uniqueKeys: true });
  if (doc.errors.length) throw new Error(`${file}: ${doc.errors[0].message}`);
  return doc.toJS();
}
export function load(root) {
  return {
    vocabulary: read(path.join(root, 'rules/vocabulary.json')),
    envelope: read(path.join(root, 'rules/envelope.json')),
    specs: files(path.join(root, 'specs')).filter(f => /\.(yaml|yml)$/.test(f))
      .map(f => ({ file: path.relative(root, f).replaceAll('\\', '/'), data: read(f) })),
  };
}
