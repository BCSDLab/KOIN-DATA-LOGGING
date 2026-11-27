"""Deterministic evidence summaries from this run's snapshots; no network or AI."""
import re
from collections import Counter, defaultdict
from .normalization import normalize_observation


GROUPS = ('event_date', 'app_version', 'event_name', 'screen_view', 'event_category')
CHECKS = {
    'unregistered_label': '고정된 명세 커밋의 현행·과거 목록과 SDK의 label 철자를 확인하세요.',
    'historical_label_still_collected': '관측 버전의 배포일과 새 로깅 전환 범위를 확인하세요. 과거 데이터는 자동 수정하지 않습니다.',
    'legacy_event_name': 'CAMPUS·BUSINESS·USER의 신규 전송 경로와 해당 버전의 전환 계획을 확인하세요.',
    'event_name_mismatch': '이 label·플랫폼의 명세 event_name과 해당 버전 SDK의 전송 설정을 대조하세요.',
    'unexpected_event_name': '실제 event_name의 철자와 전송 네임스페이스를 확인하세요.',
    'screen_view_mismatch': '화면 전환 전후 중 어느 시점에 screen_view를 설정하는지 확인하세요.',
    'event_category_mismatch': '버튼 클릭과 제스처를 구분한 명세 및 SDK의 category 설정을 확인하세요.',
    'platform_mismatch': '명세의 플랫폼 메타데이터와 본문의 지원 범위를 확인하세요. SDK 오류로 단정하지 않습니다.',
    'value_missing': '해당 버전의 필수 value 설정과 파라미터 존재·NULL·빈 문자열 처리를 확인하세요.',
    'fixed_value_mismatch': '명세의 고정 value와 실제 동작의 의미를 확인하세요. 다른 동작을 같은 label로 보내는지도 검토하세요.',
    'enum_value_mismatch': '명세의 허용값과 플랫폼별 전송 분기를 확인하세요.',
    'specification_conflict': '명세 담당자에게 충돌·미확정 계약의 해석을 확인하세요. 임의의 정답을 선택하지 않습니다.',
    'duplicate_parameter_key': 'SDK의 공통 파라미터와 개별 이벤트 파라미터가 중복 추가되는지 확인하세요.',
    'event_label_missing': 'SDK 공통 전송 함수에서 event_label이 누락되는 분기를 확인하세요.',
}


def identifier(value, field=None):
    if value in (None, ''):
        return '(missing)'
    text = str(value)
    if text == '(missing)':
        return text
    pattern = r'\d{8}' if field == 'event_date' else r'\d{1,4}(?:\.\d{1,4}){1,3}' if field == 'app_version' else r'[A-Za-z][A-Za-z0-9_]{0,255}'
    return text if re.fullmatch(pattern, text) else '(invalid identifier)'


def breakdown(rows, field):
    counts = Counter()
    for row in rows:
        counts[identifier(row.get(field), field)] += int(row['event_count'])
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return dict(total_events=sum(counts.values()),
                groups=[dict(key=key, events=count) for key, count in ordered[:30]],
                omitted_groups=max(0, len(ordered) - 30),
                omitted_events=sum(count for _, count in ordered[30:]))


def investigate(catalog, report, rows, limit=4):
    """Cover each affected platform first, then highest single-rule event counts."""
    if not report.get('complete'):
        return dict(mode='rules', status='skipped', reason='AuditIncomplete', external_ai_called=False)
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError('Invalid investigation limit')
    groups = defaultdict(list)
    for finding in report.get('findings', []):
        for platform in finding['platforms']:
            groups[(finding['label'], platform)].append(finding)
    ordered = sorted(groups, key=lambda key: (
        -max(f['platform_counts'][key[1]] for f in groups[key]), key[1], key[0]))
    selected, covered = [], set()
    for key in ordered:
        if key[1] not in covered and len(selected) < limit:
            selected.append(key)
            covered.add(key[1])
    selected.extend(key for key in ordered if key not in selected)
    selected = selected[:limit]
    row_index = defaultdict(list)
    for original in rows:
        row = normalize_observation(original)
        row_index[(row.get('event_label') or '(missing)', row.get('platform'))].append(row)
    investigations = []
    for label, platform in selected:
        evidence_rows = row_index[(label, platform)]
        reasons = sorted(groups[(label, platform)], key=lambda f: f['reason'])
        contracts = [c for c in catalog['by_label'].get(label, [])
                     if not c['platforms'] or platform in c['platforms']]
        fields = ('names', 'screens', 'categories', 'platforms', 'status', 'url')
        dates = sorted({r['event_date'] for r in evidence_rows
                        if re.fullmatch(r'\d{8}', str(r.get('event_date', '')))})
        investigations.append(dict(
            id='R' + str(len(investigations) + 1), label=identifier(label), platform=identifier(platform),
            observed_events=sum(int(r['event_count']) for r in evidence_rows),
            largest_single_rule_events=max(f['platform_counts'][platform] for f in reasons),
            reasons=[dict(reason=f['reason'], events=f['platform_counts'][platform]) for f in reasons],
            first_observed_date=dates[0] if dates else None,
            last_observed_date=dates[-1] if dates else None,
            breakdowns={field: breakdown(evidence_rows, field) for field in GROUPS},
            contracts=[{field: c[field] for field in fields if field in c} for c in contracts],
            historical_sources=catalog.get('legacy_by_label', {}).get(label, []),
            checks=list(dict.fromkeys(CHECKS.get(f['reason'], 'SDK 전송 설정과 명세를 확인하세요.') for f in reasons)),
            query_job_id=report.get('query_job_id'), source_revision=report.get('source_revision')))
    return dict(mode='rules', status='completed', external_ai_called=False,
                investigations=investigations, total_label_platform_findings=len(ordered),
                investigated_label_platforms=len(investigations),
                limitations=[
                    '전체 이상 판정은 규칙 목록에 보존하며 상세 분석은 플랫폼을 우선 배분한 상위 항목 표본입니다.',
                    '관측 총건수는 해당 label 전체 수집이며 오류 건수와 다릅니다. 사유별 건수는 서로 겹칠 수 있어 합산하지 않습니다.',
                    '최초·최종 날짜는 이번 조회 범위의 관측일이며 실제 배포일이나 최초 발생일이 아닙니다.',
                    '확인 항목은 고정 규칙 안내이며 원인 확정이나 AI 추론 결과가 아닙니다. 동적 value·사용자 행동·미관측 구현은 검증하지 않습니다.'])
