export const dashboardHtml = String.raw`<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>KOIN 로깅 계약 작업실</title>
<style>
:root{font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;color:#18263a;background:#f1f5fa;font-synthesis:none}*{box-sizing:border-box}body{margin:0}button,input,select,textarea{font:inherit}button{cursor:pointer}button:disabled{cursor:not-allowed;opacity:.55}a{color:#135baa;overflow-wrap:anywhere}h1,h2,h3,p{margin-top:0}h1{font-size:1.5rem;margin-bottom:0}h2{font-size:1.13rem}h3{font-size:1rem}small,.muted{color:#56677e}code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}.shell{max-width:1900px;margin:auto;padding:22px}.top{display:flex;gap:18px;align-items:center;justify-content:space-between;margin-bottom:16px}.brand{display:flex;align-items:center;gap:13px}.mark{display:grid;place-items:center;background:#1258a8;color:white;border-radius:13px;width:43px;height:43px;font-weight:800}.eyebrow{color:#4475a9;text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:800;margin-bottom:4px}.panel{background:white;border:1px solid #dce5ef;border-radius:16px;box-shadow:0 4px 18px #1f3f6609;padding:18px;min-width:0}.layout{display:grid;grid-template-columns:minmax(230px,290px) minmax(420px,1fr) minmax(330px,390px);gap:15px;align-items:start}.stack{display:grid;gap:15px;min-width:0}.row{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}.wrap{display:flex;flex-wrap:wrap;gap:8px}.button{background:#fff;color:#173755;border:1px solid #b8cadd;border-radius:8px;padding:8px 11px;font-weight:650}.button:hover:not(:disabled){background:#edf4fc}.button.primary{background:#135baa;color:white;border-color:#135baa}.button.primary:hover:not(:disabled){background:#104a8a}.button.danger{color:#a3302d}.field{display:grid;gap:5px;margin:10px 0}.field label{font-size:.85rem;font-weight:700}.field input,.field select,.field textarea,textarea{width:100%;border:1px solid #b7c8d9;border-radius:8px;padding:9px;background:white;color:#18263a}.field input:focus,.field select:focus,.field textarea:focus,textarea:focus{outline:2px solid #86b7ed}.hint{font-size:.84rem;line-height:1.5;color:#536680}.status{border-radius:9px;background:#eaf2fb;padding:10px 13px;line-height:1.45;white-space:pre-wrap;overflow-wrap:anywhere}.status[data-tone="error"]{background:#fff0ee;color:#842b26}.status[data-tone="success"]{background:#e6f6ed;color:#16603d}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:15px}.stat{background:#eaf2fb;padding:9px 12px;border-radius:9px;font-size:.85rem}.stat strong{display:block;font-size:1.2rem}.list{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:5px;max-height:490px;overflow:auto}.list button{width:100%;text-align:left;padding:9px;border:1px solid #dae5ef;border-radius:8px;background:white;overflow-wrap:anywhere}.list button[aria-current="true"]{border-color:#135baa;background:#eaf3ff}.list small{display:block;margin-top:3px}.divider{border:0;border-top:1px solid #dce5ef;margin:17px 0}.source-markdown{white-space:pre-wrap;overflow-wrap:anywhere;max-height:510px;overflow:auto;border:1px solid #dce5ef;background:#f9fbfe;padding:14px;border-radius:9px;font-size:.83rem;line-height:1.55}.properties{white-space:pre-wrap;max-height:190px;overflow:auto;background:#f7f9fc;border-radius:8px;padding:10px;font-size:.8rem}.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:9px;max-height:320px;overflow:auto}.thumb{border:1px solid #d3e1ed;border-radius:9px;background:white;padding:6px;text-align:left;min-width:0}.thumb[aria-pressed="true"]{border:2px solid #135baa;background:#eaf3ff}.thumb img{width:100%;height:90px;object-fit:contain;background:#f5f7fa}.thumb small{display:block;overflow-wrap:anywhere}.card{border:1px solid #dce5ef;border-radius:10px;padding:12px;margin:9px 0;background:#fbfdff}.badge{display:inline-block;font-size:.75rem;font-weight:750;padding:3px 8px;border-radius:20px;background:#e6eef8;color:#173e65}.badge[data-status="draft"],.badge[data-status="unknown"]{background:#fff1d8;color:#805309}.badge[data-status="legacy"],.badge[data-status="frozen"],.badge[data-status="unsupported"]{background:#f0e8ea;color:#713c48}.badge[data-status="approved"],.badge[data-status="confirmed"]{background:#e6f5eb;color:#16603d}.platform-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px;margin-top:10px}.platform{background:#f0f4f9;padding:8px;border-radius:7px;font-size:.76rem;overflow-wrap:anywhere}.platform .badge{margin-left:3px}.platform p{margin:5px 0 0;white-space:pre-wrap}.yaml{min-height:340px;resize:vertical;font-size:.82rem;line-height:1.55;tab-size:2}.code{white-space:pre-wrap;overflow:auto;max-height:270px;background:#f5f8fc;border-radius:8px;padding:12px;font-size:.76rem}.messages{list-style:none;padding:0}.messages li{margin:6px 0;background:#fff0ee;border-radius:6px;padding:8px;overflow-wrap:anywhere}.messages li.ok{background:#e6f6ed}.canvas-frame{border:1px solid #dce5ef;background:#eff3f7;overflow:auto;max-height:570px;text-align:center;border-radius:8px}.canvas-frame canvas{display:block;max-width:100%;height:auto;margin:auto;touch-action:none;cursor:crosshair}.coords{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}.coords input{width:100%}.annotation-list{list-style:none;padding:0;max-height:190px;overflow:auto}.annotation-list li{padding:6px;border-bottom:1px solid #e4ebf2}.annotation-list button{border:0;background:none;text-align:left;color:#135baa}.caption{font-size:.79rem;color:#576b84;overflow-wrap:anywhere}.policy{max-height:180px;overflow:auto}.link-line{display:block;margin:8px 0}.hidden,[hidden]{display:none!important}@media(max-width:1250px){.layout{grid-template-columns:minmax(220px,300px) minmax(0,1fr)}.right{grid-column:2}}@media(max-width:760px){.shell{padding:10px}.top{align-items:flex-start;flex-direction:column}.layout{display:block}.layout>*{margin-bottom:12px}.list{max-height:250px}.platform-grid{grid-template-columns:1fr}}
html{overflow-wrap:anywhere}
</style></head><body><div class="shell">
<header class="top"><div class="brand"><div class="mark" aria-hidden="true">K</div><div><p class="eyebrow">KOIN · SOURCE TO CONTRACT</p><h1>로깅 계약 작업실</h1></div></div><button type="button" class="button" id="reload">스냅샷 다시 읽기</button></header>
<div id="notice" class="status" role="status" aria-live="polite">저장소 스냅샷을 불러오는 중…</div><p id="provenance" class="hint"></p>
<div class="stats"><div class="stat">원문 문서 <strong id="n-docs">—</strong></div><div class="stat">참고 이미지 <strong id="n-images">—</strong></div><div class="stat">정본 YAML <strong id="n-specs">—</strong></div><div class="stat">approved 파일럿 이벤트 <strong id="n-approved">—</strong></div><div class="stat">draft <strong id="n-draft">—</strong></div><div class="stat">legacy / frozen <strong id="n-history">—</strong></div></div>
<div class="layout"><aside class="stack">
<section class="panel"><h2>원문 전체 검색</h2><div class="field"><label for="search">제목 · 경로 · 원문 내용</label><input id="search" type="search" autocomplete="off" placeholder="원문 검색"></div><p id="search-count" class="hint"></p><ul id="sources" class="list"></ul><button id="more" type="button" class="button" hidden>결과 더 보기</button></section>
<section class="panel"><h2>정본 화면 계약</h2><p class="hint">원문 아카이브와 별개의 승인된 파일럿 계약입니다. 원문 발견만으로 승인하지 않습니다.</p><ul id="specs" class="list"></ul><hr class="divider"><h3>새 화면 초안</h3><p class="hint">기존 승인 계약은 복제하지 않습니다. 신규 이벤트의 필수 필드는 YAML에서 직접 작성하고 검사를 통과해야 합니다.</p><form id="new-form"><div class="field"><label for="new-service">서비스 (등록된 값)</label><select id="new-service" required></select></div><div class="field"><label for="new-screen">화면 screen_view</label><input id="new-screen" required pattern="[a-z][a-z0-9]*(?:_[a-z0-9]+)*" placeholder="screen_name" autocomplete="off"></div><div class="field"><label for="new-source">원문 ID (선택한 문서 또는 직접 입력)</label><input id="new-source" required pattern="[a-f0-9]{32}" maxlength="32" autocomplete="off"></div><button type="submit" class="button">빈 draft 계약 시작</button></form></section>
</aside><main class="stack">
<section class="panel"><div class="row"><div><p class="eyebrow">ARCHIVED SOURCE · NOT APPROVAL</p><h2 id="source-title">원문을 선택하세요</h2></div><a id="source-link" class="link-line" target="_blank" rel="noopener noreferrer" hidden>커밋의 원문 보기 ↗</a></div><p id="source-meta" class="hint">목록의 문서는 원문 스냅샷입니다.</p><div id="source-contracts" class="wrap"></div><details><summary>원문 속성 · 출처</summary><pre id="properties" class="properties"></pre></details><h3>보존된 Markdown 원문</h3><pre id="markdown" class="source-markdown">원문을 선택하면 이곳에 실제 Markdown이 표시됩니다. HTML로 해석하지 않습니다.</pre><div class="row"><h3>원문 참조 이미지</h3><span id="image-count" class="hint"></span></div><p class="hint">이미지는 원문 참고 자료이며 플랫폼 지원이나 최신 native 캡처를 입증하지 않습니다.</p><div id="gallery" class="gallery"></div></section>
<section class="panel"><p class="eyebrow">CANONICAL YAML</p><h2 id="spec-title">정본 계약을 선택하세요</h2><p id="spec-meta" class="hint">원본 파일과 Git SHA를 확인한 뒤 편집합니다.</p><div class="field"><label for="yaml">원본 YAML (모든 필드 직접 편집)</label><textarea id="yaml" class="yaml mono" spellcheck="false" autocomplete="off" disabled></textarea></div><div class="wrap"><button id="validate" type="button" class="button primary" disabled>전체 모델 검사</button><button id="yaml-download" type="button" class="button" disabled>YAML 내려받기</button><button id="reset" type="button" class="button" disabled>원본으로 되돌리기</button></div><p id="dirty" class="hint"></p><ul id="diagnostics" class="messages" aria-live="polite"></ul><div id="events"></div></section>
<section class="panel"><h2>생성 결과</h2><p class="hint">기본은 approved 계약만 포함합니다. draft 포함은 명시적인 미리보기이며 생산 환경에 통합하면 안 됩니다. 생성은 SDK 배포·실수집 확인이 아닙니다.</p><label><input id="preview" type="checkbox"> draft 포함 미리보기 (PREVIEW)</label><div class="wrap"><button id="generate" type="button" class="button primary" disabled>정본에서 생성</button><select id="generated-file" aria-label="생성 파일" disabled></select><button id="generated-download" type="button" class="button" disabled>선택 파일 내려받기</button></div><p id="generated-meta" class="hint"></p><pre id="generated-text" class="code" hidden></pre></section>
</main><aside class="stack right">
<section class="panel"><h2>원본 픽셀 이미지 주석</h2><p class="hint">원문 이미지를 선택해 드래그하거나 정수 좌표를 입력하세요. 주석은 정본 YAML에 들어가지 않으며 JSON sidecar와 PNG만 내려받습니다.</p><p id="image-meta" class="caption">원문 이미지를 선택하세요.</p><div class="canvas-frame"><canvas id="canvas" hidden aria-label="원본 픽셀 주석 이미지"></canvas><p id="image-placeholder" class="hint">이미지 없음</p></div><div class="field"><label for="annotation-label">주석 이름 (설명)</label><input id="annotation-label" autocomplete="off" placeholder="사용자가 입력할 설명"></div><div class="coords"><div class="field"><label for="rect-x">x</label><input id="rect-x" type="number" min="0" step="1"></div><div class="field"><label for="rect-y">y</label><input id="rect-y" type="number" min="0" step="1"></div><div class="field"><label for="rect-w">폭</label><input id="rect-w" type="number" min="1" step="1"></div><div class="field"><label for="rect-h">높이</label><input id="rect-h" type="number" min="1" step="1"></div></div><div class="wrap"><button id="save-rect" type="button" class="button" disabled>사각형 저장</button><button id="delete-rect" type="button" class="button danger" disabled>선택 주석 삭제</button></div><ul id="annotation-list" class="annotation-list"></ul><div class="wrap"><button id="annotation-png" type="button" class="button" disabled>주석 PNG</button><button id="annotation-json" type="button" class="button" disabled>JSON sidecar</button></div><p class="hint">다운로드 파일은 개인 작업 결과입니다. 서버 제안에 업로드되지 않습니다.</p></section>
<section class="panel"><h2>읽기 전용 정책</h2><p class="hint">서버 검사는 아래 정본 JSON 규칙과 전체 모델을 사용합니다. 이 화면에서는 정책을 변경하지 않습니다.</p><details><summary>vocabulary.json</summary><pre id="vocabulary" class="code policy"></pre></details><details><summary>envelope.json</summary><pre id="envelope" class="code policy"></pre></details></section>
<section class="panel"><h2>저장소 변경 제안</h2><p id="proposal-mode" class="hint">원격 연결을 확인하고 있습니다.</p><div class="field"><label for="pr-title">PR 제목</label><input id="pr-title" maxlength="120" autocomplete="off" placeholder="화면 로깅 계약 변경"></div><button id="propose" type="button" class="button primary" disabled>검사 후 제안 PR 만들기</button><p class="hint">제안 전에 경로, 기준 커밋, 기대 SHA, 변경된 YAML, 생성 범위를 다시 확인합니다. 서버는 원격 충돌을 검사하며 토큰은 브라우저로 보내지 않습니다.</p><a id="proposal-link" class="link-line" target="_blank" rel="noopener noreferrer" hidden></a><p id="proposal-message" class="status" role="status" aria-live="polite"></p></section>
</aside></div></div>
<script>(function(){'use strict';
const $ = id => document.getElementById(id);
const ui = Object.fromEntries(['notice','provenance','reload','n-docs','n-images','n-specs','n-approved','n-draft','n-history','search','search-count','sources','more','specs','new-form','new-service','new-screen','new-source','source-title','source-link','source-meta','source-contracts','properties','markdown','image-count','gallery','spec-title','spec-meta','yaml','validate','yaml-download','reset','dirty','diagnostics','events','preview','generate','generated-file','generated-download','generated-meta','generated-text','image-meta','canvas','image-placeholder','annotation-label','rect-x','rect-y','rect-w','rect-h','save-rect','delete-rect','annotation-list','annotation-png','annotation-json','vocabulary','envelope','proposal-mode','pr-title','propose','proposal-link','proposal-message'].map(id=>[id,$(id)]));
const state={catalog:null,model:null,status:null,source:null,sourceId:'',sourceSeq:0,sourceLimit:60,specPath:'',specText:'',original:'',sha:'',specSeq:0,revision:0,validated:-1,parsedSpec:null,generated:null,generatedRevision:-1,busy:false,image:null,imageFile:'',imageUrl:'',imageSeq:0,annotations:new Map(),selectedRect:-1,drag:null,proposalKey:''};
const imageMaxPixels=40000000, imageMaxAxis=16000;
function notify(text,tone){ui.notice.textContent=text;ui.notice.dataset.tone=tone||''}
function proposalMessage(text,tone){ui['proposal-message'].textContent=text;ui['proposal-message'].dataset.tone=tone||''}
function explain(error){
  let text=error instanceof Error?error.message:'요청에 실패했습니다.';
  if(Array.isArray(error?.errors)&&error.errors.length)text+='\n'+error.errors.join('\n');
  if(typeof error?.recovery==='string')text+='\n복구: '+error.recovery;
  else if(typeof error?.recovery?.message==='string')text+='\n복구: '+error.recovery.message;
  return text;
}
async function api(url,body){
  let response;
  try{
    response=await fetch(url,{method:body===undefined?'GET':'POST',credentials:'same-origin',headers:body===undefined?{Accept:'application/json'}:{Accept:'application/json','Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),cache:'no-store'});
  }catch{throw Error('서버에 연결할 수 없습니다. 네트워크를 확인하고 다시 시도하세요.')}
  let data;
  try{data=await response.json()}
  catch{throw Error('서버 응답을 읽을 수 없습니다 ('+response.status+'). 연결을 확인하세요.')}
  if(!response.ok){
    const error=Error(data&&typeof data.error==='string'?data.error:'요청 실패 ('+response.status+')');
    error.recovery=data?.recovery;
    error.errors=data?.errors;
    throw error;
  }
  return data;
}
const post=(url,body)=>api(url,body);
function node(tag,text,className){const el=document.createElement(tag);el.textContent=String(text??'');if(className)el.className=className;return el}
function badge(value){const el=node('span',value||'미확인','badge');el.dataset.status=value||'unknown';return el}
function githubFile(path){if(!state.catalog||!state.catalog.commit)return '';const repository=String(state.catalog.repository||'');if(!/^[\w.-]+\/[\w.-]+$/.test(repository)||!/^[a-f0-9]{40}$/.test(state.catalog.commit))return '';return 'https://github.com/'+repository+'/blob/'+state.catalog.commit+'/'+path.split('/').map(encodeURIComponent).join('/')}
function githubLink(el,url,label){el.hidden=true;el.removeAttribute('href');el.textContent='';try{const u=new URL(url);if(u.protocol==='https:'&&u.hostname==='github.com'&&!u.username&&!u.password){el.href=u.href;el.textContent=label;el.hidden=false}}catch{}}
function count(value){return Number.isInteger(value)?value.toLocaleString('ko-KR'):'—'}
function renderCounts(){const c=state.catalog&&state.catalog.counts||{},m=state.model&&state.model.model;ui['n-docs'].textContent=count(c.documents??state.catalog?.documents?.length);ui['n-images'].textContent=count(c.images??state.catalog?.assets?.length);ui['n-specs'].textContent=count(c.specFiles??m?.specs?.length);let events=(m?.specs||[]).flatMap(s=>Array.isArray(s.data?.events)?s.data.events:[]);const statuses={approved:0,draft:0,legacy:0,frozen:0};for(const event of events)if(Object.hasOwn(statuses,event.status))statuses[event.status]++;ui['n-approved'].textContent=count(statuses.approved);ui['n-draft'].textContent=count(statuses.draft);ui['n-history'].textContent=count(statuses.legacy)+' / '+count(statuses.frozen);const commit=state.catalog?.commit||state.model?.commit||'';ui.provenance.textContent=state.catalog?'원문·정본 기준: '+state.catalog.repository+' @ '+commit+' · snapshot SHA-256 '+(state.catalog.snapshotHash||'미확인')+' · 원문과 계약은 서로 다른 자료입니다.':''}
function renderMode(){let s=state.status;ui['proposal-mode'].textContent=!s?'원격 연결 미확인':s.connected?'원격 '+s.repository+' · 기준 '+(s.snapshotCommit||'미확인')+' · 제안 시 최신 HEAD와 다시 대조합니다.':'읽기·검사·생성 가능 (로컬 스냅샷). '+(s.message||'GitHub 제안 연결이 없어 PR은 만들 수 없습니다.');updateActions()}
function dirty(){return !!state.specPath&&(state.sha?state.specText!==state.original:true)}
function discard(){return !dirty()||window.confirm('저장하지 않은 YAML 편집 내용이 사라집니다. 계속하시겠습니까?')}
function updateActions(){
  const active=!!state.specPath&&!state.busy;
  ui.yaml.disabled=!active;
  ui.validate.disabled=!active;
  ui['yaml-download'].disabled=!state.specPath;
  ui.reset.disabled=!active||(!state.sha&&!state.specText)||(!dirty()&&!!state.sha);
  ui.generate.disabled=!active;
  ui['generated-file'].disabled=!state.generated||state.generatedRevision!==state.revision;
  ui['generated-download'].disabled=ui['generated-file'].disabled;
  ui.propose.disabled=!active||!dirty()||!state.status?.connected||!state.model||!ui['pr-title'].value.trim()||state.proposalKey===proposalKey();
  ui.reload.disabled=state.busy;
  ui['new-form'].querySelector('button').disabled=state.busy;
  ui['save-rect'].disabled=!state.image;
  ui['delete-rect'].disabled=!state.image||state.selectedRect<0;
  ui['annotation-png'].disabled=!state.image;
  ui['annotation-json'].disabled=!state.image;
  ui.dirty.textContent=!state.specPath?'':dirty()?'● 저장하지 않은 YAML 변경이 있습니다. 다운로드하거나 검사 후 제안하세요.':'원본 YAML과 일치합니다.';
}
function invalidate(){state.revision++;state.validated=-1;state.parsedSpec=null;state.generated=null;state.generatedRevision=-1;ui.diagnostics.replaceChildren();ui['generated-text'].hidden=true;ui['generated-meta'].textContent='편집 내용이 바뀌었습니다. 다시 생성하세요.';ui['generated-file'].replaceChildren();renderEvents();updateActions()}
function renderSources(){ui.sources.replaceChildren();if(!state.catalog)return;const query=ui.search.value.trim().toLocaleLowerCase('ko');const docs=state.catalog.documents.filter(d=>(String(d.title||'')+' '+String(d.path||'')+' '+String(d.searchText||'')).toLocaleLowerCase('ko').includes(query));ui['search-count'].textContent=count(docs.length)+' / '+count(state.catalog.documents.length)+'개 원문 검색 결과';for(const d of docs.slice(0,state.sourceLimit)){const li=node('li',''),button=node('button',d.title||d.id);button.type='button';button.setAttribute('aria-current',String(state.sourceId===d.id));button.appendChild(node('small',d.path||d.file));button.addEventListener('click',()=>selectSource(d.id));li.appendChild(button);ui.sources.appendChild(li)}ui.more.hidden=docs.length<=state.sourceLimit}
function renderSpecs(){ui.specs.replaceChildren();for(const entry of state.model?.model?.specs||[]){const d=entry.data||{};const li=node('li',''),b=node('button',entry.file);b.type='button';b.setAttribute('aria-current',String(state.specPath===entry.file));b.appendChild(node('small',String(d.service||'')+' / '+String(d.screen_view||'')+' · '+(Array.isArray(d.events)?d.events.length:0)+' 이벤트'));b.addEventListener('click',()=>selectSpec(entry.file));li.appendChild(b);ui.specs.appendChild(li)}const services=Object.keys(state.model?.model?.vocabulary?.services||{});ui['new-service'].replaceChildren(...services.map(value=>{const option=node('option',value);option.value=value;return option}));ui['new-form'].querySelector('button').disabled=!services.length}
function assetFor(file){return state.catalog?.assets?.find(a=>a.file===file)}
function imageUrl(file){return '/api/image?file='+encodeURIComponent(file)}
async function selectSource(id){
  const d=state.catalog?.documents?.find(item=>item.id===id);
  if(!d)return;
  const seq=++state.sourceSeq;
  state.sourceId=id;
  state.source=null;
  ++state.imageSeq;
  if(state.imageUrl)URL.revokeObjectURL(state.imageUrl);
  state.imageUrl='';
  state.imageFile='';
  disableImage('이 원문의 이미지를 선택하세요.');
  ui['source-title'].textContent='원문을 불러오는 중…';
  ui['source-meta'].textContent='원문 ID '+id+' · 읽는 중…';
  ui['source-contracts'].replaceChildren();
  ui.markdown.textContent='';
  ui.gallery.replaceChildren();
  ui['source-link'].hidden=true;
  renderSources();
  try{
    const page=await api('/api/source?id='+encodeURIComponent(id));
    if(seq!==state.sourceSeq)return;
    if(page.id!==id||typeof page.markdown!=='string')throw Error('원문 응답이 요청한 문서와 일치하지 않습니다.');
    state.source=page;
    ui['source-title'].textContent=page.title||d.title;
    ui['source-meta'].textContent='원문 ID '+id+' · '+(page.path||d.path||'상위 경로 없음')+' · '+(page.imageFiles||[]).length+'개 이미지 · 기준 커밋 '+state.catalog.commit+' · Markdown SHA-256 계산 중…';
    ui.properties.textContent=JSON.stringify({id:page.id,file:d.file,path:page.path,properties:page.properties},null,2);
    const links=Array.isArray(page.pilotSpecPaths)?page.pilotSpecPaths:[];
    if(links.length){
      ui['source-contracts'].appendChild(node('span','이 원문을 인용한 파일럿 정본: ','hint'));
      for(const path of links){
        if(!state.model?.files?.some(file=>file.path===path))continue;
        const button=node('button',path,'button');
        button.type='button';
        button.addEventListener('click',()=>selectSpec(path));
        ui['source-contracts'].appendChild(button);
      }
    }else ui['source-contracts'].appendChild(node('span','이 원문을 인용한 파일럿 정본 없음 · 승인 상태를 추정하지 마세요.','hint'));
    ui.markdown.textContent=page.markdown;
    githubLink(ui['source-link'],githubFile(d.file.startsWith('notion/')?d.file:'notion/'+d.file),'이 커밋의 Markdown 원문 ↗');
    renderGallery();
    ui['new-source'].value=id;
    notify('원문을 열었습니다. 아카이브 원문은 승인 계약과 구분하세요.','success');
    const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(page.markdown));
    if(seq===state.sourceSeq)ui['source-meta'].textContent='원문 ID '+id+' · '+(page.path||d.path||'상위 경로 없음')+' · '+(page.imageFiles||[]).length+'개 이미지 · 기준 커밋 '+state.catalog.commit+' · Markdown SHA-256 '+Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,'0')).join('');
  }catch(error){
    if(seq!==state.sourceSeq)return;
    if(state.source){ui['source-meta'].textContent+=' · Markdown SHA-256 계산 불가';return}
    state.source=null;
    ui['source-title'].textContent='원문 읽기 실패';
    ui.markdown.textContent=explain(error);
    notify('원문 읽기 실패: '+explain(error),'error');
  }
}
function renderGallery(){ui.gallery.replaceChildren();const files=Array.isArray(state.source?.imageFiles)?state.source.imageFiles:[];ui['image-count'].textContent=files.length+'개 참조';for(const file of files){const asset=assetFor(file);if(!asset)continue;const button=node('button','', 'thumb');button.type='button';button.setAttribute('aria-pressed',String(state.imageFile===file));const img=document.createElement('img');img.src=imageUrl(file);img.loading='lazy';img.alt='원문 참고 이미지 '+file;const label=node('small',file.split('/').pop()+' · SHA-256 '+asset.sha256);button.append(img,label);button.addEventListener('click',()=>selectImage(file));ui.gallery.appendChild(button)}if(!files.length)ui.gallery.appendChild(node('p','이 원문에 연결된 이미지가 없습니다.','hint'));else if(!ui.gallery.children.length)ui.gallery.appendChild(node('p','스냅샷에 확인된 이미지가 없습니다.','hint'))}
function selectSpec(path){if(!discard())return;const m=state.model;const file=m?.files?.find(item=>item.path===path);if(!file){notify('원본 YAML을 찾지 못했습니다. 스냅샷을 다시 읽어 주세요.','error');return}state.specPath=path;state.specText=file.text;state.original=file.text;state.sha=file.sha;state.specSeq++;ui.yaml.value=file.text;ui['spec-title'].textContent=path;ui['spec-meta'].textContent='기준 커밋 '+m.commit+' · YAML Git blob SHA '+file.sha;invalidate();renderSpecs();renderEvents();notify('정본 YAML을 열었습니다. 변경 전후 전체 모델 검사를 사용하세요.','success')}
function renderEvents(){ui.events.replaceChildren();if(!state.specPath)return;const parsed=state.parsedSpec;const original=state.model?.model?.specs?.find(s=>s.file===state.specPath)?.data;const d=parsed||(!dirty()?original:null);const heading=node('h3','계약 이벤트 '+(Array.isArray(d?.events)?d.events.length:'—')+'개');ui.events.appendChild(heading);if(!d){ui.events.appendChild(node('p','편집한 YAML의 카드 정보는 서버 검사 성공 후 갱신됩니다. 원본 카드로 현재 변경을 대표하지 않습니다.','hint'));return}for(const event of d.events||[]){const card=node('article','','card'),row=node('div','','row'),title=node('strong',event.event_label||'label 없음','mono');row.append(title,badge(event.status));card.appendChild(row);card.appendChild(node('p',String(event.event_name||'')+' · '+String(event.event_category||'')+' · '+String(d.screen_view||''),'hint'));card.appendChild(node('p',event.description||'발생 조건 없음'));card.appendChild(node('p','value: '+JSON.stringify(event.value)+' · params: '+JSON.stringify(event.params),'caption'));card.appendChild(node('p','source: '+(event.source||'')+' · platforms: '+(event.platforms||[]).join(', '),'caption'));if(event.decision)card.appendChild(node('p','결정: '+event.decision,'caption'));if(event.notes)card.appendChild(node('p','주의: '+event.notes,'caption'));const grid=node('div','','platform-grid');for(const platform of state.model?.model?.vocabulary?.platforms||[]){const support=event.platform_support?.[platform],box=node('div','','platform');box.append(node('strong',platform+' '),badge(support?.state||'unknown'),node('p',support?.evidence||'근거 없음'));grid.appendChild(box)}card.appendChild(grid);ui.events.appendChild(card)}}
function showErrors(errors){ui.diagnostics.replaceChildren();if(errors.length){for(const message of errors)ui.diagnostics.appendChild(node('li',message));ui.diagnostics.scrollIntoView({block:'nearest'})}else ui.diagnostics.appendChild(node('li','전체 정본 모델 검사 통과. 원격 반영이나 배포 검증은 별개입니다.','ok'))}
async function validate(){if(!state.specPath||state.busy)return false;const version=state.revision,path=state.specPath,text=state.specText;state.busy=true;updateActions();try{const data=await post('/api/validate',{path,text});if(version!==state.revision||path!==state.specPath)return false;if(!Array.isArray(data.errors))throw Error('검사 응답이 올바르지 않습니다.');showErrors(data.errors);state.validated=data.errors.length? -1:version;state.parsedSpec=state.validated===version&&data.spec&&typeof data.spec==='object'?data.spec:null;renderEvents();notify(data.errors.length?'검사 오류 '+data.errors.length+'개. 위 메시지를 수정하세요.':'전체 정본 모델 검사를 통과했습니다.',data.errors.length?'error':'success');return !data.errors.length}catch(error){if(version===state.revision){state.validated=-1;showErrors([explain(error)]);notify('검사 실패: '+explain(error),'error')}return false}finally{state.busy=false;updateActions()}}
function download(content,filename,type){
  const blob=content instanceof Blob?content:new Blob([content],{type});
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;
  a.download=filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),2000);
}
function proposalKey(){return state.specPath+'\u0000'+state.sha+'\u0000'+state.model?.commit+'\u0000'+state.specText+'\u0000'+ui['pr-title'].value.trim()}
function renderGenerated(){const files=state.generated?.files||{};ui['generated-file'].replaceChildren();for(const name of Object.keys(files)){const option=node('option',name);option.value=name;ui['generated-file'].appendChild(option)}ui['generated-file'].value=Object.hasOwn(files,'manifest.json')?'manifest.json':Object.keys(files)[0]||'';showGeneratedFile();updateActions()}
function showGeneratedFile(){const name=ui['generated-file'].value,content=state.generated?.files?.[name];ui['generated-text'].hidden=typeof content!=='string';ui['generated-text'].textContent=typeof content==='string'?content:'';const m=state.generated?.manifest;ui['generated-meta'].textContent=m?'생성 모드 '+(ui.preview.checked?'PREVIEW · draft 포함 · 생산 사용 금지':'approved 전용')+' · manifest '+JSON.stringify(m):''}
async function generate(){if(!state.specPath||state.busy)return;const version=state.revision,path=state.specPath,text=state.specText,preview=ui.preview.checked;state.busy=true;updateActions();try{const result=await post('/api/generate',{path,text,preview});if(version!==state.revision||path!==state.specPath||preview!==ui.preview.checked)return;if(!result.files||typeof result.files!=='object'||!result.manifest)throw Error('생성 응답이 올바르지 않습니다.');state.generated=result;state.generatedRevision=version;renderGenerated();notify(preview?'PREVIEW: draft 포함 결과입니다. 생산 코드로 통합하지 마세요.':'approved 계약만 생성했습니다. SDK 배포·수집은 별도 확인이 필요합니다.','success')}catch(error){if(version===state.revision)notify('생성 실패: '+explain(error),'error')}finally{state.busy=false;updateActions()}}
async function propose(){if(!state.specPath||state.busy||!state.status?.connected)return;const version=state.revision,path=state.specPath,text=state.specText,title=ui['pr-title'].value.trim(),key=proposalKey();if(!title)return;const valid=await validate();if(!valid||version!==state.revision||path!==state.specPath||key!==proposalKey())return;const summary='GitHub 저장소 변경 제안\n\n저장소: '+state.status.repository+'\nYAML: '+path+'\n제목: '+title+'\n기준 커밋: '+state.model.commit+'\n원본 YAML Git blob SHA: '+(state.sha||'(신규 파일)')+'\nYAML 변경: '+(dirty()?'있음':'원본과 동일')+'\n생성 범위: approved 전용 (draft PREVIEW 제외)\n\n이미지 주석은 포함되지 않습니다. 제안 PR 생성 후 별도의 검토·병합이 필요합니다. 제출하시겠습니까?';if(!window.confirm(summary)){proposalMessage('제안 제출을 취소했습니다.');return}if(version!==state.revision||key!==proposalKey()){proposalMessage('확인 도중 초안이 바뀌었습니다. 다시 검사해 주세요.','error');return}state.busy=true;updateActions();proposalMessage('원격 커밋·SHA를 확인하며 제안 중…');try{const response=await post('/api/proposals',{path,text,title,commit:state.model.commit,sha:state.sha});if(typeof response.url!=='string')throw Error('제안 URL이 없는 서버 응답입니다.');state.proposalKey=key;githubLink(ui['proposal-link'],response.url,'생성된 제안 PR 열기 ↗');proposalMessage('제안 PR을 만들었습니다. 검토·병합·배포는 별도입니다.','success')}catch(error){const recovery=error&&error.recovery;proposalMessage('제안 실패: '+explain(error)+(recovery?.branch?'\n브랜치 '+recovery.branch+'의 상태를 확인한 뒤 재시도하세요. 자동 재제출하지 않습니다.':''),'error');if(typeof recovery?.compareUrl==='string'){state.proposalKey=key;githubLink(ui['proposal-link'],recovery.compareUrl,'복구용 브랜치 비교 보기 ↗')}}finally{state.busy=false;updateActions()}}
function annotationKey(){return state.catalog?.snapshotHash+'\u0000'+state.sourceId+'\u0000'+state.imageFile+'\u0000'+assetFor(state.imageFile)?.sha256}
function rects(){const key=annotationKey();if(!state.annotations.has(key))state.annotations.set(key,[]);return state.annotations.get(key)}
function disableImage(message){state.image=null;ui.canvas.hidden=true;ui['image-placeholder'].hidden=false;ui['image-placeholder'].textContent=message;ui['image-meta'].textContent=message;state.selectedRect=-1;renderAnnotations();updateActions()}
async function selectImage(file){
  if(!state.source||!state.source.imageFiles.includes(file))return;
  const asset=assetFor(file);
  if(!asset)return;
  const seq=++state.imageSeq,sourceId=state.sourceId;
  state.imageFile=file;
  state.selectedRect=-1;
  state.drag=null;
  if(state.imageUrl)URL.revokeObjectURL(state.imageUrl);
  state.imageUrl='';
  disableImage('원본 이미지를 불러오는 중…');
  renderGallery();
  let url='';
  try{
    const response=await fetch(imageUrl(file),{credentials:'same-origin',cache:'no-store'});
    if(!response.ok)throw Error('이미지 요청 실패 ('+response.status+'). 원문 이미지 경로와 인증을 확인하세요.');
    url=URL.createObjectURL(await response.blob());
    if(seq!==state.imageSeq||sourceId!==state.sourceId)return;
    const img=new Image();
    img.src=url;
    await img.decode();
    if(seq!==state.imageSeq||sourceId!==state.sourceId)return;
    const w=img.naturalWidth,h=img.naturalHeight;
    if(!w||!h||w>imageMaxAxis||h>imageMaxAxis||w*h>imageMaxPixels){
      disableImage('원본 '+w+' × '+h+'px · 주석 한도(축당 '+imageMaxAxis+'px / '+imageMaxPixels.toLocaleString()+'px)를 초과했습니다. 원본은 위 갤러리에서 볼 수 있습니다.');
      return;
    }
    state.image=img;
    ui.canvas.width=w;
    ui.canvas.height=h;
    ui.canvas.hidden=false;
    ui['image-placeholder'].hidden=true;
    ui['image-meta'].textContent=file+' · '+w+' × '+h+' 원본 픽셀 · SHA-256 '+asset.sha256;
    renderAnnotations();
    draw();
    state.imageUrl=url;
    url='';
    updateActions();
  }catch(error){
    if(seq===state.imageSeq)disableImage('이미지 열기 실패: '+explain(error));
  }finally{
    if(url)URL.revokeObjectURL(url);
  }
}
function drawRect(ctx,rect,i,selected){const [x,y,w,h]=rect;ctx.save();ctx.fillStyle=selected?'#fb6b3c44':'#1367c044';ctx.strokeStyle=selected?'#eb5524':'#135baa';ctx.lineWidth=Math.max(2,Math.min(5,state.image.naturalWidth/650));ctx.fillRect(x,y,w,h);ctx.strokeRect(x+.5,y+.5,w,h);const font=Math.max(16,Math.min(38,state.image.naturalWidth/32));ctx.font='bold '+font+'px sans-serif';const label=String(i+1),labelWidth=Math.max(font*1.6,ctx.measureText(label).width+10);ctx.fillStyle=selected?'#c8421d':'#135baa';ctx.fillRect(x,y,labelWidth,font+8);ctx.fillStyle='#fff';ctx.fillText(label,x+5,y+font);ctx.restore()}
function draw(){if(!state.image)return;const canvas=ui.canvas,ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(state.image,0,0);rects().forEach((item,i)=>drawRect(ctx,item.rect,i,i===state.selectedRect));if(state.drag?.rect)drawRect(ctx,state.drag.rect,rects().length,true)}
function renderAnnotations(){ui['annotation-list'].replaceChildren();if(state.image)rects().forEach((item,i)=>{const li=node('li',''),button=node('button',(i+1)+'. '+(item.label||'설명 없음')+' — '+item.rect.join(', '));button.type='button';button.addEventListener('click',()=>{state.selectedRect=i;ui['annotation-label'].value=item.label;[ui['rect-x'],ui['rect-y'],ui['rect-w'],ui['rect-h']].forEach((input,j)=>{input.value=item.rect[j]});draw();updateActions()});li.appendChild(button);ui['annotation-list'].appendChild(li)});if(!state.image||state.selectedRect<0){ui['annotation-label'].value='';[ui['rect-x'],ui['rect-y'],ui['rect-w'],ui['rect-h']].forEach(input=>{input.value=''})}updateActions()}
function point(event){const box=ui.canvas.getBoundingClientRect(),x=Math.round((event.clientX-box.left)*ui.canvas.width/box.width),y=Math.round((event.clientY-box.top)*ui.canvas.height/box.height);return [Math.min(ui.canvas.width,Math.max(0,x)),Math.min(ui.canvas.height,Math.max(0,y))]}
function validRect(){
  if(!state.image)throw Error('이미지를 먼저 선택하세요.');
  const inputs=[ui['rect-x'],ui['rect-y'],ui['rect-w'],ui['rect-h']];
  if(inputs.some(input=>input.value===''))throw Error('x, y, 폭, 높이를 모두 입력하세요.');
  const r=inputs.map(input=>Number(input.value));
  if(r.some((v,i)=>!Number.isSafeInteger(v)||v<(i<2?0:1)))throw Error('x, y는 0 이상, 폭과 높이는 1 이상의 정수여야 합니다.');
  if(r[0]+r[2]>state.image.naturalWidth||r[1]+r[3]>state.image.naturalHeight)throw Error('사각형이 이미지 원본 '+state.image.naturalWidth+' × '+state.image.naturalHeight+'px 경계를 넘습니다.');
  return r;
}
function sidecar(){
  const asset=assetFor(state.imageFile);
  const sourceFile=state.catalog?.documents?.find(item=>item.id===state.sourceId)?.file||'';
  return {
    schema_version:1,
    repository:state.catalog?.repository||'',
    commit:state.catalog?.commit||'',
    source_id:state.sourceId,
    source_file:sourceFile,
    image_file:state.imageFile,
    image_sha256:asset?.sha256||'',
    image_width:state.image.naturalWidth,
    image_height:state.image.naturalHeight,
    coordinate_system:'natural image pixels, origin top-left',
    annotations:rects().map((item,i)=>({number:i+1,label:item.label,rect:{x:item.rect[0],y:item.rect[1],width:item.rect[2],height:item.rect[3]}}))
  };
}
function imageBase(){return (state.imageFile.split('/').pop()||'image').replace(/\.(png|jpe?g)$/i,'')+'-'+state.sourceId.slice(0,8)}
async function loadAll(){
  if(state.busy)return;
  if(dirty()&&!discard())return;
  state.busy=true;
  updateActions();
  notify('저장소 원문·정본·연결 상태를 불러오는 중…');
  try{
    const [catalog,model,status]=await Promise.all([api('/api/catalog'),api('/api/model'),api('/api/status')]);
    if(!Array.isArray(catalog.documents)||!Array.isArray(catalog.assets)||!model.model||!Array.isArray(model.files)||catalog.commit!==model.commit||catalog.snapshotHash!==model.snapshotHash)
      throw Error('원문과 정본 스냅샷의 커밋/해시가 일치하지 않습니다. 서버 스냅샷을 다시 생성하세요.');
    state.catalog=catalog;
    state.model=model;
    state.status=status;
    ++state.sourceSeq;
    state.source=null;
    state.sourceId='';
    ++state.imageSeq;
    if(state.imageUrl)URL.revokeObjectURL(state.imageUrl);
    state.imageUrl='';
    state.imageFile='';
    disableImage('원문 이미지를 선택하세요.');
    state.specPath='';
    state.sha='';
    state.original='';
    state.specText='';
    ui.yaml.value='';
    ui['spec-title'].textContent='정본 계약을 선택하세요';
    ui['spec-meta'].textContent='원본 파일과 Git SHA를 확인한 뒤 편집합니다.';
    ui['source-title'].textContent='원문을 선택하세요';
    ui['source-meta'].textContent='목록의 문서는 원문 스냅샷입니다.';
    ui['source-contracts'].replaceChildren();
    ui.markdown.textContent='원문을 선택하면 실제 Markdown이 표시됩니다.';
    ui.gallery.replaceChildren();
    ui.properties.textContent='';
    ui['source-link'].hidden=true;
    ui['image-count'].textContent='';
    invalidate();
    renderCounts();
    renderMode();
    renderSources();
    renderSpecs();
    for(const file of model.files.filter(f=>f.path==='rules/vocabulary.json'||f.path==='rules/envelope.json'))
      ui[file.path.includes('vocabulary')?'vocabulary':'envelope'].textContent=file.text;
    notify('실제 원문과 정본 계약을 불러왔습니다. 원격 제안 상태는 오른쪽에 표시됩니다.','success');
  }catch(error){
    notify('스냅샷 읽기 실패: '+explain(error)+' 다시 읽기를 눌러 재시도하세요.','error');
  }finally{
    state.busy=false;
    updateActions();
  }
}
ui.reload.addEventListener('click',loadAll);ui.search.addEventListener('input',()=>{state.sourceLimit=60;renderSources()});ui.more.addEventListener('click',()=>{state.sourceLimit+=60;renderSources()});ui.yaml.addEventListener('input',()=>{state.specText=ui.yaml.value;invalidate()});ui.validate.addEventListener('click',validate);ui['yaml-download'].addEventListener('click',()=>{if(state.specPath)download(state.specText,state.specPath.split('/').pop(),'text/yaml;charset=utf-8')});ui.reset.addEventListener('click',()=>{if(!state.specPath)return;if(state.sha){if(dirty()&&!window.confirm('편집한 YAML을 원본으로 되돌리시겠습니까?'))return;state.specText=state.original;ui.yaml.value=state.original}else{if(!discard())return;state.specPath='';state.specText='';ui.yaml.value='';ui['spec-title'].textContent='정본 계약을 선택하세요';ui['spec-meta'].textContent=''}invalidate();renderSpecs()});ui['new-form'].addEventListener('submit',event=>{event.preventDefault();const service=ui['new-service'].value,screen=ui['new-screen'].value.trim(),source=ui['new-source'].value.trim().toLowerCase(),path='specs/'+service+'/'+screen+'.yaml';if(!Object.hasOwn(state.model?.model?.vocabulary?.services||{},service)||!/^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$/.test(screen)||!/^[a-f0-9]{32}$/.test(source)||!state.catalog?.documents?.some(d=>d.id===source)){notify('등록된 서비스, snake_case 화면, 실제 원문 ID를 입력하세요.','error');return}if(state.model.files.some(f=>f.path===path)){notify('이미 존재하는 정본 파일입니다. 왼쪽 목록에서 선택하세요.','error');return}if(!discard())return;state.specPath=path;state.sha='';state.original='';state.specText=JSON.stringify({schema_version:1,service,screen_view:screen,events:[]},null,2)+'\n';ui.yaml.value=state.specText;ui['spec-title'].textContent=path+' · 신규 draft';ui['spec-meta'].textContent='원문 ID '+source+' · 새 파일 (Git blob SHA 없음) · 이벤트는 직접 작성해야 검사를 통과합니다.';invalidate();renderSpecs();notify('빈 신규 계약을 열었습니다. events는 필수입니다. 원문을 승인 계약으로 자동 승격하지 않습니다.','success')});ui.preview.addEventListener('change',()=>{state.generated=null;state.generatedRevision=-1;ui['generated-file'].replaceChildren();ui['generated-text'].hidden=true;ui['generated-meta'].textContent=ui.preview.checked?'PREVIEW: draft를 포함할 수 있습니다. 생산 환경 사용 금지.':'approved 계약만 생성합니다.';updateActions()});ui.generate.addEventListener('click',generate);ui['generated-file'].addEventListener('change',showGeneratedFile);ui['generated-download'].addEventListener('click',()=>{const name=ui['generated-file'].value,content=state.generated?.files?.[name];if(state.generatedRevision===state.revision&&typeof content==='string')download(content,name,name.endsWith('.json')?'application/json;charset=utf-8':'text/plain;charset=utf-8')});ui['pr-title'].addEventListener('input',updateActions);ui.propose.addEventListener('click',propose);
ui.canvas.addEventListener('pointerdown',event=>{
  if(!state.image)return;
  state.drag={start:point(event),rect:null};
  ui.canvas.setPointerCapture(event.pointerId);
});
ui.canvas.addEventListener('pointermove',event=>{
  if(!state.drag)return;
  const [x,y]=point(event),[sx,sy]=state.drag.start;
  state.drag.rect=[Math.min(sx,x),Math.min(sy,y),Math.abs(x-sx),Math.abs(y-sy)];
  draw();
});
ui.canvas.addEventListener('pointerup',event=>{
  if(!state.drag)return;
  const r=state.drag.rect;
  state.drag=null;
  if(r&&r[2]&&r[3]){
    [ui['rect-x'],ui['rect-y'],ui['rect-w'],ui['rect-h']].forEach((input,i)=>{input.value=r[i]});
    state.selectedRect=-1;
    updateActions();
  }
  draw();
  ui.canvas.releasePointerCapture(event.pointerId);
});
ui.canvas.addEventListener('pointercancel',()=>{state.drag=null;draw()});
ui['save-rect'].addEventListener('click',()=>{
  try{
    const rect=validRect(),label=ui['annotation-label'].value.trim(),entries=rects();
    if(state.selectedRect>=0)entries[state.selectedRect]={label,rect};
    else{entries.push({label,rect});state.selectedRect=entries.length-1}
    renderAnnotations();
    draw();
    notify('원본 픽셀 주석을 메모리에 저장했습니다. PNG/JSON을 내려받으세요.','success');
  }catch(error){notify('주석 입력 오류: '+explain(error),'error')}
});
ui['delete-rect'].addEventListener('click',()=>{
  if(state.selectedRect<0||!state.image)return;
  rects().splice(state.selectedRect,1);
  state.selectedRect=-1;
  renderAnnotations();
  draw();
});
ui['annotation-json'].addEventListener('click',()=>{
  if(state.image)download(JSON.stringify(sidecar(),null,2)+'\n',imageBase()+'.annotations.json','application/json;charset=utf-8');
});
ui['annotation-png'].addEventListener('click',()=>{
  if(!state.image)return;
  const filename=imageBase()+'.annotated.png';
  draw();
  ui.canvas.toBlob(blob=>{
    if(blob)download(blob,filename,'image/png');
    else notify('PNG를 만들지 못했습니다. 이미지 크기를 확인하세요.','error');
  },'image/png');
});
window.addEventListener('beforeunload',event=>{if(dirty()){event.preventDefault();event.returnValue=''}});
loadAll();
}());</script></body></html>`;
