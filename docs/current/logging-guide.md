# 현행 공통 가이드

[← 현행 문서와 참고 자료](README.md)

> Notion 현행 본문입니다. 본문 안의 날짜별 결정과 과거 이력을 함께 보존했습니다. 2026-11-27의 value 확정은 이전 미기재 유지 규정을 대체합니다. SDK 배포·실제 수집 완료를 의미하지 않습니다.

[Notion 기준 원문](https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5) · 원문 편집 시각: 2026-11-27T02:35:11.406Z  
조회·동기화 기준일: 2026-11-27. [참고 자료와 문서 정리 기록](reference-status.md).

<!-- notion-body:start -->
남은 프론트 요청 적용 기준 · 2026-11-08

사용자 요청으로 PC 식단 클릭 영역·동결 대상의 전송 범위·공지 스크롤·변경 없는 학기 편집 조건을 원본에 반영했다. 해당 원본 5개의 WEB (모바일) 속성도 맞춰 이번 플랫폼 반영은 누적 27개 명세이며, 게시판·식단 데이터소스에도 기존 옵션을 보존하고 WEB (모바일)만 추가했다. 기존 event\_label·DA·category·value·screen\_view는 유지한다. 아래 과거의 해당 미확정·권고·조건부 메모는 이번 기준으로 대체하며 SDK 배포·실수집 검수는 별도다.

- 메인 식단 제목·전체보기·더보기·일반 카드 본문은 WEB·WEB (모바일)·ANDROID·IOS 모두 <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a>의 <code>main__main__meal__click</code> / DA2 / click / main 계약 하나를 사용한다. value는 식사시간\_클릭대상 형식이다. 식사시간은 아침·점심·저녁, 클릭대상은 전체보기·카드·제목이며 더보기 버튼은 전체보기로 기록한다. 예: 점심\_전체보기, 점심\_카드, 점심\_제목. 한 클릭에 한 번만 전송한다. 중복 식단 1-2 명세와 기존 main\_\_main\_\_more\_\_click·cafeteria\_\_main\_\_meal\_\_click은 레거시로 보존하며 새 전송에 병행하지 않는다. 홈 1-4 코너 선택은 main\_\_main\_\_corner\_\_select / DA2 / main / select로 별도 유지한다. 홈 식단 1-3·1-4의 첫 구간은 main, 식단 화면 내부의 첫 구간은 cafeteria로 구분한다. 공용 카테고리 진입의 서비스별 계약은 유지한다.
- WEB 공지 목록은 200ms 정지 후 직전 정지 위치와 50 CSS px 이상 차이 날 때 한 번 보낸다. 50px 미만은 누적하지 않고 기준점을 갱신한다. 최초 표시·복원·자동 스크롤은 제외한다.
- 학기 편집은 현재 집합 대비 추가·삭제 변경분이 0이면 미전송한다. 유효한 사용자 적용에 기존 공통 edit\_apply를 한 번 보내며 서버 성공 이벤트로 재정의하지 않는다.
- 팀원 모집은 전용 내부 화면(<code>src/pages/team/**</code>, <code>src/components/Team/**</code> 등)에서 이미 사용 중인 <code>team_recruitment_*</code> 수집을 유지한다. 이 범위의 새 <code>team_recruit__…</code> 네이밍 전환은 이번에 강제하지 않는다.
- 공용 모바일 카테고리 <code>/category</code>의 13개 메뉴는 별도 확정된 공통 계약이다. 그 안의 팀원 모집 진입도 team\_recruit 서비스의 DA1 / category\_navigation 계약을 따른다. 팀원 모집 내부 로깅 동결을 이유로 공용 카테고리를 옛 label로 되돌리지 않는다.
- 모바일 웹 상점의 변경 제외 범위는 주문웹에서 이식된 <code>src/components/Store/mobile/**</code>와 해당 컴포넌트를 렌더하는 모바일 목록·검색·상세·메뉴·리뷰 경로다. 이 범위의 기존 <code>shop_*</code> 계열을 유지한다. <code>KOIN_ORDER_WEBVIEW</code> 원본을 별도로 사용하는 경우에도 해당 기존 수집을 유지한다.
- 같은 <code>/store</code> URL이라도 PC 렌더 경로는 위 모바일 동결에 포함하지 않으며 기존 PC 새 계약을 따른다. 공용 <code>/category</code>의 주변상점 진입·PC 헤더·푸터까지 모바일 상점 동결로 확대하지 않는다.
- PC 새 계약과 모바일 웹 구형 수집의 공존은 허용한 전환 상태다. 기기·페이지 경로·배포 버전으로 구분하고 전체 WEB이 새 네이밍 완료라고 표시하지 않는다. 과거 로그 소급 개명과 같은 클릭의 신·구 이중 전송은 하지 않는다.
- 이 결정은 네이밍 전환 범위다. 기존에 없는 로그를 동결 정책을 이유로 임의 추가하지 않고, 누락·잘못된 발생 조건은 별도 검수한다. 실제 SDK 코드 반영·릴리즈·GA4 수집은 이 문서 정리의 완료 항목과 분리한다.

원본: <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a> · <a href="https://app.notion.com/p/d400221954bc8338b341011b9a488dac">1-2.메인_식단_클릭 (레거시)</a> · <a href="https://app.notion.com/p/4290221954bc83ac8cc581ceced3f5f7">4-2. 공지사항 페이지_스크롤(상하)</a> · <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> · <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> · <a href="https://app.notion.com/p/4120221954bc81edbdd5ea742eb94a0e">프론트엔드 로깅 질의 회신안 · 모바일 웹 카테고리</a>

플랫폼 속성 후속 반영 · 2026-11-08

사용자 요청으로 확인된 현행 명세 22개의 platform 다중 선택값을 직접 수정하고 재조회했다. WEB과 WEB (모바일)을 구분했으며, 홈 카테고리 대표·개별 명세의 모바일 웹 지원 대상도 포함한다. 홈·버스·시간표에는 기존 옵션을 보존하고 WEB (모바일)만 추가했다. 아래 과거의 카테고리 platform 속성 반영 대기 문구는 이 결과로 대체한다. 개별 명세의 WEB 없음 표기는 PC 웹과 모바일 웹을 구분해 읽는다.

이번에는 event\_label·본문·발생 조건·상태·SDK·데이터를 변경하지 않았다. 플랫폼 대상 명시는 팀원 모집·새/미래 상점의 SDK 동결 해제, 모든 하위 동작의 구현, 배포·실수집 검수 완료를 뜻하지 않는다. 여러 계약을 묶은 페이지의 platform은 해당 계약들의 합집합이며 모바일 웹은 GA4 원천에서 WEB으로 기록된다.

상세 현황: <a href="https://app.notion.com/p/4120221954bc81edbdd5ea742eb94a0e">프론트엔드 로깅 질의 회신안 · 모바일 웹 카테고리</a>

<b>카테고리 13개 최종 기준 · 서비스별 event\_name / category\_navigation · </b><b>2026-11-08</b>

사용자 요청으로 홈 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 13개 메뉴를 <code>service__main_category__category_navigation__진입대상__click</code> 형식으로 통일했다. 카테고리 13개 계약의 event\_name도 라벨 첫 구간의 서비스별 배정값으로 통일한다. 서비스명·value·발생 조건·사진·플랫폼 범위는 유지한다. 발생 화면·플랫폼·카테고리 여부와 관계없이 같은 서비스에는 같은 event\_name을 사용한다. 버스는 <code>timetable_entry</code>와 <code>search_entry</code>로 목적지를 구분하고, 시간표 서비스의 <code>timetable_entry</code>는 service 구간으로 구분한다.

아래 이전 4개 계약의 feature·detail 설명과 옛 라벨은 이 후속 결정을 따른다. 신규 공용 feature는 category\_navigation이며 cafeteria\_entry·shop\_entry·owner\_entry 등은 해당 메뉴의 detail이다. 기존 4개 라벨 유지 + 나머지 9개 라벨 표기 변경이다. 문서 네이밍 결정일 뿐 팀원 모집 SDK 동결 해제·기존 9개 계약 WEB 지원 확대·SDK 배포·실수집 검수 완료를 뜻하지 않는다. 신·구 이중 전송과 과거 로그 소급 개명은 하지 않는다. Silver·Gold·데이터·설정은 변경하지 않았다.

<b>모바일 WEB 카테고리 4개 계약 확정 · </b><b>2026-11-08</b>

사용자 요청으로 식단·버스 시간표·교통편 조회하기·코인 for Business의 미확정 네이밍을 아래 계약으로 확정했다. 기준 본문은 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 새 로깅이며 각 항목은 설명·screen\_view·event\_name·event\_label·value·event\_category와 사진만 표시한다.

공통: screen\_view=<code>main_category</code>, feature=<code>category_navigation</code>, event\_category=<code>click</code>. event\_name은 서비스별 배정표를 따르며 카테고리만의 일괄 DA2 예외는 두지 않는다. 이 네 계약의 WEB 모바일 적용 범위는 유지한다.

- 식단: <code>cafeteria__main_category__category_navigation__cafeteria_entry__click</code> / value=식단. <a href="https://app.notion.com/p/4120221954bc817faa33c64ee9f9ad13">Notion 원문</a>
- 버스 시간표: <code>bus__main_category__category_navigation__timetable_entry__click</code> / value=버스 시간표. <a href="https://app.notion.com/p/4120221954bc81c08b5ed63eff880be6">Notion 원문</a>
- 교통편 조회하기: <code>bus__main_category__category_navigation__search_entry__click</code> / value=교통편 조회하기. <a href="https://app.notion.com/p/4120221954bc813a91caf8623f3cfec0">Notion 원문</a>
- 코인 for Business: <code>owner__main_category__category_navigation__owner_entry__click</code> / value=코인 for Business. <a href="https://app.notion.com/p/4120221954bc81f3bc00e71813fe5f25">Notion 원문</a>

이 네 항목을 포함한 13개 카테고리 메뉴는 공통 feature <code>category_navigation</code>을 사용한다. 식단의 <code>cafeteria_entry</code>, 버스의 <code>timetable_entry</code>·<code>search_entry</code>, Business의 <code>owner_entry</code>는 detail로 구분한다. Business 클릭은 외부 사이트 이동 시도이며 실제 방문 성공·가입·이용 완료를 증명하지 않는다.

로그는 클릭 시 한 번 기록한다. 단순 노출·초기 렌더·자동 이동은 제외하며 이동 후 성공을 기다려 클릭 이벤트의 의미를 바꾸지 않는다. 개발 반영 전 기존 category\_\* 수집은 유지하고, 반영된 해당 WEB 버전부터 새 계약으로 전환한다. 같은 클릭에 신·구 라벨을 함께 보내지 않으며 과거 로그를 소급 개명하지 않는다.

옛 앱 햄버거 삭제 명세는 계속 삭제·레거시 이력이며, PC 헤더·푸터·홈 카드의 라벨을 이 모바일 카테고리에 재사용하지 않는다. 이번 결정은 이 4개 WEB 계약에 한정한다. 기존 다른 9개 계약의 WEB 지원·팀원 모집 동결은 별도이며 카테고리 메뉴 수는 13개 그대로다.

문서 계약 확정이며 SDK 구현·배포·실수집 검수 완료가 아니다. Silver 허용 카탈로그·Gold·데이터·활성화 설정은 변경하지 않았다. 기존 378라벨/904계약은 이번 변경을 반영한 최신 총계가 아니므로 현행 목록 재집계 없이 사용하지 않는다.

<b>모의수강신청 진입 — 현행 단일 대표 계약</b>

2026-11-08 사용자 요청으로 시간표 우측 상단 ‘모의 수강신청’ 버튼(/timetable → /course)은 <a href="https://app.notion.com/p/c0c0221954bc8270be5381ef9726eb8f">0. (웹) 모의수강신청 진입</a>의 기존 계약 하나만 적용한다. <a href="https://app.notion.com/p/36c0221954bc83a9b1c881a0e87ceb81">[레거시·중복 명세] 2-22. (웹) 시간표_모의 수강신청 (클릭)</a>는 동일 버튼의 중복 명세이므로 레거시 이력으로 보존하고 별도 이벤트를 추가 전송하지 않는다.

- event\_name: <code>DA2</code>
- event\_label: <code>course_practice__timetable__course_application__entry__click</code>
- screen\_view: <code>timetable</code>
- event\_category: <code>click</code>
- value: 모의수강신청. STRING 고정값이며 표시용 따옴표 없이 이 문자열을 그대로 보낸다. 2026-11-27 사용자 지시로 기존 미기재 유지 규정을 대체했다. SDK 반영·실수집 검증은 별도다.
- 플랫폼: WEB. 버튼 클릭 시 한 번 기록한다. 메인 배너·서비스 내부 강좌 신청은 이 계약과 구분한다.

2-22의 DA1·timetable 서비스 라벨·value는 아래/해당 원문의 과거 이력이다. SDK 배포·실제 수집·단일 전송 검수 완료나 과거 데이터 개명을 뜻하지 않는다. 준비 중인 허용 카탈로그·검수 목록의 후속 동기화는 별도 확인한다.

<b>카테고리 대표 위치 변경 · </b><b>2026-11-08</b>

사용자 요청으로 공용 카테고리 진입 명세를 홈화면 리디자인의 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>로 모았다. 현행 카테고리는 13개 메뉴로 정정했다: 기존 9개 계약의 문서 정리와 나머지 4개 WEB 모바일 계약 확정을 반영했다. 팀원 모집 동결 및 실제 SDK 적용·수집 검수는 별도다. 과거 회원가입 명세를 현행으로 포함한 오류를 철회하고, 해당 계정 원문은 기존 계정 문서에 보존한다. 홈에 통합한 것과 같은 클릭을 정의하는 서비스별 원문은 모두 중복 레거시로 보존한다. 주변상점·분실물·시간표·복덕방·팀원 모집 원문 5개와 기존 대응 문서 2개도 포함한다. 현행 구현 기준은 홈 3-6이며 원문·사진은 삭제하지 않는다. 새 로깅 계약을 폐기하지 않으며 아래 이전의 외부 대표 위치·이관 권고는 이 결정으로 대체한다. SDK 라벨·값·기존 플랫폼 범위와 팀원 모집 동결은 유지한다. 문서 이관만 완료됐으며 실제 Stage 화면·SDK 전송 검수는 각각 확인해야 한다.

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
| <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a> | <a href="https://app.notion.com/p/4660221954bc82939cd001cf9a20ba4c">[레거시] 1-0-2 학교 부서정보 접근 (카테고리 진입)</a> |

레거시의 라벨·값·사진은 과거 로깅에 보존한다. 메인 식단의 전체보기와 카드 본문은 위 통합 계약을 사용한다. 아래 원문 이력의 두 라벨 분리 규정은 과거 기준이며 현재 구현에 적용하지 않는다. SDK 반영·배포·실수집 검수는 별도다.

<b>전체 점검 후 문서 정리 · </b><b>2026-11-04</b>

- 동아리 전체는 사용자 지시로 레거시 보존한다. <a href="https://app.notion.com/p/98b0221954bc83189d2381251fba5a58">Notion 원문</a>의 기존 명세 55개·빈 행 2개를 보존하며 새 라벨·DA 담당을 만들지 않는다.
- 새 로깅의 고정 한글 value는 표시용 따옴표 없이 작성한다. 실제 고정값·동적 변수·후보·예시·전송 조건은 유지한다. 계정의 누락된 설명은 기존 조건을 요약해 보완했다.
- 화면 목록은 현행 70종이며 found\_item\_edit은 분실물 11-30의 실제 명세 사용값이다.
- 상점 체크박스/퀵필터의 플랫폼 범위, 리뷰 이탈과 버튼 클릭의 동시 전송, 콜밴팟 click/swipe 분기는 구현 확인 대기다. 문서 정리로 이벤트를 병합하거나 SDK 검증 완료로 표시하지 않는다.

<b>홈 중복 정리 · 최신 적용 기준 (</b><b>2026-11-04</b><b>)</b>

- 시설물·채팅 카테고리 진입의 대표는 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>이다. 개별 <a href="https://app.notion.com/p/3820221954bc82f9a58781fbc1b57a12">[레거시] 10-3. 카테고리_교내 시설물 정보_클릭</a>·<a href="https://app.notion.com/p/1d20221954bc827d923581192263ebbf">[레거시] 11-15.카테고리_채팅(쪽지)_클릭</a>은 레거시 이력으로 보존한다. 같은 클릭에 두 문서의 라벨을 모두 전송하지 않는다.
- 식단 더보기 대표는 <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a>의 <code>main__main__meal__click</code>이다. <a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a>·<a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a>은 이관 전 이력이다. 품절 제보·품절 알림은 적용 대상이 아니다.
- 새 이벤트·새 라벨을 생성하지 않았으며 실제 SDK 반영·한 번 전송은 개발 검증 대상이다. 학교 부서의 별개 유지 계약은 유지한다.

### 네이밍룰 v1.0 확정 (2026-10-28)

공통 규칙은 <a href="https://app.notion.com/p/4000221954bc81469ea6dbe19c7d8be7">로깅 네이밍룰 v1.0 — DA1·DA2 공통 확정본</a> 확정본을 따른다. 일반 label은 service\_\_page\_\_feature\[\_\_detail\]\_\_category이며 기존 승인 category와 발생 조건은 보존한다. 개별 계약 미결과 SDK/dbt·실제 전송 검증은 별도다. 품절 동결 5페이지와 팀원 모집은 변경 제외다.

screen\_view는 event\_label을 <code>__</code>로 나눈 두 번째 구간과 같은 고정 문자열로 작성한다. 헤더는 <code>header</code>, 푸터는 <code>footer</code>다. 2026-10-30 상민 직접 지시로 확정했으며, 이전 동적 화면명 표기안은 이 결정으로 대체한다. SDK 적용·실제 전송은 별도 검증이다.

### 실제 반영 기록 (2026-10-28)

- 사용자 확인한 방식 A: 기존 승인 category 보존, label 끝과 일치. DA2 category 10페이지 및 label 11개를 정렬했으며 계정 5건의 confirm\_\_click은 유지한다.
- 홈 버튼/카드의 main과 메뉴의 main\_category를 구분한다. bus\_entry/main\_entry, shop\_entry/category\_card\_entry는 main에서 발생한다.
- 회원가입 완료 value는 기존 회원가입완료를 유지하며 근거 없는 실패 value를 추가하지 않는다.
- 공용 사전의 현행 표와 과거 표현을 분리한다. 팀원 모집과 품절 관련 동결 5페이지는 변경 제외다.
- 실제 호출 지점·전송 시점·한 번 전송·SDK/dbt 배포는 문서 정리와 별도이며 미확인 항목을 완료로 처리하지 않는다. 당시 보류했던 메뉴 회원가입 진입은 2026-11-01 후속 사용자 승인으로 로그인 화면 진입과 문서상 구분했다. 시간표 과목 목록의 한 번 클릭 미리 보기·더블클릭 추가는 후속 코드 확인에 기록했다. 실제 플랫폼별 호출·SDK 전송·배포 검증은 계속 미확인이다.
- category 이름 정리는 검색어·입력 원문 수집 정책이나 기존 value 변경 승인이 아니다.

<b>화면 확인 → 명세 작성 → 사진 정리 → 문서 검수 → 개발·수집 검수</b>

2026-10-27 현행: DA1 7개 서비스의 공용 기능명·화면명을 정렬하고 기능 사전 등록을 완료했다. 아래의 네 구간 고정·단일 담당자 예시는 최신 문법과 담당자 규칙으로 갱신했다. SDK·dbt 반영과 실제 수집 검수는 개발 후속이다.

<details>
<summary>적용 범위·플랫폼 예외</summary>

- 담당자별 event\_name 유지: DA1은 주변상점·식단·버스·복덕방·사장님·팀원 모집·시간표, DA2는 계정·로그인·게시판·배너·분실물·콜밴팟·쪽지·채팅·모의수강신청·학교 부서·교내 시설물·홈화면 리디자인의 새 명세다. 홈화면은 사용자 승인(2026-11-01)으로 추가했으며 기존 CAMPUS 원문은 보존한다. 기능 사전과 label 문법은 공통으로 사용한다. 홈 3-6의 카테고리 13개 계약에도 같은 서비스별 event\_name 배정표를 적용하며 feature=category\_navigation은 유지한다.
- mobile은 ANDROID·IOS 공통 디자인이며 DB 속성에 두 값을 지정한다. 실제 검수 출처는 Android다. WEB은 리디자인 전 데스크톱 화면을 기준으로 한다.
- 카테고리·콜밴팟에는 WEB을 적용하지 않는다. ‘햄버거’는 현행 명세에서 ‘카테고리’로 쓴다. 모의수강신청은 WEB만 적용하며 시간표 진입 클릭은 <code>timetable</code>, 서비스 내부는 <code>course_practice</code>다.
- 졸학계는 레거시로 제외하고 과거 명세·사진을 보존한다. 대상 외 서비스에 DA2 규칙을 확대 적용하지 않는다.
- 서비스 배정표 (이 표를 단일 출처로 참조):
  | 기존 event\_name | 서비스 | 수 | 담당 확인 상태 |
  | --- | --- | --- | --- |
  | <code>DA1</code> | 주변상점, 식단, 버스, 복덕방, 사장님, 팀원 모집, 시간표 | 7 | 주변상점·식단·버스는 담당 미확인. 나머지는 기존 배정 원문 유지. |
  | <code>DA2</code> | 계정·로그인, 게시판, 배너, 분실물, 콜밴팟, 쪽지·채팅, 모의수강신청, 학교 부서 정보, 교내 시설물, 홈화면 리디자인 | 10 | 홈 service=main의 새 명세는 이관 경로와 관계없이 DA2다. 이관 전 DA1 값은 과거 로깅에 보존한다. 기존 CAMPUS 원문 보존. 실명 담당 승인과 구분한다. |
  | 미지정 | 새 주변상점, 미래의 주변상점, 동아리, 졸업학점 계산기 | 4 | 담당 미확인. 임의 배정하지 않는다. |
- 위 표의 DA1/DA2는 기존 event\_name 보존 기준이며 실명 담당 확정 표시가 아니다. 품절 동결 5페이지·팀원 모집·새 주변상점·미래의 주변상점은 이번 수정에서 제외한다.

</details>

## 1. 발생 화면과 시점을 확인한다

- <a href="https://app.notion.com/p/0e40221954bc823d92c301f83b5f68d0">화면 정의 및 로깅 검수</a>에서 고정 화면명을 찾고, 선택·확인·제출 중 <b>어느 순간 전송하는지</b> 먼저 정한다.
- <code>screen_view</code>는 <code>event_label.split("__")[1]</code>과 같은 고정 문자열로 작성한다. 이동·모달·팝업도 해당 라벨의 두 번째 구간을 그대로 사용한다. 공용 헤더는 <code>header</code>, 푸터는 <code>footer</code>이며 임의의 현재 화면명으로 바꾸지 않는다. 동결 명세는 변경 제외다.
- 기존 실제 캡처를 먼저 대조한다. 실제 접근이 어려우면 기존 Figma를 쓰고, 없으면 해당 플랫폼 프레임을 찾는다. <code>Figma 참고 / 실제 화면 미확인</code>과 프레임 링크를 남긴다. 이름이 정의되지 않았으면 Notion에 검토중으로 표시하고 후보·근거는 로컬 검토 문서에 기록한다.

## 2. 같은 기능은 같은 이름으로 작성한다

<code>{service}__{page}__{feature}[__{detail}]__{category}</code> 

- 4\~5구간이며 마지막 구간은 해당 event\_category 값이다. detail은 선택이며 최대 한 구간이다. 구간은 <code>__</code>, 구간 안 단어는 <code>_</code>로 나누고 <code>lower_snake_case</code>를 쓴다. 기능·행동은 <a href="https://app.notion.com/p/38b0221954bc831b912c012d8af2c857">event_label 기능·행동 네이밍 사전</a>에서 재사용한다.
- label만 보고 기능과 행동을 이해할 수 있게 쓴다. 기능만으로 충분하면 마지막에 승인된 category를 넣어도 된다. 검색어·품목·ID 등 동적 값은 label에 넣지 않는다.

| 필드 | 작성 기준 |
| --- | --- |
| <code>event_name</code> | 라벨 첫 구간 service별로 DA1 또는 DA2 하나를 사용한다. DA1: shop·cafeteria·bus·ticket·real\_estate·owner·team\_recruit·timetable. DA2: account·board·banner·callvan·chat·course\_practice·department·facility·main. |
| <code>event_label</code> | 예: <code>board__lost_item_list__filter__apply__click</code>. 일반 페이지 구간은 <code>screen_view</code>와 동일. 헤더·푸터도 label page와 screen\_view를 각각 <code>header</code> / <code>footer</code> 고정값으로 일치시킨다. |
| <code>event_category</code> | 기존 승인값 유지. 이름을 바꾼다는 이유로 행동 종류·전송 시점을 바꾸지 않는다. |
| <code>value</code>·추가 파라미터 | 고정값·동적 매핑·타입·기본값·예시를 명시한다. 콜밴팟 메시지 본문은 수집하지 않고 전송 행동만 기록한다. |

<details>
<summary>개별 명세 작성 양식</summary>

이전 로깅은 원문 토글로 보존하고 새 로깅을 작성한다. 플랫폼은 DB 속성에서 관리한다.

```txt
설명 / 정확한 발생 시점:
screen_view:
event_name: DA1 또는 DA2 (서비스 담당자 기준)
event_label: service__page__feature[__detail]__category
event_category:
value / 추가 파라미터(해당 시):
참고사진: WEB·mobile을 구분한 닫힌 토글
검토사항: 필요한 메모와 통합 가이드 링크를 토글 하나에 정리
```

본문에 적용 플랫폼·범위·작성일·화면명 근거를 반복하지 않는다.

</details>

<details>
<summary>현재 확정된 서비스별 결정</summary>

- 콜밴팟: 2-4·2-5는 예/아니오 응답, 3-1·3-2는 선택하기, 3-3은 확인 클릭 순간 전송한다. 2-7은 메시지 본문을 수집하지 않고 고정 STRING value 메시지 전송을 보내는 행동 로그로 정한다. 2026-11-27 사용자 지시로 종전 빈 value 유지 규정을 대체했다. 나머지 발생 조건·플랫폼은 유지한다.
- 분실물: 11-4·11-11은 작성완료 클릭 순간 전송하며 별도 성공 이벤트는 추가하지 않는다. 11-27 열기·11-28 확인은 분리, 11-29·11-30 수정은 적용 대상이다.
- 분실물 필터는 <a href="https://app.notion.com/p/37b0221954bc8395897801f58e65d2a6">11-23. 분실물_필터_적용_클릭</a> 적용하기 한 번으로 통합한다. 11-18은 이력만 보존하고 별도 전송하지 않는다. 기존 value ‘분실물’과 <code>filter_scope</code> / <code>filter_post_type</code> / <code>filter_item_type</code> / <code>filter_status</code> 네 STRING 값을 보낸다. 매번 네 키를 모두 보내며 기본값은 ‘전체’, 복수 선택은 중복 제거·UI 정의 순서로 <code>|</code> 연결한다.
- 품목 11-2·11-9는 실제 선택값, 키워드 12-2는 추가 클릭 시 입력값(category=submit), 12-3은 클릭한 추천값을 동적 매핑한다. 12-4는 조작 후 받기/끄기를 value로 구분한다.
- 학교 부서 검색은 아이콘·Enter 실행 시 검색어를 기록한다. 1-0-2와 공용 3-6은 별개 유지하며 상호 링크로 구분한다. 내부 부서 분류 1-1과 합치지 않는다.
- 사진: 학교 부서 Android 검색 결과·복사 확인 완료, 콜밴팟 3-2·2-4·2-5 실제 사진 교체 완료는 사용자 확인으로 기록한다. 콜밴팟 참여자·채팅·신고 4개 화면과 2-7·2-10 사진은 기존 Figma 사용 확정이며 실제 캡처 대기 조건이 아니다. 이전 사진 대조 기록은 원문에 보존한다.

</details>

## 3. 사진을 해당 로깅 아래에 붙인다

- 현재 첨부 사진과 보유 실제 캡처를 먼저 확인한다. 기능이 보이는 상태를 골라 WEB·mobile별 닫힌 토글에 넣고, 모달·필터 사진은 별도 화면 정의가 아닌 동작 설명에 사용한다.
- 원본 복사본에 <b>코드로 빨간 네모만</b> 표시한다. 문구·배치·상태·해상도와 테두리 밖 픽셀을 유지한다. 실제 캡처·사용자 제공·Figma·선명도 개선본의 출처를 구분한다.

## 4. 저장한 명세를 다시 검수한다

- [ ] screen\_view가 event\_label의 두 번째 구간과 같은 고정 문자열이고, label 4\~5구간·category 접미·사전 용어·승인 전송 시점이 맞다. 헤더·푸터도 같은 기준을 적용하며 동결 예외는 변경하지 않는다.
- [ ] category·value·파라미터와 통합/별개 유지가 최신 결정에 맞고, 플랫폼 DB 속성이 맞다.
- [ ] 이전 원문·사용자 수정·사진이 보존됐고, 사진의 대상·출처·링크·토글 위치를 확인했다.
- [ ] 이전→새 label 대응과 변경 이유를 남겼다. 문서 완료와 실제 수집 완료를 구분했다.

<details>
<summary>막힐 때 확인할 것</summary>

- 화면이 안 열리면 로그인·권한·데이터·현재 경로를 확인한다. 한 번의 로딩·접근 실패를 기능 삭제로 단정하지 않는다. Figma 사용 확정과 실기기 확인 완료는 구분한다.
- 사진이 흐리면 큰 원본·실제 파일 형식·해상도를 확인한다. 커서·클릭 표시를 제거하고 UI를 추정해 고치지 않는다.
- Notion 교체가 실패하면 최신 본문을 다시 읽고 고유한 작은 텍스트 범위로 수정한다. 공유 화면 정의 전체를 덮어쓰거나 같은 정리본을 중복 추가하지 않는다.
- 같은 native 이미지 참조는 블록을 이동시킬 수 있다. 복제는 별도 사본을 업로드하고 원본·사진 수를 재확인한다. 비동기 접수·시간 초과는 저장 완료가 아니므로 결과를 다시 읽는다.

</details>

## 동일 이벤트 계약표 · 기준 명세

기존 7개 계약과 사용자 결정 반영 3개 계약을 합쳐 현재 10개 계약을 아래에 등록한다. 이 표를 공용 사전의 요약 목록과 함께 사용할 때 본 표를 단일 기준으로 삼는다. 문서 중복 허용은 이벤트 추가 전송·원문 value 변경·SDK 검증 완료를 뜻하지 않는다. 플랫폼별 원문 조건을 유지하고 실제 한 번 전송은 별도 검증한다. 미확정 후보는 아래 표에 자동 편입하지 않는다.

| label | 기준 명세 | 대응 명세 | 등록 근거 |
| --- | --- | --- | --- |
| <code>timetable__main_category__timetable_entry__category_entry__click</code> | <a href="https://app.notion.com/p/e9d0221954bc828aa337812594729789">[레거시·중복 원문] 2-21. (앱, 반응형 웹) 카테고리_시간표 진입 (클릭) - 추가된 로깅</a> | <a href="https://app.notion.com/p/6360221954bc837f98d98135eefbf8bc">[레거시·이관 원문] 2-5. (앱, 반응형 웹) 햄버거_시간표</a> | 기존 양쪽 검토사항의 기준 명세 지정. 값·화면·category 일치, 플랫폼별 경로는 원문 유지. |
| <code>real_estate__main_category__real_estate_entry__category_entry__click</code> | <a href="https://app.notion.com/p/9890221954bc820ba81a81e6725d617b">Notion 원문</a> | <a href="https://app.notion.com/p/2640221954bc83d6a82901c92388b825">[레거시] 1-3 햄버거_복덕방 진입 (클릭)</a> | 기존 양쪽 검토사항의 기준 명세 지정. 값·화면·category 일치, 플랫폼별 경로는 원문 유지. |

### 추가 대조한 동일 계약 (5개)

최초 등록은 위 2개와 아래 5개로 총 7개였으며, 현재 총수는 후속 등록 3개를 포함한 10개다. 이 구분은 문서 등록 순서이며 승인 범위나 이벤트 전송 횟수를 늘리지 않는다.

| label | 기준 명세 | 대응 명세 | 등록 근거 |
| --- | --- | --- | --- |
| <code>shop__shop_detail__contact__phone__click</code> | <a href="https://app.notion.com/p/2d50221954bc834f8ca9019292dd4741">3-2 상점상세 전화 (클릭)</a> | <a href="https://app.notion.com/p/3d50221954bc824e9a1e81e83e042833">4-5 전화 주문 혜택 상점상세 전화 (클릭)</a> | 양쪽 검토사항의 기존 기준 명세 지정 및 값·화면·category·응답 동작 일치. 원래 플랫폼·진입 경로는 유지한다. |
| <code>account__shop_detail__login_popup__close__click</code> | <a href="https://app.notion.com/p/40c0221954bc830a8ea4015f95cf4e1f">3-23 상점상세 리뷰작성 _로그인_취소 (클릭)</a> | <a href="https://app.notion.com/p/fc90221954bc82cb9b1f01c7863d50e9">3-25 상점상세 리뷰신고 _취소누름 (비로그인)</a> | 양쪽 검토사항의 기존 기준 명세 지정 및 값·화면·category·응답 동작 일치. 원래 플랫폼·진입 경로는 유지한다. |
| <code>account__shop_detail__login_popup__login_entry__click</code> | <a href="https://app.notion.com/p/bf00221954bc8246a5ae8154ce1bcf97">3-22 상점상세 리뷰작성 들어가기_로그인누름 (비로그인)</a> | <a href="https://app.notion.com/p/c150221954bc8307920f81f1cddd95b1">3-24 상점상세 리뷰신고 _로그인 (비로그인)</a> | 양쪽 검토사항의 기존 기준 명세 지정 및 값·화면·category·응답 동작 일치. 원래 플랫폼·진입 경로는 유지한다. |
| <code>cafeteria__main__more__click</code> (이관 전 계약) | <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> | <a href="https://app.notion.com/p/0800221954bc82e0a583014cc59206f3">[레거시] 메인_식단_더보기버튼_클릭(확인필요)</a> | 이관 전 계약 이력이다. 현행 홈 기준은 <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a>의 <code>main__main__meal__click</code>이다. 0800 대응 명세도 2026-11-04 사용자 요청에 따라 레거시·참조로 표시하고 현행 홈 1-3으로 연결했다. 새 라벨과의 SDK 전환은 미확인이다. 품절 제보와 별개다. |
| <code>timetable__timetable__semester_manage__edit_apply__click</code> | <a href="https://app.notion.com/p/6550221954bc8398829381a30fe9607f">2-13. (웹, 반응형 앱) 시간표_학기 추가 (클릭)</a> | <a href="https://app.notion.com/p/0e70221954bc833a8487016d106b50ce">2-14. (웹, 반응형 앱) 시간표_학기 삭제_확정 (클릭)</a> | 웹·모바일 학기 편집 확정·적용 공통 계약. 2-13이 대표이며 2-14는 삭제 경로 설명이다. 실제 클릭 1회에 1개만 전송한다. SDK 발화는 미확인이다. |

### 사용자 결정 반영 · 추가 동일 계약 3개 (2026-11-01)

기존 7개와 아래 3개를 합쳐 현재 등록 계약은 10개다. 문서 계약 정렬이며 실제 호출 지점·SDK 전송·한 번 전송은 미확인이다.

| label | 기준 명세 | 대응 명세 | 등록 근거 |
| --- | --- | --- | --- |
| <code>account__main_profile__login__entry__click</code> | <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> | <a href="https://app.notion.com/p/2660221954bc82719b1b01589fd83c1b">4-2 로그인 클릭</a> | 프로필 로그인 화면 진입 클릭. 사용자 승인으로 value 로그인 통일. 로그인 성공 이벤트가 아니다. 문서 수만큼 중복 전송하지 않는다. |
| <code>account__main_profile__logout__click</code> | <a href="https://app.notion.com/p/1ef0221954bc83b5b92a011a45d5a60a">[레거시] 4-2 로그아웃(클릭)</a> | <a href="https://app.notion.com/p/6d90221954bc83a8839d01823f621620">4-3 로그아웃 클릭</a> | 프로필 로그아웃 버튼 클릭. label·화면·value 로그아웃·category click 일치. 문서 수만큼 중복 전송하지 않는다. |
| <code>callvan__main__callvan_entry__recruitment_list_entry__click</code> | <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> | <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> | 메인 교통 영역 모집 보기 클릭. 기존 상호 대응 근거와 사용자 승인으로 value 콜밴팟 모집보기 통일. 문서 수만큼 중복 전송하지 않는다. |

회원가입 진입 두 명세는 동일 계약으로 등록하지 않는다. <a href="https://app.notion.com/p/0820221954bc834eb41301752196a7d5">1-2 회원가입진입(클릭)</a>는 <code>account__main_category__sign_up__menu_entry__click</code> / <code>main_category</code>, <a href="https://app.notion.com/p/a1e0221954bc82ebbe390176073d8e18">1-3 로그인 화면_회원가입진입(클릭)</a>는 <code>account__login__sign_up__entry__click</code> / <code>login</code>으로 문서상 진입점을 구분했다. 실제 플랫폼별 호출 및 SDK 반영은 미확인이다.

## 문서 정합성 보정 결과 (2026-10-28)

| 분류 | 처리 결과 |
| --- | --- |
| 일치 | 최초 동일 이벤트 계약 7개를 대조해 등록했으며, 후속 사용자 결정을 반영한 현재 총수는 10개다. 라벨·category·value·플랫폼·발생 조건은 보존한다. |
| 문서 보정 이력 | 과거 헤더·푸터 25개 명세를 동적 화면명 표기로 바꾼 기록이 있으나 2026-10-30 상민 직접 지시로 해당 방식을 대체한다. 현재 screen\_view는 label 두 번째 구간과 같은 고정값이다. 이전 로깅·사진·사본 원문은 보존하며 SDK 적용 완료를 뜻하지 않는다. |
| 개발 확인 필요 | 프로필 로그인 value 로그인, 콜밴팟 모집 보기 value 콜밴팟 모집보기는 사용자 승인으로 문서상 확정했다. 로그인·로그아웃·콜밴팟의 동일 계약은 등록했고 회원가입 두 진입점은 분리했다. 실제 호출 지점·전송값·한 번 전송 및 시간표 모바일 삭제 동작은 미확인이다. |
| 변경 제외 | 품절 제보 및 관련 동결 로깅과 팀원 모집은 수정하지 않았다. 이 기록으로 예외 label·value·발생 조건을 변경하거나 공통 규칙으로 강제 변환하지 않는다. |

프로필 로그인 문서 정렬 완료·구현 검증 대기 명세: <a href="https://app.notion.com/p/5970221954bc835f9d88813176fcbe30">[레거시] 2-2 로그인 진입(클릭)</a> · <a href="https://app.notion.com/p/2660221954bc82719b1b01589fd83c1b">4-2 로그인 클릭</a>.

### DA1 명세 형식 재점검 (2026-10-28)

- 범위: 주변상점·식단·버스·복덕방·사장님·시간표의 목록 181개 중 품절·삭제 대상·기존 레거시·빈 제목 등을 제외해 160개 페이지를 읽었다. 읽은 페이지 중 추가로 확인한 레거시 안내 12개와 이미 삭제된 빈 페이지 2개는 보존·제외했다. 팀원 모집 및 품절 제보·관련 동결 로깅은 변경하지 않았다.
- 현행 142개 명세는 event\_name=DA1, 일반 label 4\~5구간, 승인 category 접미, 공용 사전 등록 feature를 확인했다. 버스 헤더·푸터의 승인된 목적지형 4개는 예외 그대로다. 이 검사는 문서 형식·사전 정합성 확인이며 실제 SDK 발화·value 정책·성공 시점·중복 전송 검증 완료를 뜻하지 않는다.
- 나머지 과거 메뉴 추가 사본 4개는 DA2 작성 양식인 이전 로깅 / 새 로깅 / 검토사항으로 정리했다. 기준 사장님 명세와 과거 label·value·category가 일치함을 대조했고, 현행 필드는 기준 명세를 참조하도록 했다. 별도 이벤트·중복 계약을 새로 만들지 않았다.
- 사본과 기준: <a href="https://app.notion.com/p/80b0221954bc831d9577810ad1a866ec">3-1 메뉴추가</a> → <a href="https://app.notion.com/p/ec90221954bc82cca0ae019240970afa">3-1 메뉴추가</a>; <a href="https://app.notion.com/p/61a0221954bc8226b26e81305d73855a">3-2 메뉴추가 - 확인</a> → <a href="https://app.notion.com/p/d440221954bc83828408017e07d87ceb">3-2 메뉴추가 - 확인</a>; <a href="https://app.notion.com/p/b890221954bc826eaab28143d98b4378">3-3 메뉴추가 - 취소</a> → <a href="https://app.notion.com/p/5030221954bc82f095f0817d9324b9d0">3-3 메뉴추가 - 취소</a>; <a href="https://app.notion.com/p/7690221954bc8218a3c5811f80dc7718">3-4 메뉴추가 - 메뉴사진</a> → <a href="https://app.notion.com/p/9420221954bc83c2b32d813e10ec3f75">3-4 메뉴추가 - 메뉴사진</a>.
- event\_name을 DA2로 바꾸지 않았고 기존 category·value·발생 조건은 유지했다. 원문과 메뉴 취소의 과거 콘솔 오류 기록도 이전 로깅 토글에 보존했다. 이미 통합된 식단 점심·저녁 페이지는 삭제 상태를 유지하고 복원하거나 새 이벤트를 만들지 않았다.

### 네이밍 후속 점검 (2026-10-29)

- 기존 현행 목록 271페이지의 label 280건(DA1 145·DA2 135)을 다시 읽어 문법·승인 category 접미·현행 사전 조합을 대조했다. 품절 동결 5페이지·팀원 모집·새 주변상점·미래의 주변상점은 조회·수정 범위에서 제외했다. 새 페이지 발견까지 포함하는 전체 워크스페이스 전수 감사는 아니다.
- 과거 헤더 로그아웃의 동적 화면명 표기 정렬 기록은 2026-10-30 상민 직접 지시로 대체한다. 현재 screen\_view는 label 두 번째 구간과 같은 <code>header</code> 고정값이다. <a href="https://app.notion.com/p/d8b0221954bc83eb94650156db128382">4-1 로그아웃(클릭)</a>의 logout은 진입 이벤트가 아니므로 기존 4구간 label을 유지한다. SDK가 동일한 header 고정값을 전송하는지와 실제 수집 검증은 별도 미확인이다.
- 사전 보충표의 <code>cart</code>·<code>feedback</code> 표기는 현행 본표와 같은 <code>shop_cart</code>·<code>bus_feedback</code>으로 정렬하고 detail/category 설명을 구분했다. 공통 템플릿은 들여쓰기 없는 native toggle 문법으로 정리했다.
- 당시 같은 label 11묶음 중 7묶음 등록·4묶음 보류였다. 후속 사용자 결정으로 회원가입 진입은 문서상 분리하고 프로필 로그인·로그아웃·콜밴팟 3묶음을 추가 등록해 현재 동일 계약은 10묶음이다. 사용자 승인된 프로필 로그인·콜밴팟 새 value 외 category·event\_name·사진·이전 로깅은 유지한다. 실제 SDK 호출·전송은 미확인이다.

### A/B 제외 후속 확인 (2026-11-01)

- 사용자 지시에 따라 품절 제보 버튼 A/B 테스트는 후속 분석·수정·검증 대상에서 제외한다. 관련 동결 페이지, 팀원 모집, 새 주변상점·미래의 주변상점은 수정하지 않는다. 아래는 공개 코드와 10/25\~31의 비 A/B 이벤트만 대조한 결과다.
- 시간표 2-18: [웹 코드](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/a1bd96d8b0b426e8c6a4b54ea643e7a7e2a7bd23/src/components/TimetablePage/components/LectureList/index.tsx#L109-L120)상 단일 클릭은 미리 보기 선택, 더블클릭은 추가다. <code>lecture_entry</code>를 유지한다. 문서 의미 확인과 운영 SDK 발화 확인을 구분한다.
- 프로필 로그인·로그아웃: [Android](https://github.com/BCSDLab/KOIN_ANDROID/blob/ee67a50f554030a76cfb7d8948b89d8efc806e9d/feature/profile/src/main/java/in/koreatech/koin/feature/profile/ProfileScreen.kt#L74-L81)·[iOS](https://github.com/BCSDLab/KOIN_iOS/blob/ea494b30ffa6197d62592369f7ae4265ced2e678/Koin/Presentation/Home/Profile/ProfileView.swift#L45-L53)에서 value 로그인/로그아웃과 클릭 시점은 문서와 맞는다. 확인 커밋은 구라벨 home\_login/home\_logout 및 CAMPUS를 사용한다. [iOS 콜밴팟](https://github.com/BCSDLab/KOIN_iOS/blob/ea494b30ffa6197d62592369f7ae4265ced2e678/Koin/Presentation/Home/Home/HomeView.swift#L65-L74)도 callvanpot/CAMPUS·value 콜밴팟 모집보기를 사용한다. 새 명세는 DA2이며 코드 마이그레이션·배포 확인이 필요하다.
- raw GA4 10/25\~31: home\_login 25건, home\_logout 1건, callvanpot 137건. 위 3개 새 label과 시간표 2-18 새 label은 해당 기간 0건이며 조회한 이벤트의 screen\_view 파라미터는 NULL이다. 자동 화면 이벤트·다른 필드의 부재나 현재 배포 미완료를 단정하지 않는다. 이 기간은 이번 문서 결정 전이다.
- [웹 전송 래퍼](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/a1bd96d8b0b426e8c6a4b54ea643e7a7e2a7bd23/src/lib/gtag.ts#L50-L77)는 event\_name 또는 기존 team을 전송하지만 확인한 명시적 파라미터 목록에 screen\_view가 없다. 공통 로거 경로별 고정 화면명·필터 파라미터 전달 검증이 필요하며 다른 SDK 경로까지 부재라고 단정하지 않는다.
- 공개 소스 커밋과 로컬 폴더만 확인했다. 로컬 dbt 모델 폴더에는 모델 SQL이 없어 운영 dbt 수정·배포는 하지 않았다. 실제 단일 동작당 전송 횟수는 실기기·네트워크 검증 전 미확인이다.

### 콜밴팟 카테고리 참조 정리 (2026-11-01 사용자 결정)

- 현행은 홈 3-6 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 기존 카테고리 콜밴팟 클릭이다. 기존 <code>callvan__main_category__category_navigation__callvan_entry__click</code>과 원문 value·발생 조건·플랫폼을 유지한다.
- 콜밴팟 1-3 <a href="https://app.notion.com/p/80c0221954bc8396a38f01b1df7cbcd8">[레거시] 1-3 카테고리 → 콜밴팟 모집</a>은 삭제하지 않고 레거시 이력으로 보존한다. 이 페이지의 과거 라벨·value·사진은 현행 구현 계약으로 재사용하거나 추가 전송하지 않는다.
- 새 로깅·라벨·이벤트는 만들지 않는다. 두 라벨을 하나로 바꾸거나 새 동일 이벤트 계약을 등록하지 않는다. 이 카테고리 판단 대기는 문서상 해소했으며 실제 SDK의 기존 호출 정리·한 번 전송·배포 여부는 미확인이다.
- 메인 교통 영역의 모집 보기(홈 1-6 / 콜밴팟 1-1) 동일 계약과는 별개다. 학교 부서의 공용 카테고리/서비스 진입 별개 유지 결정 및 홈 3-6의 나머지 세 동작은 유지한다.

## 5. 개발 반영 후 남은 4개를 검수한다

| 후속 | 할 일·관련 명세 |
| --- | --- |
| 필터 파라미터 구현 | 네 키의 SDK 전송 → dbt 추출 → 마트 열 반영과 기본값·복수 선택을 구현한다. <a href="https://app.notion.com/p/37b0221954bc8395897801f58e65d2a6">11-23. 분실물_필터_적용_클릭</a> |
| 과거 이탈 label 확인 | 이전 명세의 ‘ㅊ’ 표기를 실제 과거 수집값과 대조한다. 현행 이탈 label·click/swipe 구분은 유지한다. <a href="https://app.notion.com/p/aa90221954bc824ea10201256afedfb7">2-11 콜밴팟 찾기 이탈</a> |
| 구현 지점·중복 확인 | 메인 모집 보기/목록 모집하기 대응 명세를 함께 보고 이중 전송을 방지한다. 카테고리 콜밴팟은 홈 3-6 현행·1-3 레거시 결정에 맞춰 기존 호출을 대조한다. 별개 유지한 학교 부서 등 다른 카테고리 계약은 유지한다. <a href="https://app.notion.com/p/c020221954bc83d1b3620157ff90d195">[레거시] 1-1 메인 → 콜밴팟 모집 보기</a> · <a href="https://app.notion.com/p/b730221954bc8386a73801d4e898ddd8">Notion 원문</a> · <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a> |
| 배포 후 수집 검수 | 플랫폼·버전·적용일·이전→새 label을 기록하고 실제 시점·값·화면명·중복·누락을 검수한다. |

### 개발 적용·운영 수집 점검 (2026-10-30)

<code>kap-chat.mart.vw_mart_integrated_logs</code>를 읽기 전용으로 조회했다. 조회 조건은 2026-10-16부터 2026-10-30까지이며 실제 최신 event\_dt는 2026-10-29다. 30일 행은 0건이므로 30일 이후 배포 여부를 판단하지 않는다. 아래 건수는 마트 행 수이며 사용자 행동 수·SDK 한 번 전송 검증 결과가 아니다.

| 플랫폼 | DA1 행 수 | 이중 밑줄 label 행 수 | 확인 |
| --- | --- | --- | --- |
| ANDROID | 1,391 | 1,391 | 모두 품절·실험 동결 label |
| IOS | 1,659 | 732 | 동결 label 732행, 과거 식단 label 927행 |
| WEB | 713 | 713 | 모두 품절·실험 동결 label |

- DA2는 위 조회 범위에서 관측되지 않았다. event\_name 제한 없이 이중 밑줄 label도 대조했으며 관측된 고유 label 6개는 모두 기존 품절·실험 동결 목록에 속한다. 일반 새 명세의 SDK 적용·배포 완료 근거로 사용하지 않는다.
- 동결 label 2,836행의 service\_name은 ANDROID·IOS에서 unmapped(2,123행), WEB에서 main(713행)이다. 기존 분석 분류의 입력 의존 사항으로 기록하며 명세·동결 label을 고치거나 Gold에서 임의 보정하지 않는다.
- 이 뷰에는 screen\_view 및 filter\_scope / filter\_post\_type / filter\_item\_type / filter\_status 열이 없다. 현재 뷰만으로 고정 화면명·필터 네 키의 실제 전송을 확인할 수 없으며 원본 파라미터와 추출 경로를 개발 담당자가 대조해야 한다. 열 부재가 SDK 미전송 증거는 아니다.
- 로컬 KOIN\_DATA 분류 코드는 과거 label·화면명 CASE를 사용하며 확인한 SQL에서 새 label 구간 해석 및 위 네 키 추출은 찾지 못했다. 로컬 코드와 실제 운영 코드의 동일성·배포 상태는 미확인이다. Silver·운영 분류 수정과 배포는 이 문서 작업에서 수행하지 않는다.
- 당시 중복 후보 4묶음(8페이지)의 후속 결정: 회원가입 메뉴/로그인 화면 진입은 문서상 구분했고, 프로필 로그인·로그아웃·콜밴팟은 문서 동일 계약으로 등록했다. 로그인 value는 로그인, 콜밴팟 value는 콜밴팟 모집보기로 사용자 승인 정렬했다. 실제 호출 위치·플랫폼·버전·단일 동작당 전송 횟수는 여전히 검증 대기다.
- 새 주변상점·미래의 주변상점은 사용자의 후속 제외 지시에 따라 사진 보완·네이밍·개발 전달 대상에서 제외한다. 품절 동결 5페이지와 팀원 모집 명세도 수정하지 않는다.
- 실제 데이터 확인은 <code>kap-chat.mart.vw_mart_integrated_logs</code>를 기준으로 한다. 과거 <code>service_name</code>이 main/unmapped일 수 있으므로 기존 label·category·value·플랫폼도 함께 대조한다. 명세 정리만으로 개발·수집 완료 처리하지 않는다.

<details>
<summary>원문 및 상세 이력 · 보존</summary>

세 문서의 통합 전 원문을 보존했다. 현재 기준·결정·후속은 위 본문에서 관리하고, 아래는 과거 근거와 상세 기록을 찾을 때 펼쳐 본다.

<a href="https://app.notion.com/p/e030221954bc82ce94b4019eff7ae041">원문 · 로깅 공통 기준 · 작성 및 검수 가이드 (2026-10-16 통합 전)</a>

<a href="https://app.notion.com/p/04c0221954bc82faa18e81c65496b083">로깅 결정·검토 현황</a>

<a href="https://app.notion.com/p/ce60221954bc837e9a9901c548aed988">로깅 작업 피드백 · 트러블슈팅</a>

- 이전 통합 전 자료·장기 개선안: <a href="https://app.notion.com/p/0950221954bc83caaf63810fd27cac92">로깅 문서 이력 · 개선안</a>

</details>

## 홈화면 리디자인 추가 정렬 (2026-11-01 사용자 요청)

- 최신 변경 (2026-11-04 사용자 지시): 아래 이관 표의 홈 7페이지가 현행 기준이며 이관 전 서비스별 7페이지는 레거시다. 이 7건만 라벨 첫 구간을 main으로 변경했다. 이관 원본의 DA1 6건·DA2 1건 및 value/category를 유지한다. 아래 2026-11-01의 ‘참조만’·‘DA2 작성’ 설명은 당시 작업 이력이다.
- 대상은 기존 Event Log <a href="https://app.notion.com/p/f820221954bc82cfbe7e813b975c5be1">Event Log</a>의 홈화면 리디자인이다. 별도 Event Log 사본은 수정하지 않는다.
- 홈 목록 26페이지를 읽었다. 기존 새 명세 5페이지·8라벨은 유지한다. 로깅 중단이 명시된 3-1\~3-5 5페이지는 유지한다. 기존 형식만 있던 나머지 16페이지 중 아래 중복·연관 7페이지는 참조만, 남은 9페이지·10동작은 새 형식으로 정리한다.
- event\_name 결정: 이번 새 명세는 사용자 확인으로 DA2를 사용한다. 기존 CAMPUS 지시·원문 label·value·category·사진·DB 플랫폼/상태는 보존한다. 실명 담당 배정이나 SDK 반영 완료를 뜻하지 않는다.

### 새 형식으로 정리한 기존 동작

| 명세 | 이전 label | 새 label |
| --- | --- | --- |
| <a href="https://app.notion.com/p/fe30221954bc82e7abe4012b1fb7bd60">1-1 알림 클릭</a> | <code>notification</code> | <code>main__main__notification_list__entry__click</code> |
| <a href="https://app.notion.com/p/0aa0221954bc8284a76a8157e539e7bd">1-2 알림 클릭 내부</a> | <code>notification_list</code> | <code>main__notification_list__notification_list__item_entry__click</code> |
| <a href="https://app.notion.com/p/7c80221954bc8271aa6a01ce2be6582f">1-2-1 알림 클릭 내부</a> | <code>notification_list_delete</code> | <code>main__notification_list__notification_list__delete__click</code> |
| <a href="https://app.notion.com/p/8190221954bc831e9f0301de872fec2b">1-2-2 알림 클릭 내부</a> | <code>notification_list_read_all</code> | <code>main__notification_list__notification_list__read_all__click</code> |
| <a href="https://app.notion.com/p/8190221954bc831e9f0301de872fec2b">1-2-2 알림 클릭 내부</a> | <code>notification_delete_all</code> | <code>main__notification_list__notification_list__delete_all__click</code> |
| <a href="https://app.notion.com/p/0f00221954bc820e8396811d7926b4f4">2-1 네비게이션 바 홈 클릭</a> | <code>nav_home</code> | <code>main__main__navigation__main_entry__click</code> |
| <a href="https://app.notion.com/p/3180221954bc833385e5816ab95b23df">2-2 네비게이션 바 카테고리 클릭</a> | <code>nav_category</code> | <code>main__main__navigation__category_menu_entry__click</code> |
| <a href="https://app.notion.com/p/0350221954bc82799691811138b0b988">2-4 네비게이션 바 프로필 클릭</a> | <code>nav_profile</code> | <code>main__main__navigation__profile_entry__click</code> |
| <a href="https://app.notion.com/p/aa90221954bc83daafec817ac462f0eb">1-10 많이 찾는 상점 둘러보기 클릭</a> | <code>popular_shop</code> | <code>shop__main__shop_entry__popular_entry__click</code> |
| <a href="https://app.notion.com/p/8420221954bc82b587bc81059510b0ca">4-1 내 시간표 클릭</a> | <code>home_timetable</code> | <code>timetable__main_profile__timetable_entry__entry__click</code> |

### 홈 기준 명세로 이관한 7건 (2026-11-04 사용자 결정)

| 현행 홈 기준 명세 | 이관 전 명세 (레거시) | 적용 |
| --- | --- | --- |
| <a href="https://app.notion.com/p/4730221954bc829a90e7818e5ed78bd7">1-3 메인 식단 진입 클릭</a> | <a href="https://app.notion.com/p/6c30221954bc830680a6014a17cd887d">1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서 1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)</a> | 현행 새 label: <code>main__main__meal__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/e4c0221954bc83949b49016cfff27ccf">1-4 식단 코너 클릭</a> | <a href="https://app.notion.com/p/6d40221954bc838e93c30176607ca0ce">1-3.메인_식단_A코너_클릭 (레거시)</a> | 현행 새 label: <code>main__main__corner__select</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/3440221954bc83e3aabd01e76233e781">1-5 서틀 탑승권 클릭</a> | <a href="https://app.notion.com/p/5da0221954bc8304abd601992586328c">1-11. 셔틀 탑승권_클릭 (레거시)</a> | 현행 새 label: <code>main__main__bus_entry__ticket_entry__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/2ca0221954bc8386a12f818e14a3d5af">1-7 버스 시간표 클릭</a> | <a href="https://app.notion.com/p/6650221954bc830c8d100196a52816c7">1-12. 버스 시간표_클릭 (레거시)</a> | 현행 새 label: <code>main__main__bus_entry__timetable_entry__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/1c50221954bc821f86e20145c98947fa">1-8 버스 노선 클릭</a> | <a href="https://app.notion.com/p/fae0221954bc83d49c12815edc4f6fde">1-13. 교통편 조회하기_클릭 (레거시)</a> | 현행 새 label: <code>main__main__bus_entry__search_entry__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/0320221954bc838ba30c816a7787861c">1-9 주변 상점 전체보기 클릭</a> | <a href="https://app.notion.com/p/88c0221954bc8280855881dd07f1c38d">1-1-1 메인 → 주변상점 (클릭) - (레거시)</a> | 현행 새 label: <code>main__main__shop_entry__main_entry__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |
| <a href="https://app.notion.com/p/ac20221954bc839c82b481e92e072a58">2-3 네비게이션 바 게시판 클릭</a> | <a href="https://app.notion.com/p/4f20221954bc83fe907e815ae495b98d">2-3. 공지사항_클릭 (레거시)</a> | 현행 새 label: <code>main__main__notice_entry__navigation_entry__click</code>. 새 본문·사진은 홈으로 이관했고 원본은 레거시로 보존한다. event\_name·value·category·screen\_view·발생 조건은 이관 원본대로 유지한다. |

- 위 7건은 사용자 지시(2026-11-04)에 따라 문서의 현행 기준 위치와 service\_name 첫 구간을 변경한 것이다. 이전 홈 원문의 value/category 차이는 이전 로깅 이력에 보존했고, 새 본문은 이관 원본의 값을 따른다. 실제 SDK 매핑·배포·한 번 전송은 미확인이다. 이 표는 원문 동작이 모두 같다는 사후 검증이나 추가 전송 승인이 아니다.
- 기존 동일 계약 3묶음(홈 1-6 콜밴팟·4-2 로그인·4-3 로그아웃), 홈 4-4 설정, 홈 3-6의 현재 4라벨은 이번에 변경하지 않는다. 시설물·채팅 중복 후보도 별도 결정 전 기존 상태를 유지한다.
- 새 형식은 기존 10개 동작의 이름/문서 정렬이며 사용자 행동을 추가하거나 과거 데이터를 소급 변환하는 작업이 아니다. 실제 호출 위치·전송 label/event\_name/screen\_view·버전·한 번 전송은 개발 검증 필요다. notification\_list 화면은 화면 정의에 검토중 등록했다.
- 품절 동결 5페이지·품절 제보 버튼 A/B·팀원 모집·새 주변상점·미래의 주변상점은 변경하지 않는다. 기존 사진·이전 원문·플랫폼·상태도 변경하지 않는다.
<!-- notion-body:end -->
