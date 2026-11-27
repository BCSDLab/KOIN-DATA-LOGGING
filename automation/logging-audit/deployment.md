# 주간 검수 연결 상태 · 2026-11-24

2026-11-27 변경안: 외부 AI 호출·SDK·키 전달을 제거하고 규칙 기반 상세 분석으로 대체한다. 아래 OpenAI Secret 및 최초 AI 시험 언급은 당시 구성 기록이며 현행 실행의 요구사항이 아니다. 기존 Secret은 읽거나 삭제하지 않는다.

GCP 인증은 서비스 계정 키 없이 GitHub OIDC/Workload Identity Federation을 사용한다.

- 서비스 계정: `koin-logging-audit@kap-chat.iam.gserviceaccount.com`
- Provider: `projects/340135824028/locations/global/workloadIdentityPools/koin-logging-audit/providers/github-main`
- 허용 GitHub 조직 ID: `17200116`, 저장소 ID: `1454858401`
- 허용 ref: `refs/heads/main`
- 허용 workflow_ref: `BCSDLab/KOIN-DATA-LOGGING/.github/workflows/weekly-logging-audit.yml@refs/heads/main`
- 전용 Pool의 해당 repository_id principalSet에만 `roles/iam.workloadIdentityUser`를 부여한다.
- 두 query 프로젝트 `kap-chat`, `koin-stage-438512`에 `roles/bigquery.jobUser`를 부여한다.
- 읽기 범위는 `kap-chat.analytics_432041405`, `koin-stage-438512.analytics_427218788` 두 데이터셋의 READER다. 원천 데이터 수정 권한은 부여하지 않았다.
- kap-chat의 STS API를 활성화했다. 서비스 계정의 비공개 키는 생성하지 않았다.
- GitHub Variables `GCP_AUDIT_WIF_PROVIDER`, `GCP_AUDIT_SERVICE_ACCOUNT`를 저장하고 화면에서 값이 일치하는지 확인했다.
- Notion/OpenAI/Slack Secret 이름 3개가 등록된 상태를 확인했다. Secret 값은 읽거나 이 문서에 기록하지 않았다.

이는 인증 구성 기록이다. 실제 GitHub OIDC 인증·Notion 전체 수집·OpenAI 완료·Slack 수신 성공 여부는 최초 실행 결과로 따로 확인해야 한다.

인증 연결을 중단하려면 전용 Provider를 비활성화하고 서비스 계정의 위 IAM 바인딩을 제거한다. 다른 서비스 계정이나 Airflow 설정은 변경하지 않는다.
