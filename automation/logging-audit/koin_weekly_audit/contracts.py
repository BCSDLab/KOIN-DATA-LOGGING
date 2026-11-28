import hashlib
import html
import json
import re
from collections import defaultdict
from .value_evidence import display_value, expected_value
from .source_value import source_values, contract_value_sources
from .normalization import normalize_observation
from .naming_correspondence import for_observation

FIELDS = ('설명', 'screen_view', 'event_name', 'event_label', 'value', 'event_category')
LEGACY_EVENT_NAMES = frozenset(('CAMPUS', 'BUSINESS', 'USER'))
CATEGORIES = ('unregistered', 'legacy_logging', 'current_mismatch')
PLATFORMS = ('IOS', 'ANDROID', 'WEB')
# A user-confirmed gesture exception; it never broadens another swipe contract.
ANDROID_PHOTO_SWIPE = 'real_estate__room_detail__photo_view__slide__swipe'


def clean(text):
    # Markdown literal angle brackets are prose, not HTML spanning later fields.
    text = text.replace(r'\<', '&lt;').replace(r'\>', '&gt;')
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\\([_*{}\[\]().~`<>#+=|-])', r'\1', text)
    return html.unescape(text.replace('**', '').replace('`', '').strip())


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
        labels.update(re.findall(r'(?<![A-Za-z0-9_])[a-z][a-z0-9_]*(?:__[a-z0-9_]+)+(?![A-Za-z0-9_])', value))
        labels.update(re.findall(r'["“”‘’\']\s*([A-Za-z][A-Za-z0-9_]*)\s*["“”‘’\']', value))
        literal = value.strip(' -”“‘’\'"')
        if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', literal):
            labels.add(literal)
    return sorted(labels)


def platform_scopes(text):
    """Read only explicit per-label rows under the platform contract heading."""
    scopes = {}
    active = False
    for line in clean(text).splitlines():
        if line.strip() == '### 플랫폼별 계약 범위':
            active = True
            continue
        if active and line.startswith('#'):
            active = False
        if not active:
            continue
        match = re.fullmatch(r'\s*\|\s*([a-z][a-z0-9_]*(?:__[a-z0-9_]+)+)\s*\|\s*(IOS|ANDROID|WEB|미확정|[A-Z, ]+)\s*\|\s*', line)
        if match:
            label, value = match.groups()
            values = None if value == '미확정' else sorted(set(v.strip() for v in value.split(',')))
            if values is not None and (not values or any(v not in PLATFORMS for v in values)):
                raise ValueError('Invalid explicit platform scope')
            if label in scopes:
                raise ValueError('Duplicate explicit platform scope')
            scopes[label] = values
    return scopes


def parse_page(page):
    """Do not infer deployment, enum values or version cutovers from prose."""
    if legacy_page(page):
        return [], 'legacy_document'
    text = page['text']
    scopes = platform_scopes(text)
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
            if current_key == 'value' and re.search(r'해주세요|해 주세요|부탁|따라 달리', line):
                continue  # Explanatory child note is not part of a literal/enum value.
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
        labels = re.findall(r'(?<![A-Za-z0-9_])[a-z][a-z0-9_]*(?:__[a-z0-9_]+)+(?![A-Za-z0-9_])', fields.get('event_label', ''))
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
            scope_pending = label in scopes and scopes[label] is None
            if label in scopes:
                platforms = scopes[label] or []
            permitted_swipe = ['ANDROID','IOS'] if label == ANDROID_PHOTO_SWIPE else ['IOS']
            swipe_policy_conflict = (action == 'swipe' or cats == ['swipe']) and (not platforms or any(p not in permitted_swipe for p in platforms))
            if action == 'swipe' or cats == ['swipe']:
                platforms = sorted(set(platforms)&set(permitted_swipe)) or ['IOS']
            raw_value = fields.get('value', '').strip(' ”“\'"')
            # Only unambiguous single literal values are checked as literals.
            fixed = raw_value if raw_value and len(raw_value) < 65 and not re.search(r'[{}<>/~():：]|예시|예:|ex\)|동적|STRING|INT|선택한|해당하는|실제|→', raw_value, re.I) else None
            choices = re.split(r'\s+(?:또는|or)\s+', raw_value, flags=re.I)
            allowed = sorted(set(x.strip(' \"“”‘’') for x in choices)) if len(choices) > 1 and all(x and len(x) < 65 and not re.search(r'[{}<>/~():：]|예시|예:|동적|STRING|INT|선택한|해당하는|실제|→', x, re.I) for x in choices) else []
            unspecified_value = raw_value in ('기존 미기재 유지', '미기재 유지', '기존 값 미기재 유지')
            if allowed or unspecified_value:
                fixed = None
            status = 'unresolved' if page.get('unresolved') else 'current'
            if len(names) != 1 or not screens or not categories:
                status = 'unresolved'
            label_screen = label.split('__')[1] if '__' in label else None
            selected_screens = [label_screen] if label_screen in screens else sorted(set(screens))
            if scope_pending or swipe_policy_conflict:
                status = 'unresolved'  # Source must explicitly agree with iOS-only swipe policy.
            contracts.append(dict(label=label, names=sorted(names), screens=selected_screens,
                                  categories=cats, platforms=platforms, value_required=bool(raw_value) and not unspecified_value,
                                  fixed_value=fixed, allowed_values=allowed, value_rule='enum' if allowed else 'fixed' if fixed else 'presence_only' if raw_value and not unspecified_value else 'unspecified',
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
        value_source = source_values(page)
        for contract in contracts:
            contract['value_source'] = value_source
            if value_source and 'value' not in contract['raw_fields']:
                contract['status'] = 'unresolved'
        coverage.append(dict(url=page['url'], title=page['title'], service=page.get('service'), status=status,
                             labels=[x['label'] for x in contracts], historical_labels=past, value_source=value_source))
        for label in past:
            reference = {k: page.get(k, '') for k in ('url', 'title', 'service')}
            if reference not in legacy_by_label[label]:
                legacy_by_label[label].append(reference)
        for contract in contracts:
            if contract not in by_label[contract['label']]:
                by_label[contract['label']].append(contract)
    conflicts = []
    for label, contracts in by_label.items():
        signatures = {json.dumps({k: c[k] for k in ('names', 'screens', 'categories', 'fixed_value', 'allowed_values')}, sort_keys=True) for c in contracts}
        # Platform-specific signatures need explicit resolution; accepting any would hide drift.
        if len(signatures) > 1 or any(c['status'] == 'unresolved' for c in contracts):
            conflicts.append(label)
    fingerprint = hashlib.sha256(json.dumps(pages, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return dict(by_label=dict(by_label), legacy_by_label=dict(legacy_by_label),
                conflicts=sorted(conflicts), coverage=coverage, snapshot_sha256=fingerprint)


def contract_failures(c, obs):
    bad = []
    if obs['event_name'] not in c['names']: bad.append('event_name_mismatch')
    if c['screens'] and obs.get('screen_view') not in c['screens']: bad.append('screen_view_mismatch')
    if c['categories'] and obs.get('event_category') not in c['categories']: bad.append('event_category_mismatch')
    if c['platforms'] and obs['platform'] not in c['platforms']: bad.append('platform_mismatch')
    if c['value_required'] and obs.get('value') in (None, ''): bad.append('value_missing')
    elif c.get('allowed_values') and obs.get('value') not in c['allowed_values']: bad.append('enum_value_mismatch')
    elif c['fixed_value'] is not None and obs.get('value') != c['fixed_value']: bad.append('fixed_value_mismatch')
    if obs.get('duplicate_param_keys', 0): bad.append('duplicate_parameter_key')
    return bad


def event_name_expectation(catalog, label, platform):
    contracts = [c for c in catalog['by_label'].get(label, []) if not c['platforms'] or platform in c['platforms']]
    if not contracts:
        return ['해당 label·플랫폼의 현행 명세 없음 — event_name 정답 미확정']
    names = sorted({name for c in contracts for name in c['names']})
    if len(names) == 1 and all(c['names'] for c in contracts):
        return names
    return ['원문 event_name 충돌·미확정: ' + (' / '.join(names) or '미기재') + ' — 담당자 확인 필요']


def compare(catalog, observations):
    issues = defaultdict(lambda: dict(count=0, versions=set(), platforms=set(), event_names=set(),
                                      platform_counts=defaultdict(int), platform_versions=defaultdict(set),
                                      platform_event_names=defaultdict(set), platform_dates=defaultdict(set), platform_observed_values=defaultdict(set),
                                      platform_value_counts=defaultdict(lambda: defaultdict(int))))
    observed_labels = set()
    observed_pairs = set()
    current_labels_seen = set()
    counts = {p: dict(events=0, labels=set(), categories={k: dict(events=0, labels=set()) for k in CATEGORIES},
                      event_names=defaultdict(int)) for p in PLATFORMS}
    total = 0
    for obs in observations:
        obs = normalize_observation(obs)
        event_name = obs['event_name']
        if event_name not in ('DA1', 'DA2') and event_name.upper() not in LEGACY_EVENT_NAMES and not obs.get('event_label') and not obs.get('event_label_parameter_present'):
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
        correspondence = for_observation(catalog, obs) if not candidates else None
        reasons = []
        category = 'current_mismatch'
        if event_name.upper() in LEGACY_EVENT_NAMES:
            category, reasons = 'legacy_logging', ['legacy_event_name']
        elif not label:
            reasons = ['event_label_missing']
        elif not candidates and label in catalog.get('legacy_by_label', {}):
            category, reasons = 'legacy_logging', ['historical_label_still_collected']
        elif not candidates and correspondence:
            reference = catalog['by_label'][correspondence['current_label']]
            reasons = ['previous_naming_label'] + min((contract_failures(c, obs) for c in reference), key=len)
        elif not candidates:
            category, reasons = 'unregistered', ['unregistered_label']
        elif label in catalog['conflicts']:
            reasons = ['specification_conflict']
        else:
            reasons = min((contract_failures(c, obs) for c in candidates), key=len)
        if event_name.upper() in LEGACY_EVENT_NAMES and not candidates:
            reasons.append('event_label_missing' if not label else 'historical_label_still_collected' if label in catalog.get('legacy_by_label', {}) else 'unregistered_label')
        if event_name.upper() in LEGACY_EVENT_NAMES and candidates and label not in catalog['conflicts']:
            other = min((contract_failures(c, obs) for c in candidates), key=len)
            reasons += [r for r in other if r != 'event_name_mismatch' and r not in reasons]
        if event_name not in ('DA1','DA2') and event_name.upper() not in LEGACY_EVENT_NAMES and 'event_name_mismatch' not in reasons:
            reasons.append('unexpected_event_name')
        if obs.get('duplicate_param_keys', 0) and 'duplicate_parameter_key' not in reasons:
            reasons.append('duplicate_parameter_key')
        if reasons:
            counts[platform]['categories'][category]['events'] += count
            counts[platform]['categories'][category]['labels'].add(label)
        version = obs.get('app_version') or ('WEB' if platform == 'WEB' else 'unknown')
        for reason in reasons:
            key = (category, label or '(missing)', reason)
            issue = issues[key]
            if correspondence:
                issue['naming_correspondence'] = correspondence
            issue['count'] += count
            issue['versions'].add(version)
            issue['platforms'].add(platform)
            issue['event_names'].add(event_name)
            issue['platform_counts'][platform] += count
            issue['platform_versions'][platform].add(version)
            if re.fullmatch(r'\d{8}', str(obs.get('event_date', ''))):
                issue['platform_dates'][platform].add(obs['event_date'])
            issue['platform_event_names'][platform].add(event_name)
            field = {'event_name_mismatch': 'event_name', 'legacy_event_name': 'event_name', 'unexpected_event_name':'event_name',
                     'screen_view_mismatch': 'screen_view', 'event_category_mismatch': 'event_category',
                     'platform_mismatch': 'platform', 'unregistered_label': 'event_label', 'previous_naming_label': 'event_label',
                     'historical_label_still_collected': 'event_label', 'event_label_missing': 'event_label'}.get(reason)
            if field:
                observed = obs.get(field)
                observed = '(누락)' if observed in (None, '') else str(observed)
                observed = observed if observed == '(누락)' or re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,159}', observed) else '(형식 오류)'
            elif reason == 'specification_conflict':
                observed = '; '.join(k + '=' + (str(obs.get(k)) if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,159}', str(obs.get(k))) else '(누락/형식 오류)') for k in ('event_name','screen_view','event_category'))
            elif reason == 'duplicate_parameter_key':
                observed = '중복 파라미터 키 ' + str(obs.get('duplicate_param_keys', 0)) + '개'
            else:
                observed = display_value(obs.get('value'), obs.get('value_parameter_present')) if reason in ('value_missing', 'fixed_value_mismatch', 'enum_value_mismatch') else '확인 필요'
            issue['platform_value_counts'][platform][observed] += count
            issue['platform_observed_values'][platform].add(observed)
    findings = []
    for (category, label, reason), data in sorted(issues.items()):
        correspondence = data.get('naming_correspondence')
        reference_label = correspondence['current_label'] if correspondence else label
        current_contracts = catalog['by_label'].get(reference_label, [])
        contracts = (catalog.get('legacy_by_label', {}).get(label, []) or current_contracts) if category == 'legacy_logging' else current_contracts
        expected_key = {'event_name_mismatch': 'names', 'legacy_event_name': 'names', 'screen_view_mismatch': 'screens',
                        'event_category_mismatch': 'categories', 'platform_mismatch': 'platforms'}.get(reason)
        expected = sorted({v for c in current_contracts for v in c.get(expected_key, [])}) if expected_key else []
        per_platform_expected = {}
        if reason in ('legacy_event_name','unexpected_event_name','event_name_mismatch'):
            per_platform_expected = {p:event_name_expectation(catalog,reference_label,p) for p in data['platforms']}
            expected = sorted({v for values in per_platform_expected.values() for v in values})
        if reason in ('value_missing', 'fixed_value_mismatch', 'enum_value_mismatch'):
            expected = expected_value(current_contracts)
        if reason == 'specification_conflict':
            expected = ['; '.join(k + '=' + ','.join(c.get(k, [])) for k in ('names','screens','categories','platforms')) + '; value=' + ','.join(expected_value([c])) for c in current_contracts]
        if reason == 'duplicate_parameter_key': expected = ['각 파라미터 키는 1개씩']
        if reason == 'previous_naming_label': expected = [reference_label]
        if reason == 'unregistered_label': expected = ['현행·과거 명세에 이 event_label 없음']
        if reason == 'historical_label_still_collected': expected = ['현행 명세의 event_label 사용 (과거 명세 링크 참고)']
        if reason == 'event_label_missing': expected = ['명세에 등록된 event_label 필수']
        field = {'legacy_event_name':'event_name','unexpected_event_name':'event_name','event_name_mismatch':'event_name','screen_view_mismatch':'screen_view','event_category_mismatch':'event_category','platform_mismatch':'platform','event_label_missing':'event_label','unregistered_label':'event_label','previous_naming_label':'event_label','historical_label_still_collected':'event_label','specification_conflict':'contract','duplicate_parameter_key':'event_params'}.get(reason, 'value')
        findings.append(dict(naming_correspondence=correspondence, field=field, category=category, label=label, reason=reason, count=data['count'],
                             versions=sorted(data['versions']), platforms=sorted(data['platforms']),
                             event_names=sorted(data['event_names']), platform_counts=dict(data['platform_counts']),
                             platform_versions={p: sorted(v) for p, v in data['platform_versions'].items()},
                             platform_dates={p: sorted(v) for p, v in data['platform_dates'].items()},
                             platform_event_names={p: sorted(v) for p, v in data['platform_event_names'].items()},
                             specification_urls=sorted(set(x['url'] for x in contracts)), expected_values=expected,
                             platform_expected_values=per_platform_expected,
                             platform_value_source={p:contract_value_sources(catalog,reference_label,p) for p in data['platforms']} if field == 'value' else {},
                             expectation_sources=[dict(url=c['url'],event_names=c['names'],platforms=c['platforms']) for c in current_contracts],
                             platform_observed_values={p: sorted(v) for p, v in data['platform_observed_values'].items()},
                             platform_value_counts={p: dict(v) for p, v in data['platform_value_counts'].items()}))
    expected_pairs = {(label, p) for label, cs in catalog['by_label'].items() for c in cs for p in c['platforms']}
    platform_summary = {p: dict(events=v['events'], observed_labels=len(v['labels']), event_names=dict(v['event_names']),
                               categories={k: dict(events=c['events'], labels=len(c['labels'])) for k, c in v['categories'].items()}) for p, v in counts.items()}
    return dict(events=total, observed_labels=len(observed_labels), findings=findings,
                platform_summary=platform_summary,
                unobserved_labels=sorted(set(catalog['by_label']) - current_labels_seen),
                unobserved_platform_contracts=[dict(label=l, platform=p) for l, p in sorted(expected_pairs - observed_pairs)],
                snapshot_sha256=catalog['snapshot_sha256'],
                interpretation='Latest-spec mismatches are candidates; deployment/version cutovers are not inferred. Dynamic values are checked for presence only.')

