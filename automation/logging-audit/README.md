# 주간 로깅 검수 · GitHub main → BigQuery → Slack

Airflow·Docker·Tailscale·개인 PC 없이 GitHub Actions에서 실행합니다.

## AI 조사 에이전트

규칙 검수 후 OpenAI **Agents API**가 Stage·Prod 각각에서 조사할 항목과 후속 도구를 선택합니다. 한 번의 요약 요청으로 끝내지 않고, 명세 조회와 날짜·앱 버전별 집계를 반복해 중요한 1~4개 항목의 관측·원인 가설·다음 확인을 작성합니다. 모든 로그를 검사하는 규칙 결과와 중요한 항목을 표본 조사하는 AI 결과는 구분합니다.

- `list_findings`: 플랫폼별 규칙 판정 목록을 8개씩 확인합니다.
- `read_contract`: 이번 실행의 GitHub main snapshot에서 현행/과거 계약을 확인합니다. 원문 지시나 raw value를 모델에 전달하지 않습니다.
- `breakdown`: 이미 조회한 BigQuery 결과를 선택한 label·플랫폼의 날짜/버전/event_name/screen_view/category별로 다시 집계합니다. 새 SQL 조회는 실행하지 않습니다.

도구 응답에 근거 ID(E1 등)를 부여하고 최종 답변의 근거 ID가 실제 응답에 있는지 검사합니다. Slack에는 짧은 요약을 표시하며, 관측·가설·다음 확인과 근거 번호 및 집계·query job ID·명세 출처는 report artifact에서 확인합니다. 근거 ID의 존재 검사는 AI 문장 전체가 사실임을 보장하지 않으므로 가설은 담당자 검토 대상입니다.

샌드박스 없는 `environment.type=none`이며 도구 호출은 GitHub runner가 처리합니다. AI에는 SQL 작성·명세 변경·쉘 실행·Slack 직접 전송 도구가 없습니다. 환경별 최대 12회 도구 호출, 약 180초 조사 제한(진행 중 HTTP 요청은 최대 30초 추가), 항목/출력 크기 제한을 적용합니다. 중단 시 취소와 세션 삭제를 시도하며 정리 실패는 세션 ID와 함께 표시합니다. 세션/turn ID·토큰 사용량(제공된 경우)도 결과에 기록합니다. 모델/API를 자동으로 바꾸거나 실패를 정상으로 간주하지 않습니다.

API 키·권한·요금 한도·모델 접근 오류 또는 근거 없는 출력이면 **AI 추가 조사 미확인**으로 알리고 기존 규칙 집계는 유지합니다. 규칙 검수와 요청한 Slack 전송이 완료되면 Actions는 성공으로 표시하고, AI 추가 조사 실패는 별도 경고로 남깁니다. 명세 수집·BigQuery 조회·Slack 전송 실패는 계속 실행 실패로 표시합니다. 원본 event value·사용자 ID는 OpenAI 입력이나 조사 도구 응답에 포함하지 않습니다. 상세 보고서에는 고정·열거형 UI value의 실제 값과 건수를 표시하며, 동적 value와 민감정보 가능 값은 제외하거나 가립니다. event label·정규화된 계약·집계·앱 버전 등의 메타데이터는 OpenAI API로 전달됩니다.

## 일정과 검수 범위

- 예약: 월요일 09:00 KST (`0 0 * * 1`, UTC). GitHub 예약 실행은 대기열 등으로 늦어질 수 있어 정각 전달을 보장하지 않습니다.
- Stage: `koin-stage-438512.analytics_427218788`.
- Production: `kap-chat.analytics_432041405`.
- WEB·ANDROID·IOS의 **DA1·DA2 전체**를 현행 명세와 비교합니다. 추가로 기존 event_name **CAMPUS·BUSINESS·USER**가 수집되는 경우도 감지합니다(대소문자 무관). 그 외 event_name은 제외합니다.
- 직전 완료된 월요일~일요일 7일의 daily export를 검사합니다. 이전 기간 마지막 3일도 지연 도착 확인을 위해 재검사합니다. intraday와 daily를 중복 합산하지 않습니다.
- 실행 시 main 커밋으로 고정된 checkout에서 `event-log/**/*.md` 전체를 읽습니다. README 목차와 `_archive` 이전 자료는 현행 허용 목록에 넣지 않습니다. 문서 안 과거 구간과 레거시 서비스는 과거 label 감지용으로 읽습니다. 소스 링크는 동일 커밋에 고정합니다.
- 레거시 서비스와 과거 로깅 구간의 명시적 event_label도 읽어 과거 label 목록을 만듭니다. 새 event_name·label을 임의로 만들거나 기존 명세를 수정하지 않습니다.
- 검수 기준은 GitHub main입니다. Notion API·토큰은 사용하지 않습니다. Notion만 수정한 내용이나 미병합 PR은 검수 기준에 반영되지 않습니다. 명세를 main에 병합한 후 다음 실행에서 반영됩니다.

## 자동 판정과 한계

Stage·Prod 각각의 메시지 안에 **IOS / ANDROID / WEB 세 플랫폼을 항상 표시**하고, 플랫폼별로 다음 세 유형을 구분합니다. 해당 플랫폼에 로그가 없어도 `수집 0건`을 표시하며, 조회가 실패한 경우에는 0건이 아니라 `미확인`으로 표시합니다.

| 유형 | 판정 |
| --- | --- |
| ① 미등록 로그 | DA1·DA2의 label이 현행·과거 명세 모두에 없음 |
| ② 과거 로깅 지속 수집 | DA1·DA2에서 과거에만 있는 label 수집, 또는 event_name이 CAMPUS·BUSINESS·USER |
| ③ 현행 명세 불일치·검토 | 현행 계약의 필드·플랫폼·고정값 불일치, label 누락, 명세 충돌·미확정 |

label이 현행과 과거에 모두 있으면 현행 계약을 우선합니다. 단, CAMPUS·BUSINESS·USER는 label이 현행과 같아도 기존 event_name 수집으로 알립니다. 과거 label은 과거 구간의 `event_label` 필드 또는 명시적으로 레거시인 문서에서 읽으며 설명 문장에서 추측하지 않습니다. 레거시 상태 문서의 새 정의도 현행 허용 목록으로 자동 승격하지 않습니다.

한 페이지의 여러 계약은 각각 보존합니다. 화면별 계약 뒤에서 한 번만 선언된 공통 필드는 페이지 내 값이 유일할 때만 누락된 계약에 상속하고, 모호한 필수 필드는 미등록으로 오인하지 않고 명세 검토 대상으로 표시합니다. 기존 event_name만 수집된 경우에는 해당 label의 DA1·DA2 현행 계약이 관측된 것으로 계산하지 않습니다.

발생 건수는 플랫폼별 실제 건수이며, 한 로그에 여러 필드 오류가 있어도 유형별 발생 건수를 중복 합산하지 않습니다. 상세 오류 항목 수와 발생 로그 건수는 서로 다른 지표입니다. 과거 로그가 구버전의 정상 동작일 수 있으므로 앱 버전·적용 시점은 담당자가 함께 확인합니다.

event_label 등록 여부, event_name·screen_view·category·플랫폼 불일치, 필수 value 누락, 명확한 단일 고정 value 불일치, 중복 파라미터 키를 검사합니다. 여러 계약이 충돌하거나 강제 업데이트 이탈처럼 미확정인 경우에는 명세 검토 대상으로 표시합니다.

동적 value는 존재 여부만 확인합니다. 실제 매물명·게시글 원본과의 일치, 임의 파라미터 전체의 타입·허용값, 사용자 동작 1회당 전송 1회 여부까지 검증했다고 표시하지 않습니다. 배포 버전·적용일이 명세에 없으면 최신 명세 불일치 후보로 보고하며 구버전 오류로 단정하지 않습니다. 미관측은 구현 누락이 아닙니다. WEB의 PC/모바일 구분은 GA4 platform 값만으로 확정하지 않습니다.

GitHub 추적 문서 누락·커밋 불일치·소스 범위 축소(21개 미만 서비스 또는 700개 미만 문서)·BigQuery 테이블 누락·권한 오류는 **검수 불완전**입니다. 과거·참조·미해석 페이지 수와 플랫폼별 미관측 계약을 따로 공개합니다. 정당하게 문서 구조를 대폭 변경했다면 최소 범위 검사를 함께 검토해야 합니다.

## 처음 한 번 필요한 연결

저장소 Settings → Secrets and variables → Actions에 아래 값을 설정합니다. 비밀값은 채팅·소스·PR에 붙이지 않습니다. 연결된 GitHub 도구에서는 관리용 Secrets API를 지원하지 않으므로 저장소 관리자가 설정해야 합니다.

| 종류 | 이름 | 내용 |
| --- | --- | --- |
| Secret | `SLACK_LOGGING_AUDIT_STAGE_WEBHOOK` | Stage 채널에 연결된 전용 Incoming Webhook URL. 기존 운영 채널 웹훅을 넣지 않습니다 |
| Secret | `OPENAI_API_KEY` | OpenAI 프로젝트 API 키. Agents 읽기·쓰기 및 모델 추론 권한과 사용 가능한 API 잔액/한도 필요 |
| Variable | `OPENAI_AGENT_MODEL` | 선택 사항. 기본 `gpt-6-astra`(공식 Agents quickstart 기준). 프로젝트 접근 가능 여부는 실제 실행에서 확인 |
| Variable | `GCP_AUDIT_WIF_PROVIDER` | 권장: 이 저장소 main 전용 Workload Identity Provider 전체 경로 |
| Variable | `GCP_AUDIT_SERVICE_ACCOUNT` | 위 Provider에서 사용할 전용 검수 서비스 계정 이메일 |
| Secret | `GCP_AUDIT_CREDENTIALS_JSON` | WIF가 없는 경우에만 사용: 기존 전용 읽기 계정의 JSON 키. WIF 설정 시 사용하지 않음 |

GCP 인증은 WIF 두 Variable 또는 전용 JSON Secret 중 **한 방식만** 준비하면 됩니다. 검수 계정은 두 원천 데이터셋의 `BigQuery Data Viewer`와 두 query 실행 프로젝트의 `BigQuery Job User`가 필요합니다. 원천 데이터 수정 권한은 필요하지 않습니다. WIF 신뢰 조건은 `BCSDLab/KOIN-DATA-LOGGING`의 main 브랜치로 제한해야 합니다. fork/임의 저장소의 인증을 허용하지 않습니다.

현재 채팅의 MCP 로그인이나 Airflow에 저장한 Slack 연결이 GitHub runner로 자동 전달되지는 않습니다. GitHub 환경에서 위 연결을 별도로 설정해야 합니다. 새 권한·계정·토큰 생성은 이 PR에서 수행하지 않습니다.

## 활성화와 최초 시험

1. 코드 검사 통과 후 기본 브랜치 main에 반영합니다. schedule 이벤트는 기본 브랜치의 workflow를 사용합니다.
2. 위 연결을 준비하고 Actions의 **주간 로깅 검수 → Run workflow**로 먼저 `send_slack=false` 실행합니다.
3. GitHub 명세 파일 수, 미해석 목록, 두 환경 조회와 AI의 실제 완료·도구 호출·근거·세션 정리 결과를 확인합니다. `send_slack=false`도 OpenAI API를 호출하므로 API 비용이 발생할 수 있습니다.
4. `send_slack=true`로 실행해 Stage/Prod 메시지 2개가 기존 채널에 도착하는지 확인합니다.
5. 정기 실행을 확인합니다. 실패한 작업을 정상 전달로 표시하지 않습니다. 인증 미설정 상태에서는 자동 검수가 준비 완료된 것이 아닙니다.

수동 `week_start`는 검수 대상 주의 월요일(YYYY-MM-DD)입니다. 비우면 직전 완료 주를 선택합니다. workflow에는 secrets를 사용하는 PR 트리거나 pull_request_target 실행이 없습니다.

## 결과·비용·중복

- 상세 JSON, 명세 snapshot, 전송문은 실행의 `logging-audit-results` artifact에 35일 보관합니다. 결과 링크를 Slack에 첨부합니다.
- Slack에는 개인 ID·이메일·원본 event value를 넣지 않습니다. 조회 결과 원본은 artifact로 올리지 않습니다. schema 식별자·버전·발생 건수·명세 링크를 사용합니다.
- GCP 쿼리는 SELECT뿐이며 날짜 제한과 환경별 5 GiB 청구 상한이 있습니다. BigQuery 조회 및 private 저장소 Actions 실행·artifact는 계정의 무료 할당량을 넘으면 비용이 생길 수 있습니다. Slack 메시지 기능의 별도 유료 업그레이드는 이 코드의 요구사항이 아닙니다.
- OpenAI API는 ChatGPT 구독과 별도로 과금됩니다. 도구 횟수·시간 제한은 금액 상한 보장이 아닙니다. OpenAI 프로젝트의 사용량·예산/지출 제한을 별도로 관리해야 합니다.
- 같은 주의 전송 영수증을 Actions cache로 복원해 수동 재실행의 중복 알림을 억제합니다. Slack 응답이 유실되면 delivery_unknown으로 보존하고 자동 재전송하지 않습니다.
- runner 강제 종료·cache 유실·만료를 포함한 정확히 한 번 전송은 보장하지 않습니다. 같은 주를 다시 전송해야 할 경우 채널 수신 상태와 cache를 담당자가 확인해야 합니다.
- GitHub 자체의 장애, checkout/runner 시작 실패처럼 검수 코드가 실행되지 않는 경우 Slack 실패 알림도 보장할 수 없습니다. Actions 실패 알림을 함께 확인합니다.

## 개발 검증

```sh
cd automation/logging-audit
python -m unittest discover -s tests -v
```

규칙·무필터 페이지네이션·다중 label·WEB 모바일 표기·click/swipe·미확정 충돌·환경별 실패 격리·주간 날짜·비밀값 비노출·재전송 억제를 검사합니다. 실제 GitHub checkout·GCP 인증·Slack 수신은 연결 설정 후 별도 검증합니다.

AI 테스트는 가짜 API 세션으로 도구 선택·근거 검증·실패·취소·정리를 재현합니다. 이 테스트나 Secret 등록만으로 실제 Agents API 접근 및 Slack 전달이 검증된 것은 아닙니다. API 계약은 [공식 Agents 문서](https://developers.openai.com/api/docs/guides/agents-api/quickstart)와 설치한 `openai==3.13.0` SDK의 session/event/items 형식을 확인했습니다.

## 주간 알림과 상세보기

매주 월요일 09:00 KST에 직전 월요일~일요일 7일을 검사합니다. GitHub Actions 예약은 대기열에 따라 지연될 수 있습니다. 현재 Stage·Prod 두 결과 모두 `SLACK_LOGGING_AUDIT_STAGE_WEBHOOK`에 연결된 `코인_이벤트알림_stage` 채널로 보냅니다. 기존 운영 웹훅으로 대체하지 않습니다.

Slack은 iOS·Android·Web별로 수집된 로그가 명세에 맞으면 `이상 없음`, 문제가 있으면 `이상·확인 필요 N개 label`을 표시합니다. 수집 0건은 `판정 대상 없음`, 조회 실패는 `판정 불가`입니다. 미관측 명세를 구현 누락으로 단정하지 않습니다. AI 부가 조사 실패를 로깅 오류로 표시하지 않습니다.

`상세보기`는 해당 GitHub Actions 작업의 상세 보고서 위치로 바로 연결됩니다. 보고서 첫 화면의 환경·플랫폼 목차에서 문제 목록을 선택할 수 있습니다. 플랫폼별 전체 문제 목록을 생략 없이 보여주며 event_label, 미등록·과거·불일치 사유, 명세 값, 실제 수집 값, 발생 건수, 앱 버전, 해당 커밋의 명세 링크를 확인할 수 있습니다. Slack에 일부 label 예시만 표시하고 전체는 ZIP에서 찾도록 하던 방식을 대체합니다.

명세 충돌·미확정은 앱 오류로 단정하지 않고 담당자 확인 대상으로 구분합니다. 실제 event value와 개인 ID는 표시하지 않습니다. value는 필수값 누락·명확한 고정값 불일치만 판단하고 동적 값의 내용은 검증하지 않습니다. 규칙에 없는 임의 추가 파라미터 전체의 타입 검사도 포함하지 않습니다.

이전 기간 마지막 3일의 지연 수집 재검사는 별도 상태로 기록합니다. 이전 날짜의 테이블 누락이 이번 주 전체 검수 결과를 무효화하지 않습니다. 이번 주 테이블이 누락되면 정상 판정을 하지 않습니다.

알림 형식 v6 적용 후 첫 실행은 새 형식으로 한 번 전송하며 이후 같은 주·환경·대상·형식의 반복 전송은 막습니다. 대상은 웹훅 단방향 해시로만 영수증에 구분하며 URL은 기록하지 않습니다. 전송 성공과 모든 검수·AI 조사의 성공은 다른 상태입니다.


## 모바일 최신 버전 검수 범위

`app-versions.json`에 담당자가 확인한 Stage/Prod별 iOS·Android 버전을 저장합니다. 2026-11-24 확인 기준: Stage iOS 5.2.6, Prod iOS 5.2.5, Android는 양쪽 모두 5.2.4입니다. 웹은 버전 필터 없이 기존대로 검사합니다.

명세 대조·Slack 이상 수·AI 추가 조사에는 해당 버전의 모바일 로그만 포함합니다. 구버전, 기준보다 높은 테스트 빌드(예: Stage iOS 5.3.0), 버전 누락은 상세 보고서의 참고 표에 플랫폼·버전·수집 건수·label 수로만 표시하며 이상으로 판정하지 않습니다. 선택 버전 수집이 없으면 이상 없음 대신 수집 0건·판정 대상 없음으로 표시합니다. 이전 기간 재검사도 같은 버전 범위를 적용합니다.

새 배포 시 이 파일을 PR로 갱신해야 합니다. 수집 버전 중 숫자가 가장 큰 값으로 자동 변경하지 않습니다. 각 실행은 고정된 GitHub 커밋의 버전 설정을 사용하므로 명세와 검수 범위를 재현할 수 있습니다. 설정 누락·형식 오류 시 검수 실패로 처리합니다. 참고 표의 건수는 이 도구의 조회 대상 event_name(DA1·DA2·CAMPUS·BUSINESS·USER)에 한정됩니다.


## 실제 값 근거와 Stage·Prod 비교

매주 동일 기간의 Stage·Prod BigQuery 실제 수집을 각각 조회하고 고정 GitHub 커밋 명세와 대조합니다. 테스트 로그를 새로 만들거나 앱 동작을 실행하는 작업은 아닙니다. 상세 오류에는 명세의 정확한 고정값·허용값·필수 value 설명과 실제 값별 건수를 표시합니다. value 파라미터 없음, NULL, 빈 문자열을 구분합니다. `또는`/`or`로 명확하게 열거한 리터럴은 허용값으로 읽고 문장 전체를 고정값으로 비교하지 않습니다.

고정·열거형 value의 짧은 UI 문자열은 보고서에 표시합니다. 이메일·전화번호·URL·긴 토큰 등 민감정보 가능 패턴은 가리고 동적 value 원문은 보존하지 않습니다. 가림은 개인정보 검출의 완전성을 보장하지 않으므로 수집 value에는 사용자 입력을 넣지 않는 계약을 유지해야 합니다. AI에는 새 실제 value 필드를 전달하지 않습니다.

Stage·Prod의 같은 label·플랫폼에서 관측된 event_name·screen_view·event_category 및 고정·열거형 value 집합을 추가 비교합니다. 값별 건수는 근거로 표시하지만 건수 차이를 오류로 판정하지 않습니다. 동적 value와 가린 값은 양 환경 일치 여부를 판정하지 않습니다. 한 환경에서만 관측된 항목은 구현 누락으로 판단하지 않습니다. 관측 값 차이는 버전·사용 동작 차이 때문일 수 있으며, 관측 값이 같아도 명세 일치 여부는 각 환경의 규칙 검수 결과로 확인해야 합니다. 공통 관측이 없거나 조회 실패·기간/명세가 다르면 동일하다고 주장하지 않습니다.

환경별 report JSON의 observed_evidence와 environment-comparison.json에 집계 근거를 보관하며 GitHub Actions 요약에서 비교 표를 볼 수 있습니다. 주간 조회 job ID와 기준 버전·명세 커밋도 각 report JSON에 보존합니다.
