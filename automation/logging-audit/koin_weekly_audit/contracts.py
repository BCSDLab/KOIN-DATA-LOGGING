import hashlib
import json
import re
from collections import defaultdict

FIELDS = ('설명', 'screen_view', 'event_name', 'event_label', 'value', 'event_category')


def clean(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\\([_*{}\[\]().~`<>#+=|-])', r'\1', text)
    return text.replace('**', '').replace('`', '').strip()


def parse_page(page):
    """Do not infer deployment, enum values or version cutovers from prose."""
    text = page['text']
    lines = clean(text).splitlines()
    new = next((i for i, line in enumerate(lines)
                if re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?새\s*로깅', line)), None)
    if new is None:
        return [], 'no_current_contract'
    lines = lines[new:]
    # A page may explicitly contain more than one contract.
    chunks, current, current_key = [], {}, None
    for line in lines:
        match = re.match(r'^\s*(?:[-*]\s*)?(' + '|'.join(FIELDS) + r')\s*[:：]\s*(.*)', line)
        if match:
            key, val = match.groups()
            if key == 'event_label' and key in current:
                chunks.append(current)
                current = {}
            current[key] = val.strip()
            current_key = key
        elif current_key and re.match(r'^\s+[-*]\s+', line):
            current[current_key] += ' ' + re.sub(r'^\s+[-*]\s+', '', line)
        elif line.strip():
            current_key = None
    if current:
        chunks.append(current)
    contracts = []
    for fields in chunks:
        names = set(re.findall(r'\bDA[12]\b', fields.get('event_name', '')))
        if not names:
            continue
        labels = re.findall(r'\b[a-z][a-z0-9_]*(?:__[a-z0-9_]+)+\b', fields.get('event_label', ''))
        if not labels:
            literal = fields.get('event_label', '').strip(' ”“\'"')
            labels = [literal] if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*', literal) else []
        screens = re.findall(r'\b[a-z][a-z0-9_]*\b', fields.get('screen_view', ''))
        categories = re.findall(r'\b(click|swipe|scroll|view|submit|toggle|exit|page_exit|entry|show|impression|complete)\b', fields.get('event_category', ''))
        for label in labels:
            action = label.split('__')[-1]
            cats = [action] if action in categories else sorted(set(categories))
            platforms = sorted(set('WEB' if p.upper().startswith('WEB') else p.upper()
                                   for p in page.get('platforms', [])))
            if action == 'swipe' and re.search(r'iOS만|IOS만|iOS\s*전용', fields.get('event_label', '') + fields.get('event_category', '')):
                platforms = ['IOS']
            raw_value = fields.get('value', '').strip(' ”“\'"')
            # Only unambiguous single literal values are checked as literals.
            fixed = raw_value if raw_value and len(raw_value) < 65 and not re.search(r'[{}<>/~():：]|예시|예:|ex\)|동적|STRING|INT|선택한|실제|→', raw_value, re.I) else None
            status = 'unresolved' if page.get('unresolved') else 'current'
            label_screen = label.split('__')[1] if '__' in label else None
            selected_screens = [label_screen] if label_screen in screens else sorted(set(screens))
            if action == 'swipe' and '모바일' in fields.get('event_label', '') and platforms == ['WEB']:
                status = 'unresolved'  # Body and platform metadata conflict; don't guess support.
            contracts.append(dict(label=label, names=sorted(names), screens=selected_screens,
                                  categories=cats, platforms=platforms, value_required=bool(raw_value),
                                  fixed_value=fixed, value_rule='fixed' if fixed else 'presence_only' if raw_value else 'unspecified',
                                  status=status, url=page['url'], title=page['title'], service=page.get('service', ''),
                                  raw_fields=fields))
    return contracts, 'parsed' if contracts else 'unparsed_or_legacy'


def build_catalog(pages):
    by_label = defaultdict(list)
    coverage = []
    for page in pages:
        contracts, status = parse_page(page)
        coverage.append(dict(url=page['url'], title=page['title'], service=page.get('service'), status=status,
                             labels=[x['label'] for x in contracts]))
        for contract in contracts:
            if contract not in by_label[contract['label']]:
                by_label[contract['label']].append(contract)
    conflicts = []
    for label, contracts in by_label.items():
        signatures = {json.dumps({k: c[k] for k in ('names', 'screens', 'categories', 'fixed_value')}, sort_keys=True) for c in contracts}
        # Platform-specific signatures need explicit resolution; accepting any would hide drift.
        if len(signatures) > 1 or any(c['status'] == 'unresolved' for c in contracts):
            conflicts.append(label)
    fingerprint = hashlib.sha256(json.dumps(pages, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return dict(by_label=dict(by_label), conflicts=sorted(conflicts), coverage=coverage, snapshot_sha256=fingerprint)


def compare(catalog, observations):
    issues = defaultdict(lambda: dict(count=0, versions=set(), platforms=set()))
    observed_labels = set()
    observed_pairs = set()
    total = 0
    for obs in observations:
        count = int(obs['event_count'])
        total += count
        label = obs.get('event_label')
        observed_labels.add(label)
        observed_pairs.add((label, obs['platform']))
        candidates = catalog['by_label'].get(label, [])
        reasons = []
        if not label:
            reasons = ['event_label_missing']
        elif not candidates:
            reasons = ['unregistered_label_or_old_version']
        elif label in catalog['conflicts']:
            reasons = ['specification_conflict']
        else:
            failures = []
            for c in candidates:
                bad = []
                if obs['event_name'] not in c['names']:
                    bad.append('event_name_mismatch')
                if c['screens'] and obs.get('screen_view') not in c['screens']:
                    bad.append('screen_view_mismatch')
                if c['categories'] and obs.get('event_category') not in c['categories']:
                    bad.append('event_category_mismatch')
                if c['platforms'] and obs['platform'] not in c['platforms']:
                    bad.append('platform_mismatch')
                if c['value_required'] and obs.get('value') in (None, ''):
                    bad.append('value_missing')
                elif c['fixed_value'] is not None and obs.get('value') != c['fixed_value']:
                    bad.append('fixed_value_mismatch')
                if obs.get('duplicate_param_keys', 0):
                    bad.append('duplicate_parameter_key')
                failures.append(bad)
            # A match to any explicitly supported contract is sufficient.
            reasons = min(failures, key=len)
        for reason in reasons:
            key = (label or '(missing)', reason)
            issue = issues[key]
            issue['count'] += count
            issue['versions'].add(obs.get('app_version') or 'WEB/unknown')
            issue['platforms'].add(obs['platform'])
    findings = []
    for (label, reason), data in sorted(issues.items()):
        contracts = catalog['by_label'].get(label, [])
        findings.append(dict(label=label, reason=reason, count=data['count'],
                             versions=sorted(data['versions']), platforms=sorted(data['platforms']),
                             specification_urls=sorted(set(x['url'] for x in contracts))))
    expected_pairs = {(label, p) for label, cs in catalog['by_label'].items() for c in cs for p in c['platforms']}
    return dict(events=total, observed_labels=len(observed_labels), findings=findings,
                unobserved_labels=sorted(set(catalog['by_label']) - observed_labels),
                unobserved_platform_contracts=[dict(label=l, platform=p) for l, p in sorted(expected_pairs - observed_pairs)],
                snapshot_sha256=catalog['snapshot_sha256'],
                interpretation='Latest-spec mismatches are candidates; deployment/version cutovers are not inferred. Dynamic values are checked for presence only.')
