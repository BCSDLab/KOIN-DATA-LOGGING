# event_label 기능·행동 네이밍 사전

[← 현행 문서와 참고 자료](README.md)

[Notion 기준 원문](https://app.notion.com/p/38b0221954bc831b912c012d8af2c857) · 조회·동기화 기준일: 2026-11-28.

<!-- notion-body:start -->
PC WEB 동아리 신규 계약 · 2026-11-28

사용자 요청으로 <a href="https://app.notion.com/p/4260221954bc80ceab95e8c9e4cac8f1">동아리</a>에 Stage PC 동작을 기준으로 정리한 21개 신규 계약을 등록한다. service는 club(로그인 안내는 account), screen\_view는 header·footer·club\_list·club\_detail, event\_name은 새 명세 DA1이다. 플랫폼은 PC WEB만이며 모바일 WEB·ANDROID·IOS·swipe는 포함하지 않는다. 고정 value는 한국어다. 기존 동아리 55개 레거시·사진·전송값은 보존하며 전체를 현행으로 복원하지 않는다. 이전의 동아리 신규 네이밍 전면 제외 설명은 과거 명세 보존 범위를 뜻하고, 이번 PC WEB 계약에는 적용하지 않는다.

작업 담당자는 서비스별로 고정되지 않는다. 기존 계약의 event\_name은 개별 명세의 명시값을 따르며 서비스만으로 DA1/DA2를 일괄 변경하지 않는다. 로그인·관리자 화면과 실제 구현·배포·실수집은 별도 검수 대상이다.

### PC WEB 동아리 기능 등록

| service | feature | detail·category | 범위 |
| --- | --- | --- | --- |
| club | club\_entry | header\_entry / footer\_entry · click | PC 공통 헤더·푸터의 동아리 목록 진입 |
| club | club\_detail | card\_entry / search\_entry · click | 목록 카드 본문·검색 자동완성 결과에서 상세 진입 |
| club | club\_create | entry · click | 생성하기 버튼 시도. 생성 성공 아님 |
| club | filter | category / recruiting / tab / event\_status · click, sort · select | 과거 click 유지. 목록 정렬만 새 선택 계약이며 초기 표시·자동 재조회는 제외 |
| club | search | search\_input / clear · click | 검색창 클릭·검색어 삭제. 검색어 원문 미수집 |
| club | like | 목록 add / remove · click, 상세 detail 생략 · click | 목록 좋아요 클릭·해제 분리. 서버 성공 이벤트 아님 |
| club | qna\_write | entry · click | 질의응답 추가 진입 시도. 작성 내용 미수집 |
| club | navigation | scroll\_top · click | 상세의 맨 위로 버튼. PC 뒤로가기·WEB swipe 없음 |
| account | login\_popup | login\_entry / close · click | 동아리 발생 논리 화면 club\_list·club\_detail을 유지 |

<b>카테고리 13개 최종 기준 · 서비스별 event\_name / category\_navigation · </b><b>2026-11-08</b>

사용자 요청으로 홈 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 13개 메뉴를 <code>service__main_category__category_navigation__진입대상__click</code> 형식으로 통일했다. 사용자 후속 요청으로 이 카테고리 13개 계약의 event\_name은 라벨 첫 구간 서비스별 DA 배정으로 통일한다. 서비스명·value·발생 조건·사진·플랫폼 범위는 유지한다. 같은 서비스에는 화면·플랫폼·카테고리 여부와 관계없이 같은 event\_name을 사용한다. 버스는 <code>timetable_entry</code>와 <code>search_entry</code>로 목적지를 구분하고, 시간표 서비스의 <code>timetable_entry</code>는 service 구간으로 구분한다.

아래 이전 4개 계약의 feature·detail 설명과 옛 라벨은 이 후속 결정을 따른다. 신규 공용 feature는 category\_navigation이며 cafeteria\_entry·shop\_entry·owner\_entry 등은 해당 메뉴의 detail이다. 기존 4개 라벨 유지 + 나머지 9개 라벨 표기 변경이다. 문서 네이밍 결정일 뿐 팀원 모집 SDK 동결 해제·기존 9개 계약 WEB 지원 확대·SDK 배포·실수집 검수 완료를 뜻하지 않는다. 신·구 이중 전송과 과거 로그 소급 개명은 하지 않는다. Silver·Gold·데이터·설정은 변경하지 않았다.

<b>모바일 WEB 카테고리 4개 계약 확정 · </b><b>2026-11-08</b>

사용자 요청으로 식단·버스 시간표·교통편 조회하기·코인 for Business의 미확정 네이밍을 아래 계약으로 확정했다. 기준 본문은 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 새 로깅이며 각 항목은 설명·screen\_view·event\_name·event\_label·value·event\_category와 사진만 표시한다.

공통: event\_name은 서비스별 DA 배정을 따르며, screen\_view=<code>main_category</code>, feature=<code>category_navigation</code>, event\_category=<code>click</code>. 최신 서비스별 event\_name 통일 기준이 과거의 카테고리 전체 DA2 예외보다 우선한다. 이 네 계약의 WEB 모바일 적용 범위는 유지한다.

- 식단: <code>cafeteria__main_category__category_navigation__cafeteria_entry__click</code> / value=식단. <a href="https://app.notion.com/p/4120221954bc817faa33c64ee9f9ad13">Notion 원문</a>
- 버스 시간표: <code>bus__main_category__category_navigation__timetable_entry__click</code> / value=버스 시간표. <a href="https://app.notion.com/p/4120221954bc81c08b5ed63eff880be6">Notion 원문</a>
- 교통편 조회하기: <code>bus__main_category__category_navigation__search_entry__click</code> / value=교통편 조회하기. <a href="https://app.notion.com/p/4120221954bc813a91caf8623f3cfec0">Notion 원문</a>
- 코인 for Business: <code>owner__main_category__category_navigation__owner_entry__click</code> / value=코인 for Business. <a href="https://app.notion.com/p/4120221954bc81f3bc00e71813fe5f25">Notion 원문</a>

이 네 항목을 포함한 13개 카테고리 메뉴는 공통 feature <code>category_navigation</code>을 사용한다. 식단의 <code>cafeteria_entry</code>, 버스의 <code>timetable_entry</code>·<code>search_entry</code>, Business의 <code>owner_entry</code>는 detail로 구분한다. Business 클릭은 외부 사이트 이동 시도이며 실제 방문 성공·가입·이용 완료를 증명하지 않는다.

로그는 클릭 시 한 번 기록한다. 단순 노출·초기 렌더·자동 이동은 제외하며 이동 후 성공을 기다려 클릭 이벤트의 의미를 바꾸지 않는다. 개발 반영 전 기존 category\_\* 수집은 유지하고, 반영된 해당 WEB 버전부터 새 계약으로 전환한다. 같은 클릭에 신·구 라벨을 함께 보내지 않으며 과거 로그를 소급 개명하지 않는다.

옛 앱 햄버거 삭제 명세는 계속 삭제·레거시 이력이며, PC 헤더·푸터·홈 카드의 라벨을 이 모바일 카테고리에 재사용하지 않는다. 이번 결정은 이 4개 WEB 계약에 한정한다. 기존 다른 9개 계약의 WEB 지원·팀원 모집 동결은 별도이며 카테고리 메뉴 수는 13개 그대로다.

문서 계약 확정이며 SDK 구현·배포·실수집 검수 완료가 아니다. Silver 허용 카탈로그·Gold·데이터·활성화 설정은 변경하지 않았다. 기존 378라벨/904계약은 이번 변경을 반영한 최신 총계가 아니므로 현행 목록 재집계 없이 사용하지 않는다.

<b>모의수강신청 진입 — 현행 단일 대표 계약</b>

2026-11-08 사용자 요청으로 시간표 우측 상단 ‘모의 수강신청’ 버튼(/timetable → /course)은 <a href="https://app.notion.com/p/e4c0221954bc828f8f77018f22ccff49">0. (웹) 모의수강신청 진입</a>의 기존 계약 하나만 적용한다. <a href="https://app.notion.com/p/36c0221954bc83a9b1c881a0e87ceb81">[레거시·중복 명세] 2-22. (웹) 시간표_모의 수강신청 (클릭)</a>는 동일 버튼의 중복 명세이므로 레거시 이력으로 보존하고 별도 이벤트를 추가 전송하지 않는다.

- event\_name: <code>DA2</code>
- event\_label: <code>course_practice__timetable__course_application__entry__click</code>
- screen\_view: <code>timetable</code>
- event\_category: <code>click</code>
- value: 기존 0번의 미기재 기준 유지. ‘모의 수강신청’ 값을 추가하지 않으며 ‘미기재 유지’라는 문구 자체를 값으로 보내지 않는다.
- 플랫폼: WEB. 버튼 클릭 시 한 번 기록한다. 메인 배너·서비스 내부 강좌 신청은 이 계약과 구분한다.

2-22의 DA1·timetable 서비스 라벨·value는 아래/해당 원문의 과거 이력이다. SDK 배포·실제 수집·단일 전송 검수 완료나 과거 데이터 개명을 뜻하지 않는다. 준비 중인 허용 카탈로그·검수 목록의 후속 동기화는 별도 확인한다.

<b>카테고리 대표 위치 변경 · </b><b>2026-11-08</b>

사용자 요청으로 공용 카테고리 진입 명세를 홈화면 리디자인의 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>로 모았다. 현행 카테고리는 13개 메뉴로 정정했다: 기존 9개 계약의 문서 정리와 나머지 4개 WEB 모바일 계약 확정을 반영했다. 팀원 모집 동결 및 실제 SDK 적용·수집 검수는 별도다. 과거 회원가입 명세를 현행으로 포함한 오류를 철회하고, 해당 계정 원문은 기존 계정 문서에 보존한다. 홈에 통합한 것과 같은 클릭을 정의하는 서비스별 원문은 모두 중복 레거시로 보존한다. 주변상점·분실물·시간표·복덕방·팀원 모집 원문 5개와 기존 대응 문서 2개도 포함한다. 현행 구현 기준은 홈 3-6이며 원문·사진은 삭제하지 않는다. 새 로깅 계약을 폐기하지 않으며 아래 이전의 외부 대표 위치·이관 권고는 이 결정으로 대체한다. SDK 라벨·값·기존 플랫폼 범위와 팀원 모집 동결은 유지한다. 문서 이관만 완료됐으며 실제 Stage 화면·SDK 전송 검수는 각각 확인해야 한다.

<b>웹·모바일 공통 네이밍 — 최신 사용자 결정</b>

2026-11-05 같은 기능의 같은 이벤트는 WEB·ANDROID·IOS에서 공통 screen\_view와 event\_label을 사용한다. 이 6항목·8페이지의 종전 플랫폼별 분리 규정은 아래 계약으로 대체한다. screen\_view는 URL·별도 화면/모달 여부보다 해당 이벤트의 고정 논리 화면을 나타내며 label 두 번째 구간과 일치한다. 기존 value·event\_name·category·발생 시점·사진·DB 플랫폼 속성은 보존한다. 본문과 사진에서 UI 경로 차이는 설명할 수 있다.

| 공통 event\_label | 공통 screen\_view | 기준·대응 명세 | 발생 조건 |
| --- | --- | --- | --- |
| <code>timetable__timetable__semester_manage__edit_apply__click</code> | <code>timetable</code> | <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> · <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> | 학기 편집 확정·적용. 추가·삭제를 한 번에 적용하면 1회 |
| <code>chat__chat_list__chat_conversation__entry__click</code> | <code>chat_list</code> | <a href="https://app.notion.com/p/21a0221954bc838c9a3981d753328a4d">11-16.쪽지리스트_대화창_클릭</a> | 쪽지 목록 대화 선택. WEB 통합 화면의 목록 영역도 동일 |
| <code>board__lost_item_report__lost_item_report__submit</code> | <code>lost_item_report</code> | <a href="https://app.notion.com/p/37a0221954bc822d9b29812a9dbc33fe">11-14.분실물_게시글신고하기_신고하기_클릭</a> | 신고 내용 제출. 모달·별도 페이지 모두 신고 논리 화면 |
| <code>account__user_type_selection__sign_up__user_type__click</code> | <code>user_type_selection</code> | <a href="https://app.notion.com/p/9bd0221954bc833c845a818f39ef8ca0">1-7 정보입력_학생_외부인_구분(클릭)</a> · <a href="https://app.notion.com/p/6400221954bc829089cb01755624814f">1-7 정보입력_학생_외부인_구분(클릭)</a> | 회원가입 학생·외부인 선택 |
| <code>account__password_change__password_change__confirm__click</code> | <code>password_change</code> | <a href="https://app.notion.com/p/1250221954bc82a5bdb38115ed63b652">3-4 비밀번호수정완료(클릭)</a> · <a href="https://app.notion.com/p/1150221954bc8217aaee812619b3653f">3-4 비밀번호수정완료(클릭)</a> | 정보수정 경로의 비밀번호 변경 완료·실패 기존 조건 |

학기 추가·삭제 두 문서는 하나의 학기 편집 적용 계약을 공유한다. 실제 적용 버튼 1회에 하나의 이벤트만 전송하며 모바일 일괄 편집을 문서별로 중복 호출하지 않는다. WEB의 기존 연도·학기 value만으로 추가/삭제를 구별할 수 없는 한계는 남으며 value 정책을 임의 변경하지 않는다. 화면명 통일을 이유로 계정의 인증번호 발송·검증, 일반 프로필 수정, 시간표 목록 선택 등 다른 동작의 화면명을 일괄 치환하지 않는다. 품절 관련 동결·팀원 모집·새/미래 주변상점은 변경 제외다. SDK 적용·배포·실제 단일 전송은 미확인이다.

<b>최신 기준: 홈 리디자인 유지 · 외부 중복 명세는 레거시</b>

2026-11-05 사용자 결정으로 홈의 로깅은 모두 유지한다. 프로필 로그인·로그아웃·메인 콜밴팟 모집보기·버스 노선 조회·학교 부서 카테고리는 홈 명세를 현행 기준으로 사용하며, 겹치는 다른 서비스 명세는 레거시다. 이전의 외부 대표 명세 지정·같은 라벨 공동 구현·부서 별개 유지 안내보다 이 결정이 우선한다.

| 현행 홈 명세 | 레거시 원문 |
| --- | --- |
| <a href="https://app.notion.com/p/2660221954bc82719b1b01589fd83c1b">4-2 로그인 클릭</a> | <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> |
| <a href="https://app.notion.com/p/6d90221954bc83a8839d01823f621620">4-3 로그아웃 클릭</a> | <a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> |
| <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> | <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> |
| <a href="https://app.notion.com/p/1c50221954bc821f86e20145c98947fa">1-8 버스 노선 클릭</a> | <a href="https://app.notion.com/p/5dd0221954bc83bd8da7819f055c5270">[레거시] 1-14. 메인_버스_클릭</a> |
| <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a> | <a href="https://app.notion.com/p/4660221954bc82939cd001cf9a20ba4c">[레거시] 1-0-2 학교 부서정보 접근 (카테고리 진입)</a> |

레거시의 라벨·값·사진·플랫폼·이전 로깅은 삭제하지 않는다. 같은 클릭에 레거시 라벨을 추가 전송하지 않는다. 코드 대조 결과 일반 식단 카드 본문과 전체보기는 별도 클릭이므로 식단 1-2는 카드 본문 명세로 유지한다. 홈 1-3은 전체보기·더보기만 담당하며 같은 탭에 두 라벨을 함께 보내지 않는다. iOS 빈 상태 카드의 공유 콜백과 카드 본문의 명시 로그 누락 후보는 개발 검증 대상으로 남긴다. SDK 중단·전환·단일 전송은 미확인이다.

<b>동아리 전체 레거시 · </b><b>2026-11-04</b>

동아리 기존 명세 55개와 빈 행 2개는 과거 기록으로 보존한다. 이 사전에서 동아리 service·신규 feature·DA 담당자를 추가 배정하지 않는다.

<b>홈 7건 현행 기준 변경 · </b><b>2026-11-04</b>

사용자 지시로 아래 7건은 홈 페이지에 새 본문·사진을 이관하고 label 첫 구간을 main으로 변경했다. 원본 서비스별 페이지는 레거시다. 기능/detail·category·screen\_view·value·event\_name은 이관 원본대로 유지하며 DA1 6건·DA2 1건이다. 과거 표에 남은 이관 전 라벨·원본 링크는 변경 이력이다.

| 현행 홈 기준 | 새 event\_label |
| --- | --- |
| <a href="https://app.notion.com/p/0320221954bc838ba30c816a7787861c">1-9 주변 상점 전체보기 클릭</a> | <code>main__main__shop_entry__main_entry__click</code> |
| <a href="https://app.notion.com/p/1c50221954bc821f86e20145c98947fa">1-8 버스 노선 클릭</a> | <code>main__main__bus_entry__search_entry__click</code> |
| <a href="https://app.notion.com/p/2ca0221954bc8386a12f818e14a3d5af">1-7 버스 시간표 클릭</a> | <code>main__main__bus_entry__timetable_entry__click</code> |
| <a href="https://app.notion.com/p/3440221954bc83e3aabd01e76233e781">1-5 서틀 탑승권 클릭</a> | <code>main__main__bus_entry__ticket_entry__click</code> |
| <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a> | <code>main__main__more__click</code> |
| <a href="https://app.notion.com/p/ac20221954bc839c82b481e92e072a58">2-3 네비게이션 바 게시판 클릭</a> | <code>main__main__notice_entry__navigation_entry__click</code> |
| <a href="https://app.notion.com/p/e4c0221954bc83949b49016cfff27ccf">1-4 식단 코너 클릭</a> | <code>main__main__corner__select</code> |

<code>cafeteria__main__more__click</code>의 0800 대응 명세는 2026-11-04 사용자 요청으로 레거시·참조로 정리하고 현행 홈 1-3에 연결했다. 새 main 라벨과 동일 라벨 계약으로 간주하지 않으며 SDK 전환은 별도 검증한다. 품절 관련 명세는 변경하지 않는다.

※ 네이밍룰 v1.0 확정 (2026-10-28): label은 공통 확정본(<a href="https://app.notion.com/p/4000221954bc81469ea6dbe19c7d8be7">로깅 네이밍룰 v1.0 — DA1·DA2 공통 확정본</a>)의 <code>service__page__feature[__detail]__category</code> 형식으로 통일. 아래 2026-10-15\~16 대응표와 label 예시는 변경 이력이며 현행 label은 각 명세 페이지를 따른다.

- 확정일: 2026-10-16
- 적용 범위: 기존에 작업한 계정·로그인, 게시판, 배너, 분실물, 콜밴팟, 쪽지·채팅, 모의수강신청, 학교 부서 정보, 교내 시설물의 새 명세. event\_name은 DA2다.
- 관련 기준: <a href="https://app.notion.com/p/0e40221954bc823d92c301f83b5f68d0">화면 정의 및 로깅 검수</a>, <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>.

작성 순서·공통 기준·확정 사항·남은 후속은 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>를 따른다.

## 1. label 작성 기준

<code>{service}__{page}__{feature}[__{detail}]__{category}</code>

- label은 4\~5구간이며 마지막 구간은 항상 해당 event\_category 값이다. detail은 필요한 경우에만 최대 한 구간 넣는다. 결과형 품절 제보의 동결 예외는 기존 라벨을 그대로 유지한다.
- 구간 구분자는 <code>__</code>, 구간 안 단어 구분자는 <code>_</code>다. detail과 category를 합치지 않는다. 예: <code>user_type__click</code>, <code>phone__click</code>. 승인 category가 select인 별도 계약만 select를 사용한다. category 단어를 detail에 반복하지 않는다.
- 기능은 같은 목적·대상·흐름의 동작을 묶는다. 사전에서 동일 기능명을 재사용하고, 필요한 세부 동작은 feature 뒤의 detail로 구분한다. 마지막 구간은 category다. 새 기능이 필요하면 포함할 행동과 목적을 함께 기록한 뒤 사전에 추가한다.
- 페이지는 정의된 고정 화면명이며 screen\_view는 event\_label의 두 번째 구간과 정확히 같게 작성한다. 공용 헤더는 <code>header</code>, 푸터는 <code>footer</code>다. 기능명 정리는 label·value·발생 시점을 임의 변경하는 승인이 아니다.
- 기능·행동 네이밍 통일은 이벤트 통합·추가 전송·보류 해제를 뜻하지 않는다. 별도 승인한 분실물 필터만 통합한다.
- 물품·검색어·선택값·게시물 ID 등 변하는 값은 label에 넣지 않고 value 또는 합의한 파라미터로 전송한다.
- 방식 A (2026-10-28 사용자 확인): 승인 category를 이름 정리 때문에 바꾸지 않는다. label 끝을 해당 값에 맞춘다. 예: <code>search__click</code>, <code>sign_up__user_type__click</code>, <code>sign_up__confirm__click</code>. 승인된 submit/select/toggle 계약은 그 값을 유지한다.
- 공용 <code>shop_entry</code>의 홈 카테고리 카드 detail은 <code>category_card_entry</code>, <code>bus_entry</code>의 홈 버튼은 <code>main_entry</code>다. 둘 다 page/screen은 <code>main</code>이다. <code>category_entry</code>는 <code>main_category</code> 메뉴에 한정한다.

## 2. 행동 용어

detail과 category는 서로 다른 구간이다. 아래 예시의 <code>__</code>는 두 구간을 나누며, 마지막 category는 연결 명세의 기존 승인값을 따른다. <code>click</code>을 선택·제출이라는 설명만으로 <code>select</code>·<code>submit</code>으로 바꾸지 않는다.

- entry: 화면·서비스·대화 진입 detail. 위치가 필요하면 <code>header_entry</code>, <code>footer_entry</code>, <code>category_entry</code>, <code>title_entry</code>로 구분하고 뒤에 승인 category를 붙인다.
- open / confirm / response: 열기 / 최종 값 확정 / 예·아니오 응답을 구분하는 detail. 예: <code>open__click</code>, <code>departure_confirm__select</code>, <code>join_response__click</code>. 같은 confirm 단어라도 category·전송 시점은 원래 계약을 따른다.
- select: 승인된 선택 category다. 대상은 detail로 두며 예: <code>filter__tab__select</code>, <code>keyword_manage__recommended_keyword__select</code>. category 단어를 detail에 다시 붙이지 않는다.
- submit: 승인된 제출·실행 category다. 예: <code>search__submit</code>, <code>keyword_manage__add__submit</code>. 모의수강신청의 <code>course_application__lecture__click</code>과 계정의 <code>sign_up__confirm__click</code>은 기존 click을 유지한다. 서버 성공 시점으로 바꾸지 않는다.
- click: 승인된 클릭 category다. 예: <code>contact__phone__click</code>, <code>search__search_input__click</code>, <code>keyword_manage__delete__click</code>.
- toggle / scroll / swipe / exposure / fail: 승인된 category일 때만 마지막 구간에 쓴다. 예: <code>keyword_manage__notification__toggle</code>. 같은 notification detail의 기존 click 계약과 임의 통합하지 않는다.
- back / return: 뒤로가기 / 지정 화면 복귀 detail. <code>back</code>, <code>notice_list_return</code>, <code>main_return</code>처럼 구분하고 뒤에 승인 category를 붙인다.
- success / available: 원문이 성공·사용 가능 결과 시점으로 정한 경우의 detail이다. <code>code_verify_success</code>, <code>id_available</code>, <code>nickname_available</code>의 기존 발생 조건을 유지하고 뒤에 승인 category를 붙인다.

## 3. 기능 사전

- 카테고리 콜밴팟 최신 결정 (2026-11-01): 현행은 홈 3-6 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 기존 <code>category_navigation</code> / <code>callvan_entry</code> → <code>click</code>이다. 콜밴팟 1-3 <a href="https://app.notion.com/p/80c0221954bc8396a38f01b1df7cbcd8">[레거시] 1-3 카테고리 → 콜밴팟 모집</a>의 <code>callvan_entry</code> / <code>category_entry</code> → <code>click</code>은 레거시 이력으로만 보존한다. 아래 과거 변경 대응표의 1-3 행도 이력이며 현행 적용 대상이 아니다. 새 로깅·라벨·추가 전송·동일 계약은 만들지 않는다. 메인 모집 보기의 기존 <code>recruitment_list_entry</code> 계약은 유지한다.

2026-10-28 방식 A 사용자 확인 반영. 아래 표는 현재 명세에 있는 feature와 detail/category 조합을 한 곳에서 확인하기 위한 현행 표다. 실제 SDK·dbt 반영이나 새로운 전송 시점 승인을 뜻하지 않는다.

- category는 기존 승인값을 유지하고 label 마지막 구간과 일치시킨다. 같은 제출 동작이어도 승인된 <code>click</code>과 <code>submit</code>이 공존할 수 있다.
- detail이 없으면 4구간이다. 표의 <code>없음</code>은 label에 넣을 문자열이 아니다.
- 조합은 연결 명세별 조건을 따른다. 서로 다른 행·조합의 detail과 category를 임의로 교차 결합하지 않는다.
- 팀원 모집은 이번 변경 제외다. 해당 기능·detail·category는 기존 정의를 그대로 표시하며 이 표를 근거로 다시 이름을 바꾸지 않는다.
- 품절 관련 동결 5페이지는 원문 유지다. 결과형 예외와 label은 이 작업으로 변경하지 않는다.
- <code>lecture_add</code>의 웹 2-18은 [확인한 코드](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/a1bd96d8b0b426e8c6a4b54ea643e7a7e2a7bd23/src/components/TimetablePage/components/LectureList/index.tsx#L109-L120)에서 한 번 클릭 시 미리 보기 선택, 더블클릭 시 과목 추가로 구분된다. 2-18의 <code>lecture_entry</code>를 유지하며 추가·저장 성공으로 해석하지 않는다. 운영 배포·SDK의 실제 전송은 별도 미확인이다.

<table>
<tr>
<td>
기능명
</td>
<td>
목적과 범위
</td>
<td>
서비스
</td>
<td>
현행 detail → category 조합
</td>
<td>
발생 조건
</td>
<td>
근거 명세
</td>
</tr>
<tr>
<td>
<code>account_config</code>
</td>
<td>
계정 설정 진입
</td>
<td>
홈화면 리디자인
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/82f0221954bc8307929201bfe07559ed">4-4 설정 클릭</a>
</td>
</tr>
<tr>
<td>
<code>account_recovery</code>
</td>
<td>
아이디·비밀번호 찾기
</td>
<td>
로그인/회원가입/정보수정 V2·사장님
</td>
<td>
<code>id_entry</code> → <code>click</code>; <code>password_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bda0221954bc833eb901010249bdaac2">2-5 비밀번호찾기(클릭)</a> · <a href="https://app.notion.com/p/cd20221954bc8307a5b38176275d6992">2-4 아이디찾기(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>callvan_chat</code>
</td>
<td>
콜밴팟 단체 채팅
</td>
<td>
콜밴팟
</td>
<td>
<code>card_entry</code> → <code>click</code>; <code>message_send</code> → <code>click</code>; <code>participant_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/02b0221954bc828991040191d3ae2c3f">2-7 콜밴팟 채팅 전송</a> · <a href="https://app.notion.com/p/6900221954bc83729a9781ba8343aee6">2-10 콜밴팟 채팅방 입장 클릭</a>
</td>
</tr>
<tr>
<td>
<code>callvan_entry</code>
</td>
<td>
콜밴팟 목록 진입
</td>
<td>
콜밴팟·홈화면 리디자인
</td>
<td>
<code>recruitment_list_entry</code> → <code>click</code><br />현행 메인 모집 보기 근거: <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> · <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a>. 기존 근거 칸의 1-3은 레거시 참조이며 현행 적용 대상이 아니다.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> · <a href="https://app.notion.com/p/80c0221954bc8396a38f01b1df7cbcd8">[레거시] 1-3 카테고리 → 콜밴팟 모집</a>
</td>
</tr>
<tr>
<td>
<code>callvan_participation</code>
</td>
<td>
참여·참여취소 확인 응답
</td>
<td>
콜밴팟
</td>
<td>
<code>cancel_response</code> → <code>click</code>; <code>join_response</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/b380221954bc82a78d25814da4b3d86d">2-5 콜밴팟 참여 취소하기</a> · <a href="https://app.notion.com/p/efd0221954bc8367ad8c01a1cab38cd1">2-4 콜밴팟 참여하기</a>
</td>
</tr>
<tr>
<td>
<code>callvan_write</code>
</td>
<td>
콜밴팟 모집글 작성
</td>
<td>
콜밴팟
</td>
<td>
<code>arrival_confirm</code> → <code>click</code>; <code>confirm</code> → <code>click</code>; <code>departure_confirm</code> → <code>click</code>; <code>departure_time_confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/3770221954bc82c2a0a881f6e84cf070">3-4 콜밴팟 모집 작성 완료</a> · <a href="https://app.notion.com/p/68f0221954bc8223a01881e4a00e304a">2-9·3-6 콜밴팟 목록 → 모집하기</a>
</td>
</tr>
<tr>
<td>
<code>category_navigation</code>
</td>
<td>
3-6 공용 카테고리 13개 메뉴 클릭
</td>
<td>
홈화면 리디자인
</td>
<td>
<code>team_recruit_entry</code> → <code>click</code>; <code>lost_item_entry</code> → <code>click</code>; <code>facility_entry</code> → <code>click</code>; <code>department_entry</code> → <code>click</code>; <code>cafeteria_entry</code> → <code>click</code>; <code>shop_entry</code> → <code>click</code>; <code>timetable_entry</code> → <code>click</code>; <code>search_entry</code> → <code>click</code>; <code>callvan_entry</code> → <code>click</code>; <code>chat_entry</code> → <code>click</code>; <code>real_estate_entry</code> → <code>click</code>; <code>owner_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>
</td>
</tr>
<tr>
<td>
<code>chat_conversation</code>
</td>
<td>
공용 쪽지 대화 선택
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/21a0221954bc838c9a3981d753328a4d">11-16.쪽지리스트_대화창_클릭</a>
</td>
</tr>
<tr>
<td>
<code>chat_entry</code>
</td>
<td>
공용 쪽지·채팅 진입
</td>
<td>
게시판·팀원 모집
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code><br />팀원 모집 제외 · 기존 정의 유지: <code>entry</code>, <code>applicant_entry</code>, <code>group_entry</code> / category: 각 기존 명세 유지
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/15d0221954bc82da9b0001cb92292190">11-17.헤더_쪽지_클릭</a> · <a href="https://app.notion.com/p/1d20221954bc827d923581192263ebbf">[레거시] 11-15.카테고리_채팅(쪽지)_클릭</a><br /><br />2026-11-04 기존 카테고리 명세는 레거시 참조다. 현행은 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 category_navigation / chat_entry → click이다. 헤더·푸터 계약은 유지한다.
</td>
</tr>
<tr>
<td>
<code>contact</code>
</td>
<td>
콜밴팟 전화·학교 부서 연락처 복사
</td>
<td>
주변상점·콜밴팟·학교 부서 정보
</td>
<td>
<code>phone</code> → <code>click</code>; <code>phone_copy</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/2d50221954bc834f8ca9019292dd4741">3-2 상점상세 전화 (클릭)</a> · <a href="https://app.notion.com/p/3d50221954bc824e9a1e81e83e042833">4-5 전화 주문 혜택 상점상세 전화 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>course_application</code>
</td>
<td>
모의수강신청 진입·과목 신청
</td>
<td>
모의수강신청·시간표
</td>
<td>
<code>entry</code> → <code>click</code>; <code>lecture</code> → <code>click</code>; <code>preselected</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/2510221954bc82d8804901536761828c">1-3. 모의수강신청_강좌 신청 클릭</a> · 진입 대표: <a href="https://app.notion.com/p/e4c0221954bc828f8f77018f22ccff49">0. (웹) 모의수강신청 진입</a> · 중복 이력: <a href="https://app.notion.com/p/36c0221954bc83a9b1c881a0e87ceb81">[레거시·중복 명세] 2-22. (웹) 시간표_모의 수강신청 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>department_category</code>
</td>
<td>
부서 내부 분류 선택
</td>
<td>
학교 부서 정보
</td>
<td>
<code>없음</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/9a40221954bc825ca9da01d7e8129ffc">1-1 카테고리 클릭</a>
</td>
</tr>
<tr>
<td>
<code>department_entry</code>
</td>
<td>
학교 부서 서비스 진입
</td>
<td>
학교 부서 정보
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/2370221954bc83afaba301e35693f565">1-0-1 학교 부서 정보 접근 (푸터 진입)</a> · <a href="https://app.notion.com/p/3320221954bc82cc95f10156b7668099">1-0 학교 부서 정보 접근 (헤더 진입)</a>
</td>
</tr>
<tr>
<td>
<code>external_link</code>
</td>
<td>
외부 사이트·원본 바로가기
</td>
<td>
게시판
</td>
<td>
<code>original_entry</code> → <code>click</code>; <code>shortcut_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/7ae0221954bc8322930581d4782416b6">5-3. 공지 원본 바로가기_클릭</a> · <a href="https://app.notion.com/p/a100221954bc82429edf81333432e776">3-2. 공지사항_바로가기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>facility_entry</code>
</td>
<td>
교내 시설물 서비스 진입
</td>
<td>
게시판
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/29a0221954bc82788e2c81c4dbec50d7">10-1. 헤더_교내 시설물 정보_클릭</a> · <a href="https://app.notion.com/p/3820221954bc82f9a58781fbc1b57a12">[레거시] 10-3. 카테고리_교내 시설물 정보_클릭</a><br /><br />2026-11-04 기존 카테고리 명세는 레거시 참조다. 현행은 <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 category_navigation / facility_entry → click이다. 헤더·푸터 계약은 유지한다.
</td>
</tr>
<tr>
<td>
<code>filter</code>
</td>
<td>
공지·분실물·콜밴팟 필터 열기·선택·적용
</td>
<td>
게시판·버스·주변상점·콜밴팟·팀원 모집
</td>
<td>
<code>apply</code> → <code>click</code>; <code>bus_type</code> → <code>click</code>; <code>bus_type</code> → <code>select</code>; <code>category</code> → <code>click</code>; <code>checkbox</code> → <code>select</code>; <code>city_direction</code> → <code>select</code>; <code>city_route</code> → <code>select</code>; <code>daeseong_direction</code> → <code>select</code>; <code>keyword</code> → <code>select</code>; <code>min_amount</code> → <code>select</code>; <code>open</code> → <code>click</code>; <code>quick_filter</code> → <code>select</code>; <code>shuttle_route</code> → <code>select</code>; <code>sort</code> → <code>select</code>; <code>tab</code> → <code>select</code>; <code>to_home</code> → <code>click</code>; <code>to_school</code> → <code>click</code><br />팀원 모집 제외 · 기존 정의 유지: <code>checkbox</code>, <code>sort</code>, <code>category</code>, <code>quick_filter</code>, <code>min_amount</code>, <code>daeseong_direction</code>, <code>city_direction</code>, <code>bus_type</code>, <code>shuttle_route</code>, <code>to_home</code>, <code>to_school</code>, <code>city_route</code>, <code>status</code>, <code>reset</code>, <code>apply</code>, <code>open</code>, <code>method</code>, <code>close</code> / category: 각 기존 명세 유지
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0090221954bc83caa53201000c97e7db">2-18 상점 카테고리 최소주문금액 설정 - 레거시</a> · <a href="https://app.notion.com/p/1490221954bc828fbc28815a97a32f94">5-12. 교통편 차종_클릭</a>
</td>
</tr>
<tr>
<td>
<code>keyword_manage</code>
</td>
<td>
공지·분실물 키워드 관리
</td>
<td>
게시판
</td>
<td>
<code>add</code> → <code>submit</code>; <code>delete</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>notification</code> → <code>click</code>; <code>notification</code> → <code>toggle</code>; <code>recommended_keyword</code> → <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/4760221954bc8316a54a81a8b347f918">12-4. 키워드 알림받기_클릭</a> · <a href="https://app.notion.com/p/0490221954bc82298d940143a3b6a266">7-1. 키워드 관리_클릭</a>
</td>
</tr>
<tr>
<td>
<code>login</code>
</td>
<td>
로그인 진입·실행
</td>
<td>
로그인/회원가입/정보수정 V2·사장님·홈화면 리디자인
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>없음</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0540221954bc8395b443814167ca48b1">4-1 로그인 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>login_popup</code>
</td>
<td>
로그인 안내 팝업 응답
</td>
<td>
게시판·시간표·주변상점
</td>
<td>
<code>close</code> → <code>click</code>; <code>login_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/40c0221954bc830a8ea4015f95cf4e1f">3-23 상점상세 리뷰작성 _로그인_취소 (클릭)</a> · <a href="https://app.notion.com/p/a450221954bc82e5b34281b954d80f08">2-29. (웹) 시간표_로그인 팝업_취소하기 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>logout</code>
</td>
<td>
로그아웃
</td>
<td>
로그인/회원가입/정보수정 V2·홈화면 리디자인
</td>
<td>
<code>없음</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> · <a href="https://app.notion.com/p/d8b0221954bc83eb94650156db128382">4-1 로그아웃(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_delete</code>
</td>
<td>
분실물·습득물 삭제
</td>
<td>
게시판
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>open</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/37b0221954bc838a8ac48197faf0541d">11-6.분실물_습득물신고_삭제확인_클릭</a> · <a href="https://app.notion.com/p/f890221954bc8341b0a701c76ac55892">11-5.분실물_습득물_삭제_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_detail</code>
</td>
<td>
분실물·습득물 상세 진입
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0b60221954bc8278b63a016f2e8b03a6">11-24. 분실물_게시글_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_edit</code>
</td>
<td>
분실물·습득물 수정 — 11-29·11-30 적용 대상 확정
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>submit</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bf30221954bc82f995e501455ac1d711">11-30. 분실물_수정완료_클릭</a> · <a href="https://app.notion.com/p/6b40221954bc82b38a5b01c509b2222d">11-29. 분실물_수정_버튼_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_entry</code>
</td>
<td>
분실물 서비스 진입
</td>
<td>
게시판
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>main_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/3470221954bc826ca5c38185e5348e37">11-32. 헤더_분실물_클릭</a> · <a href="https://app.notion.com/p/4580221954bc8381a5f081247e03288e">[레거시·중복 원문] 11-21. 카테고리_분실물_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_message</code>
</td>
<td>
분실물·습득물 쪽지 진입
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/74c0221954bc832eaf4e8126dc10c6cc">11-12.분실물_쪽지보내기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_report</code>
</td>
<td>
게시물 신고
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>submit</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/37a0221954bc822d9b29812a9dbc33fe">11-14.분실물_게시글신고하기_신고하기_클릭</a> · <a href="https://app.notion.com/p/e6b0221954bc831f9a1d01ed1a3bb145">11-13.분실물_신고하기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_status</code>
</td>
<td>
분실물 상태 변경
</td>
<td>
게시판
</td>
<td>
<code>found_confirm</code> → <code>click</code>; <code>open</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/aac0221954bc8364b36b81377bd730b5">11-27. 분실물_상태변경_클릭</a> · <a href="https://app.notion.com/p/b7d0221954bc82d387e581ae8037751f">11-28. 분실물_찾음_버튼_클릭</a>
</td>
</tr>
<tr>
<td>
<code>lost_item_write</code>
</td>
<td>
분실물·습득물 작성
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>; <code>item_add</code> → <code>click</code>; <code>item_category</code> → <code>select</code>; <code>post_type</code> → <code>select</code>; <code>없음</code> → <code>submit</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/7fa0221954bc826387d001b996d833b3">11-11.분실물_분실물신고_작성완료_클릭</a> · <a href="https://app.notion.com/p/b140221954bc825eb442014df33f2f90">11-4.분실물_습득물신고_작성완료_클릭</a>
</td>
</tr>
<tr>
<td>
<code>modal</code>
</td>
<td>
메인 배너 모달
</td>
<td>
배너
</td>
<td>
<code>close</code> → <code>click</code>; <code>hide_7d</code> → <code>click</code>; <code>next</code> → <code>click</code>; <code>next</code> → <code>swipe</code>; <code>없음</code> → <code>click</code>; <code>없음</code> → <code>exposure</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6400221954bc82c58d4a01c203a5e06d">1-5. (모바일)메인_다음모달_스왑</a> · <a href="https://app.notion.com/p/58a0221954bc8299aba081716dcade0b">1-3. 메인_모달닫기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>navigation</code>
</td>
<td>
뒤로가기·목록·메인 복귀
</td>
<td>
게시판·모의수강신청·버스·시간표·주변상점·콜밴팟·팀원 모집
</td>
<td>
<code>back</code> → <code>click</code>; <code>back</code> → <code>swipe</code>; <code>bus_search_return</code> → <code>click</code>; <code>main_return</code> → <code>click</code>; <code>nearby_entry</code> → <code>click</code>; <code>notice_list_return</code> → <code>click</code>; <code>order_history_entry</code> → <code>click</code>; <code>review_exit</code> → <code>click</code><br />팀원 모집 제외 · 기존 정의 유지: <code>review_exit</code>, <code>back</code>, <code>nearby_entry</code>, <code>order_history_entry</code>, <code>bus_search_return</code>, <code>main_return</code> / category: 각 기존 명세 유지
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/02a0221954bc835181bf818c2a57779e">2-19 상점 카테고리 → 홈 - 레거시</a> · <a href="https://app.notion.com/p/5340221954bc826d95bf016a2eb7895c">5-7. 뒤로가기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>notice_detail</code>
</td>
<td>
공지 상세 진입
</td>
<td>
게시판
</td>
<td>
<code>entry</code> → <code>click</code>; <code>keyword_notification_entry</code> → <code>click</code>; <code>popular_post_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/5690221954bc82c3afd881ec1864a3b2">6-4. 공지글 검색_공지상세_클릭</a> · <a href="https://app.notion.com/p/76a0221954bc839ab58e01d56b51c40f">3-1. 공지사항_가장 많이 본 게시물_클릭</a>
</td>
</tr>
<tr>
<td>
<code>notice_entry</code>
</td>
<td>
공지사항 서비스 진입
</td>
<td>
게시판
</td>
<td>
<code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>more_entry</code> → <code>click</code>; <code>navigation_entry</code> → <code>click</code>; <code>title_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/29b0221954bc82ad8c9201dc7628f57f">2-1. 헤더_공지사항_클릭</a> · <a href="https://app.notion.com/p/2de0221954bc8295b75d01c951e05d36">1-1.메인_공지사항_더보기_클</a>
</td>
</tr>
<tr>
<td>
<code>notice_list</code>
</td>
<td>
공지 목록 탐색
</td>
<td>
게시판
</td>
<td>
<code>없음</code> → <code>scroll</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/4290221954bc83ac8cc581ceced3f5f7">4-2. 공지사항 페이지_스크롤(상하)</a>
</td>
</tr>
<tr>
<td>
<code>password_change</code>
</td>
<td>
정보 수정 경로의 비밀번호 변경
</td>
<td>
로그인/회원가입/정보수정 V2
</td>
<td>
<code>confirm</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1150221954bc8217aaee812619b3653f">3-4 비밀번호수정완료(클릭)</a> · <a href="https://app.notion.com/p/1250221954bc82a5bdb38115ed63b652">3-4 비밀번호수정완료(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>profile_edit</code>
</td>
<td>
계정·프로필 정보 수정
</td>
<td>
로그인/회원가입/정보수정 V2·팀원 모집
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code><br />팀원 모집 제외 · 기존 정의 유지: <code>entry</code>, <code>load</code>, <code>major</code>, <code>next</code>, <code>skill_add</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>activity_add</code>, <code>activity_add_confirm</code>, <code>open</code>, <code>confirm</code>, <code>cancel</code> / category: 각 기존 명세 유지
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/3880221954bc82cab508816eaa753bd3">3-1 헤더_정보수정하기(클릭)</a> · <a href="https://app.notion.com/p/8290221954bc8278bc2b013efa8c22fe">3-3 정보수정완료(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>search</code>
</td>
<td>
공지·콜밴팟·학교 부서·모의수강신청 검색·조회
</td>
<td>
게시판·모의수강신청·버스·시간표·주변상점·콜밴팟·팀원 모집·학교 부서 정보
</td>
<td>
<code>arrival_confirm</code> → <code>select</code>; <code>arrival_open</code> → <code>click</code>; <code>curriculum</code> → <code>select</code>; <code>department</code> → <code>click</code>; <code>department</code> → <code>select</code>; <code>departure_confirm</code> → <code>select</code>; <code>departure_open</code> → <code>click</code>; <code>departure_time_confirm</code> → <code>click</code>; <code>departure_time_now</code> → <code>click</code>; <code>departure_time_open</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>popular_keyword</code> → <code>select</code>; <code>search_input</code> → <code>click</code>; <code>swap</code> → <code>click</code>; <code>없음</code> → <code>click</code>; <code>없음</code> → <code>submit</code><br />팀원 모집 제외 · 기존 정의 유지: <code>departure_confirm</code>, <code>departure_open</code>, <code>departure_time_now</code>, <code>arrival_confirm</code>, <code>arrival_open</code>, <code>departure_time_confirm</code>, <code>swap</code>, <code>departure_time_open</code>, <code>department</code>, <code>curriculum</code> / category: 각 기존 명세 유지
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0a00221954bc83bca117013903d780d7">2-20. (웹) 시간표_수정_해당 학부 (클릭)</a> · <a href="https://app.notion.com/p/3590221954bc82af9069812df48a7ce8">5-11. 완료_클릭</a>
</td>
</tr>
<tr>
<td>
<code>sign_up</code>
</td>
<td>
회원가입 전체 흐름
</td>
<td>
로그인/회원가입/정보수정 V2·사장님
</td>
<td>
<code>code_verify_success</code> → <code>click</code>; <code>confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>menu_entry</code> → <code>click</code>; <code>id_available</code> → <code>click</code>; <code>next</code> → <code>click</code>; <code>nickname_available</code> → <code>click</code>; <code>send_code</code> → <code>click</code>; <code>terms_agree</code> → <code>click</code>; <code>user_type</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0820221954bc834eb41301752196a7d5">1-2 회원가입진입(클릭)</a> · <a href="https://app.notion.com/p/3630221954bc82c98974813502966a87">1-1 헤더_회원가입진입(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>review_report</code>
</td>
<td>
상점 리뷰 신고 화면 진입과 신고 완료 버튼 클릭
</td>
<td>
주변상점
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/a200221954bc8282ab5701cb4978f627">3-14 상점상세 리뷰 신고 (클릭)</a> · <a href="https://app.notion.com/p/c810221954bc835381ed81ae8f0e5ce9">3-15 상점상세 리뷰 신고 완료 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>review_write</code>
</td>
<td>
상점 리뷰 작성 화면 진입과 작성 완료 버튼 클릭
</td>
<td>
주변상점
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0d40221954bc835b82a281b6adedd95d">3-13 상점상세 리뷰작성 들어간후(클릭)</a> · <a href="https://app.notion.com/p/db00221954bc82f5a2148164f7e27474">3-12 상점상세 리뷰작성 들어가기 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>review_delete</code>
</td>
<td>
상점 리뷰 삭제창 열기·최종 삭제·취소
</td>
<td>
주변상점
</td>
<td>
<code>cancel</code> → <code>click</code>; <code>confirm</code> → <code>click</code>; <code>open</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/54a0221954bc8367b002012884670248">3-20 상점상세 리뷰 최종삭제하기 (클릭)</a> · <a href="https://app.notion.com/p/a130221954bc83b9bb2b011f769a00ff">3-19 상점상세 리뷰 삭제하기 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shop_detail</code>
</td>
<td>
상점 카드에서 상세 화면 진입
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/8f00221954bc83d0afe881e3ddd2deed">3-1 상점 카테고리 → 상점상세 (클릭)</a> · <a href="https://app.notion.com/p/dd10221954bc839392818196deaac6e0">4-4 전화 주문 혜택 상점상세 페이지(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shop_event</code>
</td>
<td>
상점 이벤트 영역·이벤트 상점 선택과 목록 탐색
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>scroll</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0a30221954bc83ed998d01d79b96fb0b">3-9 상점상세 이벤트 (스크롤)</a> · <a href="https://app.notion.com/p/69f0221954bc83c9adb481420b9fb21f">3-8 상점상세 이벤트 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shop_list</code>
</td>
<td>
상점 목록 스크롤 탐색
</td>
<td>
주변상점
</td>
<td>
<code>없음</code> → <code>scroll</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/c9c0221954bc82da8f7b8141ef147047">2-2 상점 카테고리 (스크롤)</a>
</td>
</tr>
<tr>
<td>
<code>shop_benefit</code>
</td>
<td>
전화 주문 혜택 상점 모아보기 진입
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/19c0221954bc837b85ed813f6a80e9df">4-3 카테고리에서 혜택페이지(클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shop_review</code>
</td>
<td>
상점 리뷰 탭 진입과 리뷰 목록 탐색
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>scroll</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6570221954bc831683fe81c8826bffc4">3-11 상점상세 리뷰 (스크롤)</a> · <a href="https://app.notion.com/p/6700221954bc829490bf812977cce992">3-10 상점상세 리뷰 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>photo_view</code>
</td>
<td>
사진 보기 열기와 사진 슬라이드 이동; 파일 업로드와 구분
</td>
<td>
복덕방·식단·주변상점
</td>
<td>
<code>open</code> → <code>click</code>; <code>slide</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1700221954bc827b8c48019d6a980646">3-3 상점상세 사진 (클릭)</a> · <a href="https://app.notion.com/p/35e0221954bc82eebe7201b2af3e755d">4-1. 식단_코너 사진_클릭</a>
</td>
</tr>
<tr>
<td>
<code>shop_entry</code>
</td>
<td>
주변상점 서비스 진입; 메인 일반 진입과 카테고리 값 선택 진입 구분
</td>
<td>
주변상점
</td>
<td>
<code>category_card_entry</code> → <code>click</code>; <code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>main_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/3bd0221954bc82c8a6cd01f8d9c902d4">1-5 카테고리 → 주변상점 (클릭) - 레거시</a> · <a href="https://app.notion.com/p/6590221954bc833897ce01751fa56dbc">1-4 푸터 → 주변상점 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shop_cart</code>
</td>
<td>
장바구니 진입
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/b3a0221954bc82b984dd015025c78148">2-9 상점 카테고리 → 카트 - 레거시</a>
</td>
</tr>
<tr>
<td>
<code>real_estate_entry</code>
</td>
<td>
복덕방 서비스 진입; 웹 메뉴와 앱 카테고리에서 같은 진입 계약 사용
</td>
<td>
복덕방
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1740221954bc83cebc8601faa22ca3a5">1-1 헤더_복덕방 진입(클릭)</a> · <a href="https://app.notion.com/p/2640221954bc83d6a82901c92388b825">[레거시] 1-3 햄버거_복덕방 진입 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>room_detail</code>
</td>
<td>
방 카드에서 복덕방 상세 화면 진입
</td>
<td>
복덕방
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/5da0221954bc829d8cc70189be42fb74">2-1 복덕방 목록_방 카드 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>shop_manage</code>
</td>
<td>
사장님 가게 정보 수정 진입·이미지 추가·운영시간 설정·저장·취소·닫기
</td>
<td>
사장님
</td>
<td>
<code>close</code> → <code>click</code>; <code>edit_cancel</code> → <code>click</code>; <code>edit_confirm</code> → <code>click</code>; <code>edit_entry</code> → <code>click</code>; <code>image_add</code> → <code>click</code>; <code>time_edit</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1360221954bc837abbd7017830ceb477">2-3 가게 정보 수정 - 시간 수정</a> · <a href="https://app.notion.com/p/22d0221954bc82f7be2501d0361154f9">2-4 가게 정보 수정 - 이미지 추가</a>
</td>
</tr>
<tr>
<td>
<code>shop_event_manage</code>
</td>
<td>
사장님 이벤트 추가·수정·삭제; 추가/수정 저장 확인과 취소 구분
</td>
<td>
사장님
</td>
<td>
<code>add_cancel</code> → <code>click</code>; <code>add_confirm</code> → <code>click</code>; <code>add_entry</code> → <code>click</code>; <code>delete</code> → <code>click</code>; <code>edit_confirm</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/51e0221954bc83449571811347a16bc3">1-2 이벤트 추가 - 등록하기</a> · <a href="https://app.notion.com/p/7d50221954bc8332862301d66a85dc6a">1-1 이벤트 추가</a>
</td>
</tr>
<tr>
<td>
<code>shop_menu_manage</code>
</td>
<td>
사장님 메뉴 추가 진입·사진 추가·등록 확인·취소
</td>
<td>
사장님
</td>
<td>
<code>add_cancel</code> → <code>click</code>; <code>add_confirm</code> → <code>click</code>; <code>add_entry</code> → <code>click</code>; <code>image_add</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/5030221954bc82f095f0817d9324b9d0">3-3 메뉴추가 - 취소</a> · <a href="https://app.notion.com/p/9420221954bc83c2b32d813e10ec3f75">3-4 메뉴추가 - 메뉴사진</a>
</td>
</tr>
<tr>
<td>
<code>meal_time</code>
</td>
<td>
식사 시간 선택과 선택한 시간의 식단 목록 스크롤
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>scroll</code>; <code>없음</code> → <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/9f20221954bc8275b0f301f1b220b3f5">3-4. 식단_아침_스크롤</a> · <a href="https://app.notion.com/p/e5f0221954bc821c881e01997734ea21">3-1. 식단_식사시간 선택 (클릭) - 3-2·3-3 통합</a>
</td>
</tr>
<tr>
<td>
<code>corner</code>
</td>
<td>
메인 식단 위젯의 표시 코너 선택; 화면 이동 없음
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6d40221954bc838e93c30176607ca0ce">1-3.메인_식단_A코너_클릭 (레거시)</a>
</td>
</tr>
<tr>
<td>
<code>cafeteria_entry</code>
</td>
<td>
식단 서비스 진입; 헤더·푸터·카카오 외부 진입
</td>
<td>
식단
</td>
<td>
<code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>; <code>kakao_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/8f50221954bc82e4ac5201545f5fa260">2-2. 푸터_식단_클릭</a> · <a href="https://app.notion.com/p/c420221954bc831497240194ccc6ae54">2-1. 헤더_식단_클릭</a>
</td>
</tr>
<tr>
<td>
<code>meal</code>
</td>
<td>
메인 식단 위젯 한정. 메인 식단 칸 클릭; 기존 홈화면 리디자인 이력 유지
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/d400221954bc8338b341011b9a488dac">1-2.메인_식단_클릭 (레거시)</a>
</td>
</tr>
<tr>
<td>
<code>more</code>
</td>
<td>
메인 식단 위젯 한정. 메인 식단 더보기; 기존 1-1 대표 명세와 중복 참고 명세의 공통 계약
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a> · <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a>
</td>
</tr>
<tr>
<td>
<code>ab_test</code>
</td>
<td>
식단 상점가기 배너 A/B 그룹 노출; 품절 제보 실험과 별개
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>exposure</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/ca20221954bc8338ab2b8107ff9e4663">0-2. 식단_ABtest_진입</a>
</td>
</tr>
<tr>
<td>
<code>cafeteria_info</code>
</td>
<td>
학생식당 운영 정보 진입
</td>
<td>
식단
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/7e40221954bc8363933501688180ca9b">3-7. 식단_학생식당정보_클릭</a>
</td>
</tr>
<tr>
<td>
<code>shop_banner</code>
</td>
<td>
식단 상점가기 배너 클릭·스와이프로 닫기; 기존 실험·세션 정의 유지
</td>
<td>
식단
</td>
<td>
<code>없음</code> → <code>click</code>; <code>없음</code> → <code>swipe</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/18a0221954bc823d80958141c2d73d6d">0-3. 식단_ABtest_상점가기_닫기</a> · <a href="https://app.notion.com/p/a9e0221954bc8389898d81cab7af5dd6">0-1. 식단_ABtest_상점가기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>notification_config</code>
</td>
<td>
알림 설정 진입과 식단 사진 업로드 알림 토글; 품절 관련 알림 명세는 동결
</td>
<td>
식단
</td>
<td>
<code>entry</code> → <code>click</code>; <code>photo_upload</code> → <code>toggle</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/e0f0221954bc82469a9181b6760e37d2">5-1. (Android / iOS) 알림설정_클릭</a> · <a href="https://app.notion.com/p/f580221954bc834f80618109036b55c7">5-6. (Android / iOS) 알림설정_식단사진 업로드_토글</a>
</td>
</tr>
<tr>
<td>
<code>share</code>
</td>
<td>
외부 공유 실행; 전달 수단은 detail로 구분
</td>
<td>
식단
</td>
<td>
<code>kakao</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6650221954bc8290b31301687986010e">3-8. (Android / iOS) 식단_카카오톡_공유하기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>bus_notice</code>
</td>
<td>
버스 공지 열기·닫기; 고정 논리 화면 bus_timetable 사용
</td>
<td>
버스
</td>
<td>
<code>close</code> → <code>click</code>; <code>open</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/c180221954bc834a94af012006c49967">4-2. 버스 공지_클릭</a> · <a href="https://app.notion.com/p/fa40221954bc8240b0d3815afa162398">4-3. 버스 공지_닫기_클릭</a>
</td>
</tr>
<tr>
<td>
<code>bus_entry</code>
</td>
<td>
버스 서비스 진입; 조회·시간표·탑승권 진입 대상 구분
</td>
<td>
버스
</td>
<td>
<code>main_entry</code> → <code>click</code>; <code>search_entry</code> → <code>click</code>; <code>ticket_entry</code> → <code>click</code>; <code>timetable_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/5da0221954bc8304abd601992586328c">1-11. 셔틀 탑승권_클릭 (레거시)</a> · <a href="https://app.notion.com/p/5dd0221954bc83bd8da7819f055c5270">[레거시] 1-14. 메인_버스_클릭</a>
</td>
</tr>
<tr>
<td>
<code>bus_route</code>
</td>
<td>
셔틀 노선에서 시간표 상세 진입; 노선 필터 선택과 구분 현행 셔틀 상세 진입은 <code>shuttle_route</code>로 정정됐으며 이 이름을 새로 배포하도록 지시하지 않는다.
</td>
<td>
버스
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/ad50221954bc836eab1b817b8f266a4d">4-6. 지역별 세부 노선_클릭 (세부 노선 변경시 업데이트 필요)</a>
</td>
</tr>
<tr>
<td>
<code>bus_feedback</code>
</td>
<td>
운행 정보 오류 제보 진입; 고정 논리 화면 bus_timetable 사용
</td>
<td>
버스
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bc80221954bc83a591fb81a50ed12a22">4-1. 정보가 정확하지 않나요?_클릭 (세부 노선 변경시 업데이트 필요)</a>
</td>
</tr>
<tr>
<td>
<code>team_edit</code>
</td>
<td>
모집글 편집 진입·조건 선택·수정 확인창 열기·확정·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code>, <code>category</code>, <code>method</code>, <code>role</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code> / category: <code>click</code>, <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/8ce0221954bc836ca589012bcbd1fc8a">4-2. 모집글 편집</a>
</td>
</tr>
<tr>
<td>
<code>team_profile_write</code>
</td>
<td>
팀원 모집 프로필 작성; 정보 불러오기·학부·기술·활동 이력·단계 이동·확정·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code>, <code>load</code>, <code>major</code>, <code>next</code>, <code>skill_add</code>, <code>activity_add</code>, <code>activity_add_confirm</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code> / category: <code>click</code>, <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a> · <a href="https://app.notion.com/p/ba90221954bc83c89dd2015dbd8eead0">7-1-2. 프로필 작성하기 내부</a>
</td>
</tr>
<tr>
<td>
<code>team_created</code>
</td>
<td>
내가 작성한 모집글 목록 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a>
</td>
</tr>
<tr>
<td>
<code>team_applied</code>
</td>
<td>
내가 지원한 모집글 목록 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a>
</td>
</tr>
<tr>
<td>
<code>team_apply</code>
</td>
<td>
팀원 모집 지원서 작성 진입·정보 선택·활동 이력·단계 이동·제출 확인·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>load</code>, <code>major</code>, <code>skill_add</code>, <code>activity_add</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>next</code>, <code>role</code>, <code>open</code>, <code>confirm</code>, <code>cancel</code>, <code>entry</code> / category: <code>click</code>, <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/8ad0221954bc8220a76c81eee39f2cab">6. 지원서 작성</a> · <a href="https://app.notion.com/p/d270221954bc83ecb5a2818dafc2b6d7">4. 모집글 상세</a>
</td>
</tr>
<tr>
<td>
<code>team_write</code>
</td>
<td>
모집글 작성 진입·카테고리/방식/역할 선택·확인창·최종 확인·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>category</code>, <code>method</code>, <code>role</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code>, <code>entry</code> / category: <code>select</code>, <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1f90221954bc832e881f81b896901f72">5-1. 모집글 작성</a> · <a href="https://app.notion.com/p/fcb0221954bc83d5a2d701a05d558798">5. 모집하기 클릭</a>
</td>
</tr>
<tr>
<td>
<code>team_delete</code>
</td>
<td>
모집글 삭제창 열기·최종 삭제·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>open</code>, <code>confirm</code>, <code>cancel</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/f670221954bc83bc9f9d8174df96f17c">4-1. 모집글 상세 및 삭제</a>
</td>
</tr>
<tr>
<td>
<code>team_application_review</code>
</td>
<td>
지원자 승인·거절 각각의 확인창 열기·확정·취소
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>approve_open</code>, <code>approve_confirm</code>, <code>approve_cancel</code>, <code>reject_open</code>, <code>reject_confirm</code>, <code>reject_cancel</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/71e0221954bc8396966e813f4e080389">11. 지원자 상세</a>
</td>
</tr>
<tr>
<td>
<code>team_applicant</code>
</td>
<td>
내 모집글 지원자 관리 목록 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0aa0221954bc82a288d001afd2850c08">9. 내가 작성한 모집글</a> · <a href="https://app.notion.com/p/d270221954bc83ecb5a2818dafc2b6d7">4. 모집글 상세</a>
</td>
</tr>
<tr>
<td>
<code>team_deadline</code>
</td>
<td>
모집 마감 버튼·확인창·최종 마감·취소; 마감은 close가 아닌 deadline
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>open</code>, <code>cancel</code>, <code>confirm</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0aa0221954bc82a288d001afd2850c08">9. 내가 작성한 모집글</a>
</td>
</tr>
<tr>
<td>
<code>team_notification</code>
</td>
<td>
팀원 모집 알림 목록 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/a030221954bc827d93920103041dcc09">0. 알림 클릭</a>
</td>
</tr>
<tr>
<td>
<code>team_applicant_detail</code>
</td>
<td>
지원자 카드에서 지원자 상세 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6a60221954bc828bb4e601b073d671f6">10. 지원자 관리</a>
</td>
</tr>
<tr>
<td>
<code>team_profile</code>
</td>
<td>
팀원 모집 프로필 화면 진입; 프로필 작성/수정은 별도 기능
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/ea20221954bc82229ef181d419ea2214">7. 프로필 클릭</a>
</td>
</tr>
<tr>
<td>
<code>team_detail</code>
</td>
<td>
모집글 카드에서 상세 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/f260221954bc823f9015010400ff257f">3. 게시글 클릭</a>
</td>
</tr>
<tr>
<td>
<code>team_recruit_entry</code>
</td>
<td>
팀원 모집 서비스 헤더·푸터·카테고리 진입
</td>
<td>
팀원 모집
</td>
<td>
팀원 모집 제외 · 기존 정의 유지: <code>header_entry</code>, <code>category_entry</code>, <code>footer_entry</code> / category: <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/4f60221954bc83f89a17810c28e045ac">12. 헤더_팀원 모집 진입 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/4340221954bc834e9d4701a526f76405">[레거시·중복 원문] 14. 카테고리_팀원 모집 진입 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>semester_manage</code>
</td>
<td>
시간표 학기 선택과 학기 편집. 추가·삭제 확정/적용은 웹·모바일 edit_apply 공통 1회 이벤트
</td>
<td>
시간표
</td>
<td>
<code>edit_apply</code> → <code>click</code>; <code>없음</code> → <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> · <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>timetable_config</code>
</td>
<td>
시간표 설정 열기·이름/기본 설정 저장·삭제
</td>
<td>
시간표
</td>
<td>
<code>delete</code> → <code>click</code>; <code>open</code> → <code>click</code>; <code>save</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/1b90221954bc8221815481a568880eee">2-15. (웹) 시간표_저장 (클릭)</a> · <a href="https://app.notion.com/p/2af0221954bc823f99db815887a20279">2-16. (웹) 시간표_삭제 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>timetable_export</code>
</td>
<td>
시간표 이미지 저장·다운로드
</td>
<td>
시간표
</td>
<td>
<code>image_save</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/27e0221954bc821da617812bbc62ce44">2-6. 시간표_이미지 저장 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>timetable_entry</code>
</td>
<td>
시간표 헤더·푸터·카테고리 진입
</td>
<td>
시간표
</td>
<td>
<code>category_entry</code> → <code>click</code>; <code>footer_entry</code> → <code>click</code>; <code>header_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/2150221954bc83968571018a8f92635f">2-4. (웹) 푸터_시간표</a> · <a href="https://app.notion.com/p/6360221954bc837f98d98135eefbf8bc">[레거시·이관 원문] 2-5. (앱, 반응형 웹) 햄버거_시간표</a>
</td>
</tr>
<tr>
<td>
<code>timetable_edit</code>
</td>
<td>
시간표 수정 진입·정규/직접추가 탭·직접 일정 저장·수정 완료
</td>
<td>
시간표
</td>
<td>
<code>confirm</code> → <code>click</code>; <code>custom_save</code> → <code>click</code>; <code>entry</code> → <code>click</code>; <code>tab</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/77c0221954bc83668e97011d488705e0">2-30. (웹) 시간표 수정_탭 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/8260221954bc82028314819c7fdd3b8a">2-23. (웹, 반응형 앱) 시간표_시간표 수정 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>timetable_list</code>
</td>
<td>
시간표 목록 진입과 목록 내 시간표 선택
</td>
<td>
시간표
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>select</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/8ce0221954bc83fda1e801087dc95497">2-27. (앱, 반응형 웹) 시간표 목록_시간표 선택 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/d450221954bc82b49338816b4cfa598d">2-26. (앱, 반응형 웹) 시간표_학기 시간표 선택 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>timetable_manage</code>
</td>
<td>
선택 학기에 시간표 추가
</td>
<td>
시간표
</td>
<td>
<code>add</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/a790221954bc82fcba5d81decfc5bd71">2-24. (웹) 시간표_시간표 추가하기 (클릭) - 추가된 로깅</a>
</td>
</tr>
<tr>
<td>
<code>shop_menu</code>
</td>
<td>
상점 메뉴 탭 진입과 메뉴 목록 스크롤
</td>
<td>
주변상점
</td>
<td>
<code>entry</code> → <code>click</code>; <code>없음</code> → <code>scroll</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/19f0221954bc8311877d8105cb3f2af0">3-4, 4.5 상점상세 메뉴 (클릭,스크롤)</a>
</td>
</tr>
<tr>
<td>
<code>shop__shop_detail__contact__phone__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/2d50221954bc834f8ca9019292dd4741">3-2 상점상세 전화 (클릭)</a> · <a href="https://app.notion.com/p/3d50221954bc824e9a1e81e83e042833">4-5 전화 주문 혜택 상점상세 전화 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>account__shop_detail__login_popup__close__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/40c0221954bc830a8ea4015f95cf4e1f">3-23 상점상세 리뷰작성 _로그인_취소 (클릭)</a> · <a href="https://app.notion.com/p/fc90221954bc82cb9b1f01c7863d50e9">3-25 상점상세 리뷰신고 _취소누름 (비로그인)</a>
</td>
</tr>
<tr>
<td>
<code>account__shop_detail__login_popup__login_entry__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/bf00221954bc8246a5ae8154ce1bcf97">3-22 상점상세 리뷰작성 들어가기_로그인누름 (비로그인)</a> · <a href="https://app.notion.com/p/c150221954bc8307920f81f1cddd95b1">3-24 상점상세 리뷰신고 _로그인 (비로그인)</a>
</td>
</tr>
<tr>
<td>
<code>real_estate__main_category__real_estate_entry__category_entry__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/9890221954bc820ba81a81e6725d617b">Notion 원문</a> · <a href="https://app.notion.com/p/2640221954bc83d6a82901c92388b825">[레거시] 1-3 햄버거_복덕방 진입 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>cafeteria__main__more__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> · <a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a>
</td>
</tr>
<tr>
<td>
<code>timetable__timetable__semester_manage__edit_apply__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> · <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>timetable__main_category__timetable_entry__category_entry__click</code>
</td>
<td>
기존 공용 기능. 대상·발생 조건은 연결 명세를 따른다.
</td>
<td>
기존 범위 유지
</td>
<td>
이번 현행 적용 범위에서 사용 확인 없음. 기존 정의는 아래 이력에 보존.
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/e9d0221954bc828aa337812594729789">[레거시·중복 원문] 2-21. (앱, 반응형 웹) 카테고리_시간표 진입 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/6360221954bc837f98d98135eefbf8bc">[레거시·이관 원문] 2-5. (앱, 반응형 웹) 햄버거_시간표</a>
</td>
</tr>
<tr>
<td>
<code>lecture_add</code>
</td>
<td>
시간표 편집에서 과목 선택·추가. 즉시 추가인지 상세·미리보기 진입인지는 실제 동작 확인 전 미확인.
</td>
<td>
시간표
</td>
<td>
<code>lecture_entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/f7c0221954bc828abee78131aee31d6e">2-18. (웹) 시간표_수정_과목 선택 (클릭)</a>
</td>
</tr>
<tr>
<td>
<code>shuttle_route</code>
</td>
<td>
셔틀 노선에서 시간표 상세 화면으로 진입. 노선 필터 선택과 구분.
</td>
<td>
버스
</td>
<td>
<code>entry</code> → <code>click</code>
</td>
<td>
원래 value·플랫폼·전송 시점 유지. 실제 구현 검증과 별개.
</td>
<td>
<a href="https://app.notion.com/p/ad50221954bc836eab1b817b8f266a4d">4-6. 지역별 세부 노선_클릭 (세부 노선 변경시 업데이트 필요)</a>
</td>
</tr>
</table>

<details>
<summary>이전 기능 사전과 확장표 (2026-10-28 이전 표현 보존)</summary>

아래 표·예시는 변경 이력이다. 합친 행동/category 표현과 옛 submit 예시를 새 명세의 승인값으로 사용하지 않는다. 팀원 모집의 제외된 기존 정의는 위 현행 표에서도 보존한다.

기능 구간에 적용하는 사전이다. 같은 단어가 페이지 이름에도 쓰인다고 페이지 정의까지 변경하지 않는다.

<table>
<tr>
<td>
기능명
</td>
<td>
범위
</td>
<td>
세부기능·행동
</td>
</tr>
<tr>
<td>
<code>account_config</code>
</td>
<td>
계정 설정 진입
</td>
<td>
<code>entry</code>
</td>
</tr>
<tr>
<td>
<code>account_recovery</code>
</td>
<td>
아이디·비밀번호 찾기
</td>
<td>
<code>id_entry</code>, <code>password_entry</code>
</td>
</tr>
<tr>
<td>
<code>callvan_chat</code>
</td>
<td>
콜밴팟 단체 채팅
</td>
<td>
<code>card_entry</code>, <code>message_send</code>, <code>participant_entry</code>
</td>
</tr>
<tr>
<td>
<code>callvan_entry</code>
</td>
<td>
콜밴팟 목록 진입
</td>
<td>
<code>recruitment_list_entry</code>, <code>category_entry</code>
</td>
</tr>
<tr>
<td>
<code>callvan_participation</code>
</td>
<td>
참여·참여취소 확인 응답
</td>
<td>
<code>join_response</code>, <code>cancel_response</code>
</td>
</tr>
<tr>
<td>
<code>callvan_write</code>
</td>
<td>
콜밴팟 모집글 작성
</td>
<td>
<code>entry</code>, <code>departure_confirm</code>, <code>arrival_confirm</code>, <code>departure_time_confirm</code>, <code>submit</code>
</td>
</tr>
<tr>
<td>
<code>category_navigation</code>
</td>
<td>
3-6 공용 카테고리 13개 메뉴 클릭
</td>
<td>
<code>team_recruit_entry</code>, <code>lost_item_entry</code>, <code>facility_entry</code>, <code>department_entry</code>, <code>cafeteria_entry</code>, <code>shop_entry</code>, <code>timetable_entry</code>, <code>search_entry</code>, <code>callvan_entry</code>, <code>chat_entry</code>, <code>real_estate_entry</code>, <code>owner_entry</code>
</td>
</tr>
<tr>
<td>
<code>chat_conversation</code>
</td>
<td>
공용 쪽지 대화 선택
</td>
<td>
<code>entry</code>
</td>
</tr>
<tr>
<td>
<code>chat_entry</code>
</td>
<td>
공용 쪽지·채팅 진입
</td>
<td>
<code>category_entry</code>, <code>header_entry</code>, <code>footer_entry</code>
</td>
</tr>
<tr>
<td>
<code>contact</code>
</td>
<td>
콜밴팟 전화·학교 부서 연락처 복사
</td>
<td>
<code>phone_click</code>, <code>phone_copy</code>
</td>
</tr>
<tr>
<td>
<code>course_application</code>
</td>
<td>
모의수강신청 진입·과목 신청
</td>
<td>
<code>entry</code>, <code>lecture_submit</code>, <code>preselected_submit</code>
</td>
</tr>
<tr>
<td>
<code>department_category</code>
</td>
<td>
부서 내부 분류 선택
</td>
<td>
<code>select</code>
</td>
</tr>
<tr>
<td>
<code>department_entry</code>
</td>
<td>
학교 부서 서비스 진입
</td>
<td>
<code>header_entry</code>, <code>footer_entry</code>, <code>category_entry</code>
</td>
</tr>
<tr>
<td>
<code>external_link</code>
</td>
<td>
외부 사이트·원본 바로가기
</td>
<td>
<code>shortcut_entry</code>, <code>original_entry</code>
</td>
</tr>
<tr>
<td>
<code>facility_entry</code>
</td>
<td>
교내 시설물 서비스 진입
</td>
<td>
<code>header_entry</code>, <code>footer_entry</code>, <code>category_entry</code>
</td>
</tr>
<tr>
<td>
<code>filter</code>
</td>
<td>
공지·분실물·콜밴팟 필터 열기·선택·적용
</td>
<td>
<code>tab_select</code>, <code>keyword_select</code>, <code>open</code>, <code>apply</code>
</td>
</tr>
<tr>
<td>
<code>keyword_manage</code>
</td>
<td>
공지·분실물 키워드 관리
</td>
<td>
<code>entry</code>, <code>add_submit</code>, <code>recommended_keyword_select</code>, <code>notification_toggle</code>, <code>delete_click</code>
</td>
</tr>
<tr>
<td>
<code>login</code>
</td>
<td>
로그인 진입·실행
</td>
<td>
<code>header_entry</code>, <code>entry</code>, <code>submit</code>
</td>
</tr>
<tr>
<td>
<code>login_popup</code>
</td>
<td>
로그인 안내 팝업 응답
</td>
<td>
<code>login_entry</code>, <code>close</code>
</td>
</tr>
<tr>
<td>
<code>logout</code>
</td>
<td>
로그아웃
</td>
<td>
<code>click</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_delete</code>
</td>
<td>
분실물·습득물 삭제
</td>
<td>
<code>open</code>, <code>confirm</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_detail</code>
</td>
<td>
분실물·습득물 상세 진입
</td>
<td>
<code>entry</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_edit</code>
</td>
<td>
분실물·습득물 수정 — 11-29·11-30 적용 대상 확정
</td>
<td>
<code>entry</code>, <code>submit</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_entry</code>
</td>
<td>
분실물 서비스 진입
</td>
<td>
<code>main_entry</code>, <code>category_entry</code>, <code>footer_entry</code>, <code>header_entry</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_message</code>
</td>
<td>
분실물·습득물 쪽지 진입
</td>
<td>
<code>entry</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_report</code>
</td>
<td>
게시물 신고
</td>
<td>
<code>entry</code>, <code>submit</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_status</code>
</td>
<td>
분실물 상태 변경
</td>
<td>
<code>open</code>, <code>found_confirm</code>
</td>
</tr>
<tr>
<td>
<code>lost_item_write</code>
</td>
<td>
분실물·습득물 작성
</td>
<td>
<code>entry</code>, <code>item_category_select</code>, <code>item_add_click</code>, <code>submit</code>, <code>post_type_select</code>
</td>
</tr>
<tr>
<td>
<code>modal</code>
</td>
<td>
메인 배너 모달
</td>
<td>
<code>exposure</code>, <code>click</code>, <code>close</code>, <code>hide_7d</code>, <code>next_swipe</code>, <code>next_click</code>
</td>
</tr>
<tr>
<td>
<code>navigation</code>
</td>
<td>
뒤로가기·목록·메인 복귀
</td>
<td>
<code>notice_list_return</code>, <code>back</code>, <code>main_return</code>
</td>
</tr>
<tr>
<td>
<code>notice_detail</code>
</td>
<td>
공지 상세 진입
</td>
<td>
<code>entry</code>, <code>popular_post_entry</code>, <code>keyword_notification_entry</code>
</td>
</tr>
<tr>
<td>
<code>notice_entry</code>
</td>
<td>
공지사항 서비스 진입
</td>
<td>
<code>more_entry</code>, <code>title_entry</code>, <code>header_entry</code>, <code>footer_entry</code>, <code>navigation_entry</code>
</td>
</tr>
<tr>
<td>
<code>notice_list</code>
</td>
<td>
공지 목록 탐색
</td>
<td>
<code>scroll</code>
</td>
</tr>
<tr>
<td>
<code>password_change</code>
</td>
<td>
정보 수정 경로의 비밀번호 변경
</td>
<td>
<code>submit</code>
</td>
</tr>
<tr>
<td>
<code>profile_edit</code>
</td>
<td>
계정·프로필 정보 수정
</td>
<td>
<code>header_entry</code>, <code>entry</code>, <code>submit</code>
</td>
</tr>
<tr>
<td>
<code>search</code>
</td>
<td>
공지·콜밴팟·학교 부서·모의수강신청 검색·조회
</td>
<td>
<code>entry</code>, <code>popular_keyword_select</code>, <code>search_submit</code>, <code>search_input_click</code>, <code>department_select</code>
</td>
</tr>
<tr>
<td>
<code>sign_up</code>
</td>
<td>
회원가입 전체 흐름
</td>
<td>
<code>header_entry</code>, <code>entry</code>, <code>terms_agree_click</code>, <code>send_code</code>, <code>code_verify_success</code>, <code>user_type_select</code>, <code>id_available</code>, <code>nickname_available</code>, <code>submit</code>
</td>
</tr>
</table>

### DA1 공용·서비스 기능 등록 (2026-10-27)

이번 DA1 7개 서비스 정렬의 현행 사전이다. 아래 신규 기능은 기존 DA2 기능으로 의미를 보존해 매핑할 수 없는 목적을 등록한 것이다. 같은 목적은 공용 기능으로 재사용하며, category·발생 시점·value·event\_name은 기존 명세를 유지한다. 품절 제보와 관련 알림의 동결 명세는 변경하지 않는다.

| 기능명 | 목적·포함 행동 | 적용 서비스 | detail | category | 근거 명세 |
| --- | --- | --- | --- | --- | --- |
| <code>review_report</code> | 상점 리뷰 신고 화면 진입과 신고 완료 버튼 클릭 | 주변상점 | <code>confirm</code>, <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/c810221954bc835381ed81ae8f0e5ce9">3-15 상점상세 리뷰 신고 완료 (클릭)</a> · <a href="https://app.notion.com/p/a200221954bc8282ab5701cb4978f627">3-14 상점상세 리뷰 신고 (클릭)</a> |
| <code>review_write</code> | 상점 리뷰 작성 화면 진입과 작성 완료 버튼 클릭 | 주변상점 | <code>confirm</code>, <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/0d40221954bc835b82a281b6adedd95d">3-13 상점상세 리뷰작성 들어간후(클릭)</a> · <a href="https://app.notion.com/p/db00221954bc82f5a2148164f7e27474">3-12 상점상세 리뷰작성 들어가기 (클릭)</a> |
| <code>review_delete</code> | 상점 리뷰 삭제창 열기·최종 삭제·취소 | 주변상점 | <code>confirm</code>, <code>open</code>, <code>cancel</code> | <code>click</code> | <a href="https://app.notion.com/p/54a0221954bc8367b002012884670248">3-20 상점상세 리뷰 최종삭제하기 (클릭)</a> · <a href="https://app.notion.com/p/a130221954bc83b9bb2b011f769a00ff">3-19 상점상세 리뷰 삭제하기 (클릭)</a> |
| <code>shop_detail</code> | 상점 카드에서 상세 화면 진입 | 주변상점 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/8f00221954bc83d0afe881e3ddd2deed">3-1 상점 카테고리 → 상점상세 (클릭)</a> · <a href="https://app.notion.com/p/dd10221954bc839392818196deaac6e0">4-4 전화 주문 혜택 상점상세 페이지(클릭)</a> |
| <code>shop_event</code> | 상점 이벤트 영역·이벤트 상점 선택과 목록 탐색 | 주변상점 | <code>entry</code> | <code>click</code>, <code>scroll</code> | <a href="https://app.notion.com/p/69f0221954bc83c9adb481420b9fb21f">3-8 상점상세 이벤트 (클릭)</a> · <a href="https://app.notion.com/p/0a30221954bc83ed998d01d79b96fb0b">3-9 상점상세 이벤트 (스크롤)</a> |
| <code>shop_list</code> | 상점 목록 스크롤 탐색 | 주변상점 | 없음: category만 사용 | <code>scroll</code> | <a href="https://app.notion.com/p/c9c0221954bc82da8f7b8141ef147047">2-2 상점 카테고리 (스크롤)</a> |
| <code>shop_benefit</code> | 전화 주문 혜택 상점 모아보기 진입 | 주변상점 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/19c0221954bc837b85ed813f6a80e9df">4-3 카테고리에서 혜택페이지(클릭)</a> |
| <code>shop_review</code> | 상점 리뷰 탭 진입과 리뷰 목록 탐색 | 주변상점 | <code>entry</code> | <code>click</code>, <code>scroll</code> | <a href="https://app.notion.com/p/6700221954bc829490bf812977cce992">3-10 상점상세 리뷰 (클릭)</a> · <a href="https://app.notion.com/p/6570221954bc831683fe81c8826bffc4">3-11 상점상세 리뷰 (스크롤)</a> |
| <code>photo_view</code> | 사진 보기 열기와 사진 슬라이드 이동; 파일 업로드와 구분 | 주변상점·복덕방·식단 | <code>open</code>, <code>slide</code> | <code>click</code> | <a href="https://app.notion.com/p/1700221954bc827b8c48019d6a980646">3-3 상점상세 사진 (클릭)</a> · <a href="https://app.notion.com/p/bf10221954bc82f5995681a6d437697a">3-1 복덕방 상세_사진 넘기기 (클릭) - 추가된 로깅</a> |
| <code>shop_entry</code> | 주변상점 서비스 진입; 메인 일반 진입과 카테고리 값 선택 진입 구분 | 주변상점 | <code>main_entry</code>, <code>category_entry</code>, <code>header_entry</code>, <code>footer_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/88c0221954bc8280855881dd07f1c38d">1-1-1 메인 → 주변상점 (클릭) - (레거시)</a> · <a href="https://app.notion.com/p/cb70221954bc82f084078198ab552627">1-1 메인 → 상점 카테고리 (클릭) - 레거시</a> |
| <code>shop_cart</code> | 장바구니 진입 | 주변상점 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/b3a0221954bc82b984dd015025c78148">2-9 상점 카테고리 → 카트 - 레거시</a> |
| <code>real_estate_entry</code> | 복덕방 서비스 진입; 웹 메뉴와 앱 카테고리에서 같은 진입 계약 사용 | 복덕방 | <code>category_entry</code>, <code>header_entry</code>, <code>footer_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/2640221954bc83d6a82901c92388b825">[레거시] 1-3 햄버거_복덕방 진입 (클릭)</a> · <a href="https://app.notion.com/p/1740221954bc83cebc8601faa22ca3a5">1-1 헤더_복덕방 진입(클릭)</a> |
| <code>room_detail</code> | 방 카드에서 복덕방 상세 화면 진입 | 복덕방 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/5da0221954bc829d8cc70189be42fb74">2-1 복덕방 목록_방 카드 (클릭) - 추가된 로깅</a> |
| <code>shop_manage</code> | 사장님 가게 정보 수정 진입·이미지 추가·운영시간 설정·저장·취소·닫기 | 사장님 | <code>edit_entry</code>, <code>image_add</code>, <code>time_edit</code>, <code>edit_cancel</code>, <code>edit_confirm</code>, <code>close</code> | <code>click</code> | <a href="https://app.notion.com/p/8770221954bc830c806181d36174c4de">2-1 가게 정보 수정</a> · <a href="https://app.notion.com/p/22d0221954bc82f7be2501d0361154f9">2-4 가게 정보 수정 - 이미지 추가</a> |
| <code>shop_event_manage</code> | 사장님 이벤트 추가·수정·삭제; 추가/수정 저장 확인과 취소 구분 | 사장님 | <code>add_entry</code>, <code>delete</code>, <code>add_cancel</code>, <code>add_confirm</code>, <code>edit_confirm</code> | <code>click</code> | <a href="https://app.notion.com/p/7d50221954bc8332862301d66a85dc6a">1-1 이벤트 추가</a> · <a href="https://app.notion.com/p/9140221954bc8279be910174e2ca2302">1-4 이벤트 삭제 (클릭) - 추가된 로깅</a> |
| <code>shop_menu_manage</code> | 사장님 메뉴 추가 진입·사진 추가·등록 확인·취소 | 사장님 | <code>add_entry</code>, <code>add_cancel</code>, <code>add_confirm</code>, <code>image_add</code> | <code>click</code> | <a href="https://app.notion.com/p/ec90221954bc82cca0ae019240970afa">3-1 메뉴추가</a> · <a href="https://app.notion.com/p/5030221954bc82f095f0817d9324b9d0">3-3 메뉴추가 - 취소</a> |
| <code>meal_time</code> | 식사 시간 선택과 선택한 시간의 식단 목록 스크롤 | 식단 | 없음: category만 사용 | <code>scroll</code>, <code>select</code> | <a href="https://app.notion.com/p/9f20221954bc8275b0f301f1b220b3f5">3-4. 식단_아침_스크롤</a> · <a href="https://app.notion.com/p/e5f0221954bc821c881e01997734ea21">3-1. 식단_식사시간 선택 (클릭) - 3-2·3-3 통합</a> |
| <code>corner</code> | 메인 식단 위젯의 표시 코너 선택; 화면 이동 없음 | 식단·홈(main) | 없음: category만 사용 | <code>select</code> | <a href="https://app.notion.com/p/e4c0221954bc83949b49016cfff27ccf">1-4 식단 코너 클릭</a> |
| <code>cafeteria_entry</code> | 식단 서비스 진입; 헤더·푸터·카카오 외부 진입 | 식단 | <code>footer_entry</code>, <code>header_entry</code>, <code>kakao_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/8f50221954bc82e4ac5201545f5fa260">2-2. 푸터_식단_클릭</a> · <a href="https://app.notion.com/p/c420221954bc831497240194ccc6ae54">2-1. 헤더_식단_클릭</a> |
| <code>meal</code> | 메인 식단 칸 클릭; 기존 홈화면 리디자인 이력 유지 | 식단 | 없음: category만 사용 | <code>click</code> | <a href="https://app.notion.com/p/d400221954bc8338b341011b9a488dac">1-2.메인_식단_클릭 (레거시)</a> |
| <code>more</code> | 메인 식단 더보기; 기존 1-1 대표 명세와 중복 참고 명세의 공통 계약 | 식단 | 없음: category만 사용 | <code>click</code> | <a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a> · <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> |
| <code>ab_test</code> | 식단 상점가기 배너 A/B 그룹 노출; 품절 제보 실험과 별개 | 식단 | 없음: category만 사용 | <code>exposure</code> | <a href="https://app.notion.com/p/ca20221954bc8338ab2b8107ff9e4663">0-2. 식단_ABtest_진입</a> |
| <code>cafeteria_info</code> | 학생식당 운영 정보 진입 | 식단 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/7e40221954bc8363933501688180ca9b">3-7. 식단_학생식당정보_클릭</a> |
| <code>shop_banner</code> | 식단 상점가기 배너 클릭·스와이프로 닫기; 기존 실험·세션 정의 유지 | 식단 | 없음: category만 사용 | <code>swipe</code>, <code>click</code> | <a href="https://app.notion.com/p/18a0221954bc823d80958141c2d73d6d">0-3. 식단_ABtest_상점가기_닫기</a> · <a href="https://app.notion.com/p/a9e0221954bc8389898d81cab7af5dd6">0-1. 식단_ABtest_상점가기_클릭</a> |
| <code>notification_config</code> | 알림 설정 진입과 식단 사진 업로드 알림 토글; 품절 관련 알림 명세는 동결 | 식단 | <code>entry</code>, <code>photo_upload</code> | <code>click</code>, <code>toggle</code> | <a href="https://app.notion.com/p/e0f0221954bc82469a9181b6760e37d2">5-1. (Android / iOS) 알림설정_클릭</a> · <a href="https://app.notion.com/p/f580221954bc834f80618109036b55c7">5-6. (Android / iOS) 알림설정_식단사진 업로드_토글</a> |
| <code>share</code> | 외부 공유 실행; 전달 수단은 detail로 구분 | 식단 | <code>kakao</code> | <code>click</code> | <a href="https://app.notion.com/p/6650221954bc8290b31301687986010e">3-8. (Android / iOS) 식단_카카오톡_공유하기_클릭</a> |
| <code>bus_notice</code> | 버스 공지 열기·닫기; 고정 논리 화면 bus\_timetable 사용 | 버스 | <code>open</code>, <code>close</code> | <code>click</code> | <a href="https://app.notion.com/p/c180221954bc834a94af012006c49967">4-2. 버스 공지_클릭</a> · <a href="https://app.notion.com/p/fa40221954bc8240b0d3815afa162398">4-3. 버스 공지_닫기_클릭</a> |
| <code>bus_entry</code> | 버스 서비스 진입; 조회·시간표·탑승권 진입 대상 구분 | 버스 | <code>category_entry</code>, <code>search_entry</code>, <code>ticket_entry</code>, <code>timetable_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/5dd0221954bc83bd8da7819f055c5270">[레거시] 1-14. 메인_버스_클릭</a> · <a href="https://app.notion.com/p/fae0221954bc83d49c12815edc4f6fde">1-13. 교통편 조회하기_클릭 (레거시)</a> |
| <code>bus_route</code> | 셔틀 노선에서 시간표 상세 진입; 노선 필터 선택과 구분 | 버스 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/ad50221954bc836eab1b817b8f266a4d">4-6. 지역별 세부 노선_클릭 (세부 노선 변경시 업데이트 필요)</a> |
| <code>bus_feedback</code> | 운행 정보 오류 제보 진입; 고정 논리 화면 bus\_timetable 사용 | 버스 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/bc80221954bc83a591fb81a50ed12a22">4-1. 정보가 정확하지 않나요?_클릭 (세부 노선 변경시 업데이트 필요)</a> |
| <code>team_edit</code> | 모집글 편집 진입·조건 선택·수정 확인창 열기·확정·취소 | 팀원 모집 | <code>entry</code>, <code>category</code>, <code>method</code>, <code>role</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code> | <code>click</code>, <code>select</code> | <a href="https://app.notion.com/p/8ce0221954bc836ca589012bcbd1fc8a">4-2. 모집글 편집</a> |
| <code>team_profile_write</code> | 팀원 모집 프로필 작성; 정보 불러오기·학부·기술·활동 이력·단계 이동·확정·취소 | 팀원 모집 | <code>entry</code>, <code>load</code>, <code>major</code>, <code>next</code>, <code>skill_add</code>, <code>activity_add</code>, <code>activity_add_confirm</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code> | <code>click</code>, <code>select</code> | <a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a> · <a href="https://app.notion.com/p/ba90221954bc83c89dd2015dbd8eead0">7-1-2. 프로필 작성하기 내부</a> |
| <code>team_created</code> | 내가 작성한 모집글 목록 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a> |
| <code>team_applied</code> | 내가 지원한 모집글 목록 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/bae0221954bc825dab8b8111da763c84">7-1. 프로필 내부</a> |
| <code>team_apply</code> | 팀원 모집 지원서 작성 진입·정보 선택·활동 이력·단계 이동·제출 확인·취소 | 팀원 모집 | <code>load</code>, <code>major</code>, <code>skill_add</code>, <code>activity_add</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>next</code>, <code>role</code>, <code>open</code>, <code>confirm</code>, <code>cancel</code>, <code>entry</code> | <code>click</code>, <code>select</code> | <a href="https://app.notion.com/p/8ad0221954bc8220a76c81eee39f2cab">6. 지원서 작성</a> · <a href="https://app.notion.com/p/d270221954bc83ecb5a2818dafc2b6d7">4. 모집글 상세</a> |
| <code>team_write</code> | 모집글 작성 진입·카테고리/방식/역할 선택·확인창·최종 확인·취소 | 팀원 모집 | <code>category</code>, <code>method</code>, <code>role</code>, <code>open</code>, <code>cancel</code>, <code>confirm</code>, <code>entry</code> | <code>select</code>, <code>click</code> | <a href="https://app.notion.com/p/1f90221954bc832e881f81b896901f72">5-1. 모집글 작성</a> · <a href="https://app.notion.com/p/fcb0221954bc83d5a2d701a05d558798">5. 모집하기 클릭</a> |
| <code>team_delete</code> | 모집글 삭제창 열기·최종 삭제·취소 | 팀원 모집 | <code>open</code>, <code>confirm</code>, <code>cancel</code> | <code>click</code> | <a href="https://app.notion.com/p/f670221954bc83bc9f9d8174df96f17c">4-1. 모집글 상세 및 삭제</a> |
| <code>team_application_review</code> | 지원자 승인·거절 각각의 확인창 열기·확정·취소 | 팀원 모집 | <code>approve_open</code>, <code>approve_confirm</code>, <code>approve_cancel</code>, <code>reject_open</code>, <code>reject_confirm</code>, <code>reject_cancel</code> | <code>click</code> | <a href="https://app.notion.com/p/71e0221954bc8396966e813f4e080389">11. 지원자 상세</a> |
| <code>team_applicant</code> | 내 모집글 지원자 관리 목록 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/0aa0221954bc82a288d001afd2850c08">9. 내가 작성한 모집글</a> · <a href="https://app.notion.com/p/d270221954bc83ecb5a2818dafc2b6d7">4. 모집글 상세</a> |
| <code>team_deadline</code> | 모집 마감 버튼·확인창·최종 마감·취소; 마감은 close가 아닌 deadline | 팀원 모집 | <code>open</code>, <code>cancel</code>, <code>confirm</code> | <code>click</code> | <a href="https://app.notion.com/p/0aa0221954bc82a288d001afd2850c08">9. 내가 작성한 모집글</a> |
| <code>team_notification</code> | 팀원 모집 알림 목록 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/a030221954bc827d93920103041dcc09">0. 알림 클릭</a> |
| <code>team_applicant_detail</code> | 지원자 카드에서 지원자 상세 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/6a60221954bc828bb4e601b073d671f6">10. 지원자 관리</a> |
| <code>team_profile</code> | 팀원 모집 프로필 화면 진입; 프로필 작성/수정은 별도 기능 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/ea20221954bc82229ef181d419ea2214">7. 프로필 클릭</a> |
| <code>team_detail</code> | 모집글 카드에서 상세 진입 | 팀원 모집 | <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/f260221954bc823f9015010400ff257f">3. 게시글 클릭</a> |
| <code>team_recruit_entry</code> | 팀원 모집 서비스 헤더·푸터·카테고리 진입 | 팀원 모집 | <code>header_entry</code>, <code>category_entry</code>, <code>footer_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/4f60221954bc83f89a17810c28e045ac">12. 헤더_팀원 모집 진입 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/4340221954bc834e9d4701a526f76405">[레거시·중복 원문] 14. 카테고리_팀원 모집 진입 (클릭) - 추가된 로깅</a> |
| <code>semester_manage</code> | 시간표 학기 선택과 학기 편집. 추가·삭제 확정/적용은 웹·모바일 edit\_apply 공통 1회 이벤트 | 시간표 | <code>edit_apply</code> (학기 추가·삭제 확정/적용 공통) | <code>click</code>, <code>select</code> | <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> · <a href="https://app.notion.com/p/8550221954bc82d88ad9017112a13e74">2-7. 시간표_학기 드롭다운 (클릭)</a> |
| <code>timetable_config</code> | 시간표 설정 열기·이름/기본 설정 저장·삭제 | 시간표 | <code>save</code>, <code>delete</code>, <code>open</code> | <code>click</code> | <a href="https://app.notion.com/p/1b90221954bc8221815481a568880eee">2-15. (웹) 시간표_저장 (클릭)</a> · <a href="https://app.notion.com/p/2af0221954bc823f99db815887a20279">2-16. (웹) 시간표_삭제 (클릭)</a> |
| <code>timetable_export</code> | 시간표 이미지 저장·다운로드 | 시간표 | <code>image_save</code> | <code>click</code> | <a href="https://app.notion.com/p/27e0221954bc821da617812bbc62ce44">2-6. 시간표_이미지 저장 (클릭)</a> |
| <code>timetable_entry</code> | 시간표 헤더·푸터·카테고리 진입 | 시간표 | <code>category_entry</code>, <code>footer_entry</code>, <code>header_entry</code> | <code>click</code> | <a href="https://app.notion.com/p/6360221954bc837f98d98135eefbf8bc">[레거시·이관 원문] 2-5. (앱, 반응형 웹) 햄버거_시간표</a> · <a href="https://app.notion.com/p/2150221954bc83968571018a8f92635f">2-4. (웹) 푸터_시간표</a> |
| <code>timetable_edit</code> | 시간표 수정 진입·정규/직접추가 탭·직접 일정 저장·수정 완료 | 시간표 | <code>confirm</code>, <code>custom_save</code>, <code>tab</code>, <code>entry</code> | <code>click</code> | <a href="https://app.notion.com/p/ab10221954bc8289881d817c8687d52f">2-17. (웹) 시간표_수정 완료 (클릭)</a> · <a href="https://app.notion.com/p/ce60221954bc8306ad7281a40e03cfda">2-19. (웹) 시간표_수정_일정 저장 (클릭)</a> |
| <code>timetable_list</code> | 시간표 목록 진입과 목록 내 시간표 선택 | 시간표 | <code>entry</code> | <code>click</code>, <code>select</code> | <a href="https://app.notion.com/p/d450221954bc82b49338816b4cfa598d">2-26. (앱, 반응형 웹) 시간표_학기 시간표 선택 (클릭) - 추가된 로깅</a> · <a href="https://app.notion.com/p/8ce0221954bc83fda1e801087dc95497">2-27. (앱, 반응형 웹) 시간표 목록_시간표 선택 (클릭) - 추가된 로깅</a> |
| <code>timetable_manage</code> | 선택 학기에 시간표 추가 | 시간표 | <code>add</code> | <code>click</code> | <a href="https://app.notion.com/p/a790221954bc82fcba5d81decfc5bd71">2-24. (웹) 시간표_시간표 추가하기 (클릭) - 추가된 로깅</a> |
| <code>shop_menu</code> | 상점 메뉴 탭 진입과 메뉴 목록 스크롤 | 주변상점 | <code>entry</code> | <code>click</code>, <code>scroll</code> | <a href="https://app.notion.com/p/19f0221954bc8311877d8105cb3f2af0">3-4, 4.5 상점상세 메뉴 (클릭,스크롤)</a> |

### 기존 공용 기능의 DA1 detail 확장

feature의 기존 뜻을 유지하면서 아래 목적·대상을 detail로 구분한다. detail에 submit/click/select 등 category 단어를 다시 넣지 않는다. click을 submit으로 바꾸거나 전송 시점을 바꾸는 변경이 아니다.

| 공용 기능 | DA1 포함 detail | 적용 서비스 |
| --- | --- | --- |
| <code>filter</code> | <code>checkbox</code>, <code>sort</code>, <code>category</code>, <code>quick_filter</code>, <code>min_amount</code>, <code>daeseong_direction</code>, <code>city_direction</code>, <code>bus_type</code>, <code>shuttle_route</code>, <code>to_home</code>, <code>to_school</code>, <code>city_route</code>, <code>status</code>, <code>reset</code>, <code>apply</code>, <code>open</code>, <code>method</code>, <code>close</code> | 주변상점·버스·팀원 모집 |
| <code>navigation</code> | <code>review_exit</code>, <code>back</code>, <code>nearby_entry</code>, <code>order_history_entry</code>, <code>bus_search_return</code>, <code>main_return</code> | 주변상점·버스·팀원 모집·시간표 |
| <code>contact</code> | <code>phone</code> | 주변상점 |
| <code>search</code> | <code>departure_confirm</code>, <code>departure_open</code>, <code>departure_time_now</code>, <code>arrival_confirm</code>, <code>arrival_open</code>, <code>departure_time_confirm</code>, <code>swap</code>, <code>departure_time_open</code>, <code>department</code>, <code>curriculum</code> | 주변상점·버스·팀원 모집·시간표 |
| <code>login_popup</code> | <code>close</code>, <code>login_entry</code> | 주변상점·시간표 |
| <code>login</code> | 없음: category만 사용 | 사장님 |
| <code>sign_up</code> | <code>next</code>, <code>entry</code> | 사장님 |
| <code>account_recovery</code> | <code>password_entry</code> | 사장님 |
| <code>profile_edit</code> | <code>entry</code>, <code>load</code>, <code>major</code>, <code>next</code>, <code>skill_add</code>, <code>activity_edit</code>, <code>activity_edit_confirm</code>, <code>activity_add</code>, <code>activity_add_confirm</code>, <code>open</code>, <code>confirm</code>, <code>cancel</code> | 팀원 모집 |
| <code>chat_entry</code> | <code>entry</code>, <code>applicant_entry</code>, <code>group_entry</code> | 팀원 모집 |

- DA1 검색 실행·로그인 등 이미 4구간인 명세는 category를 유지한다. DA2의 과거 detail 예시와 전송 시점을 혼동하지 않는다.
- 공용 헤더·푸터는 label page와 screen\_view를 각각 <code>header</code> / <code>footer</code>로 고정한다. 메뉴·카테고리는 <code>main_category</code>이며 두 필드가 같다. 버스 공지·정보 오류 제보는 기존 <code>bus_timetable</code>을 유지한다. 2026-10-30 상민 직접 지시로 확정하며 이전 동적 표기안은 대체한다. SDK 적용·실제 수집은 별도 검증이다.
- 버스 헤더·푸터의 목적지형 feature(route/timetable)는 변환 제외 예외다. 품절 결과형 접미 없는 라벨과 A/B 병기는 동결 예외다.

### 동일 이벤트 계약을 공유하는 명세 (2026-10-27)

문서가 여러 개인 경우에도 같은 사용자 동작에서 중복 전송하지 않는다. 플랫폼별 기존 경로·value·발생 시점은 각 원문을 유지한다. 아래 10개는 기존 7개와 후속 사용자 결정 3개를 반영한 문서상 동일 계약 요약이며, 등록·상태의 단일 기준은 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>의 동일 이벤트 계약표다. 품절 제보 A/B 동결 예외와 별개다. 시간표 모바일 학기 편집의 추가·삭제 공통 적용 label은 유지하되, 체크 해제의 실제 삭제 동작과 SDK의 한 번 전송은 검증 완료로 간주하지 않는다.

| 현행 label | 기준 명세 | 함께 설명하는 명세 |
| --- | --- | --- |
| <code>account__main_profile__login__entry__click</code> | <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> | <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> · <a href="https://app.notion.com/p/2660221954bc82719b1b01589fd83c1b">4-2 로그인 클릭</a> |
| <code>account__main_profile__logout__click</code> | <a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> | <a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> · <a href="https://app.notion.com/p/6d90221954bc83a8839d01823f621620">4-3 로그아웃 클릭</a> |
| <code>callvan__main__callvan_entry__recruitment_list_entry__click</code> | <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> | <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> · <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> |
| <code>shop__shop_detail__contact__phone__click</code> | <a href="https://app.notion.com/p/2d50221954bc834f8ca9019292dd4741">3-2 상점상세 전화 (클릭)</a> | <a href="https://app.notion.com/p/2d50221954bc834f8ca9019292dd4741">3-2 상점상세 전화 (클릭)</a> · <a href="https://app.notion.com/p/3d50221954bc824e9a1e81e83e042833">4-5 전화 주문 혜택 상점상세 전화 (클릭)</a> |
| <code>account__shop_detail__login_popup__close__click</code> | <a href="https://app.notion.com/p/40c0221954bc830a8ea4015f95cf4e1f">3-23 상점상세 리뷰작성 _로그인_취소 (클릭)</a> | <a href="https://app.notion.com/p/fc90221954bc82cb9b1f01c7863d50e9">3-25 상점상세 리뷰신고 _취소누름 (비로그인)</a> · <a href="https://app.notion.com/p/40c0221954bc830a8ea4015f95cf4e1f">3-23 상점상세 리뷰작성 _로그인_취소 (클릭)</a> |
| <code>account__shop_detail__login_popup__login_entry__click</code> | <a href="https://app.notion.com/p/bf00221954bc8246a5ae8154ce1bcf97">3-22 상점상세 리뷰작성 들어가기_로그인누름 (비로그인)</a> | <a href="https://app.notion.com/p/c150221954bc8307920f81f1cddd95b1">3-24 상점상세 리뷰신고 _로그인 (비로그인)</a> · <a href="https://app.notion.com/p/bf00221954bc8246a5ae8154ce1bcf97">3-22 상점상세 리뷰작성 들어가기_로그인누름 (비로그인)</a> |
| <code>real_estate__main_category__real_estate_entry__category_entry__click</code> | <a href="https://app.notion.com/p/9890221954bc820ba81a81e6725d617b">Notion 원문</a> | <a href="https://app.notion.com/p/2640221954bc83d6a82901c92388b825">[레거시] 1-3 햄버거_복덕방 진입 (클릭)</a> · <a href="https://app.notion.com/p/9890221954bc820ba81a81e6725d617b">Notion 원문</a> |
| <code>cafeteria__main__more__click</code> (이관 전 계약) | <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> | <a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a> · <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> |
| <code>timetable__timetable__semester_manage__edit_apply__click</code> | <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> | <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> · <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> |
| <code>timetable__main_category__timetable_entry__category_entry__click</code> | <a href="https://app.notion.com/p/e9d0221954bc828aa337812594729789">[레거시·중복 원문] 2-21. (앱, 반응형 웹) 카테고리_시간표 진입 (클릭) - 추가된 로깅</a> | <a href="https://app.notion.com/p/6360221954bc837f98d98135eefbf8bc">[레거시·이관 원문] 2-5. (앱, 반응형 웹) 햄버거_시간표</a> · <a href="https://app.notion.com/p/e9d0221954bc828aa337812594729789">[레거시·중복 원문] 2-21. (앱, 반응형 웹) 카테고리_시간표 진입 (클릭) - 추가된 로깅</a> |

</details>

## 4. 이번에 통일한 기능 묶음

- keyword\_manage: 공지·분실물의 키워드 관리·추가·추천·알림·삭제. 이전 기능 notice\_keyword\_manage, lost\_item\_keyword\_manage, keyword\_add, lost\_item\_keyword\_add, keyword\_notification, lost\_item\_keyword\_notification, lost\_item\_keyword\_delete를 묶는다. 페이지명 notice\_keyword\_manage / lost\_item\_keyword\_manage는 유지한다.
- profile\_edit: 수정 진입과 제출. 기능 구간 edit\_profile을 통일하며 화면 이름 edit\_profile은 유지한다.
- account\_recovery: find\_id / find\_password를 묶고 id\_entry / password\_entry로 구분한다.
- navigation: notice\_detail\_exit / callvan\_exit / course\_practice\_exit를 묶고 back / notice\_list\_return / main\_return으로 구분한다.
- callvan\_participation: callvan\_join / callvan\_join\_cancel을 묶고 join\_response / cancel\_response로 구분한다.
- filter / notice\_list: 필터 선택과 목록 탐색을 구분한다. tab\_selection·목록 키워드 필터는 filter, list\_explore는 notice\_list로 정리한다.
- filter: notice\_filter / lost\_item\_filter / callvan\_filter를 같은 기능명으로 통일한다. 서비스·페이지·세부 행동으로 적용 맥락을 구분한다.
- search: notice\_search / callvan\_search / department\_search / course\_search의 검색·조회 기능명을 통일한다. 검색 입력 클릭과 최종 검색 실행은 마지막 행동에서 구분한다.
- contact: callvan\_contact / department\_contact를 통일하고 phone\_click / phone\_copy로 구분한다.
- search / course\_application: 개설학부 선택·강좌 조회와 실제 과목 신청을 구분한다.
- category\_navigation: 3-6의 대상 메뉴를 공용 카테고리 클릭 기능으로 묶는다. 개별 서비스 진입 명세는 별도로 유지한다.

## 5. 카테고리 두 명세의 별개 유지

- <a href="https://app.notion.com/p/4660221954bc82939cd001cf9a20ba4c">[레거시] 1-0-2 학교 부서정보 접근 (카테고리 진입)</a>: 학교 부서 서비스 진입. <code>department__main_category__department_entry__category_entry</code>.
- <a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>: 공용 카테고리 메뉴 클릭. 부서 항목은 <code>department__main_category__category_navigation__department_entry</code>.
- 두 문서는 서로 링크하고 별개 유지한다. 한쪽을 대체하거나 합치지 않는다. 실제 전송·수집 검수는 후속 작업이다.

## 6. 분실물 필터 통합

- 현행 구현은 <a href="https://app.notion.com/p/37b0221954bc8395897801f58e65d2a6">11-23. 분실물_필터_적용_클릭</a> 하나로 통합한다. <a href="https://app.notion.com/p/0b10221954bc83dea9960100951f760d">11-18.분실물_게시물종류_클릭 (11-23 통합)</a>는 이력으로 보존하고 별도 전송하지 않는다.
- 적용하기 클릭에서 최종 상태를 filter\_scope / filter\_post\_type / filter\_item\_type / filter\_status 네 STRING 파라미터로 보낸다. 복수 선택은 정의된 순서로 ‘\|’ 연결하고 전체·기본값은 ‘전체’로 기록한다. 기존 value ‘분실물’은 공통 식별값으로 유지한다.
- 네 그룹을 하나의 JSON·혼합 리스트 문자열로 묶지 않는다. SDK 전송과 dbt 추출·마트 반영은 개발 후속 작업이며 상세 규칙은 11-23 명세를 따른다.

## 7. 적용·참고사진

### 2026-10-16 결정 반영 — label 변경 3개

아래는 최신 결정에 따른 현재 label이다. 이전 2026-10-15 대응표는 당시 변경 이력으로 보존한다.

<table>
<tr>
<td>
명세
</td>
<td>
이전 label
</td>
<td>
현행 label
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/8e50221954bc8332a66f81398c9a9f4e">3-2 콜밴팟 도착지 선택</a>
</td>
<td>
<code>callvan__callvan_write__callvan_write__arrival_select</code>
</td>
<td>
<code>callvan__callvan_write__callvan_write__arrival_confirm</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d110221954bc837a81ca81811affc966">12-2. 키워드 추가_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__add_click</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__add_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4760221954bc8316a54a81a8b347f918">12-4. 키워드 알림받기_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__notification_click</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__notification_toggle</code>
</td>
</tr>
</table>

- 분실물 로그인 요청 11-25·11-26은 누른 버튼에 따라 login\_entry / close 중 label 하나만 전송한다. 기존 value·클릭 시점은 유지한다.
- 콜밴팟 2-4·2-5는 예·아니오 응답 시점, 3-1·3-2는 선택하기 클릭, 3-3은 확인 클릭 시점을 유지한다. 3-2의 세부 행동은 <code>arrival_confirm</code>이다.
- 분실물 12-2는 <code>add_submit</code>·category <code>submit</code>·추가 클릭 시 입력 키워드 value로 확정했다. 12-3은 클릭한 추천 키워드를 동적으로 매핑한다. 12-4는 <code>notification_toggle</code>과 value “받기” / “끄기”로 변경 후 상태를 구분하고 category <code>click</code>을 유지한다. 11-2·11-9는 실제 품목 선택 순간의 표시값을 동적으로 매핑한다.
- 분실물 11-29·11-30은 보류가 아닌 현행 적용 대상이다. 11-26·12-5의 사진은 사용자가 현재 버전으로 수정 완료했고, 습득물 수정은 제목 차이를 설명한 공통 사진을 사용한다. 레거시 원문과 대상 밖 서비스는 확대 수정하지 않는다.
- 참고사진은 해당 로깅 바로 아래 토글로 넣고 원본·출처·플랫폼 구분을 보존한다. 명세 저장과 구현·배포·실제 수집 검수 완료는 별도다.

<details>
<summary>이번 label 변경 대응표 (96개)</summary>

이 표의 수정 전 값은 이번 작업 직전 초안이다. 각 명세의 ‘이전 로깅’ 원문은 별도로 보존한다.

<table>
<tr>
<td>
명세
</td>
<td>
수정 전 초안
</td>
<td>
적용 label
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/7910221954bc822fbaf881a78dc1919d">1-4 약관동의(클릭)</a>
</td>
<td>
<code>account__sign_up_policy__sign_up__terms_agreement__click</code>
</td>
<td>
<code>account__sign_up_policy__sign_up__terms_agree_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9dd0221954bc83328f3101973bcaff2b">1-6 본인인증_인증완료</a>
</td>
<td>
<code>account__identity_verification__sign_up__code_accurate</code>
</td>
<td>
<code>account__identity_verification__sign_up__code_verify_success</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/6400221954bc829089cb01755624814f">1-7 정보입력_학생_외부인_구분(클릭)</a>
</td>
<td>
<code>account__identity_verification__sign_up__user_type__select</code>
</td>
<td>
<code>account__identity_verification__sign_up__user_type_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9bd0221954bc833c845a818f39ef8ca0">1-7 정보입력_학생_외부인_구분(클릭)</a>
</td>
<td>
<code>account__user_type_selection__sign_up__user_type__select</code>
</td>
<td>
<code>account__user_type_selection__sign_up__user_type_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5460221954bc83d493598115740d1ed5">1-8 학생_외부인_아이디_중복확인</a>
</td>
<td>
<code>account__input_user_info__sign_up__id_duplicate_check</code>
</td>
<td>
<code>account__input_user_info__sign_up__id_available</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/8110221954bc82ee8db301cfdfb3df24">1-8 학생_외부인_닉네임_중복확인</a>
</td>
<td>
<code>account__input_user_info__sign_up__nickname_duplicate_check</code>
</td>
<td>
<code>account__input_user_info__sign_up__nickname_available</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4830221954bc8355887e01f988251647">1-9 학생_외부인_회원가입완료(클릭)</a>
</td>
<td>
<code>account__input_user_info__sign_up__complete</code>
</td>
<td>
<code>account__input_user_info__sign_up__submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/cd20221954bc8307a5b38176275d6992">2-4 아이디찾기(클릭)</a>
</td>
<td>
<code>account__login__find_id__entry</code>
</td>
<td>
<code>account__login__account_recovery__id_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/bda0221954bc833eb901010249bdaac2">2-5 비밀번호찾기(클릭)</a>
</td>
<td>
<code>account__login__find_password__entry</code>
</td>
<td>
<code>account__login__account_recovery__password_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/8290221954bc8278bc2b013efa8c22fe">3-3 정보수정완료(클릭)</a>
</td>
<td>
<code>account__edit_profile__edit_profile__submit</code>
</td>
<td>
<code>account__edit_profile__profile_edit__submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/6400221954bc82c58d4a01c203a5e06d">1-5. (모바일)메인_다음모달_스왑</a>
</td>
<td>
<code>banner__main__modal__swipe</code>
</td>
<td>
<code>banner__main__modal__next_swipe</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9550221954bc8211b30381b6165e244f">1-6. (웹)메인_다음모달_클릭</a>
</td>
<td>
<code>banner__main__modal__next</code>
</td>
<td>
<code>banner__main__modal__next_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/2de0221954bc8295b75d01c951e05d36">1-1.메인_공지사항_더보기_클</a>
</td>
<td>
<code>board__main__notice_entry__notice_more</code>
</td>
<td>
<code>board__main__notice_entry__more_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/aa70221954bc8350b61801d87fe1eb46">1-2. 메인_공지사항_클릭</a>
</td>
<td>
<code>board__main__notice_entry__title</code>
</td>
<td>
<code>board__main__notice_entry__title_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9e60221954bc828eb30081180eaaadc2">1-3. 메인_공지사항_상세_클릭</a>
</td>
<td>
<code>board__main__notice_detail</code>
</td>
<td>
<code>board__main__notice_detail__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/76a0221954bc839ab58e01d56b51c40f">3-1. 공지사항_가장 많이 본 게시물_클릭</a>
</td>
<td>
<code>board__main_notice__notice_detail__popular_notice</code>
</td>
<td>
<code>board__main_notice__notice_detail__popular_post_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/a100221954bc82429edf81333432e776">3-2. 공지사항_바로가기_클릭</a>
</td>
<td>
<code>board__main_notice__external_link__shortcut</code>
</td>
<td>
<code>board__main_notice__external_link__shortcut_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/db60221954bc82a7981281691197c64e">3-3·4-3. 공지사항_상세_클릭 (웹·앱)</a>
</td>
<td>
<code>board__main_notice__notice_detail</code>
</td>
<td>
<code>board__main_notice__notice_detail__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d490221954bc825892e98110078adff4">4-1. 탭 메뉴바_클릭</a>
</td>
<td>
<code>board__main_notice__tab_selection</code>
</td>
<td>
<code>board__main_notice__filter__tab_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4290221954bc83ac8cc581ceced3f5f7">4-2. 공지사항 페이지_스크롤(상하)</a>
</td>
<td>
<code>board__main_notice__list_explore__scroll</code>
</td>
<td>
<code>board__main_notice__notice_list__scroll</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/1fa0221954bc82798cef0121f9052c78">Notion 원문</a>
</td>
<td>
<code>board__main_notice__notice_detail</code>
</td>
<td>
<code>board__main_notice__notice_detail__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d5b0221954bc83e7bcbe811f66e58865">5-1. 목록_클릭</a>
</td>
<td>
<code>board__notice_detail__notice_detail_exit</code>
</td>
<td>
<code>board__notice_detail__navigation__notice_list_return</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/ec20221954bc832ab2e2816bb6ee9c8e">5-2. 인기있는 공지_클릭</a>
</td>
<td>
<code>board__notice_detail__notice_detail__popular_notice</code>
</td>
<td>
<code>board__notice_detail__notice_detail__popular_post_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/7ae0221954bc8322930581d4782416b6">5-3. 공지 원본 바로가기_클릭</a>
</td>
<td>
<code>board__notice_detail__external_link__original_shortcut</code>
</td>
<td>
<code>board__notice_detail__external_link__original_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b6e0221954bc8309be9e811da1679706">6-1. 공지글 검색_클릭</a>
</td>
<td>
<code>board__main_notice__notice_search__entry</code>
</td>
<td>
<code>board__main_notice__search__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/1ad0221954bc8335b0c981b8db6a7259">6-2. 많이 검색되는 키워드_클릭</a>
</td>
<td>
<code>board__notice_search__notice_search__popular_keyword_selection</code>
</td>
<td>
<code>board__notice_search__search__popular_keyword_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/af00221954bc832b866501b4e470f143">6-3. 공지글 검색_검색하기_클릭</a>
</td>
<td>
<code>board__notice_search__notice_search__search_submit</code>
</td>
<td>
<code>board__notice_search__search__search_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5690221954bc82c3afd881ec1864a3b2">6-4. 공지글 검색_공지상세_클릭</a>
</td>
<td>
<code>board__notice_search__notice_detail</code>
</td>
<td>
<code>board__notice_search__notice_detail__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/0490221954bc82298d940143a3b6a266">7-1. 키워드 관리_클릭</a>
</td>
<td>
<code>board__main_notice__notice_keyword_manage__entry</code>
</td>
<td>
<code>board__main_notice__keyword_manage__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/2110221954bc82d6b86c81aee8c65dab">7-2. 모두 보기_클릭</a>
</td>
<td>
<code>board__main_notice__notice_keyword_manage__filter_selection</code>
</td>
<td>
<code>board__main_notice__filter__keyword_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5400221954bc8234bee481082eedbf31">7-3. 키워드_추가_클릭</a>
</td>
<td>
<code>board__notice_keyword_manage__keyword_add__submit</code>
</td>
<td>
<code>board__notice_keyword_manage__keyword_manage__add_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/28c0221954bc83ffbed48182e259f4cb">7-5. 추천 키워드_클릭</a>
</td>
<td>
<code>board__notice_keyword_manage__keyword_add__recommended_keyword</code>
</td>
<td>
<code>board__notice_keyword_manage__keyword_manage__recommended_keyword_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/2e40221954bc827e91f18112cc879791">7-6. 로그인팝업_로그인하기_클릭</a>
</td>
<td>
<code>account__notice_keyword_manage__login_popup__entry</code>
</td>
<td>
<code>account__notice_keyword_manage__login_popup__login_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/6830221954bc8252a40b815d2dc51b82">7-8. 키워드 알림받기_토글</a>
</td>
<td>
<code>board__notice_keyword_manage__keyword_notification__toggle</code>
</td>
<td>
<code>board__notice_keyword_manage__keyword_manage__notification_toggle</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/ce80221954bc83c8923f01b225bf5415">7-9. 알림설정_공지사항 키워드 알림_클릭</a>
</td>
<td>
<code>board__notification_config__notice_keyword_manage__entry</code>
</td>
<td>
<code>board__notification_config__keyword_manage__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/ae50221954bc83b697ef01c87e276c72">9-1. 키워드 게시물_알림</a>
</td>
<td>
<code>board__from_external__notice_detail__keyword_notification</code>
</td>
<td>
<code>board__from_external__notice_detail__keyword_notification_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/29a0221954bc82788e2c81c4dbec50d7">10-1. 헤더_교내 시설물 정보_클릭</a>
</td>
<td>
<code>facility__header__facility_entry__header</code>
</td>
<td>
<code>facility__header__facility_entry__header_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/dea0221954bc8215b04301c51eb64ad9">10-2. 푸터_교내 시설물 정보_클릭</a>
</td>
<td>
<code>facility__footer__facility_entry__footer</code>
</td>
<td>
<code>facility__footer__facility_entry__footer_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/3820221954bc82f9a58781fbc1b57a12">[레거시] 10-3. 카테고리_교내 시설물 정보_클릭</a>
</td>
<td>
<code>facility__main_category__facility_entry__category</code>
</td>
<td>
<code>facility__main_category__facility_entry__category_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/e980221954bc83b09ff901a5b0876f13">11-2.분실물_습득물신고_품목선택_클릭</a>
</td>
<td>
<code>board__found_item_write__lost_item_write__item_category_selection</code>
</td>
<td>
<code>board__found_item_write__lost_item_write__item_category_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/44c0221954bc82999e1001a307e3680c">11-3.분실물_습득물신고_물품추가_클릭</a>
</td>
<td>
<code>board__found_item_write__lost_item_write__item_add</code>
</td>
<td>
<code>board__found_item_write__lost_item_write__item_add_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/f890221954bc8341b0a701c76ac55892">11-5.분실물_습득물_삭제_클릭</a>
</td>
<td>
<code>board__lost_item_detail__lost_item_delete__entry</code>
</td>
<td>
<code>board__lost_item_detail__lost_item_delete__open</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/e780221954bc837fb69b81094731590c">11-7·11-8.분실물_글종류선택(잃어버렸어요·주인을찾아요)_클릭</a>
</td>
<td>
<code>board__lost_item_list__lost_item_write__post_type_selection</code>
</td>
<td>
<code>board__lost_item_list__lost_item_write__post_type_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b670221954bc820ebbf081fa822c1a9b">Notion 원문</a>
</td>
<td>
<code>board__lost_item_list__lost_item_write__post_type_selection</code>
</td>
<td>
<code>board__lost_item_list__lost_item_write__post_type_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d140221954bc8228b3c9819a6eb39cb4">11-9.분실물_분실물신고_품목선택_클릭</a>
</td>
<td>
<code>board__lost_item_write__lost_item_write__item_category_selection</code>
</td>
<td>
<code>board__lost_item_write__lost_item_write__item_category_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b290221954bc82dd95d9011a48439322">11-10.분실물_분실물신고_물품추가_클릭</a>
</td>
<td>
<code>board__lost_item_write__lost_item_write__item_add</code>
</td>
<td>
<code>board__lost_item_write__lost_item_write__item_add_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/1d20221954bc827d923581192263ebbf">[레거시] 11-15.카테고리_채팅(쪽지)_클릭</a>
</td>
<td>
<code>chat__main_category__chat_entry__category</code>
</td>
<td>
<code>chat__main_category__chat_entry__category_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/15d0221954bc82da9b0001cb92292190">11-17.헤더_쪽지_클릭</a>
</td>
<td>
<code>chat__header__chat_entry__header</code>
</td>
<td>
<code>chat__header__chat_entry__header_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b8d0221954bc8292920c81b609c67a2f">11-19.푸터_쪽지_클릭</a>
</td>
<td>
<code>chat__footer__chat_entry__footer</code>
</td>
<td>
<code>chat__footer__chat_entry__footer_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4830221954bc8367af8b0138839c7ffa">11-22. 분실물_필터_클릭</a>
</td>
<td>
<code>board__lost_item_list__lost_item_filter__entry</code>
</td>
<td>
<code>board__lost_item_list__filter__open</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/37b0221954bc8395897801f58e65d2a6">11-23. 분실물_필터_적용_클릭</a>
</td>
<td>
<code>board__lost_item_list__lost_item_filter__apply</code>
</td>
<td>
<code>board__lost_item_list__filter__apply</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/0b60221954bc8278b63a016f2e8b03a6">11-24. 분실물_게시글_클릭</a>
</td>
<td>
<code>board__lost_item_list__lost_item_detail</code>
</td>
<td>
<code>board__lost_item_list__lost_item_detail__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/aac0221954bc8364b36b81377bd730b5">11-27. 분실물_상태변경_클릭</a>
</td>
<td>
<code>board__lost_item_detail__lost_item_status__entry</code>
</td>
<td>
<code>board__lost_item_detail__lost_item_status__open</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/63e0221954bc831abe6d811030116db6">12-1. 키워드 설정_클릭</a>
</td>
<td>
<code>board__lost_item_list__lost_item_keyword_manage__entry</code>
</td>
<td>
<code>board__lost_item_list__keyword_manage__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d110221954bc837a81ca81811affc966">12-2. 키워드 추가_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__lost_item_keyword_add</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__add_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/eaf0221954bc83da8fd28151ac8e36f2">12-3. 추천 키워드_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__lost_item_keyword_add__recommended_keyword</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__recommended_keyword_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4760221954bc8316a54a81a8b347f918">12-4. 키워드 알림받기_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__lost_item_keyword_notification</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__notification_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9fd0221954bc837a995e81fb4a803008">12-5. 키워드 삭제_클릭</a>
</td>
<td>
<code>board__lost_item_keyword_manage__lost_item_keyword_delete</code>
</td>
<td>
<code>board__lost_item_keyword_manage__keyword_manage__delete_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a>
</td>
<td>
<code>callvan__main__callvan_entry__recruitment_view</code>
</td>
<td>
<code>callvan__main__callvan_entry__recruitment_list_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/80c0221954bc8396a38f01b1df7cbcd8">[레거시] 1-3 카테고리 → 콜밴팟 모집</a>
</td>
<td>
<code>callvan__main_category__callvan_entry__category</code>
</td>
<td>
<code>callvan__main_category__callvan_entry__category_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d730221954bc822980e0813e19eedf5e">2-1 콜밴팟 검색바 클릭</a>
</td>
<td>
<code>callvan__callvan_list__callvan_search__search_bar</code>
</td>
<td>
<code>callvan__callvan_list__search__search_input_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9340221954bc821ca94c01a598747209">2-2 콜밴팟 필터 클릭</a>
</td>
<td>
<code>callvan__callvan_list__callvan_filter__open</code>
</td>
<td>
<code>callvan__callvan_list__filter__open</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/fca0221954bc834b898e81f4823caa26">2-3 콜밴팟 필터 적용하기</a>
</td>
<td>
<code>callvan__callvan_list__callvan_filter__apply</code>
</td>
<td>
<code>callvan__callvan_list__filter__apply</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/efd0221954bc8367ad8c01a1cab38cd1">2-4 콜밴팟 참여하기</a>
</td>
<td>
<code>callvan__callvan_list__callvan_join__confirm</code>
</td>
<td>
<code>callvan__callvan_list__callvan_participation__join_response</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b380221954bc82a78d25814da4b3d86d">2-5 콜밴팟 참여 취소하기</a>
</td>
<td>
<code>callvan__callvan_list__callvan_join_cancel__confirm</code>
</td>
<td>
<code>callvan__callvan_list__callvan_participation__cancel_response</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/d0c0221954bc82a5b4d901d49d8d9122">2-6 콜밴팟 채팅 클릭</a>
</td>
<td>
<code>callvan__callvan_list__callvan_chat__open_from_card</code>
</td>
<td>
<code>callvan__callvan_list__callvan_chat__card_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/02b0221954bc828991040191d3ae2c3f">2-7 콜밴팟 채팅 전송</a>
</td>
<td>
<code>callvan__callvan_chat__callvan_chat__send_message</code>
</td>
<td>
<code>callvan__callvan_chat__callvan_chat__message_send</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4bf0221954bc8319afe8810bf62ccfb5">2-8 콜밴팟 전화 클릭</a>
</td>
<td>
<code>callvan__callvan_list__callvan_contact__phone</code>
</td>
<td>
<code>callvan__callvan_list__contact__phone_click</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/6900221954bc83729a9781ba8343aee6">2-10 콜밴팟 채팅방 입장 클릭</a>
</td>
<td>
<code>callvan__callvan_participant_list__callvan_chat__entry</code>
</td>
<td>
<code>callvan__callvan_participant_list__callvan_chat__participant_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/aa90221954bc824ea10201256afedfb7">2-11 콜밴팟 찾기 이탈</a>
</td>
<td>
<code>callvan__callvan_list__callvan_exit</code>
</td>
<td>
<code>callvan__callvan_list__navigation__back</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/c6d0221954bc82339621018555928042">3-1 콜밴팟 출발지 선택</a>
</td>
<td>
<code>callvan__callvan_write__callvan_write__departure_selection</code>
</td>
<td>
<code>callvan__callvan_write__callvan_write__departure_confirm</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/8e50221954bc8332a66f81398c9a9f4e">3-2 콜밴팟 도착지 선택</a>
</td>
<td>
<code>callvan__callvan_write__callvan_write__arrival_selection</code>
</td>
<td>
<code>callvan__callvan_write__callvan_write__arrival_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/c480221954bc8209b5040109456cf55e">3-3 콜밴팟 출발 시각 선택</a>
</td>
<td>
<code>callvan__callvan_write__callvan_write__departure_time_selection</code>
</td>
<td>
<code>callvan__callvan_write__callvan_write__departure_time_confirm</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/3770221954bc82c2a0a881f6e84cf070">3-4 콜밴팟 모집 작성 완료</a>
</td>
<td>
<code>callvan__callvan_write__callvan_write__complete</code>
</td>
<td>
<code>callvan__callvan_write__callvan_write__submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/dcd0221954bc825cb2e9011166f89553">3-5 콜밴팟 모집 이탈</a>
</td>
<td>
<code>callvan__callvan_write__callvan_exit</code>
</td>
<td>
<code>callvan__callvan_write__navigation__back</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/3320221954bc82cc95f10156b7668099">1-0 학교 부서 정보 접근 (헤더 진입)</a>
</td>
<td>
<code>department__header__department_entry__header</code>
</td>
<td>
<code>department__header__department_entry__header_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/2370221954bc83afaba301e35693f565">1-0-1 학교 부서 정보 접근 (푸터 진입)</a>
</td>
<td>
<code>department__footer__department_entry__footer</code>
</td>
<td>
<code>department__footer__department_entry__footer_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/4660221954bc82939cd001cf9a20ba4c">[레거시] 1-0-2 학교 부서정보 접근 (카테고리 진입)</a>
</td>
<td>
<code>department__main_category__department_entry__category</code>
</td>
<td>
<code>department__main_category__department_entry__category_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/9a40221954bc825ca9da01d7e8129ffc">1-1 카테고리 클릭</a>
</td>
<td>
<code>department__department_main__department_category__selection</code>
</td>
<td>
<code>department__department_main__department_category__select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/c050221954bc82ee93188142c99e760f">1-2 검색 아이콘 쿨릭</a>
</td>
<td>
<code>department__department_main__department_search__search_submit</code>
</td>
<td>
<code>department__department_main__search__search_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/c050221954bc82ee93188142c99e760f">1-2 검색 아이콘 쿨릭</a>
</td>
<td>
<code>department__department_list__department_search__search_submit</code>
</td>
<td>
<code>department__department_list__search__search_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/a6c0221954bc8251b852016c99e980df">1-3 전화번호 복사</a>
</td>
<td>
<code>department__department_list__department_contact__phone_copy</code>
</td>
<td>
<code>department__department_list__contact__phone_copy</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/a6c0221954bc8251b852016c99e980df">1-3 전화번호 복사</a>
</td>
<td>
<code>department__department_main__department_contact__phone_copy</code>
</td>
<td>
<code>department__department_main__contact__phone_copy</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/e4c0221954bc828f8f77018f22ccff49">0. (웹) 모의수강신청 진입</a>
</td>
<td>
<code>course_practice__timetable__course_practice_entry</code>
</td>
<td>
<code>course_practice__timetable__course_application__entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/ce30221954bc83b2ae9e01276e0cf090">1-1. 모의수강신청_개설학부(과) 선택</a>
</td>
<td>
<code>course_practice__course_practice__course_application__department_selection</code>
</td>
<td>
<code>course_practice__course_practice__search__department_select</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/ef10221954bc83d29ff981456a9eb032">1-2. 모의수강신청_조회 클릭</a>
</td>
<td>
<code>course_practice__course_practice__course_application__query</code>
</td>
<td>
<code>course_practice__course_practice__search__search_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/2510221954bc82d8804901536761828c">1-3. 모의수강신청_강좌 신청 클릭</a>
</td>
<td>
<code>course_practice__course_practice__course_application__lecture_application</code>
</td>
<td>
<code>course_practice__course_practice__course_application__lecture_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/f2e0221954bc82d8892081d7e1cf9824">1-4. 모의수강신청_예비수강과목 신청 클릭</a>
</td>
<td>
<code>course_practice__course_practice__course_application__preselected_application</code>
</td>
<td>
<code>course_practice__course_practice__course_application__preselected_submit</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/0140221954bc8310a04f013fed656d61">1-5. 모의수강신청_메인으로 클릭</a>
</td>
<td>
<code>course_practice__course_practice__course_practice_exit__main_button</code>
</td>
<td>
<code>course_practice__course_practice__navigation__main_return</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a>
</td>
<td>
<code>callvan__main__callvan_entry__recruitment_view</code>
</td>
<td>
<code>callvan__main__callvan_entry__recruitment_list_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>
</td>
<td>
<code>facility__main_category__facility_entry__category</code>
</td>
<td>
<code>facility__main_category__category_navigation__facility_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>
</td>
<td>
<code>department__main_category__department_entry__category</code>
</td>
<td>
<code>department__main_category__category_navigation__department_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>
</td>
<td>
<code>callvan__main_category__callvan_entry__category</code>
</td>
<td>
<code>callvan__main_category__category_navigation__callvan_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5e70221954bc83759ba681e63c11da87">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>
</td>
<td>
<code>chat__main_category__chat_entry__category</code>
</td>
<td>
<code>chat__main_category__category_navigation__chat_entry</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/b820221954bc83b990c8817684fbd5cf">11-25. 분실물_쪽지_로그인요청_클릭</a>
</td>
<td>
<code>account__lost_item_detail__login_popup__message</code>
</td>
<td>
<code>account__lost_item_detail__login_popup__login_entry</code> / <code>account__lost_item_detail__login_popup__close</code>
</td>
</tr>
<tr>
<td>
<a href="https://app.notion.com/p/5570221954bc825c93438162f520c50a">11-26. 분실물_글쓰기_로그인요청_클릭</a>
</td>
<td>
<code>account__lost_item_list__login_popup__write</code>
</td>
<td>
<code>account__lost_item_list__login_popup__login_entry</code> / <code>account__lost_item_list__login_popup__close</code>
</td>
</tr>
</table>

</details>

## 전체 서비스 보완 (2026-10-27)

계정 V2의 기존 event\_category <code>click</code>과 완료/시도 전송 시점·성공/실패 value를 유지한다. 아래 5개는 기존 <code>submit</code> suffix를 현재 category와 일치시키는 최종 정렬이며, 위의 과거 마이그레이션 표보다 우선한다. 성공 이벤트를 별도로 신설하지 않는다.

| feature | 추가 detail | category | 적용 |
| --- | --- | --- | --- |
| <code>password_change</code> | <code>confirm</code> | <code>click</code> | WEB·모바일 공통 password\_change 논리 화면 |
| <code>sign_up</code> | <code>confirm</code> | <code>click</code> | input\_user\_info 화면 |
| <code>profile_edit</code> | <code>confirm</code> | <code>click</code> | edit\_profile 화면 |
| <code>login</code> | <code>confirm</code> | <code>click</code> | login 화면 |

- <code>account__edit_profile__password_change__submit</code> → <code>account__edit_profile__password_change__confirm__click</code>
- <code>account__password_change__password_change__submit</code> → <code>account__password_change__password_change__confirm__click</code>
- <code>account__input_user_info__sign_up__submit</code> → <code>account__input_user_info__sign_up__confirm__click</code>
- <code>account__edit_profile__profile_edit__submit</code> → <code>account__edit_profile__profile_edit__confirm__click</code>
- <code>account__login__login__submit</code> → <code>account__login__login__confirm__click</code>

### 전체 서비스 중복 라벨의 확인 상태 (2026-10-28)

같은 label이 여러 문서에 있다는 사실만으로 동일 이벤트나 SDK의 한 번 전송을 확정하지 않는다. 중복 허용은 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>의 동일 이벤트 계약표에 기준 명세와 함께 등록된 계약만 적용한다. 아래 표는 과거 후보 4묶음의 최신 확인 상태다. 로그인·로그아웃·콜밴팟 3묶음은 가이드 계약표에 등록했고, 회원가입은 메뉴와 로그인 화면의 별개 진입점으로 정렬했다. 사용자 승인 범위 외 value·발생 시점·플랫폼은 임의 통합하지 않는다. 동일 계약으로 확정된 한 사용자 동작은 문서 수만큼 추가 전송하지 않는다.

| label | 연결 명세 | 확인 상태 |
| --- | --- | --- |
| <code>callvan__main__callvan_entry__recruitment_list_entry__click</code> | <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> · <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> | 사용자 승인으로 새 value 콜밴팟 모집보기 통일. 기준 명세 콜밴팟 1-1, 대응 홈 1-6. 문서 계약 등록 완료·실제 호출 및 한 번 전송 미확인. |
| <code>account__main_profile__login__entry__click</code> | <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> · <a href="https://app.notion.com/p/2660221954bc82719b1b01589fd83c1b">4-2 로그인 클릭</a> | 사용자 승인으로 새 value 로그인 통일. 기준 명세 계정 2-2, 대응 홈 4-2. 로그인 화면 진입 클릭의 문서 계약 등록 완료·SDK 및 한 번 전송 미확인. |
| <code>account__main_profile__logout__click</code> | <a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> · <a href="https://app.notion.com/p/6d90221954bc83a8839d01823f621620">4-3 로그아웃 클릭</a> | 필드가 일치하는 프로필 로그아웃 클릭의 문서 계약 등록 완료. 기준 명세 계정 4-2, 대응 홈 4-3. 기존 value 로그아웃 유지·실제 한 번 전송 미확인. |
| <code>account__main_category__sign_up__menu_entry__click</code> / <code>account__login__sign_up__entry__click</code> | <a href="https://app.notion.com/p/0820221954bc834eb41301752196a7d5">1-2 회원가입진입(클릭)</a> · <a href="https://app.notion.com/p/a1e0221954bc82ebbe390176073d8e18">1-3 로그인 화면_회원가입진입(클릭)</a> | 사용자 승인으로 1-2 메뉴는 main\_category / menu\_entry, 1-3 로그인 화면은 login / entry로 문서상 구분했다. 동일 이벤트 계약으로 등록하지 않으며 실제 호출·SDK 적용은 미확인. |

## 홈화면 리디자인 기존 동작 추가 등록 (2026-11-01)

기존 동작 10개를 공통 형식으로 정리한다. 사용자 승인으로 새 명세 event\_name은 DA2다. 기존 CAMPUS 원문은 보존하며 SDK 마이그레이션·추가 전송·새 사용자 동작 생성은 이 문서 정리로 실행하지 않는다. 아래는 신규 어휘 및 기존 feature의 한정 확장 등록이며 다른 계약의 category를 변경하지 않는다.

| service | feature | 목적·범위 | detail → category | 기준 명세 |
| --- | --- | --- | --- | --- |
| <code>main</code> | <code>notification_list</code> | 공용 홈 알림 목록 진입·개별 항목 진입·목록 관리. 팀원 모집 전용 알림 진입 및 품절 제보/알림 개별 명세와 구분한다. | <code>entry</code>, <code>item_entry</code>, <code>delete</code>, <code>read_all</code>, <code>delete_all</code> → <code>click</code> | <a href="https://app.notion.com/p/fe30221954bc82e7abe4012b1fb7bd60">1-1 알림 클릭</a> · <a href="https://app.notion.com/p/0aa0221954bc8284a76a8157e539e7bd">1-2 알림 클릭 내부</a> · <a href="https://app.notion.com/p/7c80221954bc8271aa6a01ce2be6582f">1-2-1 알림 클릭 내부</a> · <a href="https://app.notion.com/p/8190221954bc831e9f0301de872fec2b">1-2-2 알림 클릭 내부</a> |
| <code>main</code> | <code>navigation</code> | 기존 공용 navigation 기능을 홈 하단 바 3개 버튼에 한정해 재사용. source page는 main이다. 게시판 버튼은 기존 게시판 명세를 참조한다. | <code>main_entry</code>, <code>category_menu_entry</code>, <code>profile_entry</code> → <code>click</code> | <a href="https://app.notion.com/p/0f00221954bc820e8396811d7926b4f4">2-1 네비게이션 바 홈 클릭</a> · <a href="https://app.notion.com/p/3180221954bc833385e5816ab95b23df">2-2 네비게이션 바 카테고리 클릭</a> · <a href="https://app.notion.com/p/0350221954bc82799691811138b0b988">2-4 네비게이션 바 프로필 클릭</a> |
| <code>shop</code> | <code>shop_entry</code> | 메인의 많이 찾는 상점 둘러보기 버튼. 제목/전체보기·카테고리 카드와 구분한다. | <code>popular_entry</code> → <code>click</code> | <a href="https://app.notion.com/p/aa90221954bc83daafec817ac462f0eb">1-10 많이 찾는 상점 둘러보기 클릭</a> |
| <code>timetable</code> | <code>timetable_entry</code> | 프로필의 내 시간표 버튼. category/header/footer 진입과 구분한다. | <code>entry</code> → <code>click</code> | <a href="https://app.notion.com/p/8420221954bc82b587bc81059510b0ca">4-1 내 시간표 클릭</a> |

- main은 공용 홈 기능을 나타내는 service 구간이며 담당자 event\_name과 다르다. 팀원 모집 0번의 기존 검토사항에서도 공용 알림을 main 서비스로 구분하며 그 명세는 수정하지 않는다.
- notification\_list 화면은 <a href="https://app.notion.com/p/0e40221954bc823d92c301f83b5f68d0">화면 정의 및 로깅 검수</a>에 검토중 등록했다. screen\_view는 label 두 번째 구간과 같다.
- 기존 고정 value·분류값·click category를 유지한다. 알림 본문·제목 등 자유 텍스트 수집을 추가하지 않는다. 삭제는 노출된 삭제 버튼 클릭이며 스와이프나 처리 성공 이벤트가 아니다.
- 중복·연관 참고 7페이지에는 별도 label을 만들지 않는다. 값/category/클릭 위치 차이가 있는 후보를 동일 이벤트 계약표에 임의 등록하지 않는다. 상세 목록은 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>의 이번 정리 기록을 따른다.

### 주변상점 보완 기능

| feature | 의미 | detail | event\_category |
| --- | --- | --- | --- |
| <code>shop_info</code> | 상점 상세의 가게정보 진입 | <code>entry</code> | <code>click</code> |
| <code>filter</code> | 상점 상세 리뷰의 정렬 기준 선택 | <code>review_sort</code> | <code>click</code> |
| <code>photo_view</code> | 상점 상세 사진 인덱스 변경 | <code>slide</code> | <code>swipe</code> |
| <code>navigation</code> | 상점 목록·특정 상점 혜택 화면의 뒤로가기 완료 | <code>back</code> | <code>click</code>, <code>swipe</code> |
| <code>shop_event</code> | 특정 상점 혜택 화면의 접힌 문구 펼치기 | <code>expand</code> | <code>click</code> |

검색 결과에서 상점으로 진입하는 계약의 논리 화면은 <code>shop_search</code>, feature는 <code>shop_detail</code>, detail은 <code>entry</code>, category는 <code>click</code>이다. 위 계약의 event\_name은 주변상점 공통 <code>DA1</code>이다.

### WEB 홈 고정 배너

| feature | screen\_view | detail | category | 대표 명세 |
| --- | --- | --- | --- | --- |
| fixed\_banner | main | 생략 | click | <a href="https://app.notion.com/p/4120221954bc81be8c90d3330724620b">1-11 고정 배너 본문 클릭</a> |
| fixed\_banner | main | previous / next | click | <a href="https://app.notion.com/p/4120221954bc8177a03ef13754b93695">1-12 고정 배너 이전·다음 클릭</a> |
| fixed\_banner | main | page\_select | click | <a href="https://app.notion.com/p/4120221954bc81f39ecafcad2997ed0e">1-13 고정 배너 하단 점 선택</a> |

서비스는 banner, event\_name은 DA2다. 팝업 모달과 구분하며 자동 전환은 클릭 계약에서 제외한다. SDK 반영·배포·실수집 검수는 별도다.

## 강제 업데이트 공통 기능 추가

2026-11-11 사용자 요청으로 새 문서 계약을 추가한다. 플랫폼별 label을 만들지 않으며 웹 기능 미지원 시 임의 전송하지 않는다. 기준: <a href="https://app.notion.com/p/4150221954bc81658736d9971120feaa">Notion 원문</a>.

| service | screen\_view | feature | detail | category |
| --- | --- | --- | --- | --- |
| main | forced\_update | app\_update | 없음 | exposure |
| main | forced\_update | app\_update | store\_entry | click |
| main | forced\_update | app\_update | already\_done | click |
| main | forced\_update | update\_popup | close | click |
| main | forced\_update | update\_popup | store\_entry | click |

기존 page\_view/update/page\_exit와 플랫폼별 원문 value는 과거 로깅에 보존한다. 위 새 계약의 SDK·Silver 카탈로그·배포는 미반영이다. page\_exit를 click으로 바꾸지 않으며 신규 이탈 계약은 보류한다.

### 콜밴팟 전용 알림 추가

2026-11-12 사용자 요청으로 콜밴팟 ‘1. 메인화면’ 테이블에 1-4\~1-11 명세를 추가했다. service=<code>callvan</code>, event\_name=<code>DA2</code>. 알림 진입은 <code>callvan_list / notification_list / entry / click</code>, 알림 화면 내부는 <code>callvan_notification</code>이다. <code>notification_list</code>의 detail은 <code>item_entry</code>, <code>menu_open</code>, <code>read_all</code>, <code>delete_all_open</code>, <code>delete_all_confirm</code>, <code>delete_all_cancel</code>이며 모두 category=<code>click</code>. 뒤로가기 버튼은 <code>navigation / back / click</code>이다. 삭제 메뉴 열기와 확인 버튼 클릭은 별개이며 API 성공을 뜻하지 않는다. 항목 클릭도 상세 이동 성공을 뜻하지 않는다. 플랫폼별 라벨은 나누지 않으며 Android 코드 스냅샷에서 확인한 동작을 기준으로 작성했다. iOS·WEB 지원, 이미지, SDK·Silver 반영은 미확인이다. 기준: <a href="https://app.notion.com/p/1450221954bc824f819601e4c482a0c0">Notion 원문</a>.
<!-- notion-body:end -->
