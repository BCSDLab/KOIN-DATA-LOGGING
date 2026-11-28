# 주간 로깅 검수 · GitHub 명세 → BigQuery → Slack

GitHub Actions가 명세와 실제 수집을 비교하고 규칙 기반 상세 분석을 작성합니다. 외부 AI API·모델·OpenAI SDK·API 키를 사용하지 않습니다.

[Notion 로깅 검수 보고서 · 플랫폼별 정상 수집·명세 불일치·미관측·명세 밖 로그 및 실행 체크](https://app.notion.com/p/4230221954bc815fa3e0e2323d99ff8c)

보고서에는 마지막 갱신 실행·관측 기간·입력 대기 여부가 표시됩니다. 문서 링크 추가가 재검수 실행이나 최신 수집 정상 판정을 뜻하지 않습니다.

## 일정과 수집 범위

일별 자동 BigQuery 조회는 비용 확인 전 비활성입니다. 저장소 변수 `DAILY_LOGGING_REPORT_ENABLED=true`를 사용자 확인 후 설정해야 실행됩니다. 미설정 상태에서는 일별 job을 건너뛰며, 수동 `notion_write_test=true`는 BigQuery·Slack 없이 기존 요약을 동일 내용으로 다시 써서 연결만 확인합니다. 각 BigQuery Job은 최대 1GiB를 허용하지만 프로젝트·결제 계정의 무료 잔여량을 보장하는 한도는 아닙니다.

Notion 보고서는 `daily-logging-audit.yml`이 매일 09:00 KST에 당일 하루 기준으로 갱신합니다. 정상·불일치·미관측·명세 밖 라벨 수와 개발자가 우선 확인할 최대 3개 동작만 요약하고, 실제값·명세값·전체 항목은 해당 실행의 상세 결과에 연결합니다. 당일 수집은 잠정이며 이전 3일 지연 도착 재검사는 상세 결과에서 구분합니다. 일별 실행에는 Slack 웹훅을 전달하지 않고 전송도 호출하지 않습니다. 아래 월요일 Slack 일정은 유지합니다.

Notion 자동화는 보고서 상단의 `오늘의 로깅 검수`로 시작하는 문단 1개만 갱신하고 읽어 확인합니다. 상세 페이지·실행 체크·사용자 메모·과거 기록은 수정하거나 삭제하지 않습니다. 표식이 없거나 중복이면 쓰기를 중단합니다. `NOTION_LOGGING_REPORT_TOKEN`을 우선 사용하고 없으면 기존 `NOTION_LOGGING_READ_TOKEN`을 사용하되, 이름이 아닌 실제 보고서 접근·쓰기 시험으로 권한을 판정합니다. 토큰을 코드·출력·artifact에 기록하지 않습니다.

연결만 확인하려면 별도 브랜치에서 기존 workflow에 `offline_check=true`, `probe_notion_report=true`, `send_slack=false`를 지정합니다. Notion 보고서 읽기만 시험하며 BigQuery·Notion 쓰기·Slack은 실행하지 않습니다. Notion 쓰기가 실패하면 일별 예약이 있어도 자동 갱신 완료로 보지 않습니다.

- 매주 월요일 09:00 KST (`0 0 * * 1`, UTC). GitHub 대기열에 따라 지연될 수 있습니다.
- Stage: `koin-stage-438512.analytics_427218788`.
- Production: `kap-chat.analytics_432041405`.
- IOS·ANDROID·WEB의 DA1·DA2를 검사하고 CAMPUS·BUSINESS·USER 지속 수집을 감지합니다. event_label이 있는 다른 event_name도 판정 목록에 포함합니다.
- 직전 완료된 월요일~일요일의 daily export를 검사하고, 이전 기간 마지막 3일을 재검사합니다. intraday는 합산하지 않습니다.
- 실행 checkout의 커밋을 고정해 `event-log/**/*.md` 전체를 읽습니다. README·_archive를 현행 계약으로 허용하지 않습니다. 과거 구간·레거시 문서는 과거 label 감지용입니다.
- 신규 서비스·계약은 현행 문서 인덱스와 서비스 등록에 함께 추가합니다. 실행 시 고정된 main의 전체 계약을 읽으므로 개별 label 목록을 별도로 늘리지 않습니다. 동아리 PC WEB 21개도 병합 후 자동 포함되며 미관측은 오류·미구현으로 단정하지 않습니다.
- GitHub 명세 기준입니다. **Notion 직접 대조는 미실행**이며 Notion 변경·미병합 PR은 반영되지 않습니다.
- 별도 Stage WEB 데이터셋 `analytics_440323811`은 현재 자동 수집 대상에 포함되지 않습니다.
- 원천 데이터와 Silver·Gold·Airflow를 수정하지 않습니다.

## Android 디버그

Android의 event_name·event_category 끝 `_debug`, event_label 끝 ` (debug)` 또는 `_debug`는 비교할 때 한 번만 제거합니다. 원래 식별자와 원천 데이터는 보존합니다. iOS·WEB, screen_view·value와 문자열 중간의 debug는 바꾸지 않습니다.

정규화 뒤에도 실제 미등록 label·과거 event_name·필드 불일치는 계속 검출합니다. event_label 자체가 누락된 Android DA 디버그도 조회 대상에 포함합니다. 규칙 판정·환경 비교·상세 분석은 같은 식별자를 사용합니다.

## 규칙 기반 상세 분석

전체 판정 목록은 유지하고, 추가 분석은 영향이 큰 label·플랫폼 조합 최대 4개를 대상으로 합니다. 오류가 있는 플랫폼에 먼저 한 항목씩 배분한 뒤, 가장 큰 단일 사유 발생 건수로 나머지를 선택합니다. 순서와 집계는 같은 입력이면 같습니다.

각 항목에는 다음 근거를 붙입니다.

- 날짜·앱 버전·event_name·screen_view·category별 건수
- 해당 플랫폼의 현행 명세, 과거 명세 출처, 고정 커밋·query job ID
- 조회 범위 내 최초·최종 관측일
- 오류 유형별 고정된 확인 항목: 배포 범위, SDK 파라미터, 화면 전환 시점, 명세 충돌 등

관측 총건수와 오류 건수는 다릅니다. 사유별 오류 건수는 겹칠 수 있어 합산하지 않습니다. 그룹이 30개를 넘으면 나머지 그룹·건수를 따로 표시합니다. 최초 관측일을 실제 배포일로 간주하지 않습니다. 확인 항목은 원인 확정이나 AI가 만든 가설이 아닙니다.

원본 동적 value·사용자 ID는 추가 분석에 넣지 않습니다. 개인정보 가능 식별자는 가립니다. 추가 분석은 이미 조회한 집계를 사용하며 별도 SQL이나 외부 조사를 실행하지 않습니다.

## 판정과 한계

| 유형 | 판정 |
| --- | --- |
| 미등록 | 현행·과거 명세에 없는 label, label 누락 |
| 과거 로깅 지속 수집 | 과거에만 있는 label 또는 CAMPUS·BUSINESS·USER |
| 현행 명세 불일치·검토 | event_name·screen_view·category·플랫폼, 필수 value, 명확한 고정·열거형 value, 중복 파라미터 키, 충돌·미확정 계약 |

모바일은 `app-versions.json`의 담당자 확인 버전만 판정·추가 분석합니다. 2026-11-24 기준 Stage iOS 5.2.6, Prod iOS 5.2.5, Android 양쪽 5.2.4입니다. 나머지 버전은 참고 집계로 보존하고 Web은 버전 필터 없이 검사합니다.

미관측은 구현 누락이 아니며 수집 0건은 정상 판정이 아닙니다. 누락 daily 테이블·소스 축소·권한 오류는 검수 불완전입니다. 이전 기간의 누락은 이번 주 상태와 따로 표시합니다. 동적 value의 내용, 모든 임의 파라미터의 타입, 사용자 동작 1회당 전송 1회, 실제 SDK 배포일·클릭 조건은 이 검수만으로 확인하지 않습니다.

## Slack과 결과

Stage·Prod 결과 2개를 현재 `SLACK_LOGGING_AUDIT_STAGE_WEBHOOK`에 연결된 `코인_이벤트알림_stage` 채널로 보냅니다. 기존 운영 웹훅으로 대체하지 않습니다. 각 메시지는 iOS·Android·Web 상태, 실제 명세 기준, 규칙 상세 분석 상태, `AI API: 사용 안 함`을 표시합니다.

`상세보기`는 해당 실행의 작업 요약으로 연결됩니다. 플랫폼별 전체 오류 목록, 실제·기대값, 규칙 상세 분석, Stage·Prod 비교를 볼 수 있습니다. JSON·명세 snapshot·전송문은 artifact에 35일 보관합니다. 원본 event value·사용자 ID는 Slack에 넣지 않습니다.

같은 주 전송 영수증을 cache로 복원해 중복을 억제합니다. 내용 해시·성공 시각과 재사용 여부를 기록합니다. 해시가 없거나 현재 내용과 다르면 이번 내용 전달을 미확인으로 처리하며 자동 재전송하지 않습니다. 전달 불명 상태도 담당자가 수신·Job 상태를 확인하기 전 다시 보내지 않습니다. cache 유실 등을 포함한 정확히 한 번 전송은 보장하지 않습니다.

## 필요한 연결

| 종류 | 이름 | 내용 |
| --- | --- | --- |
| Secret | `SLACK_LOGGING_AUDIT_STAGE_WEBHOOK` | 지정된 Stage 채널 전용 Incoming Webhook |
| Variable | `GCP_AUDIT_WIF_PROVIDER` | main 전용 Workload Identity Provider |
| Variable | `GCP_AUDIT_SERVICE_ACCOUNT` | 전용 읽기 서비스 계정 |
| Secret | `GCP_AUDIT_CREDENTIALS_JSON` | WIF가 없는 경우에만 사용 |

API 키·모델 설정은 필요하지 않습니다. 기존 OpenAI Secret을 삭제하거나 값을 읽지 않습니다. [기존 GCP 인증 기록](deployment.md)의 main 전용 WIF·읽기 범위를 유지합니다.

BigQuery Data Viewer와 query 프로젝트의 BigQuery Job User를 사용하며 원천 수정 권한은 필요하지 않습니다. BigQuery·GitHub Actions 비용은 기존 요금·할당량에 따라 발생할 수 있습니다. 외부 AI API 비용은 발생시키지 않습니다.

## 시험과 반영

1. 로컬에서 `python -m unittest discover -s tests`, `python offline_check.py`를 실행합니다.
2. 별도 브랜치에서 `offline_check=true`, `send_slack=false`로 수동 실행합니다. 합성 데이터만 사용하며 Google Cloud 인증·BigQuery·Slack·전송 cache를 실행하지 않습니다. SDK 의존성 설치도 생략합니다.
3. 코드 리뷰 후 main 반영을 판단합니다. main 병합 전에는 기존 예약 실행 코드가 바뀌지 않습니다.
4. main의 실제 읽기 검수는 `offline_check=false`, `send_slack=false`로 확인합니다. WIF는 main 전용이므로 테스트 브랜치용으로 권한을 넓히지 않습니다.
5. 별도로 발송을 요청받은 경우에만 실제 Slack 수신을 시험합니다.

기본 예약은 실데이터 읽기와 기존 채널 발송을 수행합니다. 수동 week_start는 완료된 주의 월요일입니다. fork·PR의 비밀값 실행 경로는 추가하지 않습니다. 이번 변경으로 실제 수신·실데이터 전체 검증·운영 반영이 완료됐다고 표시하지 않습니다.

## 현재 명세로 검수 코드 확인

수집기는 체크아웃된 커밋의 공식 문서 목록과 추가 원문 목록을 사용합니다. 이전 원본으로 안내하는 링크 문서는 검수 문서 수에서 제외하며, 등록된 문서의 누락·예상 밖 문서·내용 해시 변경은 불완전으로 처리합니다. Notion을 실시간 조회한 결과로 표시하지 않습니다.

`python current_spec_check.py`는 실제 체크아웃 명세로 카탈로그를 만들고 정상 플랫폼 사례, 사용자 확정 value 16페이지·18계약, value 누락·오류, 미지원 플랫폼, Android 디버그를 검사합니다. 외부 데이터 조회·AI API·Slack 전송은 차단합니다. 이 검사는 코드 CI와 `offline_check=true` 합성 시험에 포함됩니다. 정보가 불충분하거나 충돌하는 라벨은 결과의 `unresolved_labels`에 남기며 임의로 확정하지 않습니다. 실제 BigQuery 수집·main 인증·Slack 수신 검증은 별도입니다.


복덕방 상세 사진을 손으로 넘기는 `real_estate__room_detail__photo_view__slide__swipe`는 IOS·ANDROID 지원입니다. 웹 화살표 click은 WEB입니다. 이 정확한 사진 swipe 라벨만 예외이며 다른 swipe는 기존 IOS 전용 정책을 유지합니다. 앱의 사진 click 수집은 기능 미지원 확정이 아니라 동작·전송 라벨 확인 대상입니다.
