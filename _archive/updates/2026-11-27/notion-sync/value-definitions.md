# 새 value 확정 · Android 관측 결과

2026-11-27 사용자 지시로 기존 16페이지·18계약의 새 로깅 value를 아래 고정 STRING으로 설정했습니다. SDK 배포 완료·실수집 반영을 의미하지 않습니다. 과거 로깅과 나머지 필드·속성·사진은 보존했습니다.

| 서비스·명세 | 변경 전 Notion value | 확정 value | 새 라벨 Android Stage / Production | 과거 라벨 Android Stage / Production |
| --- | --- | --- | --- | --- |
| [콜밴팟 · 2-1 콜밴팟 검색바 클릭](https://app.notion.com/p/7770221954bc826a864201306b07869e) | 검색어 | 검색창 | 1 / 13 | 0 / 5 |
| [콜밴팟 · 2-11  콜밴팟 찾기 이탈](https://app.notion.com/p/0d50221954bc8277b81781104e8776f9) | 기존 미기재 유지 | 뒤로가기 | 20 / 15 | 0 / 0 |
| [콜밴팟 · 2-10 콜밴팟 채팅방 입장 클릭](https://app.notion.com/p/6d00221954bc83c4a2ca011e1d083230) | 기존 미기재 유지 | 채팅방 입장 | 7 / 0 | 2 / 3 |
| [콜밴팟 · 2-2  콜밴팟 필터 클릭](https://app.notion.com/p/eba0221954bc827d869b81c4360fb4de) | 기존 미기재 유지 | 필터 | 244 / 7 | 0 / 0 |
| [콜밴팟 · 2-8  콜밴팟 전화 클릭](https://app.notion.com/p/0610221954bc8359a9c4013f54bf8a3e) | 기존 미기재 유지 | 전화 | 0 / 1 | 0 / 1 |
| [콜밴팟 · 2-7  콜밴팟 채팅 전송](https://app.notion.com/p/d1b0221954bc83559f3f0181593cc36b) | 기존 미기재 유지 | 메시지 전송 | 19 / 0 | 5 / 1 |
| [콜밴팟 · 3-5 콜밴팟 모집 이탈](https://app.notion.com/p/be30221954bc83f1b8a5019f78b03299) | 기존 미기재 유지 | 뒤로가기 | 0 / 1 | 0 / 0 |
| [콜밴팟 · 2-6  콜밴팟 채팅 클릭](https://app.notion.com/p/52d0221954bc83ccb88281fef33b5eba) | 기존 미기재 유지 | 채팅 | 5 / 0 | 0 / 0 |
| [콜밴팟 · 3-4 콜밴팟 모집 작성 완료](https://app.notion.com/p/7830221954bc83beb94581d75e38565a) | 기존 미기재 유지 | 작성 완료 | 0 / 5 | 1 / 23 |
| [콜밴팟 · 2-9·3-6 콜밴팟 목록 → 모집하기](https://app.notion.com/p/aaf0221954bc838392610164dea9dfac) | 기존 미기재 유지 | 모집하기 | 1 / 30 | 1 / 21 |
| [콜밴팟 · 2-3  콜밴팟 필터 적용하기](https://app.notion.com/p/f7b0221954bc830a877501bf42a919c0) | 기존 미기재 유지 | 필터 적용 | 2 / 4 | 0 / 4 |
| [모의수강신청 · 0. (웹) 모의수강신청 진입](https://app.notion.com/p/c0c0221954bc8270be5381ef9726eb8f) | 기존 미기재 유지 | 모의수강신청 | 0 / 0 | 0 / 0 |
| [모의수강신청 · 1-4. 모의수강신청_예비수강과목 신청 클릭](https://app.notion.com/p/f0e0221954bc83e9889b8133e4803901) | 기존 미기재 유지 | 예비수강과목 신청 | 0 / 0 | 0 / 0 |
| [모의수강신청 · 1-5. 모의수강신청_메인으로 클릭](https://app.notion.com/p/9a70221954bc82b1965081a80de5cafb) | 기존 미기재 유지 | 메인으로 | 0 / 0 | 0 / 0 |
| [모의수강신청 · 1-3. 모의수강신청_강좌 신청 클릭](https://app.notion.com/p/9e30221954bc82a5956a0169ef3c819c) | 기존 미기재 유지 | 개설강좌 신청 | 0 / 0 | 0 / 0 |
| [모의수강신청 · 1-2. 모의수강신청_조회 클릭](https://app.notion.com/p/0400221954bc820681380123672fea01) | 기존 미기재 유지 | 강좌 조회 | 0 / 0 | 0 / 0 |

- 모든 확정 value는 표의 한글 문자열 그대로 전송합니다. 입력 검색어·메시지 본문·전화번호·필터 상세 JSON을 value로 전송하지 않습니다. 필터 선택내역 등 추가 파라미터 계약을 이번에 만들지 않습니다.
- 검색바는 검색 실행·입력 완료 이벤트가 아니므로 value 검색창으로 정의했습니다. 조회 직전 검색어로 바뀐 원문도 확인한 뒤 사용자의 전체 값 지정 요청에 따라 정렬했습니다.
- 작성 완료·강좌 신청은 버튼 클릭 계약입니다. 서버 등록·신청 성공으로 의미를 바꾸지 않았습니다.
- Android 대상은 콜밴팟 11페이지의 click 11계약입니다. 이탈 swipe 2계약은 기존 iOS 전용을 유지합니다. 모의수강신청 5계약은 WEB 전용입니다.
- 조회 대상: 2026-10-30~2026-11-27 GA4 daily 및 daily가 없는 날짜의 intraday. Stage analytics_427218788, Production analytics_432041405. Stage 11/14 daily는 없으며 11/27은 당일 부분 데이터, Production 11/26~27은 intraday입니다.
- 실제 Android 관측: Stage 308건(새 299·과거 9), Production 134건(새 76·과거 58). 총 442건 모두 value 키 자체 없음. 빈 문자열·NULL 키와 구분했고 다른 value 계열 키도 발견하지 못했습니다. 관측되지 않은 label은 값 없음으로 단정하지 않습니다.
- Android _debug 및 label (debug)는 비교에만 반영했고 원본 이름·값은 보존했습니다.
- 공통 가이드의 모의수강신청 미기재 유지·콜밴팟 메시지 전송 빈 value 유지 조항을 이번 결정으로 대체했습니다.

## 계약별 확정값

| event_label | 플랫폼 | value |
| --- | --- | --- |
| course_practice__timetable__course_application__entry__click | WEB | 모의수강신청 |
| course_practice__course_practice__search__click | WEB | 강좌 조회 |
| course_practice__course_practice__course_application__lecture__click | WEB | 개설강좌 신청 |
| course_practice__course_practice__course_application__preselected__click | WEB | 예비수강과목 신청 |
| course_practice__course_practice__navigation__main_return__click | WEB | 메인으로 |
| callvan__callvan_list__search__search_input__click | ANDROID, IOS | 검색창 |
| callvan__callvan_participant_list__callvan_chat__participant_entry__click | ANDROID, IOS | 채팅방 입장 |
| callvan__callvan_list__navigation__back__click | ANDROID, IOS | 뒤로가기 |
| callvan__callvan_list__navigation__back__swipe | IOS | 뒤로가기 |
| callvan__callvan_list__filter__open__click | ANDROID, IOS | 필터 |
| callvan__callvan_list__filter__apply__click | ANDROID, IOS | 필터 적용 |
| callvan__callvan_list__callvan_chat__card_entry__click | ANDROID, IOS | 채팅 |
| callvan__callvan_chat__callvan_chat__message_send__click | ANDROID, IOS | 메시지 전송 |
| callvan__callvan_list__contact__phone__click | ANDROID, IOS | 전화 |
| callvan__callvan_list__callvan_write__entry__click | ANDROID, IOS | 모집하기 |
| callvan__callvan_write__callvan_write__confirm__click | ANDROID, IOS | 작성 완료 |
| callvan__callvan_write__navigation__back__click | ANDROID, IOS | 뒤로가기 |
| callvan__callvan_write__navigation__back__swipe | IOS | 뒤로가기 |
