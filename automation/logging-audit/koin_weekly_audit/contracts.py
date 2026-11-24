import hashlib
import json
import re
from collections import defaultdict

FIELDS = ('설명', 'screen_view', 'event_name', 'event_label', 'value', 'event_category')
LEGACY_EVENT_NAMES = frozenset(('CAMPUS', 'BUSINESS', 'USER'))
CATEGORIES = ('unregistered', 'legacy_logging', 'current_mismatch')
PLATFORMS = ('IOS', 'ANDROID', 'WEB')


def clean(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\\([_*{}\[\]().~`<>#+=|-])', r'\1', text)
    return text.replace('**', '').replace('`', '').strip()


def legacy_page(page):
    return bool(re.search(r'레거시|\blegacy\b', ' '.join(str(page.get(k, '')) for k in
                ('title', 'service', 'lifecycle_status')), re.I))


def historical_labels(page):
    """Read explicit label fields, never guess historical labels from prose."""
    lines = clean(page['text']).splitlines()
    has_sections = any(re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?(?:과거|이전|새)\s*로깅', l) for l in lines)
    whole = legacy_page(page) or (not has_sections and not re.search(r'event_name\s*:\s*[”"\']?DA[12]\b', clean(page['text'])))
    section, in_label, values = 'plain', False, []
    for line in lines:
        marker = re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?(과거|이전|새)\s*로깅', line)
        if marker:
            section, in_label = marker.group(1), False
            continue
        if not whole and section not in ('과거', '이전'):
            continue
        field = re.match(r'^\s*(?:[-*]\s*)?([a-z_]+)\s*[:：]\s*(.*)', line)
        if field:
            in_label = field.group(1) == 'event_label'
            if in_label:
                values.append(field.group(2))
        elif in_label and re.match(r'^\s+[-*]\s+', line):
            values.append(line)
        elif line.strip():
            in_label = False
    labels = set()
    for value in values:
        labels.update(re.findall(r'\b[a-z][a-z0-9_]*(?:__[a-z0-9_]+)+\b', value))
        labels.update(re.findall(r'["“”‘’\']\s*([A-Za-z][A-Za-z0-9_]*)\s*["“”‘’\']', value))
        literal = value.strip(' -”“‘’\'"')
        if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', literal):
            labels.add(literal)
    return sorted(labels)


def parse_page(page):
    """Do not infer deployment, enum values or version cutovers from prose."""
    if legacy_page(page):
        return [], 'legacy_document'
    text = page['text']
    lines = clean(text).splitlines()
    new = next((i for i, line in enumerate(lines)
                if re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?새\s*로깅', line)), None)
    if new is None:
        return [], 'no_current_contract'
    selected, in_new = [], False
    for line in lines[new:]:
        marker = re.match(r'^\s*(?:[-*]\s*)?(?:#+\s*)?(과거|이전|새)\s*로깅', line)
        if marker:
            in_new = marker.group(1) == '새'
        if in_new:
            selected.append(line)
    lines = selected
    # A page may explicitly contain more than one contract.
    chunks, current, current_key, key_indent = [], {}, None, 0
    for line in lines:
        match = re.match(r'^\s*(?:[-*]\s*)?(' + '|'.join(FIELDS) + r')\s*[:：]\s*(.*)', line)
        if match:
            key, val = match.groups()
            if 'event_label' in current and key in current:
                chunks.append(current)
                current = {}
            current[key] = val.strip()
            current_key = key
            key_indent = len(line) - len(line.lstrip())
        elif current_key and re.match(r'^\s+[-*]\s+', line) and (
                len(line) - len(line.lstrip()) > key_indent or
                (current_key == 'value' and re.match(r'^\s*[-*]\s*예시', line))):
            current[current_key] += ' ' + re.sub(r'^\s+[-*]\s+', '', line)
        elif line.strip():
            current_key = None
    if current:
        chunks.append(current)
    # Some pages declare event_name/value/category once after screen-specific
    # blocks. Only reuse a field when its explicit page-wide value is unique;
    # conflicting values stay unresolved rather than being guessed or dropped.
    shared = {}
    for key in ('event_name', 'screen_view', 'value', 'event_category'):
        values = {c[key] for c in chunks if c.get(key)}
        if len(values) == 1:
            shared[key] = next(iter(values))
    contracts = []
    for fields in chunks:
        inherited = []
        if not fields.get('event_name'):
            fields = dict(fields)
            for key, value in shared.items():
                if not fields.get(key):
                    fields[key] = value
                    inherited.append(key)
        names = set(re.findall(r'\bDA[12]\b', fields.get('event_name', '')))
        labels = re.findall(r'\b[a-z][a-z0-9_]*(?:__[a-z0-9_]+)+\b', fields.get('event_label', ''))
        if not labels:
            literal = fields.get('event_label', '').strip(' ”“\'"')
            labels = [literal] if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*', literal) else []
        screens = re.findall(r'\b[a-z][a-z0-9_]*\b', fields.get('screen_view', ''))
        category_text = re.sub(r'\([^)]*\)', '', fields.get('event_category', ''))
        categories = re.findall(r'\b[a-z][a-z0-9_]*\b', category_text)
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
            if not names or not screens or not categories:
                status = 'unresolved'
            label_screen = label.split('__')[1] if '__' in label else None
            selected_screens = [label_screen] if label_screen in screens else sorted(set(screens))
            if action == 'swipe' and '모바일' in fields.get('event_label', '') and platforms == ['WEB']:
                status = 'unresolved'  # Body and platform metadata conflict; don't guess support.
            contracts.append(dict(label=label, names=sorted(names), screens=selected_screens,
                                  categories=cats, platforms=platforms, value_required=bool(raw_value),
                                  fixed_value=fixed, value_rule='fixed' if fixed else 'presence_only' if raw_value else 'unspecified',
                                  status=status, url=page['url'], title=page['title'], service=page.get('service', ''),
                                  raw_fields=fields, inherited_fields=inherited))
    return contracts, 'parsed' if contracts else 'unparsed_or_legacy'


def build_catalog(pages):
    by_label = defaultdict(list)
    legacy_by_label = defaultdict(list)
    coverage = []
    for page in pages:
        contracts, status = parse_page(page)
        past = historical_labels(page)
        coverage.append(dict(url=page['url'], title=page['title'], service=page.get('service'), status=status,
                             labels=[x['label'] for x in contracts], historical_labels=past))
        for label in past:
            reference = {k: page.get(k, '') for k in ('url', 'title', 'service')}
            if reference not in legacy_by_label[label]:
                legacy_by_label[label].append(reference)
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
    return dict(by_label=dict(by_label), legacy_by_label=dict(legacy_by_label),
                conflicts=sorted(conflicts), coverage=coverage, snapshot_sha256=fingerprint)


def compare(catalog, observations):
    issues = defaultdict(lambda: dict(count=0, versions=set(), platforms=set(), event_names=set(),
                                      platform_counts=defaultdict(int), platform_versions=defaultdict(set),
                                      platform_event_names=defaultdict(set)))
    observed_labels = set()
    observed_pairs = set()
    current_labels_seen = set()
    counts = {p: dict(events=0, labels=set(), categories={k: dict(events=0, labels=set()) for k in CATEGORIES},
                      event_names=defaultdict(int)) for p in PLATFORMS}
    total = 0
    for obs in observations:
        event_name = obs['event_name']
        if event_name not in ('DA1', 'DA2') and event_name.upper() not in LEGACY_EVENT_NAMES:
            continue
        count = int(obs['event_count'])
        platform = obs['platform']
        if platform not in counts:
            counts[platform] = dict(events=0, labels=set(), categories={k: dict(events=0, labels=set()) for k in CATEGORIES}, event_names=defaultdict(int))
        total += count
        label = obs.get('event_label')
        observed_labels.add(label)
        if event_name in ('DA1', 'DA2'):
            observed_pairs.add((label, platform))
            current_labels_seen.add(label)
        counts[platform]['events'] += count
        counts[platform]['labels'].add(label)
        counts[platform]['event_names'][event_name] += count
        candidates = catalog['by_label'].get(label, [])
        reasons = []
        category = 'current_mismatch'
        if event_name.upper() in LEGACY_EVENT_NAMES:
            category, reasons = 'legacy_logging', ['legacy_event_name']
        elif not label:
            reasons = ['event_label_missing']
        elif not candidates and label in catalog.get('legacy_by_label', {}):
            category, reasons = 'legacy_logging', ['historical_label_still_collected']
        elif not candidates:
            category, reasons = 'unregistered', ['unregistered_label']
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
        if reasons:
            counts[platform]['categories'][category]['events'] += count
            counts[platform]['categories'][category]['labels'].add(label)
        version = obs.get('app_version') or ('WEB' if platform == 'WEB' else 'unknown')
        for reason in reasons:
            key = (category, label or '(missing)', reason)
            issue = issues[key]
            issue['count'] += count
            issue['versions'].add(version)
            issue['platforms'].add(platform)
            issue['event_names'].add(event_name)
            issue['platform_counts'][platform] += count
            issue['platform_versions'][platform].add(version)
            issue['platform_event_names'][platform].add(event_name)
    findings = []
    for (category, label, reason), data in sorted(issues.items()):
        contracts = (catalog.get('legacy_by_label', {}).get(label, []) or catalog['by_label'].get(label, [])) if category == 'legacy_logging' else catalog['by_label'].get(label, [])
        findings.append(dict(category=category, label=label, reason=reason, count=data['count'],
                             versions=sorted(data['versions']), platforms=sorted(data['platforms']),
                             event_names=sorted(data['event_names']), platform_counts=dict(data['platform_counts']),
                             platform_versions={p: sorted(v) for p, v in data['platform_versions'].items()},
                             platform_event_names={p: sorted(v) for p, v in data['platform_event_names'].items()},
                             specification_urls=sorted(set(x['url'] for x in contracts))))
    expected_pairs = {(label, p) for label, cs in catalog['by_label'].items() for c in cs for p in c['platforms']}
    platform_summary = {p: dict(events=v['events'], observed_labels=len(v['labels']), event_names=dict(v['event_names']),
                               categories={k: dict(events=c['events'], labels=len(c['labels'])) for k, c in v['categories'].items()}) for p, v in counts.items()}
    return dict(events=total, observed_labels=len(observed_labels), findings=findings,
                platform_summary=platform_summary,
                unobserved_labels=sorted(set(catalog['by_label']) - current_labels_seen),
                unobserved_platform_contracts=[dict(label=l, platform=p) for l, p in sorted(expected_pairs - observed_pairs)],
                snapshot_sha256=catalog['snapshot_sha256'],
                interpretation='Latest-spec mismatches are candidates; deployment/version cutovers are not inferred. Dynamic values are checked for presence only.')
