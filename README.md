# KOIN Event Log

개발자를 위한 서비스별 로깅 명세입니다. **서비스 → 로깅 목록 → 개별 명세** 순서로 열면 `event_name`, `event_label`, 설명·값·카테고리와 이미지를 한 페이지에서 확인할 수 있습니다.

과거 로깅에는 예전 정의와 예전 이미지, 새 로깅에는 새 정의와 해당 이미지가 원문 구간대로 함께 표시됩니다. 원문에 구분이 없거나 항목이 없으면 추정하지 않고 표시합니다.

## 서비스

| 순서 | 서비스 |
| --- | --- |
| 1 | [주변상점](event-log/01-%EC%A3%BC%EB%B3%80%EC%83%81%EC%A0%90/README.md) |
| 2 | [복덕방](event-log/02-%EB%B3%B5%EB%8D%95%EB%B0%A9/README.md) |
| 3 | [사장님](event-log/03-%EC%82%AC%EC%9E%A5%EB%8B%98/README.md) |
| 4 | [식단](event-log/06-%EC%8B%9D%EB%8B%A8/README.md) |
| 5 | [버스](event-log/07-%EB%B2%84%EC%8A%A4/README.md) |
| 6 | [게시판](event-log/08-%EA%B2%8C%EC%8B%9C%ED%8C%90/README.md) |
| 7 | [배너](event-log/09-%EB%B0%B0%EB%84%88/README.md) |
| 8 | [홈화면 리디자인](event-log/10-%ED%99%88%ED%99%94%EB%A9%B4-%EB%A6%AC%EB%94%94%EC%9E%90%EC%9D%B8/README.md) |
| 9 | [콜밴팟](event-log/11-%EC%BD%9C%EB%B0%B4%ED%8C%9F/README.md) |
| 10 | [학교 부서 정보](event-log/12-%ED%95%99%EA%B5%90-%EB%B6%80%EC%84%9C-%EC%A0%95%EB%B3%B4/README.md) |
| 11 | [팀원 모집](event-log/13-%ED%8C%80%EC%9B%90-%EB%AA%A8%EC%A7%91/README.md) |
| 12 | [로그인/회원가입/정보수정 V2](event-log/15-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95-V2/README.md) |
| 13 | [시간표](event-log/16-%EC%8B%9C%EA%B0%84%ED%91%9C/README.md) |
| 14 | [모의수강신청](event-log/17-%EB%AA%A8%EC%9D%98%EC%88%98%EA%B0%95%EC%8B%A0%EC%B2%AD/README.md) |
| 15 | [강제 업데이트](event-log/18-%EA%B0%95%EC%A0%9C-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8/README.md) |
| 16 | [다국어 지원](event-log/21-%EB%8B%A4%EA%B5%AD%EC%96%B4-%EC%A7%80%EC%9B%90/README.md) |

## 레거시 서비스

과거 로깅과 이미지를 보존한 참고 명세입니다.

| 순서 | 서비스 |
| --- | --- |
| 1 | [새 주변상점 - 레거시](event-log/04-%EC%83%88-%EC%A3%BC%EB%B3%80%EC%83%81%EC%A0%90-%EB%A0%88%EA%B1%B0%EC%8B%9C/README.md) |
| 2 | [미래의 주변상점 - 레거시](event-log/05-%EB%AF%B8%EB%9E%98%EC%9D%98-%EC%A3%BC%EB%B3%80%EC%83%81%EC%A0%90-%EB%A0%88%EA%B1%B0%EC%8B%9C/README.md) |
| 3 | [로그인/회원가입/정보수정 - 레거시](event-log/14-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95-%EB%A0%88%EA%B1%B0%EC%8B%9C/README.md) |
| 4 | [졸업학점 계산기 - 레거시](event-log/19-%EC%A1%B8%EC%97%85%ED%95%99%EC%A0%90-%EA%B3%84%EC%82%B0%EA%B8%B0-%EB%A0%88%EA%B1%B0%EC%8B%9C/README.md) |
| 5 | [동아리 - 레거시](event-log/20-%EB%8F%99%EC%95%84%EB%A6%AC-%EB%A0%88%EA%B1%B0%EC%8B%9C/README.md) |

[이전 원본·검증 자료·코드 생성 파일럿](./_archive/README.md)

같은 명세는 목록에서 대표 하나로 안내하며 추가 원본·플랫폼별 과거 정의·사진은 대표 페이지에서 연결합니다. 목록 대표는 776개, 보존 열람 문서는 784개이며 고유 이벤트 개수가 아닙니다. 강제 업데이트 화면 이탈은 원문 간 충돌을 표시한 전환 초안입니다.

[2026-11-19 Notion ZIP 동기화 범위·검토사항](_archive/updates/2026-11-19/README.md)

## 주간 로깅 검수

[GitHub 명세·BigQuery 규칙 검수 및 Slack 연결 설정](automation/logging-audit/README.md) — 매주 월요일 오전 9시(KST), Stage·Production의 IOS·ANDROID·WEB별 미등록·과거 로깅 지속 수집·현행 명세 불일치를 알립니다. DA1·DA2와 Android 디버그를 검사하며 CAMPUS·BUSINESS·USER 수집도 감지합니다. 중요한 항목은 날짜·버전별 집계와 명세 출처·고정된 확인 항목을 붙입니다. 외부 AI API는 사용하지 않습니다. Notion 직접 자동 대조는 미실행이며 실제 명세 기준과 검수 범위는 연결 문서에 명시합니다.
