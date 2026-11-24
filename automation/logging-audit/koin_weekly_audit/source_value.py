"""Retain exact source fragments independently of value-rule interpretation."""
import html
import re


def plain(line):
    line = re.sub(r'<[^>]*>', '', line)
    return html.unescape(re.sub(r'\\([_*])', r'\1', line)).replace('**','').replace('`','')


def source_values(page):
    active, blocks, current = False, [], None
    for number, raw in enumerate(page['text'].splitlines(), 1):
        line = plain(raw)
        marker = re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?(과거|이전|새)\s*로깅', line)
        if marker:
            active, current = marker.group(1) == '새', None
            continue
        if not active:
            continue
        match = re.match(r'^\s*(?:[-*]\s*)?value\s*[:：]\s*(.*)',line)
        if match:
            current = dict(line=number, raw_text=raw, declared_text=match.group(1),
                           url=page['url'] + '#L' + str(number))
            blocks.append(current)
            continue
        if current and raw.strip():
            indent = len(raw)-len(raw.lstrip())
            initial_indent = len(current['raw_text'].splitlines()[0])-len(current['raw_text'].splitlines()[0].lstrip())
            if indent > initial_indent and not re.match(r'^\s*(?:[-*]\s*)?(?:event_name|event_label|event_category|screen_view|설명)\s*[:：]',line):
                current['raw_text'] += '\n' + raw
                current['declared_text'] += '\n' + line.strip()
            else:
                current = None
    return blocks


def contract_value_sources(catalog, label, platform):
    contracts = [c for c in catalog['by_label'].get(label, []) if not c['platforms'] or platform in c['platforms']]
    if not contracts:
        return dict(status='no_current_contract', sources=[])
    sources = {s['url']:s for c in contracts for s in c.get('value_source', [])}
    return dict(status='source_present' if sources else 'source_value_not_extracted', sources=list(sources.values()))


def audit_markdown(coverage):
    lines = ['# GitHub 전체 문서 value 원문 추출 근거', '',
             'GitHub 고정 커밋의 모든 문서를 기록합니다. 새 로깅 구간의 value 원문을 규칙 해석과 별도로 보존합니다. 과거/레거시와 미해석 문서는 현행 계약으로 자동 간주하지 않습니다.', '']
    for row in coverage:
        lines += ['## ' + html.escape(row['title']), '', '[원문](' + row['url'] + ') · 파싱 상태: ' + row['status'], '']
        if not row.get('value_source'):
            lines += ['새 로깅 구간의 value 표기를 추출하지 못함 — 원문 구조·현행 여부 확인 필요', '']
        for source in row.get('value_source', []):
            lines += ['[원문 ' + str(source['line']) + '행](' + source['url'] + ')', '', '<pre>' + html.escape(source['raw_text']) + '</pre>', '']
    return '\n'.join(lines)
