"""Display bounded fixed/enum UI values; dynamic payloads never enter reports."""
import json
import re


def display_value(value, present=None):
    if value is None:
        return '파라미터 없음' if present is False else 'NULL (값 없음)' if present is True else 'NULL (키 존재 여부 미확인)'
    value = str(value)
    if value == '':
        return '\"\" (빈 문자열)'
    if len(value) > 120 or re.search(r'@|https?://|(?:sk|xox[baprs])[-_]|\b\d{2,3}[- ]?\d{3,4}[- ]?\d{4}\b|[A-Za-z0-9_+/=-]{32,}|[\x00-\x08\x0b\x0c\x0e-\x1f]', value, re.I):
        return '[민감정보 가능 값 가림]'
    return json.dumps(value, ensure_ascii=False)


def expected_value(contracts):
    values = set()
    for c in contracts:
        allowed = c.get('allowed_values') or ([c['fixed_value']] if c.get('fixed_value') is not None else [])
        if allowed:
            values.update(display_value(v) for v in allowed)
        elif c.get('value_required'):
            description = c.get('raw_fields', {}).get('value', '')
            values.add('필수 value · 명세: ' + description)
    return sorted(values) or ['명세 value 규칙 확인 필요']
