# 코인 사장님 헤더·푸터 진입 로그 — 레거시

[← 공통 문서](README.md) · [사장님 서비스 내부 명세](../../event-log/03-%EC%82%AC%EC%9E%A5%EB%8B%98/README.md)

2026-11-28 사용자 결정에 따라, KOIN WEB의 헤더·푸터에서 ‘코인 사장님’ 메뉴를 눌렀을 때 보내던 진입 로그는 레거시로 보존합니다. 신규 구현·새 라벨 이관 대상에서 제외하며, 기존 수집분과 아래 전송값은 과거 조사 근거로 남깁니다.

## 보존하는 기존 전송값

| 발생 위치 | event_name | event_label | event_category | value |
| --- | --- | --- | --- | --- |
| PC 헤더의 코인 사장님 메뉴 | BUSINESS | header | click | 코인 사장님 |
| PC 푸터의 코인 사장님 메뉴 | BUSINESS | footer | click | 코인 사장님 |

`header`·`footer` 라벨 자체는 다른 서비스도 공유합니다. 위 표의 메뉴/value 조합만 이번 레거시 범위이며, 공통 헤더·푸터 로그 전체를 폐기하는 결정이 아닙니다. 사장님 사이트 내부의 이벤트·가게·메뉴·계정 명세 19개와 카테고리 메뉴 계약은 이 문서를 근거로 일괄 변경하지 않습니다.

## 근거와 적용 상태

- 기준: 사용자의 사장님 로깅 제거 및 레거시 보존 요청. 이 문서는 해당 결정 기록이며, Notion 원문에 이미 레거시 처리가 끝났다는 의미가 아닙니다.
- [코인 사장님 공통 매핑](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/9b6b7a2a29e70f59409bb1136cf2ec7bb9765ab6/src/utils/hooks/analytics/shortcutLoggingMap.ts#L21)
- [PC 헤더 호출](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/9b6b7a2a29e70f59409bb1136cf2ec7bb9765ab6/src/components/layout/Header/PCHeader/index.tsx#L43)
- [푸터 호출](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/9b6b7a2a29e70f59409bb1136cf2ec7bb9765ab6/src/components/layout/Footer/index.tsx#L34)
- 이번 PR은 문서와 검수 기준 갱신입니다. 웹 코드의 전송 호출 제거·배포·운영 수집 종료는 수행하지 않았습니다. 서비스 링크나 UI 제거까지 확정하는 문서가 아닙니다.

## 검수 시 처리

위 이벤트가 계속 관측되면 과거 로깅의 지속 수집으로 조사합니다. 다른 서비스의 `header`·`footer` 로그를 같은 이유로 폐기하거나 정상 계약으로 승인하지 않습니다. 기존 검수기는 BUSINESS 등 과거 event_name을 감지하므로 이를 무시하는 예외나 새 정상 계약을 추가하지 않습니다.
