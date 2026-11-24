"""Use confirmed release targets, never infer a release from the largest log version."""
import json
import re
from collections import defaultdict
from pathlib import Path


class VersionScopeError(RuntimeError):
    pass


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{1,4}\.\d{1,4}\.\d{1,4}', value):
        return None
    return tuple(map(int, value.split('.')))


def targets_for(environment, path=None):
    policy = json.loads(Path(path or Path(__file__).resolve().parents[1] / 'app-versions.json').read_text(encoding='utf8'))
    targets = policy.get(environment, {})
    if set(targets) != {'IOS', 'ANDROID'} or not all(version(v) for v in targets.values()):
        raise VersionScopeError('Confirmed mobile versions are required')
    return dict(targets)


def select_scope(rows, targets):
    if set(targets) != {'IOS', 'ANDROID'} or not all(version(v) for v in targets.values()):
        raise VersionScopeError('Invalid mobile targets')
    selected, groups = [], defaultdict(lambda: dict(events=0, labels=set()))
    for row in rows:
        platform = row.get('platform')
        if platform not in targets or row.get('app_version') == targets[platform]:
            selected.append(row)
            continue
        actual = row.get('app_version')
        parsed = version(actual)
        kind = 'older' if parsed and parsed < version(targets[platform]) else 'newer_or_other' if parsed else 'unknown'
        # Only version identifiers and aggregate counts are retained, never raw event values.
        key = (platform, actual if parsed else '(버전 미확인)', kind)
        groups[key]['events'] += int(row['event_count'])
        groups[key]['labels'].add(row.get('event_label'))
    reference = [dict(platform=p, app_version=v, classification=kind, events=g['events'], labels=len(g['labels']))
                 for (p, v, kind), g in sorted(groups.items())]
    return selected, dict(targets=dict(targets), reference=reference,
                          excluded_events=sum(g['events'] for g in reference))
