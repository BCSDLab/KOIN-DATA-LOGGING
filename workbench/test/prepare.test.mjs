import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm, unlink, symlink } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { prepareSnapshot } from '../scripts/prepare.mjs';

const id = '00000000000000000000000000000001';
async function fixture(root) {
  for (const path of ['rules', 'specs/cafeteria', 'notion/pages', 'notion/assets']) await mkdir(join(root, path), { recursive: true });
  const bytes = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6C1sAAAAASUVORK5CYII=', 'base64');
  const platforms = ['WEB', 'WEB (모바일)', 'ANDROID', 'IOS'];
  const spec = { schema_version: 1, service: 'cafeteria', screen_view: 'main_category', events: [{
    description: '식단을 클릭할 때', event_name: 'DA1', event_label: 'cafeteria__main_category__entry__click', event_category: 'click',
    value: { type: 'string', required: true, description: '고정값', const: '식단' }, params: {}, platforms: ['WEB (모바일)'], status: 'approved',
    source: `notion/pages/${id}.md`, platform_support: Object.fromEntries(platforms.map(p => [p, { state: p === 'WEB (모바일)' ? 'confirmed' : 'unknown', evidence: 'fixture' }])),
  }] };
  await writeFile(join(root, 'rules/vocabulary.json'), JSON.stringify({ schema_version: 1, categories: ['click'], services: { cafeteria: 'DA1' }, platforms, screen_overrides: [] }));
  await writeFile(join(root, 'rules/envelope.json'), JSON.stringify({ schema_version: 1, reserved_keys: ['event_label'], notes: 'fixture' }));
  await writeFile(join(root, 'specs/cafeteria/main_category.yaml'), JSON.stringify(spec));
  await writeFile(join(root, 'notion/index.json'), JSON.stringify([{ id, title: '식단 진입', path: 'Event Log', file: `pages/${id}.md`, properties: { title: '식단 진입' } }]));
  await writeFile(join(root, 'notion/assets-manifest.json'), JSON.stringify([{ file: 'assets/source.png', bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex') }]));
  await writeFile(join(root, 'notion/assets/source.png'), bytes);
  await writeFile(join(root, `notion/pages/${id}.md`), '# 식단 진입\n![화면](../assets/source.png)\n');
  execFileSync('git', ['init', '-q', root]);
  execFileSync('git', ['-C', root, '-c', 'commit.gpgsign=false', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-q', '-m', 'fixture']);
}

test('snapshot separates archived documents from approved contracts and ties images to their source', async () => {
  const root = await mkdtemp(join(tmpdir(), 'koin-source-'));
  try {
    await fixture(root);
    const output = join(root, 'workbench/public/__repo');
    const result = await prepareSnapshot(root, output);
    assert.equal(result.documents, 1);
    assert.equal(result.images, 1);
    assert.equal(result.approved, 1);
    const source = JSON.parse(await readFile(join(output, `pages/${id}.json`), 'utf8'));
    assert.deepEqual(source.imageFiles, ['assets/source.png']);
    assert.deepEqual(source.pilotSpecPaths, ['specs/cafeteria/main_category.yaml']);
    assert.equal((await prepareSnapshot(root, output)).snapshotHash, result.snapshotHash);
    const before = await readFile(join(output, 'catalog.json'));
    await writeFile(join(root, 'notion/assets/source.png'), 'corrupt');
    await assert.rejects(prepareSnapshot(root, output));
    assert.deepEqual(await readFile(join(output, 'catalog.json')), before);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test('snapshot cannot read source symlinks outside the repository', async () => {
  const root = await mkdtemp(join(tmpdir(), 'koin-source-path-'));
  const outside = await mkdtemp(join(tmpdir(), 'koin-private-'));
  try {
    await fixture(root);
    const privateFile = join(outside, 'private.md');
    await writeFile(privateFile, 'private material');
    await unlink(join(root, `notion/pages/${id}.md`));
    await symlink(privateFile, join(root, `notion/pages/${id}.md`));
    await assert.rejects(prepareSnapshot(root, join(root, 'workbench/public/__repo')));
    await assert.rejects(readFile(join(root, 'workbench/public/__repo/catalog.json')), { code: 'ENOENT' });
  } finally { await rm(root, { recursive: true, force: true }); await rm(outside, { recursive: true, force: true }); }
});
