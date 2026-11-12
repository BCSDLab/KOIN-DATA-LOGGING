#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { load, validate, generate } from './core.mjs';

try {
  const [command, ...args] = process.argv.slice(2);
  if (!['check','find','gen'].includes(command)) throw new Error('사용법: koin-log check | find <검색어> | gen [--preview] [--check]');
  const root = process.cwd(), model = load(root), errors = validate(model);
  if (errors.length) throw new Error(errors.join('\n'));
  if (command === 'check') {
    if (args.length) throw new Error('check에는 옵션이 없습니다.');
    console.log(`명세 ${model.specs.length}개 검사 통과`);
  } else if (command === 'find') {
    const query = args.join(' ').trim().toLowerCase();
    if (!query) throw new Error('검색어 필요');
    const hits = model.specs.flatMap(s=>s.data.events.map(e=>({...e,file:s.file})))
      .filter(e=>JSON.stringify(e).toLowerCase().includes(query));
    console.log(JSON.stringify(hits,null,2));
  } else {
    if (args.some(a=>!['--preview','--check'].includes(a))) throw new Error('알 수 없는 gen 옵션');
    const preview = args.includes('--preview');
    const output = path.join(root,preview?'generated-preview':'generated');
    const contents = generate(model,{preview});
    for (const [name, content] of Object.entries(contents)) {
      const file = path.join(output,name);
      if (args.includes('--check')) {
        if (!fs.existsSync(file) || fs.readFileSync(file,'utf8') !== content) throw new Error(`${file}: 명세와 생성물 불일치. gen 실행 후 커밋하세요.`);
      } else {
        fs.mkdirSync(output,{recursive:true}); fs.writeFileSync(file,content);
      }
    }
    console.log(args.includes('--check')?'생성물 일치 확인':`${output} 생성 완료`);
  }
} catch (error) { console.error(error.message); process.exitCode = 1; }
