import { readFile, writeFile, mkdir, realpath, rm, lstat } from 'node:fs/promises';
import { resolve, relative, dirname, isAbsolute, basename } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { load, files as sourcePaths } from '../../cli/core.mjs';
import { validate } from '../../cli/contracts.mjs';

const REPOSITORY = 'BCSDLab/KOIN-DATA-LOGGING';
const MAX_IMAGE_BYTES = 20 * 1024 * 1024;
const digest = value => createHash('sha256').update(value).digest('hex');
const blobSha = value => createHash('sha1').update(`blob ${Buffer.byteLength(value)}\0`).update(value).digest('hex');
function inside(root, path) {
  const part = relative(root, path);
  return part !== '..' && !part.startsWith('../') && !part.startsWith('..\\') && !isAbsolute(part);
}
async function checkedSourcePath(root, path) {
  const actual = await realpath(resolve(root, path));
  if (!inside(root, actual)) throw new Error(`Source path escapes repository: ${path}`);
  return actual;
}
async function sourceFile(root, path) {
  return readFile(await checkedSourcePath(root, path));
}
function imageReferences(markdown, file, assets) {
  const references = new Set();
  const targets = [
    ...Array.from(markdown.matchAll(/!\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g), match => match[1]),
    ...Array.from(markdown.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi), match => match[1]),
  ];
  for (const target of targets) {
    if (/^(?:[a-z][a-z0-9+.-]*:|#)/i.test(target)) continue;
    let decoded;
    try { decoded = decodeURIComponent(target.split('#')[0]); }
    catch { throw new Error(`Invalid encoded image reference in ${file}`); }
    const normalized = relative('notion', resolve(dirname(resolve('notion', file)), decoded)).split('\\').join('/');
    if (!assets.has(normalized)) throw new Error(`Missing or unsafe source image: ${file} -> ${target}`);
    references.add(normalized);
  }
  return [...references];
}

/** Generates disposable build assets from canonical source files, never a second editable catalogue. */
export async function prepareSnapshot(repositoryRoot, outputDirectory) {
  const root = await realpath(repositoryRoot);
  const requestedRoot = resolve(repositoryRoot);
  const requestedOutput = resolve(outputDirectory);
  if (!inside(requestedRoot, requestedOutput) || requestedOutput === requestedRoot) throw new Error('Snapshot output must remain inside its repository.');
  const output = resolve(root, relative(requestedRoot, requestedOutput));
  const candidates = ['rules/vocabulary.json', 'rules/envelope.json', ...sourcePaths(resolve(root, 'specs')).filter(file => /\.(yaml|yml)$/.test(file)).map(file => relative(root, file))];
  for (const path of candidates) await checkedSourcePath(root, path);
  const model = load(root);
  const errors = validate(model);
  if (errors.length) throw new Error(errors.join('\n'));
  const pageIndex = JSON.parse((await sourceFile(root, 'notion/index.json')).toString('utf8'));
  const assets = JSON.parse((await sourceFile(root, 'notion/assets-manifest.json')).toString('utf8'));
  if (!Array.isArray(pageIndex) || !Array.isArray(assets)) throw new Error('Invalid archive indexes.');
  const assetNames = new Set();
  const ids = new Set();
  const preparedImages = [];
  for (const asset of assets) {
    if (!/^assets\/[A-Za-z0-9_.-]+\.(?:png|jpg)$/.test(asset.file) || assetNames.has(asset.file) || !/^[a-f0-9]{64}$/.test(asset.sha256) || !Number.isSafeInteger(asset.bytes) || asset.bytes < 1 || asset.bytes > MAX_IMAGE_BYTES) throw new Error('Invalid archive image manifest entry.');
    assetNames.add(asset.file);
    const bytes = await sourceFile(root, `notion/${asset.file}`);
    if (bytes.length !== asset.bytes || digest(bytes) !== asset.sha256) throw new Error(`Archive image integrity mismatch: ${asset.file}`);
    preparedImages.push({ file: asset.file, bytes });
  }
  const pages = [];
  const documents = [];
  for (const entry of pageIndex) {
    if (!/^[a-f0-9]{32}$/.test(entry.id) || entry.file !== `pages/${entry.id}.md` || ids.has(entry.id) || typeof entry.title !== 'string' || typeof entry.path !== 'string') throw new Error('Invalid archive source entry.');
    ids.add(entry.id);
    const markdown = new TextDecoder('utf-8', { fatal: true }).decode(await sourceFile(root, `notion/${entry.file}`));
    const imageFiles = imageReferences(markdown, entry.file, assetNames);
    const pilotSpecPaths = model.specs.filter(spec => spec.data.events.some(event => event.source === `notion/${entry.file}`)).map(spec => spec.file);
    const data = { id: entry.id, title: entry.title, path: entry.path, properties: entry.properties ?? {}, markdown, imageFiles, pilotSpecPaths };
    pages.push(data);
    documents.push({ id: entry.id, title: entry.title, path: entry.path, file: `notion/${entry.file}`, properties: entry.properties ?? {}, imageFiles, searchText: `${entry.title}\n${entry.path}\n${markdown}` });
  }
  for (const spec of model.specs) for (const event of spec.data.events) if (!ids.has(event.source.match(/([a-f0-9]{32})\.md$/)?.[1])) throw new Error(`Contract references an unindexed source: ${event.source}`);
  const inputPaths = ['rules/vocabulary.json', 'rules/envelope.json', ...model.specs.map(spec => spec.file)].sort();
  const files = [];
  for (const path of inputPaths) {
    const bytes = await sourceFile(root, path);
    files.push({ path, text: new TextDecoder('utf-8', { fatal: true }).decode(bytes), sha: blobSha(bytes) });
  }
  const commit = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  if (!/^[a-f0-9]{40}$/.test(commit)) throw new Error('Cannot identify source commit.');
  const snapshotHash = digest(JSON.stringify({ files, pages: pages.map(page => [page.id, digest(page.markdown)]), assets }));
  const counts = { documents: documents.length, images: assets.length, specFiles: model.specs.length, approved: 0, draft: 0, legacy: 0, frozen: 0 };
  for (const spec of model.specs) for (const event of spec.data.events) counts[event.status]++;
  const catalog = { repository: REPOSITORY, commit, snapshotHash, documents, assets, counts };
  const snapshot = { repository: REPOSITORY, commit, snapshotHash, model, files };
  // All validation happens before touching a previous build snapshot.
  const marker = resolve(output, '.generated-snapshot.json');
  let previousFiles = [];
  try {
    if (!(await lstat(marker)).isFile()) throw new Error('Generated snapshot marker must be a regular file.');
    const previous = JSON.parse(await readFile(marker, 'utf8'));
    if (!Array.isArray(previous.files) || previous.files.some(file => typeof file !== 'string' || !inside(output, resolve(output, file)))) throw new Error('Invalid generated snapshot manifest.');
    previousFiles = previous.files;
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  await mkdir(output, { recursive: true });
  if (!inside(root, await realpath(output))) throw new Error('Snapshot output symlink escapes repository.');
  const written = [];
  async function emit(path, bytes) {
    const file = resolve(output, path);
    if (!inside(output, file)) throw new Error('Unsafe generated file path.');
    await mkdir(dirname(file), { recursive: true });
    if (!inside(output, await realpath(dirname(file)))) throw new Error('Generated directory symlink escapes output.');
    try { if (!(await lstat(file)).isFile()) throw new Error('Generated target must be a regular file.'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
    await writeFile(file, bytes);
    written.push(path);
  }
  for (const page of pages) await emit(`pages/${page.id}.json`, JSON.stringify(page));
  for (const image of preparedImages) await emit(`images/${basename(image.file)}`, image.bytes);
  for (const file of files.filter(file => file.path.startsWith('specs/'))) await emit(file.path, file.text);
  await emit('model.json', JSON.stringify(snapshot));
  await emit('catalog.json', JSON.stringify(catalog));
  await emit('lookup.json', JSON.stringify({ repository: REPOSITORY, commit, snapshotHash, counts, documents: documents.map(({ id, file }) => ({ id, file })), assets }));
  await emit('assets.json', JSON.stringify(assets));
  for (const obsolete of previousFiles) if (!written.includes(obsolete)) await rm(resolve(output, obsolete), { force: true });
  await writeFile(marker, JSON.stringify({ files: written, snapshotHash }));
  return { ...counts, commit, snapshotHash };
}

const here = dirname(fileURLToPath(import.meta.url));
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const result = await prepareSnapshot(resolve(here, '../..'), resolve(here, '../public/__repo'));
    console.log(JSON.stringify(result, null, 2));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
