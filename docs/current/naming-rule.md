# 🧭 로깅 네이밍룰 v1.0 — DA1·DA2 공통 확정본

[← 현행 문서와 참고 자료](README.md)

[Notion 기준 원문](https://app.notion.com/p/4000221954bc81469ea6dbe19c7d8be7) · 조회·동기화 기준일: 2026-11-28.

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

<b>event\_name 현재 기준 · </b><b>2026-11-28</b>

작업 담당자는 서비스별로 고정되지 않는다. 전송·검수 기준은 각 개별 명세에 적힌 event\_name이며 service나 담당자만으로 DA1/DA2를 추정하지 않는다. 다국어 명세의 DA1은 그대로 유지한다. 과거 배정 기록을 이유로 기존 DA2·CAMPUS 등 개별 값이나 수집 데이터를 일괄 변경하지 않는다.

<b>서비스별 중복 카테고리 원문은 레거시 보존</b>

2026-11-08 홈의 카테고리 13개와 같은 진입 클릭을 정의한 서비스별 원문은 모두 레거시 이력이다. 현행 기준은 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 새 로깅이다. 제목만 레거시이고 본문은 현행처럼 보이던 안내도 바로잡았다. 원문의 라벨·값·플랫폼·사진·이력은 보존하고 같은 클릭을 중복 전송하지 않는다. 다른 화면에서 발생하는 상점 내부 필터·헤더·푸터·카드 동작에는 이 중복 판단을 적용하지 않는다.

<b>카테고리 13개 최종 기준 · 개별 계약의 event\_name / category\_navigation · </b><b>2026-11-08</b>

사용자 요청으로 홈 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 13개 메뉴를 <code>service__main_category__category_navigation__진입대상__click</code> 형식으로 통일했다. 카테고리 13개 계약의 event\_name은 각 개별 명세에 명시된 값을 따른다. 서비스명·value·발생 조건·사진·플랫폼 범위는 유지한다. 서비스명·발생 화면·플랫폼만으로 DA1/DA2를 추정하거나 일괄 변경하지 않는다. 버스는 <code>timetable_entry</code>와 <code>search_entry</code>로 목적지를 구분하고, 시간표 서비스의 <code>timetable_entry</code>는 service 구간으로 구분한다.

아래 이전 4개 계약의 feature·detail 설명과 옛 라벨은 이 후속 결정을 따른다. 신규 공용 feature는 category\_navigation이며 cafeteria\_entry·shop\_entry·owner\_entry 등은 해당 메뉴의 detail이다. 기존 4개 라벨 유지 + 나머지 9개 라벨 표기 변경이다. 문서 네이밍 결정일 뿐 팀원 모집 SDK 동결 해제·기존 9개 계약 WEB 지원 확대·SDK 배포·실수집 검수 완료를 뜻하지 않는다. 신·구 이중 전송과 과거 로그 소급 개명은 하지 않는다. Silver·Gold·데이터·설정은 변경하지 않았다.

<b>모바일 WEB 카테고리 4개 계약 확정 · </b><b>2026-11-08</b>

사용자 요청으로 식단·버스 시간표·교통편 조회하기·코인 for Business의 미확정 네이밍을 아래 계약으로 확정했다. 기준 본문은 <a href="https://app.notion.com/p/d950221954bc83f5b0c401cb41bbc359">3-6 카테고리 내부 클릭 (현재 로깅) 2026.08.30 이후 찍히는 로깅</a>의 새 로깅이며 각 항목은 설명·screen\_view·event\_name·event\_label·value·event\_category와 사진만 표시한다.

공통: screen\_view=<code>main_category</code>, feature=<code>category_navigation</code>, event\_category=<code>click</code>. event\_name은 각 개별 명세의 명시값을 따른다. 카테고리라는 이유로 DA1/DA2를 일괄 지정하지 않는다. 이 네 계약의 WEB 모바일 적용 범위는 유지한다.

- 식단: <code>cafeteria__main_category__category_navigation__cafeteria_entry__click</code> / value=식단. <a href="https://app.notion.com/p/4120221954bc817faa33c64ee9f9ad13">Notion 원문</a>
- 버스 시간표: <code>bus__main_category__category_navigation__timetable_entry__click</code> / value=버스 시간표. <a href="https://app.notion.com/p/4120221954bc81c08b5ed63eff880be6">Notion 원문</a>
- 교통편 조회하기: <code>bus__main_category__category_navigation__search_entry__click</code> / value=교통편 조회하기. <a href="https://app.notion.com/p/4120221954bc813a91caf8623f3cfec0">Notion 원문</a>
- 코인 for Business: <code>owner__main_category__category_navigation__owner_entry__click</code> / value=코인 for Business. <a href="https://app.notion.com/p/4120221954bc81f3bc00e71813fe5f25">Notion 원문</a>

이 네 항목을 포함한 13개 카테고리 메뉴는 공통 feature <code>category_navigation</code>을 사용한다. 식단의 <code>cafeteria_entry</code>, 버스의 <code>timetable_entry</code>·<code>search_entry</code>, Business의 <code>owner_entry</code>는 detail로 구분한다. Business 클릭은 외부 사이트 이동 시도이며 실제 방문 성공·가입·이용 완료를 증명하지 않는다.

로그는 클릭 시 한 번 기록한다. 단순 노출·초기 렌더·자동 이동은 제외하며 이동 후 성공을 기다려 클릭 이벤트의 의미를 바꾸지 않는다. 개발 반영 전 기존 category\_\* 수집은 유지하고, 반영된 해당 WEB 버전부터 새 계약으로 전환한다. 같은 클릭에 신·구 라벨을 함께 보내지 않으며 과거 로그를 소급 개명하지 않는다.

옛 앱 햄버거 삭제 명세는 계속 삭제·레거시 이력이며, PC 헤더·푸터·홈 카드의 라벨을 이 모바일 카테고리에 재사용하지 않는다. 이번 결정은 이 4개 WEB 계약에 한정한다. 기존 다른 9개 계약의 WEB 지원·팀원 모집 동결은 별도이며 카테고리 메뉴 수는 13개 그대로다.

문서 계약 확정이며 SDK 구현·배포·실수집 검수 완료가 아니다. Silver 허용 카탈로그·Gold·데이터·활성화 설정은 변경하지 않았다. 기존 378라벨/904계약은 이번 변경을 반영한 최신 총계가 아니므로 현행 목록 재집계 없이 사용하지 않는다.

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

레거시의 라벨·값·사진·플랫폼·이전 로깅은 삭제하지 않는다. 같은 클릭에 레거시 라벨을 추가 전송하지 않는다. 코드 대조 결과 일반 식단 카드 본문과 전체보기는 별도 클릭이므로 식단 1-2는 카드 본문 명세로 유지한다. 홈 1-3은 전체보기·더보기만 담당하며 같은 탭에 두 라벨을 함께 보내지 않는다. iOS 빈 상태 카드의 공유 콜백과 카드 본문의 명시 로그 누락 후보는 개발 검증 대상으로 남긴다. SDK 중단·전환·단일 전송은 미확인이다.

<b>네이밍룰 v1.0 확정</b> · 2026-10-28

사용자의 네이밍룰 확정 요청과 기존 방식 A 선택에 따라 본 문서를 공통 네이밍 기준으로 확정한다. 기능·detail 어휘는 <a href="https://app.notion.com/p/38b0221954bc831b912c012d8af2c857">event_label 기능·행동 네이밍 사전</a>의 현행 표, 작성 절차는 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>를 따른다. 충돌 시 본 확정 규칙과 명시적 동결 예외를 우선하고, 과거 대응표는 변경 이력으로만 사용한다.

확정 범위는 문법·용어·화면 표기·예외 관리다. 실제 동작·value·호출 지점이 미확인인 개별 계약과 SDK/dbt·배포·수집 검증을 완료 처리하지 않는다. 품절 관련 동결 5페이지와 팀원 모집 페이지는 변경 제외를 유지한다.

screen\_view는 event\_label을 <code>__</code>로 나눈 두 번째 구간과 정확히 같은 고정 문자열로 작성한다. 헤더는 <code>header</code>, 푸터는 <code>footer</code>다. 2026-10-30 상민의 직접 지시로 확정하며 이전 동적 표기·현재 화면명 수집안은 이 결정으로 대체한다. label·value·category·발생 시점과 동결 제외 범위는 유지한다. SDK 적용·실제 전송·한 번 전송은 별도 검증이다.

## 0. 한눈에 보기

```javascript
event_label  := service "__" page "__" feature [ "__" detail ] "__" category   (최대 5구간: detail 없으면 4구간 그대로, 있으면 5구간. 마지막 구간 = category. detail을 억지로 넣지 않는다)
service      := snake      (예: bus, timetable, team_recruit, owner, board, account)
page         := snake      (= screen_view의 고정값. 헤더는 header, 푸터는 footer)
feature      := snake      (공용 기능 사전의 현행 표에서 재사용. 진입은 {service}_entry와 위치 detail 사용. 버스 목적지형은 등록 예외)
detail       := snake      (선택, 최대 1구간. 구간 안 단어는 _로 연결. 대상·행동 동사: entry, open, confirm, response, apply, back, return, success, available 등)
category     := click | select | scroll | swipe | submit | fail | exposure | toggle   (event_category 값과 항상 일치, 라벨의 마지막 구간. 예외 목록 label만 접미 없음)
snake        := [a-z][a-z0-9]* ( "_" [a-z0-9]+ )*
```

핵심 한 줄(2026-10-27 확정): <b>통합 label의 마지막 구간은 항상 event\_category 단어(click, select, scroll, swipe, submit, fail, exposure, toggle)다.</b> 형태는 <code>service__page__feature[__detail]__category</code>로 4구간 또는 5구간이고, detail은 최대 1구간이다. 결과(submit/fail)에 따라 category가 갈리는 label만 접미 없는 예외 목록(관리 목록, 예: <code>cafeteria__cafeteria__soldout_submit</code>)으로 둔다. DA1·DA2 모두 공용 기능 사전에 맞추며, 같은 목적은 같은 feature를 재사용한다. DA2의 합친 detail/category는 분리하고 DA1의 미등록 기능은 등록 또는 공용 매핑한다. 세 번째 구간(feature)은 DA2 기능 사전 이름을 서비스 간 공유한다.

## 1. 원칙과 적용 범위

- 적용 범위: 모든 서비스와 로깅 작업 담당자. 업무 담당자는 서비스별로 고정되지 않으며 담당자·서비스 그룹에 따라 공통 네이밍 문법이 갈리지 않는다.
- 공통 원칙: 구분자 <code>__</code>, 구간 안 단어는 <code>_</code>, lower\_snake\_case, page = screen\_view의 고정값이며 헤더·푸터도 동일하다. label만 보고 기능과 행동을 알 수 있게 쓰고 동적 값은 value에 둔다. 동결 명세는 변경 제외다.
- 이름 변경은 이벤트 통합·추가 전송·전송 시점 변경을 뜻하지 않는다(DA2 기준 유지).
- <b>event\_name 규칙 (현재 기준 2026-11-28 · 서비스별 고정 배정 설명 정정)</b>
  - event\_name은 각 개별 로깅 명세에 명시된 DA1 또는 DA2 값을 따른다. service는 event\_label의 첫 구간으로 구분하며, service만 보고 event\_name을 결정하지 않는다. 같은 서비스에도 별도 계약에 따라 DA1·DA2가 함께 존재할 수 있다.
  - 작업 담당자는 서비스별로 고정되지 않는다. <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>의 과거 배정표는 당시 작성·분업 이력이며 현행 전송값을 강제하는 표가 아니다. 담당자 변경으로 기존 event\_name을 자동 변경하지 않는다.
  - 기존 수집분과 노션 명세의 event\_name은 바뀌지 않는다. 단일 값 통일안과 마트 매핑 테이블 안은 채택하지 않는다. 개선안 v2의 service\_name 구조도 채택된 적이 없다.

### 1-1. 전체 service 목록 · service\_name 조회표

2026-11-02 정리. 현재 TEAM Event Log의 공통 네이밍 문서와 기존 감사 목록을 대조하고, 아래 17개 구분(2026-11-28 PC WEB club 추가)의 대표 명세를 다시 읽어 확인했다. 새/미래 주변상점은 적용 대상에서 제외하며, 팀원 모집은 목록 확인만 하고 개별 명세를 수정하지 않는다. 이 표는 실제 배포·수집되는 service\_name의 전수 목록이나 SDK 적용 완료 선언이 아니다.

이 문서에서 조회 편의를 위해 service\_name이라고 부르는 값은 <b>event\_label 첫 번째 구간인 service</b>다. 별도 GA4/SDK 파라미터 service\_name 신설을 승인하거나 event\_name을 변경하는 결정이 아니다. 기존 service\_name 구조 미채택 기록과 구분한다.

| service / 조회용 service\_name | 한글 서비스·범위 | 구분·주의 | 대표 명세 |
| --- | --- | --- | --- |
| <code>account</code> | 계정·로그인·회원가입·정보 수정 | 서비스별 로그인 팝업도 account를 사용할 수 있음 | <a href="https://app.notion.com/p/0820221954bc834eb41301752196a7d5">1-2 회원가입진입(클릭)</a> |
| <code>banner</code> | 배너·메인 모달 | 배너/모달 노출·클릭·닫기 | <a href="https://app.notion.com/p/58a0221954bc8299aba081716dcade0b">1-3. 메인_모달닫기_클릭</a> |
| <code>board</code> | 게시판·공지사항·분실물 | 분실물은 lost\_item을 별도 service로 만들지 않고 board 내 page/feature로 구분 | <a href="https://app.notion.com/p/00c0221954bc83618638010c14368813">8-1. 더보기_클릭</a> |
| <code>bus</code> | 버스·교통편 조회·셔틀 | 목적지형 헤더/푸터 label은 기존 등록 예외 유지 | <a href="https://app.notion.com/p/1490221954bc828fbc28815a97a32f94">5-12. 교통편 차종_클릭</a> |
| <code>cafeteria</code> | 식단·학생식당 | 품절 제보·품절 알림 동결 명세는 그대로 유지 | <a href="https://app.notion.com/p/c420221954bc831497240194ccc6ae54">2-1. 헤더_식단_클릭</a> |
| <code>callvan</code> | 콜밴팟 | 메인 모집 보기와 카테고리 진입 등 page/feature로 구분 | <a href="https://app.notion.com/p/01c0221954bc837eaafa01402f06f32a">1-6 콜벤팟 모집 보기 클릭</a> |
| <code>chat</code> | 쪽지·채팅 | 게시판 안에 명세가 있어도 쪽지 service는 chat | <a href="https://app.notion.com/p/15d0221954bc82da9b0001cb92292190">11-17.헤더_쪽지_클릭</a> |
| <code>club</code> | 동아리 | PC WEB에서 확인한 신규 계약만 적용. 기존 동아리 레거시는 보존 | <a href="https://app.notion.com/p/4260221954bc80ceab95e8c9e4cac8f1">동아리</a> |
| <code>course_practice</code> | 모의수강신청 | course\_application은 feature 어휘이며 service 이름과 구분 | <a href="https://app.notion.com/p/0140221954bc8310a04f013fed656d61">1-5. 모의수강신청_메인으로 클릭</a> |
| <code>department</code> | 학교 부서 정보 | 부서 분류·검색·전화번호 복사 | <a href="https://app.notion.com/p/2370221954bc83afaba301e35693f565">1-0-1 학교 부서 정보 접근 (푸터 진입)</a> |
| <code>facility</code> | 교내 시설물 정보 | 시설물 서비스 진입 | <a href="https://app.notion.com/p/29a0221954bc82788e2c81c4dbec50d7">10-1. 헤더_교내 시설물 정보_클릭</a> |
| <code>main</code> | 공용 홈·알림 목록·네비게이션 | 홈 공용 기능과 홈 식단 1-3 진입·1-4 코너 선택은 main. 식단 화면 내부는 cafeteria. 카테고리 진입은 확정된 서비스별 계약 유지. | <a href="https://app.notion.com/p/fe30221954bc82e7abe4012b1fb7bd60">1-1 알림 클릭</a> |
| <code>owner</code> | 사장님·코인 for Business | 사장님 서비스 기능; 일반 주변상점 shop과 구분 | <a href="https://app.notion.com/p/0540221954bc8395b443814167ca48b1">4-1 로그인 (클릭) - 추가된 로깅</a> |
| <code>real_estate</code> | 복덕방 | 주거·방 정보와 서비스 진입 | <a href="https://app.notion.com/p/1740221954bc83cebc8601faa22ca3a5">1-1 헤더_복덕방 진입(클릭)</a> |
| <code>shop</code> | 주변상점 | 식단 안 상점가기 배너처럼 다른 화면의 shop label도 존재 | <a href="https://app.notion.com/p/0090221954bc83caa53201000c97e7db">2-18 상점 카테고리 최소주문금액 설정 - 레거시</a> |
| <code>team_recruit</code> | 팀원 모집 | 읽기 전용 목록에 포함. 기존 개별 명세는 변경하지 않음 | <a href="https://app.notion.com/p/8ce0221954bc836ca589012bcbd1fc8a">4-2. 모집글 편집</a> |
| <code>timetable</code> | 시간표 | 일반 시간표·강의·학기 관리; 모의수강신청과 구분 | <a href="https://app.notion.com/p/0a00221954bc83bca117013903d780d7">2-20. (웹) 시간표_수정_해당 학부 (클릭)</a> |

<b>명세에 사용되는 고유 service 구분은 17종</b>이다. 서비스 문서 수·DA 담당 배정 수·개별 이벤트 수와 다르다. 예를 들어 공지사항과 분실물은 board를 공유하고, 쪽지와 시설물은 게시판 DB 안에 있더라도 각각 chat/facility다. 홈 기능도 main 외에 목적 서비스의 shop/callvan/timetable 등을 사용할 수 있다.

복사용 목록:

```txt
account
banner
board
bus
cafeteria
callvan
chat
club
course_practice
department
facility
main
owner
real_estate
shop
team_recruit
timetable
```

### 1-2. Silver/Gold의 service\_name과 구분

| 구분 | 사용 원칙 |
| --- | --- |
| label의 service | 위 17개 구분. 이벤트의 명세상 도메인이다. page·feature·value·플랫폼·발생 조건과 함께 해석한다. |
| Silver의 service\_name | 승인된 분석 분류 결과다. label 첫 구간을 무조건 복사하거나 이름이 같다는 이유로 매핑 검증 완료로 처리하지 않는다. 과거 라벨·화면·플랫폼별 분류와 적용 시점을 함께 대조한다. |
| Gold v6의 1차 BI 범위 | shop, bus, cafeteria, timetable, board, facility, main 및 과거 grad\_calc 이력. 현행 service 전체를 대시보드 범위로 자동 확장하지 않는다. |
| grad\_calc | Gold v6의 과거 졸업학점 계산기 분석 구분이다. 현행 명세 목록에 새 label service로 추가하거나 신규 이벤트를 만들지 않는다. |
| unmapped / unknown | 분류 미확인·결측 등을 표현하는 분석 상태값이다. 새 비즈니스 service나 label 접두로 등록하지 않는다. 실제 사용값은 해당 Silver 계약에 따른다. |
| <b>all</b> | Gold 리텐션의 전체 범위 예약값이다. main·서비스 합계·SDK service 이름과 다르다. |

대표 사례: 식단 페이지의 상점가기 배너는 shop 접두를 사용할 수 있고, 상점 화면의 로그인 팝업은 account 접두를 사용할 수 있다. 화면이 속한 문서 이름만으로 service를 바꾸지 않는다. 기존 동결 label·이전 로깅·value·category·event\_name·사진·플랫폼은 이 목록 정리로 변경하지 않는다.

Gold 연결 기준: <a href="https://app.notion.com/p/40b0221954bc81e29982d9f8db59b888">골드 테이블 설계 (v6) — Superset · 단일 테이블 우선, 최대 2개</a>. 데스크탑 웹은 사용자 완료 통보 전까지 현행 파란색 디자인·실수집 기준을 유지한다.

## 2. event\_label 문법

### 2-1. 구조

<code>{service}__{page}__{feature}__{category}</code> 4구간, 또는 <code>{service}__{page}__{feature}__{detail}__{category}</code> 5구간. 마지막 구간은 항상 category다. 정규식은 8장.

- category는 event\_category 표준 목록(click, select, scroll, swipe, submit, fail, exposure, toggle) 중 하나이며 event\_category 값과 일치시킨다. 예외: 결과로 category가 갈리는 label(submit/fail)은 접미 없이 예외 목록에서 관리한다(예: <code>cafeteria__cafeteria__soldout_submit</code>, 3구간).
- 5구간은 상한이다. 자연스러운 detail이 없는 label은 4구간 그대로 두고(가짜 detail·fallback 이름을 넣지 않는다), 마지막 구간이 category인지만 확인한다. 없으면 category를 덧붙인다.
- detail은 같은 feature 안에서 대상·행동을 더 쪼갤 때 쓰는 단일 구간이다. 추가 구간은 만들지 않는다. 구간 안에서는 <code>_</code>로 이어 쓴다(예: <code>recommended_keyword</code>, <code>header_entry</code>).
- feature(3번째 구간)는 DA2 기능 사전(네이밍 사전 3장)의 이름을 서비스와 무관하게 재사용한다(filter, search, keyword\_manage, navigation, login\_popup 등). DA1 페이지 고유 feature 이름은 사전에 맞는 기능이 있으면 그 이름으로 매핑하고, 없으면 포함 행동·목적을 적어 새로 등록한 뒤 쓴다.
- 동작 동사(entry, open, confirm, response, apply, back, return, success, available 등)는 category가 아니므로 detail로 두고 뒤에 category를 붙인다. category는 기존 승인 계약을 따른다. 옵션 선택·제출이라는 설명만으로 click을 select/submit으로 바꾸지 않는다.

### 2-2. 변환 규칙

| 원본 형태 | 규칙 |
| --- | --- |
| DA1 다섯 구간 <code>s__p__f__세부__cat</code> | 변환 없음. 이미 규칙대로. feature만 사전 이름과 맞는지 확인(맞는 기능이 있으면 이름만 매핑) |
| DA1 네 구간 <code>s__p__f__cat</code> | 일반 이벤트는 유지. 공용 헤더·푸터·서비스 카테고리 진입은 4장의 공통 기능·위치 detail 기준을 적용한다. 버스 등록 예외·동결 명세·팀원 모집은 제외한다. |
| DA1 세 구간 결과형 <code>s__p__동작_submit</code> (soldout\_submit) | 변환 없음. 예외 목록에 등록(접미 없음, 결과로 submit/fail) |
| DA1 공용 헤더·푸터·서비스 카테고리 진입의 과거 4구간 형태 | 4장 기준으로 공용 feature와 위치 detail을 사용한다. 예: <code>s__header__s_entry__header_entry__click</code>. 카테고리는 <code>main_category</code>와 <code>category_entry</code>를 사용한다. 버스 등록 예외·동결 명세·팀원 모집은 변경하지 않는다. |
| DA1 로그인 팝업 등 서비스 고유 로그인 label | <code>account__{page}__login_popup__login_entry__click</code> / <code>…__close__click</code>로 매핑(4장) |
| DA2 마지막 구간이 <code>{대상}_{category}</code> 합친 형태 (<code>add_submit</code>, <code>notification_toggle</code>, <code>tab_select</code>, <code>keyword_select</code>, <code>delete_click</code>, <code>phone_click</code>) | 마지막 구간을 detail + category로 쪼갠다: <code>…__add__submit</code>, <code>…__notification__toggle</code>, <code>…__tab__select</code> |
| DA2 마지막 구간이 category 단어뿐 (<code>scroll</code>, <code>submit</code>, <code>select</code>) | 승인된 event\_category와 일치하면 유지한다. 불일치하면 category를 바꾸지 않고 label 끝을 승인값으로 정렬한다. |
| DA2 detail이 feature 이름과 같은 합친 형태 (<code>search_submit</code>) | 중복 detail 없이 <code>…__search__submit</code> |
| DA2 동작 동사가 마지막 구간 (<code>entry</code>, <code>open</code>, <code>confirm</code>, <code>response</code>, <code>apply</code>, <code>back</code>, <code>return</code>, <code>success</code>, <code>available</code>, <code>*_entry</code>, <code>*_confirm</code>, <code>*_response</code>, <code>*_return</code>) | 동사를 detail로 유지하고 기존 승인 category 추가. 아래 click 예는 승인 category가 click인 계약에만 적용: <code>…__entry__click</code>, <code>…__join_response__click</code>, <code>…__code_verify_success__click</code>(성공 조건 시점 유지) |
| DA2 헤더·푸터 <code>{svc}__header__{svc}_entry__header_entry</code> | category만 덧붙인다: <code>{svc}__header__{svc}_entry__header_entry__click</code>(푸터도 동일, page = footer) |
| DA2 카테고리 진입 <code>{svc}__main_category__{svc}_entry__category_entry</code> | <code>{svc}__main_category__{svc}_entry__category_entry__click</code> |
| DA2 공용 카테고리 메뉴 <code>…__category_navigation__{svc}_entry</code> | <code>…__category_navigation__{svc}_entry__click</code> |

### 2-3. 변환 예시 (8개)

출처 표기: \[실제\]는 현행 노션 값, \[파생\]은 규칙으로 만든 예시, 실제 페이지로 검증 필요(1번·6번).

| # | 이전 | 통합안 | 비고 |
| --- | --- | --- | --- |
| 1 | <code>bus__bus_search__departure__time__select</code> \[파생, DA1\] | 그대로 | DA1 5구간. 이미 규칙대로(detail=time, category=select) |
| 2 | <code>timetable__header__entry__click</code> \[과거 DA1 명세\] | <code>timetable__header__timetable_entry__header_entry__click</code> | 현행 공통 진입 형식. screen\_view=<code>header</code>로 label 두 번째 구간과 일치하며 SDK 적용 검증은 별도. |
| 3 | <code>cafeteria__cafeteria__soldout_submit</code> \[실제 규칙, DA1\] | 그대로 | 결과형 예외 목록(접미 없음, 3구간). category는 submit/fail |
| 4 | <code>owner__shop_detail__login__cancel__click</code> \[파생, DA1\] | <code>account__shop_detail__login_popup__close__click</code> | 로그인 팝업 매핑(4장). 실제 페이지로 검증 필요 |
| 5 | <code>board__lost_item_keyword_manage__keyword_manage__add_submit</code> \[실제 DA2\] | <code>board__lost_item_keyword_manage__keyword_manage__add__submit</code> | 합친 마지막 구간을 detail(add) + category(submit)로 분리 |
| 6 | <code>board__lost_item_keyword_manage__keyword_manage__notification_toggle</code> \[실제 DA2\] | <code>board__lost_item_keyword_manage__keyword_manage__notification__click</code> | 현행 방식 A: 승인 category click 유지. toggle로 자동 변경 금지 |
| 7 | <code>department__header__department_entry__header_entry</code> \[과거 DA2 명세\] | <code>department__header__department_entry__header_entry__click</code> | 과거 4구간에서 category(click)를 추가한 현행 5구간. |
| 8 | <code>board__lost_item_list__filter__apply</code> \[실제 DA2\] | <code>board__lost_item_list__filter__apply__click</code> | 동작 동사 apply는 category가 아니므로 detail 유지 + click 추가 |

같은 규칙의 추가 DA2 예(사전 매핑표 기준): <code>board__main_notice__filter__tab_select</code> → <code>…__filter__tab__select</code>, <code>board__notice_search__search__search_submit</code> → <code>…__search__submit</code>, <code>board__main_notice__keyword_manage__entry</code> → <code>…__keyword_manage__entry__click</code>, <code>callvan__callvan_list__callvan_participation__join_response</code> → <code>…__join_response__click</code>, <code>account__lost_item_list__login_popup__login_entry</code> → <code>…__login_popup__login_entry__click</code>.

### 방식 A 적용 기록 (2026-10-28)

사용자 확인에 따라 기존 승인 category를 보존하고 label 끝을 그 값에 맞춘다. DA2 후속 작업에서 click을 select/submit/toggle로 바꾼 10페이지는 click으로 복원했으며 학교 부서의 복수 화면을 포함해 label 11개를 정렬했다. 계정 5건의 confirm\_\_click은 유지한다. value·담당자·플랫폼·원래 전송 조건은 바꾸지 않는다.

제출·신청 지표는 승인 계약 목록과 필요한 value 조건으로 정의한다. category=submit 또는 confirm\_\_click 패턴 하나만으로 전체 제출을 집계하지 않는다. 결과형 품절 동결 예외는 이 정렬 대상에서 제외한다.

## 3. event\_category · 단어 표준

### 3-1. event\_category 표준 목록 (DA1 목록 = 합집합)

| 값 | 정의 |
| --- | --- |
| click | 버튼·카드·탭·링크를 누름. 다른 값에 해당하지 않는 클릭 |
| select | 여러 옵션 중 하나를 고름(탭·필터 옵션·추천 키워드) |
| toggle | on/off 스위치(알림 설정 등) |
| scroll | 목록 스크롤 |
| swipe | 스와이프 |
| submit | 최종 저장·등록·검색 실행·신청 제출. 발생 시점은 각 승인 명세를 따르며 서버 성공을 일괄 의미하지 않는다. |
| fail | submit이 실패한 결과 |
| exposure | 화면·모달·배너 노출 |

새 category는 만들지 않는다(back, success, result 등 금지). DA2의 기존 승인값은 이 목록에 있으면 유지하고, 목록 밖 값이 있으면 8장 검수에서 걸러 개별 협의한다.

### 3-2. 결과별 category 예외 (submit / fail)

- 원칙: category는 승인된 행동 분류다. 단어만으로 클릭 순간·API 요청·서버 응답 시점을 추정하지 않으며 각 원문 전송 조건을 유지한다. 서버 결과로 성공·실패가 갈리는 승인된 결과형만 별도 예외로 관리한다.
- 예외 이벤트는 <b>label 하나</b>를 쓰고 <b>category 접미를 붙이지 않는다</b>(예: <code>cafeteria__cafeteria__soldout_submit</code>, 3구간 허용). category 값은 성공 submit, 실패 fail로 나뉜다. 예외 label은 관리 목록에 등록하며, 8장 검수는 목록에 있는 label만 마지막 구간 검사에서 제외한다.
- 예외 목록(현재): 식단 품절 제보 (이미 구현 완료, 변경 금지). 분실물 작성완료(11-4·11-11)는 클릭 순간 전송이라 예외 아님. 목록은 통합 가이드에 명시한다. <b>label 형식 = 현행 유지 (접미 없는 예외, 확정 2026-10-27)</b>

### 3-3. 단어 표준

단어 역할은 둘로 나눈다. <b>category 단어</b>(click, select, scroll, swipe, submit, fail, exposure, toggle)는 항상 마지막 구간이다. <b>동작 동사</b>(아래 표의 confirm, response, cancel, close, deadline, entry, open, apply, back, return, success, available, copy, send, add, delete 등)는 category가 아니라 detail에 쓰고, 뒤에 category를 붙인다(<code>…__entry__click</code>, <code>…__close__click</code>). submit은 둘 다에 해당하므로 detail로 쓰지 않고 category로만 쓴다.

| 단어 | 쓰는 곳 |
| --- | --- |
| submit | 최종 저장·등록 버튼 |
| confirm | 값을 확정하는 확인 버튼 또는 확인 팝업 안의 확인 |
| response | 예·아니오 둘 다 있는 확인 응답. 값은 value로 구분(<code>join_response</code>) |
| cancel | 확인 팝업·작업의 취소(되돌리기) |
| close | 닫기(X)·안내 팝업·로그인 팝업 닫기 |
| deadline | 마감 처리. close는 마감에 쓰지 않는다 |
| entry | 화면·서비스 진입. 위치는 <code>header_entry</code>, <code>footer_entry</code>, <code>category_entry</code>, <code>title_entry</code> |
| open | 모달·필터·상태 변경창 열기 |
| back / return | 뒤로가기 / 지정 화면 복귀 |

- detail의 끝 단어와 category가 겹치는 <code>…__submit__submit</code>, <code>…__add_submit__submit</code> 형태는 만들지 않는다. detail은 대상·동사만, 행동 종류는 category가 맡는다(<code>add__submit</code>). DA2의 합친 <code>add_submit</code>은 <code>add</code> + <code>submit</code>으로 쪼갠다.

## 4. header · footer · 카테고리 · 로그인 팝업

아래 service\_entry 형식은 일반 서비스 진입의 예시다. 계정의 sign\_up/login/profile\_edit, 게시판의 notice\_entry/lost\_item\_entry 등 등록된 feature는 기존 명세대로 유지하며 service 이름으로 일괄 치환하지 않는다. 공용 헤더·푸터의 위치 detail은 header\_entry/footer\_entry다. 일반 4구간 문법을 통과한다는 이유만으로 과거 공용 진입 label을 현행으로 승인하지 않는다. 버스 등록 예외·품절 동결 명세·팀원 모집은 변경 제외다.

| 항목 | 통합 규칙 |
| --- | --- |
| 헤더 진입 | DA1·DA2 공통: <code>{svc}__header__{svc}_entry__header_entry__click</code>. label page와 screen\_view는 <code>header</code>로 고정한다. 버스 목적지형 label은 등록 예외 유지. |
| 푸터 진입 | DA1·DA2 공통: <code>{svc}__footer__{svc}_entry__footer_entry__click</code>. label page와 screen\_view는 <code>footer</code>로 고정한다. 버스 목적지형 label은 등록 예외 유지. |
| 카테고리(앱 하단·햄버거) 진입 | DA1·DA2 공통: <code>{svc}__main_category__{svc}_entry__category_entry__click</code>. screen\_view와 label page 모두 main\_category로 통일한다. 플랫폼별 경로는 원문을 유지하고 같은 클릭에서 중복 전송하지 않는다. |
| 공용 카테고리 메뉴 | <code>…__main_category__category_navigation__{svc}_entry__click</code> 별개 유지(네이밍 사전 5장). 5구간 |
| 로그인 팝업 | <code>account__{page}__login_popup__login_entry__click</code>(로그인 이동) / <code>…__login_popup__close__click</code>(닫기·취소). 누른 버튼에 따라 label 하나만 전송 |
| screen\_view | event\_label의 두 번째 구간과 같은 고정 문자열이다. 헤더 <code>header</code>, 푸터 <code>footer</code>, 카테고리 <code>main_category</code>, 버스 공지·오류 제보 <code>bus_timetable</code>을 각각 해당 label과 일치시킨다. |

<b>버스 예외</b>: 버스 헤더·푸터는 목적지가 여러 개라 목적지형을 허용한다. 현행 <code>bus__header__{목적지}__click</code>(예: <code>bus__header__timetable__click</code>)이 이미 마지막 구간 = category 규칙을 지키므로 변환하지 않고 예외로 유지한다. <b>확정: 등록된 현행 목적지형 4개는 유지한다.</b> 신규 예외는 자동 확대하지 않고 사유·대상 label·발생 조건을 명시해 승인 후 등록한다.

## 5. value 규칙

2026-11-04 문서 표기 정리: 표시용 따옴표만 제거하며 한글 고정값·동적 변수·후보·예시·전송 조건은 유지한다. 설명용 예시는 실제 SDK 전송값의 일부가 아니다. 기존 동아리 명세는 레거시로 보존한다. 2026-11-28 사용자 요청으로 새로 확인한 PC WEB 동아리 계약은 별도로 신규 네이밍을 적용하며 모바일 WEB과 앱은 제외한다.

- 한국어, <b>따옴표 없음</b>. 고정 문자열은 그대로, 동적 값은 <code>{…}</code>.
- 여러 값을 합칠 때 밑줄 <code>_</code> (예: <code>주중_천안역</code>, <code>2026_2학기</code>).
- 복수 선택(필터 다중 선택)은 <code>|</code> 연결, UI 정의 순서·중복 제거. 합친 값의 <code>_</code>와 선택 목록의 <code>|</code>는 의미가 다르다.
- 새 로깅에는 <code>(예: …)</code> 예시 1개를 쓴다. value가 고정 문자열 하나면 예시를 생략한다.
- 기본값은 명시한다(필터 미선택 = 전체).
- 값이 없는 행동 로그는 <code>value: 없음</code>(DA2 콜밴팟 메시지 본문 등)으로 쓴다.
- <b>검색어·입력 원문 (논의 필요)</b>: 현재 DA1은 수집 안 함, DA2는 일부 수집(학교 부서 검색어, 분실물 키워드 추가 값). 추천: 기본 금지, 분석 목적이 있고 개인정보가 아님을 확인한 항목만 허용 목록으로 관리한다. 허용 항목은 통합 가이드에 이벤트와 사유를 적는다. 자유 입력 텍스트(쪽지·채팅·게시글 본문)는 어떤 경우에도 수집하지 않는다.

## 6. screen\_view · page 규칙

- page 구간과 screen\_view는 모든 일반 명세에서 같은 고정 문자열이다. 이동·모달·헤더·푸터도 라벨의 두 번째 구간을 사용하며 현재 열려 있는 UI 화면명으로 대체하지 않는다. 품절 동결 명세는 변경 제외다.
- 모달·팝업·바텀시트·필터는 별도 화면이 아니라 아래 깔린 화면 이름을 유지한다(분실물 필터 <code>board__lost_item_list__filter__apply</code>).
- 공용 헤더·푸터는 label page와 screen\_view를 각각 <code>header</code> / <code>footer</code>로 고정한다. label이 <code>bus__header__timetable__click</code>이면 screen\_view는 <code>header</code>다.
- 화면 이름은 화면 정의 및 로깅 검수의 고정 이름만 쓴다. 새 이름은 거기에 먼저 추가하고 검토중으로 표시한다.
- 이름 규칙: snake\_case, 서비스 접두를 중복하지 않는다(<code>bus_timetable</code>처럼 서비스 안에서 의미가 필요하면 허용). 카테고리 화면은 <code>main_category</code>. 다른 서비스 소유 화면은 그 서비스의 service·page를 쓴다(모의수강신청 진입 클릭만 <code>course_practice__timetable__…</code>).
- 미정의 화면 이름은 임의로 만들지 않는다. <b>확정</b>: 기존 승인 화면명(예: <code>bus_timetable</code>)은 유지한다. 접두 중복만을 이유로 변경하지 않는다.

## 7. 페이지 양식 템플릿

플랫폼은 DB 속성(platform)으로 관리하고 본문에 반복하지 않는다. 사진은 웹·모바일 닫힌 토글, 빨간 네모는 코드로만 그리고 출처(실제 캡처 / Figma / 사용자 제공)를 적는다.

```txt

<details>
<summary>이전 로깅</summary>

(기존 원문 그대로 보존)

</details>

<details>
<summary>새 로깅 (YY.MM.DD)</summary>

- 설명: {화면}에서 {무엇을} 누르면 {어디로 / 어떤 결과}
- screen_view: {page} (event_label의 두 번째 구간과 같은 고정 문자열을 기입; 예: header)
- event_name: {기존 DA1 또는 DA2 유지}
- event_label: {service}__{page}__{feature}[__{detail}]__{category}
- value: {기존 고정값 또는 동적 매핑 유지} (예: {예시 1개})
- event_category: {기존 승인 category 유지}

<details>
<summary>검토사항</summary>

- 통합 가이드 링크, 전송 시점, 이전 → 새 label 대응, 사진 대기 여부

</details>

### 참고사진 (기능 표시)

웹

<details>
<summary>참고사진 · 웹</summary>

출처 / 빨간 네모 = 클릭 위치 + 기존 이미지

</details>

모바일

<details>
<summary>참고사진 · 모바일</summary>

출처 + 기존 이미지 (없으면 사진 없음)

</details>

</details>

```

- 레거시·삭제: 새 로깅에 <code>레거시: {사유}. 새 로깅을 만들지 않는다.</code>와 대체 로깅을 적는다.
- 이 양식은 DA2 페이지(분실물·게시판)와 버스 4-9 변환본 구조를 합친 것이다. DA1 쪽은 <code>과거</code> → <code>이전 로깅</code>, <code>새 로깅</code> → <code>새 로깅 (YY.MM.DD)</code>로 바꾸고 검토사항·웹/모바일 토글을 추가한다.

## 8. 자동 검수 체크리스트

정규식은 label 한 줄 기준이다(PCRE).

| # | 검사 | 패턴 / 조건 |
| --- | --- | --- |
| 1 | 4 또는 5구간·소문자 snake (일반 규칙. 3구간은 통과하지 않음. 예외는 아래 1-예외 allowlist) | <code>^[a-z][a-z0-9]*(_[a-z0-9]+)*(__[a-z][a-z0-9]*(_[a-z0-9]+)*){3,4}$</code> |
| 1-예외 | 결과형 3구간 예외 allowlist (일반 정규식 1을 3구간으로 넓히지 않고 label을 명시 등록) | label이 allowlist 정확 일치: <code>cafeteria__cafeteria__soldout_submit</code> (구현 완료·변경 금지). 일치하는 label만 1·2·10번 검사에서 제외 |
| 2 | 구간 수 4 또는 5(세부 있으면 5) | label을 <code>__</code>로 split 후 길이 4 또는 5 (1-예외 allowlist label 제외) |
| 3 | 대문자·한글·공백·따옴표 금지 | <code>[^a-z0-9_]</code> 없음 |
| 4 | 삼중 밑줄 금지 | <code>___</code> 없음 |
| 5 | page와 screen\_view | <code>screen_view == event_label.split("__")[1]</code>. 헤더·푸터도 예외 없이 각각 header/footer 고정값으로 비교한다. 동결 명세는 변경 제외다. |
| 6 | 헤더 진입·동작 구분 | 진입 label은 <code>^[a-z0-9_]+__header__[a-z0-9_]+__header_entry__click$</code>로 검사한다. 헤더 내부 동작 <code>account__header__logout__click</code>은 기존 4구간을 유지한다. 두 경우 모두 screen\_view=<code>header</code>다. 버스 목적지형은 등록 예외 유지, 팀원 모집·동결 명세는 변경 제외다. |
| 7 | 푸터 형태 | DA1·DA2 공통: <code>^[a-z0-9_]+__footer__[a-z0-9_]+__footer_entry__click$</code>. feature는 현행 사전 등록값을 사용한다. 버스 목적지형은 등록된 현행 4개 중 해당 label만 허용한다. 팀원 모집·동결 명세는 검사·변경 제외다. |
| 8 | 카테고리 진입 | DA1·DA2 공통 서비스 진입: <code>^[a-z0-9_]+__main_category__[a-z0-9_]+_entry__category_entry__click$</code>. 공용 메뉴의 feature=category\_navigation 계약은 별개로 유지한다. 팀원 모집·동결 명세는 검사·변경 제외다. |
| 8-1 | 홈과 메뉴 진입 구분 | detail이 정확히 <code>category_entry</code>이면 page/screen은 <code>main_category</code>다. 홈 버튼 <code>main_entry</code> 및 홈 카드 <code>category_card_entry</code>는 page/screen <code>main</code>을 유지한다. |
| 9 | detail 어휘 | 현행 기능 사전에 등록된 detail 및 대상 명사를 허용한다. entry/open/confirm 등 동사 끝 정규식만으로 정상 명사 detail을 오류 처리하지 않는다. 미등록 어휘는 사람 검토 경고로 분류한다. |
| 10 | 마지막 구간 = category | label의 마지막 구간 ∈ \{click,select,scroll,swipe,submit,fail,exposure,toggle\}. 단, 예외 목록(결과형)에 등록된 label은 제외. 정규식: <code>__(click\|select\|scroll\|swipe\|submit\|fail\|exposure\|toggle)$</code>. 마지막 구간이 event\_category 값과도 일치 |
| 11 | 이중 표기 금지 | detail 끝 단어가 category 단어면 안 됨(<code>add_submit__submit</code>, <code>submit__click</code>). 정규식: <code>(^\|_)(click\|select\|submit\|toggle\|scroll\|swipe\|exposure\|fail)__[a-z]+$</code> 없음 (표 안이라 세로선을 \|로 표기). 합친 구간 <code>…add_submit</code> 같은 DA2 옛 형태는 이 검사로 걸러진다 |
| 12 | deadline/close | 마감 이벤트는 <code>deadline</code>, close 아님(사람 검토) |
| 13 | value 따옴표 | value에 <code>"</code> <code>“</code> <code>”</code> <code>'</code> 없음 |
| 14 | 합친 값 | value에 공백 구분 합침 없음(사람 검토) |
| 15 | 입력 원문 | value 이름에 <code>검색어</code>, <code>{query}</code>, <code>{text}</code>가 있으면 허용 목록 대조 |
| 16 | 중복 label | 동일 이벤트 계약표에 등록되고 기준 명세가 명시된 계약만 여러 문서 설명을 허용한다. 미등록 중복 또는 의미·발생 조건·value 정책 충돌은 검토 대상이다. 실제 SDK 중복 발화는 별도 검증한다. 계약표는 <a href="https://app.notion.com/p/3c30221954bc8214b1c481c5bbb6fba5">로깅 통합 가이드</a>를 따른다. |
| 17 | 템플릿 | 새 로깅 토글 제목이 <code>새 로깅 \(\d{2}\.\d{2}\.\d{2}\)</code> |

## 9. 확정 범위와 적용 관리

### 9-1. 확정 결정

- 일반 문법은 4\~5구간이며 마지막 구간은 승인 event\_category와 일치한다. detail은 최대 1구간이다.
- event\_name은 개별 명세의 명시값을 유지한다. 서비스명이나 현재 작업 담당자만으로 DA1/DA2를 추정하지 않으며 값이 미기재된 계약은 원문을 확인한다.
- 같은 목적은 공용 사전의 feature를 재사용한다. 등록된 명사 detail도 허용한다. 신규 기능은 목적·대상·발생 조건과 함께 등록한다.
- 방식 A: category·value·발화 조건을 이름 정리 때문에 바꾸지 않는다. 계정 5건의 confirm\_\_click은 유지한다. 제출 지표는 승인 계약 목록과 value 조건으로 집계한다.
- 헤더·푸터 label page와 screen\_view는 각각 <code>header</code> / <code>footer</code>로 일치시킨다. 현재 UI 화면명이나 가변 placeholder로 작성하지 않는다.
- 메뉴 category\_entry는 main\_category, 홈 main\_entry/category\_card\_entry는 main이다. 로그인 팝업은 account 서비스와 login\_popup feature를 사용한다.
- 버스 목적지형 4개는 기존 예외 유지. 품절 관련 동결 5페이지와 팀원 모집 페이지는 변경 제외다. 품절 결과형 접미 없는 기존 label을 고치지 않는다.
- 과거 수집값·이전 로깅은 소급 변환하지 않는다. 이전→새 label 대응과 적용 버전을 남긴다.
- 동일 이벤트 계약표에 기준 명세와 함께 등록된 계약만 여러 문서 설명을 허용한다. 미등록·충돌 계약은 검토하고 문서 수만큼 이벤트를 추가 전송하지 않는다.
- 번호 정리 이력 (2026-10-28): 이전 합의 #7은 로그인 팝업 service를 account로 통일하는 항목이다. Claude 원문 수정 기록에서 9-1 번호를 1\~10으로 정리했고, 확정본 전환 때 9-1을 목록형 결정으로 바꿨다. 로그인 팝업 결정은 4장 및 위 확정 결정에 유지되며 누락·폐기한 것이 아니다.

### 9-2. 네이밍 확정과 별도로 남는 일

- 실제 동작·호출 지점·value 정책: 메뉴 회원가입/로그인 진입, 주변상점 중복 진입, 과목 추가, 이탈·스와이프·학기 삭제 등은 근거 확인 전 보류한다. 근거가 바뀌면 본 문법 안에서 개별 계약을 수정한다.
- screen\_view 적용 점검: 개별 명세를 label 두 번째 구간의 고정값으로 대조한다. SDK도 같은 값을 전송하는지 개발 담당자가 별도로 확인하며, 이번 문서 수정만으로 구현·배포·실제 수집 완료라고 주장하지 않는다.
- 검색어·입력 원문 수집은 네이밍 확정으로 승인하지 않는다. 기존 value와 개별 승인 조건을 보존하고, 신규·변경 수집은 목적·항목·사유를 명시해 별도 결정한다.
- event\_name 미확정 계약, 사본 병합, 사진 보완, SDK/dbt 수정·배포·실제 수집·한 번 전송 검증은 후속이다. 기존 병합 계획을 근거로 팀원 모집이나 동결 페이지를 자동 수정하지 않는다.

### 9-3. 변경 절차

확정본 버전은 v1.0이다. 이후 규칙 변경은 사유·영향 명세·이전→새 값·동결 예외·개발 적용 계획을 남겨 별도로 승인받는다. 오타 수정과 등록 어휘를 이용한 신규 명세 작성은 이 규칙을 따른다. 문서 확정일과 실제 개발 적용일·플랫폼·버전·검증 결과는 구분해 기록한다.
<!-- notion-body:end -->
