"""Comparison-only Android debug identifiers; never rewrite collected payloads."""


def normalize_observation(row):
    result = dict(row)
    if row.get('platform') != 'ANDROID' or 'raw_identifiers' in row:
        return result
    raw = {}
    for field in ('event_name', 'event_label', 'event_category'):
        value = row.get(field)
        if not isinstance(value, str):
            continue
        normalized = value
        if field == 'event_label' and value.endswith(' (debug)'):
            normalized = value[:-8]
        elif value.endswith('_debug'):
            normalized = value[:-6]
        if normalized != value:
            raw[field] = value
            result[field] = normalized
    if raw:
        result['raw_identifiers'] = raw
    return result


def normalization_summary(rows):
    normalized = [normalize_observation(row) for row in rows]
    return dict(android_debug_events=sum(int(row['event_count']) for row in normalized
                                         if row.get('raw_identifiers')),
                policy='ANDROID only: remove one terminal _debug or label (debug) for comparison; raw identifiers retained')
