import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { parseDocument } from 'yaml';

const snake = /^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$/;
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const text = x => typeof x === 'string' && x.trim().length > 0;
const own = (x, key) => Object.hasOwn(x, key);
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
export function validate({ specs, vocabulary: v, envelope }) {
  const errors = [], labels = new Set();
  const fail = (where, msg) => errors.push(`${where}: ${msg}`);
  const allowed = (x, keys, where) => {
    if (object(x)) for (const key of Object.keys(x)) if (!keys.includes(key)) fail(where, `알 수 없는 필드 ${key}`);
  };
  const descriptor = (x, where) => {
    if (!object(x)) { fail(where, '타입 정의 필요'); return; }
    allowed(x, ['type', 'description', 'required', 'enum', 'const'], where);
    if (!['string', 'number', 'boolean'].includes(x.type)) fail(where, 'type은 string/number/boolean');
    if (!text(x.description)) fail(where, 'description 필요');
    if (typeof x.required !== 'boolean') fail(where, 'required는 boolean');
    if (own(x, 'const') && own(x, 'enum')) fail(where, 'const와 enum 동시 사용 불가');
    if (own(x, 'enum') && (!Array.isArray(x.enum) || !x.enum.length)) fail(where, '빈 enum 불가');
    const values = own(x, 'const') ? [x.const] : (Array.isArray(x.enum) ? x.enum : []);
    if (values.some(n => typeof n !== x.type || (x.type === 'number' && !Number.isFinite(n)))) fail(where, '허용 값의 타입 불일치');
    if (new Set(values).size !== values.length) fail(where, 'enum 중복');
  };
  if (!Array.isArray(v.categories) || !object(v.services) || !Array.isArray(v.platforms) || !Array.isArray(envelope.reserved_keys)) throw new Error('규칙 파일 구조 오류');
  for (const { file, data: d } of specs) {
    if (!object(d)) { fail(file, '명세는 객체'); continue; }
    allowed(d, ['schema_version', 'service', 'screen_view', 'events'], file);
    if (d.schema_version !== 1) fail(file, 'schema_version은 1');
    if (!own(v.services, d.service)) fail(file, '등록되지 않은 service');
    if (!snake.test(d.screen_view)) fail(file, 'screen_view는 snake_case');
    if (!Array.isArray(d.events) || !d.events.length) { fail(file, 'events 필요'); continue; }
    for (const e of d.events) {
      const where = `${file} / ${e?.event_label ?? '?'}`;
      if (!object(e)) { fail(where, 'event는 객체'); continue; }
      allowed(e, ['description','event_name','event_label','event_category','value','params','platforms','status','source','decision','notes','platform_support'], where);
      if (!text(e.description)) fail(where, '발생 조건 description 필요');
      if (!['approved','draft','legacy','frozen'].includes(e.status)) fail(where, 'status 필요');
      if (!text(e.source) || !/^https:\/\//.test(e.source)) fail(where, '원문 source URL 필요');
      if (own(e, 'decision') && !text(e.decision)) fail(where, 'decision은 문자열');
      const segments = typeof e.event_label === 'string' ? e.event_label.split('__') : [];
      if (![4,5].includes(segments.length) || segments.some(s => !snake.test(s))) fail(where, 'label은 snake_case 4~5구간');
      if (segments[0] !== d.service || segments[1] !== d.screen_view) fail(where, 'label의 service/screen_view 불일치');
      if (!v.categories.includes(e.event_category) || segments.at(-1) !== e.event_category) fail(where, 'category 또는 label 접미 불일치');
      const override = v.screen_overrides?.find(o => o.service === d.service && o.screen_view === d.screen_view);
      if (e.event_name !== (override?.event_name ?? v.services[d.service])) fail(where, '서비스/화면의 DA 배정 불일치');
      if (labels.has(e.event_label)) fail(where, '중복 event_label');
      labels.add(e.event_label);
      if (!Array.isArray(e.platforms) || !e.platforms.length || e.platforms.some(p => !v.platforms.includes(p)) || new Set(e.platforms).size !== e.platforms.length) fail(where, 'platforms는 등록된 값의 중복 없는 목록');
      if (!object(e.platform_support)) fail(where, 'platform_support 필요');
      else {
        for (const p of v.platforms) {
          const support=e.platform_support[p];
          if (!object(support) || !['confirmed','unsupported','unknown'].includes(support.state) || !text(support.evidence)) fail(where, '플랫폼 상태와 근거 필요: '+p);
        }
        for (const p of Object.keys(e.platform_support)) if (!v.platforms.includes(p)) fail(where,'미등록 플랫폼: '+p);
        for (const p of Array.isArray(e.platforms)?e.platforms:[]) if (e.platform_support[p]?.state!=='confirmed') fail(where,'생성 플랫폼의 지원 확인 필요: '+p);
      }
      descriptor(e.value, `${where}.value`);
      if (!object(e.params)) { fail(where, 'params는 객체'); continue; }
      for (const [key, spec] of Object.entries(e.params)) {
        if (!snake.test(key) || envelope.reserved_keys.includes(key)) fail(where, `예약 키 또는 잘못된 params 키 ${key}`);
        descriptor(spec, `${where}.params.${key}`);
      }
    }
  }
  return errors;
}
export function events(model, preview = false) {
  return model.specs.flatMap(({ data: d }) => d.events.map(e => ({ ...e, service: d.service, screen_view: d.screen_view })))
    .filter(e => e.status === 'approved' || (preview && e.status === 'draft'))
    .sort((a,b) => a.event_label.localeCompare(b.event_label, 'en'));
}
const q = JSON.stringify;
const kt = s => q(s).replaceAll('$', '\\$');
const ktLiteral = x => typeof x === 'string' ? kt(x) : typeof x === 'number' ? String(x) + (Number.isInteger(x) ? '.0' : '') : String(x);
const fields = e => Object.entries({ value: e.value, ...e.params }).filter(([,d]) => !own(d,'const'));
const tsType = d => d.enum ? d.enum.map(q).join(' | ') : d.type;
const ktType = d => ({string:'String',number:'Double',boolean:'Boolean'})[d.type];
export function generate(model, { preview = false } = {}) {
  const all = events(model, preview);
  const revision = createHash('sha256').update(JSON.stringify(model)).digest('hex');
  const header = `// Generated by koin-log. DO NOT EDIT.\n// schema-sha256: ${revision}\n// ${preview ? 'PREVIEW: draft contracts included; do not integrate into production.' : 'Approved contracts only; SDK delivery is not verified.'}\n`;
  const web = all.filter(e => e.platforms.some(p => p.startsWith('WEB') && e.platform_support?.[p]?.state === 'confirmed'));
  let ts = header + 'export type EventArgs = {\n';
  for (const e of web) ts += `  ${q(e.event_label)}: ${fields(e).length ? `{ ${fields(e).map(([k,d]) => `${q(k)}${d.required?'':'?'}: ${tsType(d)}`).join('; ')} }` : 'Record<string, never>'};\n`;
  ts += '};\nexport const contracts = ' + q(Object.fromEntries(web.map(e => [e.event_label, {event_name:e.event_name,screen_view:e.screen_view,event_category:e.event_category,value:e.value,params:e.params,platforms:e.platforms}]))) + ' as const;\n';
  ts += `type Descriptor = { type: string; required: boolean; enum?: readonly unknown[]; const?: unknown };\nfunction validateArgs(spec: Record<string, Descriptor>, args: Record<string, unknown>) {\n  for (const key of Object.keys(args)) if (!Object.hasOwn(spec, key) || Object.hasOwn(spec[key], 'const')) throw new Error('Unexpected argument: ' + key);\n  for (const [key, d] of Object.entries(spec)) {\n    if (Object.hasOwn(d, 'const')) continue;\n    const value = args[key];\n    if (value === undefined && !d.required) continue;\n    if (typeof value !== d.type || (d.type === 'number' && !Number.isFinite(value)) || (d.enum && !d.enum.includes(value))) throw new Error('Invalid argument: ' + key);\n  }\n}\nexport function createEvent<L extends keyof EventArgs>(label: L, args: EventArgs[L]) {\n  if (!Object.hasOwn(contracts, label)) throw new Error('Unknown label: ' + String(label));\n  const c = (contracts as Record<string, {event_name:string;screen_view:string;event_category:string;value:Descriptor;params:Record<string,Descriptor>} >)[label];\n  validateArgs({value:c.value, ...c.params}, args as Record<string, unknown>);\n  const supplied = args as Record<string, unknown>;\n  const payload: Record<string, string | number | boolean> = {event_label:label,event_category:c.event_category,screen_view:c.screen_view};\n  for (const [key, d] of Object.entries({value:c.value,...c.params})) {\n    const value = Object.hasOwn(d,'const') ? d.const : supplied[key];\n    if (value !== undefined) payload[key] = value as string | number | boolean;\n  }\n  return {event_name:c.event_name, params:payload};\n}\n`;
  const android = all.filter(e => e.platforms.includes('ANDROID') && e.platform_support?.ANDROID?.state === 'confirmed');
  let kotlin = header + 'package `in`.koreatech.koin.logging.generated\n\nsealed interface KoinEvent {\n    val eventName: String\n    val params: Map<String, Any>\n}\n\n';
  for (const e of android) {
    // Underscores are preserved so distinct labels never collapse to one class name.
    const name = `Event_${e.event_label}`;
    const f = fields(e);
    kotlin += `class ${name}(${f.map(([k,d])=>`private val \`${k}\`: ${ktType(d)}${d.required?'':'? = null'}`).join(', ')}) : KoinEvent {\n`;
    if (f.length) {
      kotlin += '    init {\n';
      for (const [k,d] of f) {
        const ref = `\`${k}\``;
        if (d.type === 'number') kotlin += `        require(${d.required?'':`${ref} == null || `}${ref}.isFinite())\n`;
        if (d.enum) kotlin += `        require(${d.required?'':`${ref} == null || `}${ref} in listOf(${d.enum.map(ktLiteral).join(', ')}))\n`;
      }
      kotlin += '    }\n';
    }
    kotlin += `    override val eventName: String = ${kt(e.event_name)}\n    override val params: Map<String, Any> get() = buildMap {\n        put("event_label", ${kt(e.event_label)})\n        put("event_category", ${kt(e.event_category)})\n        put("screen_view", ${kt(e.screen_view)})\n`;
    for (const [k,d] of Object.entries({value:e.value,...e.params})) {
      if (own(d,'const')) kotlin += `        put(${kt(k)}, ${typeof d.const==='string'?kt(d.const):typeof d.const==='number'?String(d.const)+(Number.isInteger(d.const)?'.0':''):String(d.const)})\n`;
      else if (d.required) kotlin += `        put(${kt(k)}, \`${k}\`)\n`;
      else kotlin += `        \`${k}\`?.let { put(${kt(k)}, it) }\n`;
    }
    kotlin += '    }\n}\n\n';
  }
  const mdEscape = s => String(s).replaceAll('|','\\|').replaceAll('\n',' ');
  let md = `# 로깅 명세 목록\n\n자동 생성. ${preview?'초안 포함 미리보기':'approved 계약만 포함'}. 앱 적용·배포·실수집 검증 완료를 뜻하지 않는다.\n\n| event_label | event_name | screen_view | 발생 조건 | 플랫폼 | 원문 |\n| --- | --- | --- | --- | --- | --- |\n`;
  md += all.map(e=>`| ${e.event_label} | ${e.event_name} | ${e.screen_view} | ${mdEscape(e.description)} | ${e.platforms.join(', ')} | [원문](${e.source}) |`).join('\n')+'\n';
  return { 'logging.ts': ts, 'KoinEvents.kt': kotlin, 'catalog.md': md, 'manifest.json': JSON.stringify({schema_version:1,revision,preview,event_count:all.length,web_count:web.length,android_count:android.length},null,2)+'\n' };
}
