import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import path from 'node:path';
import test from 'node:test';
import worker from '../src/index.ts';
import { generate } from '../../cli/contracts.mjs';
import { remoteStatus, createProposal, GithubError } from '../src/github.ts';

const prepared = fileURLToPath(new URL('../public/__repo/', import.meta.url));
const fixture = async name => JSON.parse(await readFile(path.join(prepared, name), 'utf8'));
const model = await fixture('model.json');
const catalog = await fixture('catalog.json');
const entry = model.files.find(file => file.path.startsWith('specs/'));
const password = 'fixture-password';
const basic = `Basic ${Buffer.from(`workbench:${password}`).toString('base64')}`;
let assetReads = 0;
const assetPaths = [];
const env = {
  DASHBOARD_PASSWORD: password,
  ASSETS: {
    async fetch(request) {
      assetReads++;
      const url = new URL(request.url);
      assetPaths.push(url.pathname);
      assert.match(url.pathname, /^\/__repo\/(?:model\.json|catalog\.json|lookup\.json|pages\/[a-f0-9]{32}\.json|images\/[a-zA-Z0-9._-]+\.(?:png|jpe?g))$/i);
      try { return new Response(await readFile(path.join(prepared, url.pathname.slice('/__repo/'.length)))); }
      catch { return new Response('missing', { status: 404 }); }
    },
  },
};
const origin = 'https://workbench.example';
function request(pathname, { method = 'GET', authenticated = true, body, extraHeaders = {}, runtime = env } = {}) {
  const headers = { ...(authenticated ? { Authorization: basic } : {}), ...extraHeaders };
  if (body !== undefined) {
    headers.Origin = origin;
    headers['Content-Type'] = 'application/json';
  }
  return worker.fetch(new Request(`${origin}${pathname}`, {
    method, headers, ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  }), runtime);
}

test('Basic auth guards every route and missing password fails closed', async () => {
  const before = assetReads;
  for (const route of ['/', '/api/catalog', '/api/model', '/__repo/catalog.json', '/__repo/images/private.png', '/unknown']) {
    const denied = await request(route, { authenticated: false });
    assert.equal(denied.status, 401, route);
    assert.match(denied.headers.get('WWW-Authenticate'), /Basic realm=/);
    assert.ok((await denied.json()).error);
    assert.match(denied.headers.get('Cache-Control'), /no-store/);
    assert.equal(denied.headers.get('X-Content-Type-Options'), 'nosniff');
  }
  assert.equal(assetReads, before);
  assert.equal((await request('/', { runtime: { ...env, DASHBOARD_PASSWORD: undefined } })).status, 503);
  assert.equal(assetReads, before);
  assert.equal((await request('/', { extraHeaders: { Authorization: `Basic ${Buffer.from('not-workbench:fixture-password').toString('base64')}` } })).status, 401);
  const home = await request('/');
  assert.equal(home.status, 200);
  assert.match(home.headers.get('Content-Security-Policy'), /script-src 'sha256-/);
  assert.doesNotMatch(home.headers.get('Content-Security-Policy'), /unsafe-inline/);
});

test('only documented private API paths access prepared archive', async () => {
  const before = assetReads;
  for (const route of ['/__repo/catalog.json', '/__repo/', '/__repoevil', '/favicon.ico', '/api/unknown', '/api/source?id=../model.json']) {
    const result = await request(route);
    assert.ok(result.status === 404 || result.status === 400, route);
  }
  assert.equal(assetReads, before);
  const manifest = await (await request('/api/catalog')).json();
  assert.deepEqual(manifest.counts, catalog.counts);
  const doc = manifest.documents[0];
  const page = await (await request(`/api/source?id=${doc.id}`)).json();
  assert.equal(page.path, doc.path);
  assert.equal((await request('/api/source?id=ffffffffffffffffffffffffffffffff')).status, 404);
  const asset = manifest.assets[0];
  const firstImageRead = assetPaths.length;
  const image = await request(`/api/image?file=${encodeURIComponent(asset.file)}`);
  assert.deepEqual(assetPaths.slice(firstImageRead), [
    '/__repo/lookup.json', `/__repo/images/${asset.file.slice('assets/'.length)}`,
  ]);
  assert.equal(image.status, 200);
  assert.equal(image.headers.get('Content-Type'), asset.file.endsWith('.png') ? 'image/png' : 'image/jpeg');
  assert.equal(createHash('sha256').update(Buffer.from(await image.arrayBuffer())).digest('hex'), asset.sha256);
  assert.equal((await request('/api/image?file=assets/not-in-manifest.png')).status, 404);
  const spec = await (await request(`/api/spec?path=${encodeURIComponent(entry.path)}`)).json();
  assert.deepEqual(spec, { path: entry.path, text: entry.text, sha: entry.sha, commit: model.commit });
});

test('snapshot mode and complete canonical model do not require GitHub credentials', async () => {
  const status = await (await request('/api/status')).json();
  assert.deepEqual({ mode: status.mode, connected: status.connected, repository: status.repository, snapshotCommit: status.snapshotCommit },
    { mode: 'snapshot', connected: false, repository: model.repository, snapshotCommit: model.commit });
  const received = await (await request('/api/model')).json();
  assert.deepEqual(received, model);
  const validated = await (await request('/api/validate', { method: 'POST', body: { path: entry.path, text: entry.text } })).json();
  assert.deepEqual(validated.errors, []);
  assert.deepEqual(validated.counts, { approved: 9, draft: 0, legacy: 0, frozen: 0 });
  assert.deepEqual(validated.spec, model.model.specs.find(spec => spec.file === entry.path).data);
  const generated = await (await request('/api/generate', { method: 'POST', body: { path: entry.path, text: entry.text } })).json();
  assert.deepEqual(generated.files, generate(model.model));
  assert.deepEqual(generated.manifest, JSON.parse(generated.files['manifest.json']));
  const preview = await (await request('/api/generate', { method: 'POST', body: { path: entry.path, text: entry.text, preview: true } })).json();
  assert.deepEqual(preview.files, generate(model.model, { preview: true }));
  assert.match(preview.files['logging.ts'], /PREVIEW/);
});

test('unsafe YAML, missing source, CSRF and oversized JSON fail deliberately', async () => {
  const post = (text, headers) => request('/api/validate', { method: 'POST', body: { path: entry.path, text }, extraHeaders: headers });
  const duplicate = await (await post('service: owner\nservice: owner\n')).json();
  assert.match(duplicate.errors.join(' '), /YAML/);
  const aliased = await (await post('service: &same owner\nscreen_view: *same\n')).json();
  assert.match(aliased.errors.join(' '), /YAML/);
  const unknownSource = entry.text.replace(/notion\/pages\/[a-f0-9]{32}\.md/, 'notion/pages/ffffffffffffffffffffffffffffffff.md');
  assert.match((await (await post(unknownSource)).json()).errors.join(' '), /원문 저장소에 없는 source/);
  const invalid = await request('/api/generate', { method: 'POST', body: { path: entry.path, text: 'events: []' } });
  assert.equal(invalid.status, 422);
  assert.ok(Array.isArray((await invalid.json()).errors));
  const csrf = await worker.fetch(new Request(`${origin}/api/validate`, {
    method: 'POST', headers: { Authorization: basic, 'Content-Type': 'application/json', Origin: 'https://another.example' },
    body: JSON.stringify({ path: entry.path, text: entry.text }),
  }), env);
  assert.equal(csrf.status, 403);
  const huge = await request('/api/validate', { method: 'POST', body: { path: entry.path, text: 'x'.repeat(1024 * 1024) } });
  assert.equal(huge.status, 413);
});

test('proposals reject missing token, stale file and approved demotion before network', async () => {
  const proposal = { path: entry.path, text: entry.text, title: 'Review logging contract', commit: model.commit, sha: entry.sha };
  assert.equal((await request('/api/proposals', { method: 'POST', body: proposal })).status, 503);
  const tokenEnv = { ...env, GITHUB_TOKEN: 'local-fixture-token' };
  assert.equal((await request('/api/proposals', { method: 'POST', body: { ...proposal, sha: '0'.repeat(40) }, runtime: tokenEnv })).status, 409);
  const demoted = JSON.parse(entry.text);
  demoted.events[0].status = 'draft';
  const result = await request('/api/proposals', { method: 'POST', body: { ...proposal, text: JSON.stringify(demoted) }, runtime: tokenEnv });
  assert.equal(result.status, 409);
  assert.match((await result.json()).error, /강등/);
});

test('GitHub HEAD conflict path uses read-only fake transport', async () => {
  const seen = [];
  const fakeFetch = async (url, options) => {
    seen.push({ url, method: options.method });
    const result = url.endsWith('/repos/BCSDLab/KOIN-DATA-LOGGING')
      ? { full_name: model.repository, default_branch: 'main' }
      : { object: { sha: 'f'.repeat(40) } };
    return Response.json(result);
  };
  const status = await remoteStatus('test-token', model.repository, fakeFetch);
  assert.equal(status.head, 'f'.repeat(40));
  await assert.rejects(createProposal({
    token: 'test-token', repository: model.repository, snapshotCommit: model.commit,
    expectedFiles: model.files.map(file => ({ path: file.path, sha: file.sha })),
    specPath: entry.path, specText: entry.text, title: 'Review contract',
    generated: generate(model.model),
  }, fakeFetch), error => error instanceof GithubError && error.status === 409);
  assert.ok(seen.every(call => call.method === 'GET'));
  await assert.rejects(remoteStatus('test-token', 'other/repo', fakeFetch), error => error instanceof GithubError && error.status === 503);
});

test('new underscore paths retain CLI binary spec ordering and exact revision', async () => {
  const original = model.model.specs.find(spec => spec.file === 'specs/owner/main_category.yaml').data;
  function variant(screen) {
    const data = structuredClone(original);
    data.screen_view = screen;
    data.events = data.events.map(event => ({
      ...event,
      status: 'draft',
      event_label: event.event_label.replace('__main_category__', `__${screen}__`),
    }));
    return data;
  }
  const a1 = variant('a1');
  const a_1 = variant('a_1');
  const seeded = { ...model, model: { ...model.model,
    specs: [...model.model.specs, { file: 'specs/owner/a1.yaml', data: a1 }]
      .sort((a, b) => a.file < b.file ? -1 : a.file > b.file ? 1 : 0) } };
  const fixtureEnv = { ...env, ASSETS: { fetch(request) {
    if (new URL(request.url).pathname === '/__repo/model.json') return Promise.resolve(Response.json(seeded));
    return env.ASSETS.fetch(request);
  } } };
  const pathNew = 'specs/owner/a_1.yaml';
  const text = JSON.stringify(a_1);
  const result = await request('/api/generate', { method: 'POST', body: { path: pathNew, text }, runtime: fixtureEnv });
  assert.equal(result.status, 200, await result.clone().text());
  const expected = { ...seeded.model, specs: [...seeded.model.specs, { file: pathNew, data: a_1 }]
    .sort((a, b) => a.file < b.file ? -1 : a.file > b.file ? 1 : 0) };
  assert.ok(expected.specs.findIndex(spec => spec.file === 'specs/owner/a1.yaml') <
    expected.specs.findIndex(spec => spec.file === pathNew));
  assert.deepEqual((await result.json()).files, generate(expected));
});
