# 주간 로깅 검수 · Notion → BigQuery → Slack

Airflow·Docker·Tailscale·개인 PC 없이 GitHub Actions에서 실행합니다.

## 일정과 검수 범위

- 예약: 월요일 09:00 KST (`0 0 * * 1`, UTC). GitHub 예약 실행은 대기열 등으로 늦어질 수 있어 정각 전달을 보장하지 않습니다.
- Stage: `koin-stage-438512.analytics_427218788`.
- Production: `kap-chat.analytics_432041405`.
- WEB·ANDROID·IOS의 **DA1·DA2 전체**를 현행 명세와 비교합니다. 추가로 기존 event_name **CAMPUS·BUSINESS·USER**가 수집되는 경우도 감지합니다(대소문자 무관). 그 외 event_name은 제외합니다.
- 직전 완료된 월요일~일요일 7일의 daily export를 검사합니다. 이전 기간 마지막 3일도 지연 도착 확인을 위해 재검사합니다. intraday와 daily를 중복 합산하지 않습니다.
- 현재 Event Log 루트 `f820221954bc82cfbe7e813b975c5be1`에서 서비스·DB·하위 블록을 찾고, saved view 필터 없이 전체 행을 페이지네이션으로 조회합니다. `Event Log (과거)` 보관본은 중복 집계하지 않습니다.
- 레거시 서비스와 과거 로깅 구간의 명시적 event_label도 읽어 과거 label 목록을 만듭니다. 새 event_name·label을 임의로 만들거나 기존 명세를 수정하지 않습니다.
- 매번 최신 Notion을 읽습니다. GitHub Markdown이나 과거 ZIP을 최신 명세 대신 사용하는 fallback은 없습니다.

## 자동 판정과 한계

Stage·Prod 각각의 메시지 안에 **IOS / ANDROID / WEB 세 플랫폼을 항상 표시**하고, 플랫폼별로 다음 세 유형을 구분합니다. 해당 플랫폼에 로그가 없어도 `수집 0건`을 표시하며, 조회가 실패한 경우에는 0건이 아니라 `미확인`으로 표시합니다.

| 유형 | 판정 |
| --- | --- |
| ① 미등록 로그 | DA1·DA2의 label이 현행·과거 명세 모두에 없음 |
| ② 과거 로깅 지속 수집 | DA1·DA2에서 과거에만 있는 label 수집, 또는 event_name이 CAMPUS·BUSINESS·USER |
| ③ 현행 명세 불일치·검토 | 현행 계약의 필드·플랫폼·고정값 불일치, label 누락, 명세 충돌·미확정 |

label이 현행과 과거에 모두 있으면 현행 계약을 우선합니다. 단, CAMPUS·BUSINESS·USER는 label이 현행과 같아도 기존 event_name 수집으로 알립니다. 과거 label은 과거 구간의 `event_label` 필드 또는 명시적으로 레거시인 문서에서 읽으며 설명 문장에서 추측하지 않습니다. 레거시 상태 문서의 새 정의도 현행 허용 목록으로 자동 승격하지 않습니다.

발생 건수는 플랫폼별 실제 건수이며, 한 로그에 여러 필드 오류가 있어도 유형별 발생 건수를 중복 합산하지 않습니다. 상세 오류 항목 수와 발생 로그 건수는 서로 다른 지표입니다. 과거 로그가 구버전의 정상 동작일 수 있으므로 앱 버전·적용 시점은 담당자가 함께 확인합니다.

event_label 등록 여부, event_name·screen_view·category·플랫폼 불일치, 필수 value 누락, 명확한 단일 고정 value 불일치, 중복 파라미터 키를 검사합니다. 여러 계약이 충돌하거나 강제 업데이트 이탈처럼 미확정인 경우에는 명세 검토 대상으로 표시합니다.

동적 value는 존재 여부만 확인합니다. 실제 매물명·게시글 원본과의 일치, 임의 파라미터 전체의 타입·허용값, 사용자 동작 1회당 전송 1회 여부까지 검증했다고 표시하지 않습니다. 배포 버전·적용일이 명세에 없으면 최신 명세 불일치 후보로 보고하며 구버전 오류로 단정하지 않습니다. 미관측은 구현 누락이 아닙니다. WEB의 PC/모바일 구분은 GA4 platform 값만으로 확정하지 않습니다.

Notion 전체 조회 실패·미지원 블록·소스 범위 축소(22개 미만 데이터 소스 또는 700행 미만)·BigQuery 테이블 누락·권한 오류는 **검수 불완전**입니다. 과거·참조·미해석 페이지 수와 플랫폼별 미관측 계약을 따로 공개합니다. 정당하게 문서 구조를 대폭 변경했다면 최소 범위 검사를 함께 검토해야 합니다.

## 처음 한 번 필요한 연결

저장소 Settings → Secrets and variables → Actions에 아래 값을 설정합니다. 비밀값은 채팅·소스·PR에 붙이지 않습니다. 연결된 GitHub 도구에서는 관리용 Secrets API를 지원하지 않으므로 저장소 관리자가 설정해야 합니다.

| 종류 | 이름 | 내용 |
| --- | --- | --- |
| Secret | `NOTION_LOGGING_READ_TOKEN` | 해당 Event Log 전체 하위 페이지를 읽도록 연결한 Notion 내부 Integration 토큰. 읽기 전용 |
| Secret | `SLACK_LOGGING_AUDIT_WEBHOOK` | 기존 `#코인_이벤트알림` 채널로 연결된 Incoming Webhook URL |
| Variable | `GCP_AUDIT_WIF_PROVIDER` | 권장: 이 저장소 main 전용 Workload Identity Provider 전체 경로 |
| Variable | `GCP_AUDIT_SERVICE_ACCOUNT` | 위 Provider에서 사용할 전용 검수 서비스 계정 이메일 |
| Secret | `GCP_AUDIT_CREDENTIALS_JSON` | WIF가 없는 경우에만 사용: 기존 전용 읽기 계정의 JSON 키. WIF 설정 시 사용하지 않음 |

GCP 인증은 WIF 두 Variable 또는 전용 JSON Secret 중 **한 방식만** 준비하면 됩니다. 검수 계정은 두 원천 데이터셋의 `BigQuery Data Viewer`와 두 query 실행 프로젝트의 `BigQuery Job User`가 필요합니다. 원천 데이터 수정 권한은 필요하지 않습니다. WIF 신뢰 조건은 `BCSDLab/KOIN-DATA-LOGGING`의 main 브랜치로 제한해야 합니다. fork/임의 저장소의 인증을 허용하지 않습니다.

현재 채팅의 MCP 로그인이나 Airflow에 저장한 Slack 연결이 GitHub runner로 자동 전달되지는 않습니다. GitHub 환경에서 위 연결을 별도로 설정해야 합니다. 새 권한·계정·토큰 생성은 이 PR에서 수행하지 않습니다.

## 활성화와 최초 시험

1. 코드 검사 통과 후 기본 브랜치 main에 반영합니다. schedule 이벤트는 기본 브랜치의 workflow를 사용합니다.
2. 위 연결을 준비하고 Actions의 **주간 로깅 검수 → Run workflow**로 먼저 `send_slack=false` 실행합니다.
3. Notion 전체 행 수, 미해석 목록, 두 환경 조회와 상세 결과를 확인합니다.
4. `send_slack=true`로 실행해 Stage/Prod 메시지 2개가 기존 채널에 도착하는지 확인합니다.
5. 정기 실행을 확인합니다. 실패한 작업을 정상 전달로 표시하지 않습니다. 인증 미설정 상태에서는 자동 검수가 준비 완료된 것이 아닙니다.

수동 `week_start`는 검수 대상 주의 월요일(YYYY-MM-DD)입니다. 비우면 직전 완료 주를 선택합니다. workflow에는 secrets를 사용하는 PR 트리거나 pull_request_target 실행이 없습니다.

## 결과·비용·중복

- 상세 JSON, 명세 snapshot, 전송문은 실행의 `logging-audit-results` artifact에 35일 보관합니다. 결과 링크를 Slack에 첨부합니다.
- Slack에는 개인 ID·이메일·원본 event value를 넣지 않습니다. 조회 결과 원본은 artifact로 올리지 않습니다. schema 식별자·버전·발생 건수·명세 링크를 사용합니다.
- GCP 쿼리는 SELECT뿐이며 날짜 제한과 환경별 5 GiB 청구 상한이 있습니다. BigQuery 조회 및 private 저장소 Actions 실행·artifact는 계정의 무료 할당량을 넘으면 비용이 생길 수 있습니다. Notion 읽기·Slack 메시지 기능의 별도 유료 업그레이드는 이 코드의 요구사항이 아닙니다.
- 같은 주의 전송 영수증을 Actions cache로 복원해 수동 재실행의 중복 알림을 억제합니다. Slack 응답이 유실되면 delivery_unknown으로 보존하고 자동 재전송하지 않습니다.
- runner 강제 종료·cache 유실·만료를 포함한 정확히 한 번 전송은 보장하지 않습니다. 같은 주를 다시 전송해야 할 경우 채널 수신 상태와 cache를 담당자가 확인해야 합니다.
- GitHub 자체의 장애, checkout/runner 시작 실패처럼 검수 코드가 실행되지 않는 경우 Slack 실패 알림도 보장할 수 없습니다. Actions 실패 알림을 함께 확인합니다.

## 개발 검증

```sh
cd automation/logging-audit
python -m unittest discover -s tests -v
```

규칙·무필터 페이지네이션·다중 label·WEB 모바일 표기·click/swipe·미확정 충돌·환경별 실패 격리·주간 날짜·비밀값 비노출·재전송 억제를 검사합니다. 실제 Notion Integration·GCP 인증·Slack 수신은 연결 설정 후 별도 검증합니다.
