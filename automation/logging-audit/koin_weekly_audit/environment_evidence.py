"""Compare actually observed metadata sets, without equating traffic with coverage."""
import re
from collections import defaultdict
from .value_evidence import display_value, expected_value
from .source_value import contract_value_sources
from .normalization import normalize_observation


def value_collections(catalog, rows):
    groups = defaultdict(lambda: dict(values=defaultdict(int), versions=set(), events=0))
    for row in rows:
        row = normalize_observation(row)
        label, platform = row.get('event_label') or '(missing)', row['platform']
        group = groups[(platform,label)]
        group['values'][display_value(row.get('value'),row.get('value_parameter_present'))] += int(row['event_count'])
        group['events'] += int(row['event_count'])
        group['versions'].add(row.get('app_version') or ('WEB' if platform == 'WEB' else 'unknown'))
    result = []
    for (platform,label), group in sorted(groups.items()):
        contracts = catalog['by_label'].get(label, [])
        expected = expected_value(contracts) if contracts else ['현행 명세 없음']
        if contracts and all(not c.get('value_required') for c in contracts):
            expected = ['value 미지정 · 명세: ' + str(c.get('raw_fields', {}).get('value') or '미기재') for c in contracts]
        result.append(dict(platform=platform,label=label,expected=expected,source=contract_value_sources(catalog,label,platform),
            rules=sorted({c.get('value_rule','unspecified') for c in contracts}),
            actual=dict(group['values']),events=group['events'],versions=sorted(group['versions'])))
    return result


def observations(catalog, rows):
    groups = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for row in rows:
        row = normalize_observation(row)
        label, platform = row.get('event_label') or '(missing)', row['platform']
        fields = groups[(platform, label)]
        for field in ('event_name', 'screen_view', 'event_category'):
            value = row.get(field)
            value = '(누락)' if value is None else str(value)
            value = value if value == '(누락)' or re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,159}', value) else '(형식 오류)'
            fields[field][value] += int(row['event_count'])
        contracts = catalog['by_label'].get(label, [])
        if contracts and all(c.get('fixed_value') is not None or c.get('allowed_values') for c in contracts):
            fields['value'][display_value(row.get('value'), row.get('value_parameter_present'))] += int(row['event_count'])
    evidence = []
    for (platform, label), fields in sorted(groups.items()):
        contracts = catalog['by_label'].get(label, [])
        expected = {f: sorted({v for c in contracts for v in c.get(k, [])}) for f, k in
                    (('event_name','names'),('screen_view','screens'),('event_category','categories'))}
        if 'value' in fields:
            expected['value'] = expected_value(contracts)
        evidence.append(dict(platform=platform, label=label, fields={f:dict(counts) for f,counts in fields.items()}, expected=expected))
    return evidence


def compare_environments(reports):
    stage, prod = reports.get('stage', {}), reports.get('production', {})
    if not stage.get('complete') or not prod.get('complete') or any(not stage.get(k) or stage.get(k) != prod.get(k) for k in ('start','end','snapshot_sha256')):
        return dict(complete=False, reason='두 환경 조회 완료·동일 기간·동일 명세 확인 필요')
    indexes = [{(r['platform'],r['label']):r for r in env.get('observed_evidence', [])} for env in (stage,prod)]
    common = set(indexes[0]) & set(indexes[1])
    differences, matched, masked = [], 0, 0
    for key in sorted(common):
        a,b = [i[key] for i in indexes]
        same = True
        for field in sorted(set(a['fields']) & set(b['fields'])):
            actual_a, actual_b = a['fields'][field], b['fields'][field]
            if any('[민감정보 가능 값 가림]' in v for v in list(actual_a) + list(actual_b)):
                masked += 1
                same = False
                continue
            if set(actual_a) != set(actual_b):
                same = False
                differences.append(dict(platform=key[0],label=key[1],field=field,
                    expected=a['expected'].get(field, []),stage=actual_a,production=actual_b))
        matched += same
    return dict(complete=True, common_labels=len(common), same_observed_labels=matched,
                stage_only=len(set(indexes[0])-set(indexes[1])), production_only=len(set(indexes[1])-set(indexes[0])),
                differences=differences, masked_fields=masked)

