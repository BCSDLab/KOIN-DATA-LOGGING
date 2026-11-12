import { createHash, timingSafeEqual } from 'node:crypto';
import { parseDocument } from 'yaml';
import { validate, generate } from '../../cli/contracts.mjs';
import type { CanonicalModel } from '../../cli/contracts.mjs';
import { dashboardHtml } from './dashboard.ts';
import { createProposal, GithubError, remoteStatus } from './github.ts';

type RuntimeEnv = Env & { GITHUB_TOKEN?: string };
type Spec = CanonicalModel['specs'][number]['data'];
type Lookup = {
  repository: string;
  commit: string;
  snapshotHash: string;
  documents: Array<{ id: string; file: string }>;
  assets: Array<{ file: string; bytes: number; sha256: string }>;
  counts: { documents: number; images: number; specFiles: number; approved: number; draft: number; legacy: number; frozen: number };
};
type Snapshot = {
  model: CanonicalModel;
  files: Array<{ path: string; text: string; sha: string }>;
  repository: string;
  commit: string;
  snapshotHash: string;
};
type Overlay = { model: CanonicalModel; spec: Spec | null; errors: string[]; counts: Record<'approved' | 'draft' | 'legacy' | 'frozen', number> };

const DEFAULT_REPOSITORY = 'BCSDLab/KOIN-DATA-LOGGING';
const MAX_BODY = 1024 * 1024;
const SPEC_PATH = /^specs\/[a-z][a-z0-9_]*\/[a-z][a-z0-9_]*\.yaml$/;
const hashes = (tag: 'script' | 'style') => [...dashboardHtml.matchAll(new RegExp(`<${tag}(?:\\s[^>]*)?>([\\s\\S]*?)<\\/${tag}>`, 'gi'))]
  .map(match => `'sha256-${createHash('sha256').update(match[1]).digest('base64')}'`).join(' ') || "'none'";
const POLICY = {
  'Cache-Control': 'private, no-store',
  'X-Content-Type-Options': 'nosniff',
  'Content-Security-Policy': `default-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'; img-src 'self' blob: data:; style-src ${hashes('style')}; script-src ${hashes('script')}; connect-src 'self'`,
  'Referrer-Policy': 'no-referrer',
  'X-Frame-Options': 'DENY',
};

class ApiError extends Error {
  readonly status: number;
  readonly errors?: string[];
  constructor(message: string, status = 400, errors?: string[]) {
    super(message);
    this.status = status;
    this.errors = errors;
  }
}

function response(body: BodyInit | null, type: string, status = 200, headers?: HeadersInit): Response {
  return new Response(body, { status, headers: { ...POLICY, 'Content-Type': type, ...headers } });
}
function json(value: unknown, status = 200, headers?: HeadersInit): Response {
  return response(JSON.stringify(value), 'application/json; charset=utf-8', status, headers);
}
function reject(message: string, status: number, details?: Record<string, unknown>): Response {
  return json({ error: message, ...details }, status);
}

async function authorized(request: Request, password: string): Promise<boolean> {
  const header = request.headers.get('Authorization');
  if (!header?.startsWith('Basic ') || header.length > 4096) return false;
  let decoded: string;
  try {
    const bytes = Uint8Array.from(atob(header.slice(6)), c => c.charCodeAt(0));
    decoded = new TextDecoder('utf-8', { fatal: true, ignoreBOM: false }).decode(bytes);
  } catch { return false; }
  const split = decoded.indexOf(':');
  if (split < 0 || decoded.slice(0, split) !== 'workbench') return false;
  const encoder = new TextEncoder();
  const [actual, expected] = await Promise.all([
    crypto.subtle.digest('SHA-256', encoder.encode(decoded.slice(split + 1))),
    crypto.subtle.digest('SHA-256', encoder.encode(password)),
  ]);
  return timingSafeEqual(new Uint8Array(actual), new Uint8Array(expected));
}

async function privateAsset(env: RuntimeEnv, request: Request, path: string): Promise<Response> {
  const url = new URL(request.url);
  url.pathname = `/__repo/${path}`;
  url.search = '';
  const asset = await env.ASSETS.fetch(new Request(url, { method: 'GET' }));
  if (!asset.ok) throw new ApiError('준비된 스냅샷 자료를 찾을 수 없습니다. prepare를 다시 실행하세요.', 503);
  return asset;
}
async function privateJson<T>(env: RuntimeEnv, request: Request, path: string): Promise<T> {
  const data = await privateAsset(env, request, path);
  return await data.json() as T;
}
async function snapshot(env: RuntimeEnv, request: Request): Promise<Snapshot> {
  const data = await privateJson<Snapshot>(env, request, 'model.json');
  if (!data?.model || !Array.isArray(data.files) || !/^[a-f0-9]{40}$/.test(data.commit) || !data.snapshotHash) {
    throw new ApiError('준비된 명세 스냅샷이 올바르지 않습니다. prepare를 다시 실행하세요.', 503);
  }
  return data;
}
async function lookup(env: RuntimeEnv, request: Request): Promise<Lookup> {
  const data = await privateJson<Lookup>(env, request, 'lookup.json');
  if (!Array.isArray(data?.documents) || !Array.isArray(data?.assets) || !data.counts) {
    throw new ApiError('준비된 원문 목록이 올바르지 않습니다. prepare를 다시 실행하세요.', 503);
  }
  return data;
}
function parameter(url: URL, name: string): string {
  const values = url.searchParams.getAll(name);
  if (values.length !== 1) throw new ApiError(`${name} 값 하나가 필요합니다.`);
  return values[0];
}
function specPath(path: unknown): asserts path is string {
  if (typeof path !== 'string' || !SPEC_PATH.test(path)) throw new ApiError('명세 경로는 specs/<service>/<screen>.yaml 형식이어야 합니다.');
}
function object(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// Structural narrowing only; the shared validator remains the source of business rules.
function specShape(value: unknown): value is Spec {
  if (!object(value) || value.schema_version !== 1 || typeof value.service !== 'string' ||
      typeof value.screen_view !== 'string' || !Array.isArray(value.events)) return false;
  const primitive = (item: unknown) => ['string', 'number', 'boolean'].includes(typeof item);
  const descriptor = (item: unknown) => object(item) &&
    ['string', 'number', 'boolean'].includes(String(item.type)) &&
    typeof item.description === 'string' && typeof item.required === 'boolean' &&
    (!Object.hasOwn(item, 'enum') || (Array.isArray(item.enum) && item.enum.every(primitive))) &&
    (!Object.hasOwn(item, 'const') || primitive(item.const));
  const platforms = ['WEB', 'WEB (모바일)', 'ANDROID', 'IOS'];
  return value.events.every(event => {
    if (!object(event) || typeof event.description !== 'string' || typeof event.event_name !== 'string' ||
        typeof event.event_label !== 'string' || typeof event.event_category !== 'string' ||
        typeof event.source !== 'string' ||
        (Object.hasOwn(event, 'decision') && typeof event.decision !== 'string') ||
        (Object.hasOwn(event, 'notes') && typeof event.notes !== 'string') ||
        !['approved', 'draft', 'legacy', 'frozen'].includes(String(event.status)) ||
        !descriptor(event.value) || !object(event.params) || !Object.values(event.params).every(descriptor) ||
        !Array.isArray(event.platforms) || !event.platforms.every(platform => platforms.includes(platform))) return false;
    const supports = event.platform_support;
    return object(supports) && platforms.every(platform => {
      const support = supports[platform];
      return object(support) && ['confirmed', 'unsupported', 'unknown'].includes(String(support.state)) &&
        typeof support.evidence === 'string';
    });
  });
}

async function postBody(request: Request): Promise<Record<string, unknown>> {
  if (request.headers.get('Origin') !== new URL(request.url).origin) throw new ApiError('동일 출처 요청만 허용합니다.', 403);
  if (!/^application\/json(?:\s*;\s*charset=utf-8)?$/i.test(request.headers.get('Content-Type') || '')) throw new ApiError('JSON 본문이 필요합니다.', 415);
  const length = Number(request.headers.get('Content-Length'));
  if (Number.isFinite(length) && length > MAX_BODY) throw new ApiError('본문 크기는 1 MiB 이하여야 합니다.', 413);
  if (!request.body) throw new ApiError('JSON 본문이 필요합니다.');
  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > MAX_BODY) { await reader.cancel(); throw new ApiError('본문 크기는 1 MiB 이하여야 합니다.', 413); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  let parsed: unknown;
  try { parsed = JSON.parse(new TextDecoder('utf-8', { fatal: true, ignoreBOM: false }).decode(bytes)); }
  catch { throw new ApiError('유효한 UTF-8 JSON 본문이 필요합니다.'); }
  if (!object(parsed)) throw new ApiError('JSON 객체 본문이 필요합니다.');
  return parsed;
}

function count(model: CanonicalModel): Overlay['counts'] {
  const counts = { approved: 0, draft: 0, legacy: 0, frozen: 0 };
  for (const spec of model.specs) for (const event of Array.isArray(spec.data?.events) ? spec.data.events : []) {
    if (object(event) && typeof event.status === 'string' && Object.hasOwn(counts, event.status)) {
      counts[event.status as keyof typeof counts]++;
    }
  }
  return counts;
}

function parseSpec(text: string): { spec: Spec | null; errors: string[] } {
  try {
    const doc = parseDocument(text, { uniqueKeys: true, version: '1.2', merge: false, stringKeys: true });
    if (doc.errors.length) return { spec: null, errors: doc.errors.map(e => `YAML: ${e.message.slice(0, 400)}`) };
    const data: unknown = doc.toJS({ maxAliasCount: 0 });
    const visited = new Set<object>();
    function depth(value: unknown, level: number): void {
      if (!value || typeof value !== 'object') return;
      if (level > 40 || visited.has(value)) throw new Error('중첩 깊이 또는 순환 참조가 허용 범위를 초과했습니다.');
      visited.add(value);
      for (const child of Object.values(value)) depth(child, level + 1);
      visited.delete(value);
    }
    depth(data, 0);
    if (!specShape(data)) return { spec: null, errors: ['YAML: 정본 명세의 필수 필드와 타입을 확인하세요.'] };
    return { spec: data, errors: [] };
  } catch (error) {
    return { spec: null, errors: [`YAML: ${error instanceof Error ? error.message.slice(0, 400) : '파싱에 실패했습니다.'}`] };
  }
}

function overlay(snapshot: Snapshot, archive: Lookup, path: string, text: string): Overlay {
  const parsed = parseSpec(text);
  if (!parsed.spec) return { model: snapshot.model, spec: null, errors: parsed.errors, counts: count(snapshot.model) };
  const specs = snapshot.model.specs.filter(spec => spec.file !== path);
  const model = { ...snapshot.model, specs: [...specs, { file: path, data: parsed.spec }].sort((a, b) => a.file < b.file ? -1 : a.file > b.file ? 1 : 0) };
  const errors = [...parsed.errors];
  const segments = path.split('/');
  if (parsed.spec.service !== segments[1] || parsed.spec.screen_view !== segments[2].slice(0, -5)) errors.push('명세의 service/screen_view가 파일 경로와 다릅니다.');
  try { errors.push(...validate(model)); }
  catch { errors.push('명세 구조가 올바르지 않아 검증할 수 없습니다.'); }
  const sources = new Set(archive.documents.map(doc => doc.file));
  for (const entry of model.specs) for (const event of Array.isArray(entry.data?.events) ? entry.data.events : []) {
    if (object(event) && typeof event.source === 'string' && !sources.has(event.source)) errors.push(`${entry.file}: 원문 저장소에 없는 source ${event.source}`);
  }
  return { model, spec: parsed.spec, errors, counts: count(model) };
}

function requireText(body: Record<string, unknown>): { path: string; text: string } {
  specPath(body.path);
  if (typeof body.text !== 'string') throw new ApiError('text 문자열이 필요합니다.');
  return { path: body.path, text: body.text };
}
function proposalSafety(original: Snapshot, next: CanonicalModel): void {
  const before = new Map<string, { status: string; event: unknown }>();
  for (const file of original.model.specs) for (const event of file.data.events) before.set(event.event_label, { status: event.status, event });
  const after = new Map<string, unknown>();
  for (const file of next.specs) for (const event of file.data.events) after.set(event.event_label, event);
  for (const [label, previous] of before) {
    if (!after.has(label)) throw new ApiError(`기존 event_label을 삭제하거나 변경할 수 없습니다: ${label}`, 409);
    const current = after.get(label) as { status: string };
    if (previous.status === 'frozen' || previous.status === 'legacy') {
      if (JSON.stringify(previous.event) !== JSON.stringify(current)) throw new ApiError(`동결/레거시 계약은 수정할 수 없습니다: ${label}`, 409);
    }
    if (previous.status === 'approved' && current.status !== 'approved') throw new ApiError(`승인 계약을 강등할 수 없습니다: ${label}`, 409);
  }
}

async function route(request: Request, env: RuntimeEnv): Promise<Response> {
  if (!env.DASHBOARD_PASSWORD) return reject('DASHBOARD_PASSWORD 비밀 값이 설정되지 않았습니다.', 503);
  if (!await authorized(request, env.DASHBOARD_PASSWORD)) {
    return json({ error: '인증이 필요합니다.', recovery: 'workbench 계정의 Basic 인증을 입력하세요.' }, 401,
      { 'WWW-Authenticate': 'Basic realm="KOIN Logging Workbench", charset="UTF-8"' });
  }
  const url = new URL(request.url);
  const path = url.pathname;
  if (path.startsWith('/__repo') || path.includes('\\') || path.includes('%')) return reject('경로를 찾을 수 없습니다.', 404);
  if (request.method === 'GET' && path === '/') return response(dashboardHtml, 'text/html; charset=utf-8');
  if (request.method === 'GET' && path === '/api/catalog') {
    const data = await privateAsset(env, request, 'catalog.json');
    return response(data.body, 'application/json; charset=utf-8');
  }
  if (request.method === 'GET' && path === '/api/model') return json(await snapshot(env, request));
  if (request.method === 'GET' && path === '/api/source') {
    const id = parameter(url, 'id');
    if (!/^[a-f0-9]{32}$/.test(id)) throw new ApiError('원문 ID 형식이 올바르지 않습니다.');
    if (!(await lookup(env, request)).documents.some(doc => doc.id === id)) return reject('원문을 찾을 수 없습니다.', 404);
    return json(await privateJson(env, request, `pages/${id}.json`));
  }
  if (request.method === 'GET' && path === '/api/image') {
    const file = parameter(url, 'file');
    if (!/^assets\/[a-zA-Z0-9._-]+\.(?:png|jpe?g)$/i.test(file)) throw new ApiError('이미지 경로가 올바르지 않습니다.');
    const asset = (await lookup(env, request)).assets.find(a => a.file === file);
    if (!asset) return reject('이미지를 찾을 수 없습니다.', 404);
    const original = await privateAsset(env, request, `images/${file.slice('assets/'.length)}`);
    return response(original.body, /\.png$/i.test(file) ? 'image/png' : 'image/jpeg');
  }
  if (request.method === 'GET' && path === '/api/spec') {
    const name = parameter(url, 'path');
    specPath(name);
    const model = await snapshot(env, request);
    const file = model.files.find(f => f.path === name && model.model.specs.some(spec => spec.file === name));
    if (!file) return reject('명세 파일을 찾을 수 없습니다.', 404);
    return json({ path: name, text: file.text, sha: file.sha, commit: model.commit });
  }
  if (request.method === 'GET' && path === '/api/status') {
    const data = await snapshot(env, request);
    const repository = env.GITHUB_REPOSITORY || DEFAULT_REPOSITORY;
    if (!env.GITHUB_TOKEN) return json({ repository, snapshotCommit: data.commit, mode: 'snapshot', connected: false, message: 'GitHub 토큰 없음: 로컬 스냅샷 모드' });
    try {
      const remote = await remoteStatus(env.GITHUB_TOKEN, repository);
      return json({ repository, snapshotCommit: data.commit, mode: 'github', remoteCommit: remote.head, connected: true,
        ...(remote.head === data.commit ? {} : { message: '원격 브랜치가 변경되었습니다. 스냅샷을 새로 준비하세요.' }) });
    } catch (error) {
      return json({ repository, snapshotCommit: data.commit, mode: 'snapshot', connected: false, message: error instanceof Error ? error.message : 'GitHub 연결 실패' });
    }
  }
  if (request.method === 'POST' && ['/api/validate', '/api/generate', '/api/proposals'].includes(path)) {
    const body = await postBody(request);
    const { path: name, text } = requireText(body);
    const data = await snapshot(env, request);
    const archive = await lookup(env, request);
    if (data.snapshotHash !== archive.snapshotHash || data.commit !== archive.commit || data.repository !== archive.repository) {
      throw new ApiError('스냅샷과 원문 목록이 일치하지 않습니다. prepare를 다시 실행하세요.', 503);
    }
    const result = overlay(data, archive, name, text);
    if (path === '/api/validate') return json({ errors: result.errors, counts: result.counts, spec: result.spec });
    if (result.errors.length) throw new ApiError('명세를 검증하지 못했습니다. 오류를 수정하세요.', 422, result.errors);
    if (path === '/api/generate') {
      if (body.preview !== undefined && typeof body.preview !== 'boolean') throw new ApiError('preview는 boolean이어야 합니다.');
      const files = generate(result.model, { preview: body.preview === true });
      return json({ files, manifest: JSON.parse(files['manifest.json']) });
    }
    if (!env.GITHUB_TOKEN) throw new ApiError('GitHub 토큰이 없어 제안을 만들 수 없습니다.', 503);
    if (typeof body.title !== 'string' || !body.title.trim() || body.title.length > 120 || /[\r\n]/.test(body.title)) throw new ApiError('120자 이하의 한 줄 PR 제목이 필요합니다.');
    if (body.commit !== data.commit || !/^[a-f0-9]{40}$/.test(body.commit)) throw new ApiError('기준 커밋이 변경되었습니다. 스냅샷을 새로 불러오세요.', 409);
    const original = data.files.find(file => file.path === name);
    if (body.sha !== (original?.sha ?? '')) throw new ApiError('명세의 원본 SHA가 변경되었습니다. 명세를 새로 불러오세요.', 409);
    proposalSafety(data, result.model);
    const repository = env.GITHUB_REPOSITORY || DEFAULT_REPOSITORY;
    if (repository !== data.repository) throw new ApiError('GitHub 저장소와 스냅샷 저장소가 다릅니다.', 409);
    const generated = generate(result.model);
    return json(await createProposal({ token: env.GITHUB_TOKEN, repository, snapshotCommit: data.commit,
      expectedFiles: data.files.map(file => ({ path: file.path, sha: file.sha })),
      specPath: name, specText: text, title: body.title.trim(), generated }));
  }
  return reject('경로를 찾을 수 없습니다.', 404);
}

export default {
  async fetch(request: Request, env: RuntimeEnv): Promise<Response> {
    try { return await route(request, env); }
    catch (error) {
      if (error instanceof GithubError) return reject(error.message, error.status, error.recovery ? { recovery: error.recovery } : undefined);
      if (error instanceof ApiError) return reject(error.message, error.status, error.errors ? { errors: error.errors } : undefined);
      console.error(JSON.stringify({ message: 'workbench request failed', path: new URL(request.url).pathname, error: error instanceof Error ? error.message : String(error) }));
      return reject('요청을 처리하지 못했습니다. 잠시 후 다시 시도하세요.', 500);
    }
  },
} satisfies ExportedHandler<RuntimeEnv>;
