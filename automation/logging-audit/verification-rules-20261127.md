# 규칙 기반 상세 분석 검증 · 2026-11-27

외부 AI API를 사용하지 않는 방식으로 전환했다. agent.py·api_smoke.py·OpenAI SDK 의존성·워크플로의 API 키/모델 전달을 제거했다. 기존 Secret은 읽거나 삭제하지 않았다.

## 최신 검사

- 로컬 및 GitHub Actions 검사 각각 108개 통과.
- 최신 GitHub 합성 시험 성공: https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/45922000511
- 시험 코드 커밋: 5fa9a129355cf24a3318f0347a4d53a5b59c78d1. 이후 근거 문서만 갱신했다.
- 합성 Stage·Production 각각 9건·상세 분석 3개 완료. 네트워크 호출을 차단하고 실제 API·BigQuery·Slack 경로를 실행하지 않았다. 원격 의존성 설치·GCP 인증·실제 주간 조회·전송 cache도 건너뛰었다.
- 실제 명세 대조 중 이스케이프된 꺾쇠를 HTML로 처리해 뒤따르는 계약을 지우는 파서 오류를 발견·수정했다. 뒤로가기 label 2개와 꺾쇠 동적 value를 회귀 검사했다.
- 고정 main 커밋 3105e0c7ed27a5f66355725d8e8337129b4fc697의 blob SHA와 일치하는 명세 784개에서 현행 label 434개를 읽었다.

## 읽기 전용 실데이터 후처리

11/16~22 주간 범위와 11/13~15 이전 기간을 읽기 전용 MCP 연결로 조회하고 같은 PR의 audit·규칙 상세 분석·보고서 생성에 입력했다. Python 처리 중 추가 네트워크와 sender를 차단했으며 send=False·delivery_status=not_requested를 확인했다.

| 환경 | 기준 버전 선택 후 주간 이벤트 | 처리 | 상세 분석 | 이전 기간 재검사 |
| --- | ---: | --- | ---: | --- |
| Stage | 9,127 | 완료 | 4 | 11/14 원천 테이블 미존재로 불완전 |
| Production | 85,415 | 완료 | 4 | 완료 |

- 주간 범위의 daily 테이블은 양쪽 모두 존재한다. Stage의 이전 기간 누락을 이번 주 누락으로 오인하지 않았다.
- 실제 읽기 Job: Stage NKSPDnzmcjNmbCYNLIe9OXubpFl, Production bhvQxxaMyTNuJF4PxZeT0lXIG2E. 둘 다 SELECT·DONE.
- 비공개 비고정 value·잘못된 식별자는 BigQuery에서 먼저 가렸다. 선언된 모든 고정·열거형 값과 NULL·빈 상태는 보존했음을 확인했다. 실제 비고정 값 원문·환경별 전체 값 집합 차이는 이 시험으로 검증하지 않는다.
- 실제 데이터의 미등록·과거 수집·명세 불일치 후보는 남아 있다. 실행 성공을 모든 로깅의 정상 판정으로 해석하지 않는다.
- GitHub main 전용 서비스 계정 WIF·새 Slack 수신·향후 예약 실행은 이 실데이터 후처리 시험에 포함하지 않는다.

## 반영 범위

날짜·버전·명세 출처·query job ID와 고정된 확인 항목을 제공한다. 전체 규칙 목록과 최대 4개의 추가 분석 표본을 구분한다. Android 디버그는 비교 전용 정규화하며 label 자체가 없는 DA 디버그도 조회한다.

과거 실제 API 시험은 verification-20261127.md에 이력으로 보존한다. 이번에는 외부 AI를 재호출하지 않았다. main은 미병합이며 기존 예약 코드는 자동 교체되지 않는다. 테이블 쓰기·Slack 발송·운영 반영·권한 변경은 하지 않았다.
