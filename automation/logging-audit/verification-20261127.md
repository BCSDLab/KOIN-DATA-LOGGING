# 주간 검수 수정 검증 · 2026-11-27

기준 main: `3105e0c7ed27a5f66355725d8e8337129b4fc697`.

## 변경과 로컬 검사

- Android 디버그 접미사는 비교할 때만 제거하며 원천을 변경하지 않는다. 규칙·환경 비교·AI 집계에 같은 식별자를 사용한다.
- Slack에 실제 명세 기준과 AI 조사 완료 여부를 표시한다. GitHub 기준 실행을 Notion 직접 대조로 표현하지 않는다.
- 전송 영수증 재사용과 새 전송을 구분한다. 내용 해시가 없거나 다르면 이번 내용의 전달 성공을 단정하지 않는다. 자동 재전송하지 않는다.
- 오류 메타데이터만으로 추론 전 사용량·결제 한도 실패도 분류한다. 합성 API 시험만 비밀값을 가린 오류 문구를 보존한다.
- 로컬 `python3 -B -m unittest discover -s tests`: 108개 통과.
- 저장된 Stage Android DA 디버그 1,624건·172개 집계로 식별자 재대조: 접미사로 인한 unexpected_event_name 1,624건 → 0건. unregistered_label은 1,624건 → 68건으로 줄었으며 정규화 후에도 명세에 없는 label은 계속 검출한다. 저장 집계에는 원문 value가 없으므로 이 재대조로 value 규칙 결과를 판단하지 않았다.

## 실제 API 시험

- 기존 GitHub Actions OPENAI_API_KEY 재사용을 사용자에게 확인받았다.
- 합성 계약 전용 수동 실행: https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/45919594707
- 추가 진단 실행: https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/45919746327
- 모델 조회: gpt-6-astra available. 세션·turn 생성 후 스트리밍 APIError, 도구 호출 0회.
- 응답: 조직의 usage or billing limit에 도달했다는 메시지. 키 인증 실패나 모델 미존재로 판정하지 않는다. 잔액 부족과 설정된 사용 한도 중 어느 것인지는 이 응답만으로 구별하지 않는다.
- 생성한 두 세션 모두 삭제 확인. 조사 완료는 실패 상태이며 성공으로 표시하지 않는다.
- Google Cloud 인증·BigQuery·Slack 발송·전송 캐시 사용은 시험 경로에서 건너뛰었다.
- 과금·사용 한도·API 키를 변경하지 않았다. 한도 해결 전 반복 API 시험은 중단한다. 해결 후 실제 도구 조사·최종 결과·정리를 다시 확인해야 한다.

## 남은 범위

main 병합과 월요일 예약 경로의 배포·실제 Slack 새 메시지 수신은 하지 않았다. Notion 직접 자동 대조와 Stage 별도 analytics_440323811 자동 편입은 구현하지 않았다. Silver·Gold·원천 테이블은 변경하지 않았다.
