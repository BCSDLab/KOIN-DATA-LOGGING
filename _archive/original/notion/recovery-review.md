# 원본 87개 복구와 8개 차이 정리

기준: PR #1의 fffb46d563488d20cdab9ffcdca6f4cb93f9aed2 대조에서 확인된 누락 원본 ID. 2026-11-12 복구.

- 원본 ID 87개 모두 별도 페이지로 추가. 중복 추정 76개와 빈 페이지 3개도 제외하지 않음.
- 원본 속성·편집 시각·경로·본문은 [보충 스냅샷](recovered-source-snapshots.jsonl.gz)에 보존. Notion URL은 원본 ID 표기로 정규화했으며 원본 본문의 SHA-256도 기록.
- 이미지 태그 274개를 Markdown 상대 경로로 변환. 추가 원본 이미지 16개 저장.
- 내용이 다른 8개는 아래와 같이 보존·대조. 원본 보존 완료와 현행 전송 계약 확정은 별도. 기존 생성용 specs 및 강제 업데이트 DA1 규칙은 변경하지 않음.
- 전체 DB 숨김 행의 총수와 모든 이미지의 UI 일치는 여전히 미확인. 87개 복구를 전체 Notion 이전 완료로 해석하지 않음.

## 차이 8개

첫 네 개는 설명/값/정의 차이, 뒤 네 개는 주요 여섯 필드가 같고 이미지 연결이 다른 경우입니다.

### 11-5.분실물_습득물신고_삭제_클릭

[복구 원본](pages/3c00221954bc835f816d8121b59607eb.md) · [기존 보관본](pages/eb20221954bc832981c081c4c9f7b5ce.md)

원본의 value "삭제"를 원본 복구 페이지에 보존. 기존 보관본의 분실물/습득물 값 및 검토 기록도 유지. 동일한 계약이라고 합치거나 어느 값을 현행 전송값으로 자동 확정하지 않음.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 글 작성자가 습득물 신고 게시물에서 삭제버튼을 클릭 | 글 작성자가 습득물 신고 게시물에서 삭제버튼을 클릭. 글 종류에 따라 value를 달리 해주시면 감사하겠습니다.<br>글 작성자가 습득물 신고 게시물에서 삭제버튼을 클릭. |
| screen_view |  | lost_item_detail |
| event_name |  | DA2 |
| event_label | "find_user_delete" | "find_user_delete"<br>board__lost_item_detail__lost_item_delete__open__click |
| value | "삭제" | '분실물' or '습득물'<br>분실물 / 습득물 |
| event_category | "click" | "click"<br>click |

원본 이미지 참조 3개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 0개는 복구 원본 페이지에 연결했습니다.

### 1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서  1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)

[복구 원본](pages/3df0221954bc833a9f6381766084d23b.md) · [기존 보관본](pages/7090221954bc828fa8bc813fab79d534.md)

원본의 WEB 리디자인 설명과 cafeteria__main__more__click 및 기존 플랫폼 정의를 원본 ID에 함께 보존. 같은 제목인 기존 레거시 보관본도 유지. 원본 이미지 4개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 메인화면에서 더보기 버튼 클릭<br>WEB 리디자인에서는 홈 '오늘 식단' 영역의 '전체보기'를 클릭해 식단 페이지로 진입하는 경우. ANDROID·IOS는 기존 메인 식단 위젯(오늘 식단 / 내일 식단) 클릭 정의를 유지한다. | 메인화면에서 더보기 버튼 클릭 |
| screen_view | main |  |
| event_name | DA1 |  |
| event_label | "main_menu_moveDetailView"<br>cafeteria__main__more__click | "main_menu_moveDetailView" |
| value | "오늘 식단, 내일 식단"<br>\{아침, 점심, 저녁\}_더보기 (예: 점심_더보기) | "오늘 식단, 내일 식단" |
| event_category | "click"<br>click | "click" |

원본 이미지 참조 6개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 4개는 복구 원본 페이지에 연결했습니다.

### 1-2.메인_식단_클릭

[복구 원본](pages/77e0221954bc82b7b9030139d648368f.md) · [기존 보관본](pages/5a80221954bc8265a92e01bcddeea491.md)

원본의 카드 본문 클릭 설명·제외 조건·플랫폼 검토사항을 별도 보존. 기존 레거시 페이지와 이미지 연계를 유지하며 원본의 이미지 참조도 복원.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 메인화면에서 식단 칸 클릭<br>홈의 일반 식단 카드 본문을 눌러 식단 페이지로 진입할 때 기록한다. 전체보기·더보기 버튼, 코너 선택, 카드 단순 노출은 포함하지 않는다. 구 WEB의 오늘·내일 식단 제목 버튼과 iOS 빈 상태 안내 카드는 검토사항의 별도 경로를 따른다. | 메인화면에서 식단 칸 클릭<br>홈의 일반 식단 카드 본문을 눌러 식단 페이지로 진입할 때 기록한다. PC 웹의 식단 제목, 전체보기·더보기 버튼, 코너 선택, 카드 단순 노출은 포함하지 않는다. 구 WEB의 오늘·내일 식단 제목 버튼과 iOS 빈 상태 안내 카드는 검토사항의 별도 경로를 따른다. |
| screen_view | main | main |
| event_name | DA1 | DA1 |
| event_label | "main_menu_moveDetailView"<br>cafeteria__main__meal__click | "main_menu_moveDetailView"<br>cafeteria__main__meal__click |
| value | "오늘 식단, 내일 식단"<br>아침 / 점심 / 저녁 (예: 점심) | "오늘 식단, 내일 식단"<br>아침 / 점심 / 저녁 (예: 점심) |
| event_category | "click"<br>click | "click"<br>click |

원본 이미지 참조 4개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 1개는 복구 원본 페이지에 연결했습니다.

### 1-3.메인_식단_A코너_클릭 (레거시)

[복구 원본](pages/1560221954bc83afacc8015e25700762.md) · [기존 보관본](pages/c250221954bc8318b85201e8c22f915d.md)

원본의 cafeteria__main__corner__select와 코너 값, 1-3~1-7 통합 이유를 보존. 기존 A코너 레거시 정의를 대체하지 않음. 원본 이미지 4개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 메인화면에서 A코너 버튼 클릭<br>메인 화면 식단 위젯에서 코너 버튼(A코너 / B코너 / C코너 / 능수관 / 2캠퍼스)을 눌러 보이는 코너를 바꾸는 경우 (식단 화면으로 이동하지 않음). 1-3~1-7 코너별 페이지를 이 라벨 하나로 합침 | 메인화면에서 A코너 버튼 클릭 |
| screen_view | main |  |
| event_name | DA1 |  |
| event_label | "main_menu_corner"<br>cafeteria__main__corner__select | "main_menu_corner" |
| value | "A코너"<br>\{코너\} → A코너 / B코너 / C코너 / 능수관 / 2캠퍼스 (예: B코너) | "A코너" |
| event_category | "click"<br>select | "click" |

원본 이미지 참조 6개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 4개는 복구 원본 페이지에 연결했습니다.

### 2-1. 헤더_식단_클릭

[복구 원본](pages/3ab0221954bc8252aa2a8162a7fecc97.md) · [기존 보관본](pages/d160221954bc83abb8618181d83f8ae1.md)

여섯 주요 필드는 유사 보관본과 일치. 원본 ID별 이미지 연결을 보존하고 누락 이미지 1개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 웹 상단 헤더에서 식단을 클릭해 식단 화면으로 들어가는 경우 | 웹 상단 헤더에서 식단을 클릭해 식단 화면으로 들어가는 경우 |
| screen_view | header | header |
| event_name | DA1 | DA1 |
| event_label | "header"<br>cafeteria__header__cafeteria_entry__header_entry__click | "header"<br>cafeteria__header__cafeteria_entry__header_entry__click |
| value | "식단"<br>식단 | "식단"<br>식단 |
| event_category | "click"<br>click | "click"<br>click |

원본 이미지 참조 3개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 1개는 복구 원본 페이지에 연결했습니다.

### 2-2. 푸터_식단_클릭

[복구 원본](pages/ea00221954bc82db852e810195c314ce.md) · [기존 보관본](pages/5db0221954bc82bd9ef801061752b129.md)

여섯 주요 필드는 유사 보관본과 일치. 원본 ID별 이미지 연결을 보존하고 누락 이미지 2개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 웹 하단 푸터에서 식단을 클릭해 식단 화면으로 들어가는 경우 | 웹 하단 푸터에서 식단을 클릭해 식단 화면으로 들어가는 경우 |
| screen_view | footer | footer |
| event_name | DA1 | DA1 |
| event_label | "footer"<br>cafeteria__footer__cafeteria_entry__footer_entry__click | "footer"<br>cafeteria__footer__cafeteria_entry__footer_entry__click |
| value | "식단"<br>식단 | "식단"<br>식단 |
| event_category | "click"<br>click | "click"<br>click |

원본 이미지 참조 4개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 2개는 복구 원본 페이지에 연결했습니다.

### 3-4. 식단_아침_스크롤

[복구 원본](pages/dc00221954bc83f5923e01ff8270898e.md) · [기존 보관본](pages/51f0221954bc821cb2648147bef8d890.md)

여섯 주요 필드는 유사 보관본과 일치. 원본 ID별 이미지 연결을 보존하고 누락 이미지 4개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 식단 페이지에서 아침 식사 부분에서 스크롤<br>식단 화면에서 선택된 식사 시간(아침 / 점심 / 저녁)의 식단 목록을 스크롤하는 경우 (기존 3-4·3-5·3-6을 하나로 통합) | 식단 페이지에서 아침 식사 부분에서 스크롤<br>식단 화면에서 선택된 식사 시간(아침 / 점심 / 저녁)의 식단 목록을 스크롤하는 경우 (기존 3-4·3-5·3-6을 하나로 통합) |
| screen_view | cafeteria | cafeteria |
| event_name | DA1 | DA1 |
| event_label | "menu_time"<br>cafeteria__cafeteria__meal_time__scroll | "menu_time"<br>cafeteria__cafeteria__meal_time__scroll |
| value | "아침"<br>\{식사 시간\} (예: 점심) | "아침"<br>\{식사 시간\} (예: 점심) |
| event_category | "scroll"<br>scroll | "scroll"<br>scroll |

원본 이미지 참조 9개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 4개는 복구 원본 페이지에 연결했습니다.

### 3-9. (Android / iOS) 식단_카카오톡_코인이동_클릭 (카카오톡)

[복구 원본](pages/75a0221954bc8271ad76810365b94708.md) · [기존 보관본](pages/7b80221954bc826aa9ea01960bfe1fa6.md)

여섯 주요 필드는 유사 보관본과 일치. 카카오톡 경로와 원본 ID별 이미지 연결을 보존하고 누락 이미지 1개 추가.

| 필드 | 복구 원본 | 기존 유사 보관본 |
| --- | --- | --- |
| 설명 | 카톡으로 공유받은 식단 클릭<br>카카오톡으로 공유받은 식단 메시지에서 코인으로 이동을 눌러 앱 식단 화면으로 들어오는 경우 (기존에는 공유하기와 같은 라벨이라 분리) | 카톡으로 공유받은 식단 클릭<br>카카오톡으로 공유받은 식단 메시지에서 코인으로 이동을 눌러 앱 식단 화면으로 들어오는 경우 (기존에는 공유하기와 같은 라벨이라 분리) |
| screen_view | from_external | from_external |
| event_name | DA1 | DA1 |
| event_label | "menu_share"<br>cafeteria__from_external__cafeteria_entry__kakao_entry__click | "menu_share"<br>cafeteria__from_external__cafeteria_entry__kakao_entry__click |
| value | "코인으로 이동"<br>코인으로 이동 | "코인으로 이동"<br>코인으로 이동 |
| event_category | "click"<br>click | "click"<br>click |

원본 이미지 참조 2개. 기존 유사 문서에서 같은 ID 참조를 찾지 못했던 이미지 1개는 복구 원본 페이지에 연결했습니다.

## 복구 원본 전체 목록

| 제목 | 분류 | 관련 기존 보관본 |
| --- | --- | --- |
| [5-1. 목록_클릭](pages/2450221954bc824b8c1501a6f4961576.md) | fields_and_images_preserved_elsewhere | [2360221954bc83dfb2d90130f46b6687](pages/2360221954bc83dfb2d90130f46b6687.md), [4710221954bc82bdad73016b2c6063d9](pages/4710221954bc82bdad73016b2c6063d9.md) |
| [11-12.분실물_쪽지보내기_클릭](pages/87f0221954bc83329ea20157407117c2.md) | fields_and_images_preserved_elsewhere | [4760221954bc8274b5018173d2ab4000](pages/4760221954bc8274b5018173d2ab4000.md), [aea0221954bc8206b8b581461a538965](pages/aea0221954bc8206b8b581461a538965.md) |
| [6-1. 공지글 검색_클릭](pages/4db0221954bc826a8e4a01e906afb1d3.md) | fields_and_images_preserved_elsewhere | [5380221954bc8311a35201f0d32fa591](pages/5380221954bc8311a35201f0d32fa591.md), [cec0221954bc83fb80878101caf9ec11](pages/cec0221954bc83fb80878101caf9ec11.md) |
| [10-2. 푸터_교내 시설물 정보_클릭](pages/f6e0221954bc833d9d9d013f3cbb39ac.md) | fields_and_images_preserved_elsewhere | [c150221954bc826fad8901fadcc63f5c](pages/c150221954bc826fad8901fadcc63f5c.md), [ab30221954bc824897f5816b1fdd50b1](pages/ab30221954bc824897f5816b1fdd50b1.md) |
| [2-3. 햄버거_공지사항_클릭](pages/7c70221954bc8230b18881a41f98de50.md) | fields_and_images_preserved_elsewhere | [b0e0221954bc837f84bd01e0768a57c0](pages/b0e0221954bc837f84bd01e0768a57c0.md), [d300221954bc8330be2381687a8f27c1](pages/d300221954bc8330be2381687a8f27c1.md) |
| [7-2. 모두 보기_클릭](pages/cbd0221954bc83e599ff0186188117c9.md) | fields_and_images_preserved_elsewhere | [c300221954bc8351b17281f7cf5fc9db](pages/c300221954bc8351b17281f7cf5fc9db.md), [1280221954bc83fc9b0d01305e66e95b](pages/1280221954bc83fc9b0d01305e66e95b.md) |
| [9-1. 키워드 게시물_알림](pages/eec0221954bc83d9b7dd01b72ab8a850.md) | fields_and_images_preserved_elsewhere | [aaa0221954bc838ea10c811589bcdcf6](pages/aaa0221954bc838ea10c811589bcdcf6.md), [1440221954bc83988396811229e6f2a9](pages/1440221954bc83988396811229e6f2a9.md) |
| [5-3. 공지 원본 바로가기_클릭](pages/d1f0221954bc8296bea981977a0fa02a.md) | fields_and_images_preserved_elsewhere | [f670221954bc83c085d78119d5417ee6](pages/f670221954bc83c085d78119d5417ee6.md), [6010221954bc83d88650811c9b177501](pages/6010221954bc83d88650811c9b177501.md) |
| [11-13.분실물_신고하기_클릭](pages/a460221954bc828aad4e81e89cdd8a62.md) | fields_and_images_preserved_elsewhere | [a190221954bc82e2afc801bed93a741d](pages/a190221954bc82e2afc801bed93a741d.md), [c050221954bc821db0610121570a8c2c](pages/c050221954bc821db0610121570a8c2c.md) |
| [7-5. 추천 키워드_클릭](pages/74e0221954bc83928a03015a663d795a.md) | fields_and_images_preserved_elsewhere | [fda0221954bc8236ac64815e90e52edf](pages/fda0221954bc8236ac64815e90e52edf.md), [d3c0221954bc82b384f6018365f7f75c](pages/d3c0221954bc82b384f6018365f7f75c.md) |
| [3-4. 공지사항_새로운 서비스 요청하기_클릭](pages/8290221954bc835b9e7d0178b0eece5b.md) | fields_and_images_preserved_elsewhere | [ea70221954bc831d915c812085433be2](pages/ea70221954bc831d915c812085433be2.md), [ce30221954bc8291add801436cdffe73](pages/ce30221954bc8291add801436cdffe73.md) |
| [11-2.분실물_습득물신고_품목선택_클릭](pages/67d0221954bc829aa31d01b4fdcd7e90.md) | fields_and_images_preserved_elsewhere | [9d60221954bc83179e308165f4f53b4b](pages/9d60221954bc83179e308165f4f53b4b.md), [01c0221954bc836fa76c01c9487cd249](pages/01c0221954bc836fa76c01c9487cd249.md) |
| [3-2. 공지사항_코리아텍 바로가기_클릭](pages/4bd0221954bc830fbf8081c34c639eec.md) | fields_and_images_preserved_elsewhere | [3770221954bc82b1be09010ad7e36c85](pages/3770221954bc82b1be09010ad7e36c85.md), [30c0221954bc83e9b620818e1ae2d53b](pages/30c0221954bc83e9b620818e1ae2d53b.md) |
| [4-2. 공지사항 페이지_스크롤(상하)](pages/12e0221954bc8211966b01131cfa2859.md) | fields_and_images_preserved_elsewhere | [efc0221954bc8273b8a2818c876a2797](pages/efc0221954bc8273b8a2818c876a2797.md), [eef0221954bc83b3bf318176737e00a6](pages/eef0221954bc83b3bf318176737e00a6.md) |
| [5-2. 인기있는 공지_클릭](pages/3a60221954bc8200948081e81db8d86e.md) | fields_and_images_preserved_elsewhere | [9aa0221954bc82329de68138e08a8e91](pages/9aa0221954bc82329de68138e08a8e91.md), [a130221954bc8344a21a01c1ebb158b0](pages/a130221954bc8344a21a01c1ebb158b0.md) |
| [7-3. 새 키워드 추가_클릭](pages/9360221954bc83e49c8781b4784d4d2b.md) | fields_and_images_preserved_elsewhere | [a510221954bc8243963c01d45432380b](pages/a510221954bc8243963c01d45432380b.md), [9f20221954bc82f29d99013b23a78bb6](pages/9f20221954bc82f29d99013b23a78bb6.md) |
| [11-1.분실물_글쓰기_클릭](pages/d860221954bc839197140166ccb6103b.md) | fields_and_images_preserved_elsewhere | [57d0221954bc83f4b9d601b04f6c3eab](pages/57d0221954bc83f4b9d601b04f6c3eab.md), [cd10221954bc822899d7010ce7df27d1](pages/cd10221954bc822899d7010ce7df27d1.md) |
| [8-2. 지금 인기있는 공지 배너_클릭](pages/cbe0221954bc83678267011afd394fad.md) | fields_and_images_preserved_elsewhere | [e450221954bc82908813819138dad6c1](pages/e450221954bc82908813819138dad6c1.md), [1850221954bc83628ec401191156b73c](pages/1850221954bc83628ec401191156b73c.md) |
| [2-2. 푸터_공지사항_클릭](pages/d090221954bc82ef91ed81fe49980a28.md) | fields_and_images_preserved_elsewhere | [e280221954bc833ba2d5010881c890de](pages/e280221954bc833ba2d5010881c890de.md), [0a90221954bc82898d4d8125f9edc616](pages/0a90221954bc82898d4d8125f9edc616.md) |
| [7-6. 로그인팝업_로그인하기_클릭](pages/5e90221954bc83e58d6081e9c4b7bddd.md) | fields_and_images_preserved_elsewhere | [c7a0221954bc83ee9e1901da1fb01906](pages/c7a0221954bc83ee9e1901da1fb01906.md), [92b0221954bc8351ac0601705df4922d](pages/92b0221954bc8351ac0601705df4922d.md) |
| [3-1. 공지사항_가장 많이 본 게시물_클릭](pages/7d60221954bc82b6a55f8114a2a39a9b.md) | fields_and_images_preserved_elsewhere | [9b30221954bc82ee8b3f0131e5765de0](pages/9b30221954bc82ee8b3f0131e5765de0.md), [7660221954bc83098e7a81419ceec56f](pages/7660221954bc83098e7a81419ceec56f.md), [8b40221954bc832b99b98183f121b2cc](pages/8b40221954bc832b99b98183f121b2cc.md), [1d30221954bc82458de78134c112d361](pages/1d30221954bc82458de78134c112d361.md) |
| [11-4.분실물_습득물신고_작성완료_클릭](pages/1b10221954bc832b8752812eb3aaa340.md) | fields_and_images_preserved_elsewhere | [35d0221954bc838c872c8173f1d6171a](pages/35d0221954bc838c872c8173f1d6171a.md), [ba70221954bc83ea9da38144dc40788d](pages/ba70221954bc83ea9da38144dc40788d.md) |
| [새 페이지](pages/c1d0221954bc83878081014211eaac7c.md) | empty_page | [4970221954bc829a950681f7c1ef78db](pages/4970221954bc829a950681f7c1ef78db.md), [8cc0221954bc825db3f9017791290291](pages/8cc0221954bc825db3f9017791290291.md), [00a0221954bc837e830881248b6c5502](pages/00a0221954bc837e830881248b6c5502.md), [37d0221954bc82d390d781f04dd23c7b](pages/37d0221954bc82d390d781f04dd23c7b.md) |
| [3-5. 공지사항_BCSD Lab 알아보기_클릭](pages/fde0221954bc83c29ad801f853c20ed3.md) | fields_and_images_preserved_elsewhere | [9ee0221954bc839f8822816a84a06a79](pages/9ee0221954bc839f8822816a84a06a79.md), [b3e0221954bc82dcac480102ed53aa31](pages/b3e0221954bc82dcac480102ed53aa31.md) |
| [7-7. 로그인팝업_닫기_클릭](pages/0be0221954bc8390a68901cd61c14820.md) | fields_and_images_preserved_elsewhere | [c490221954bc83a4970701122aa95033](pages/c490221954bc83a4970701122aa95033.md), [3dc0221954bc8212999901a990961940](pages/3dc0221954bc8212999901a990961940.md) |
| [11-9.분실물_분실물신고_품목선택_클릭](pages/35c0221954bc8387b86f01410d4c06e7.md) | fields_and_images_preserved_elsewhere | [f930221954bc8248a881019231c98461](pages/f930221954bc8248a881019231c98461.md), [76f0221954bc82558fa501024dbd0c83](pages/76f0221954bc82558fa501024dbd0c83.md) |
| [2-1. 헤더_공지사항_클릭](pages/b9f0221954bc82f1a11c8114101c6b39.md) | fields_and_images_preserved_elsewhere | [c6e0221954bc83ab9b86018800c682ad](pages/c6e0221954bc83ab9b86018800c682ad.md), [1ef0221954bc831ab54781d65126045e](pages/1ef0221954bc831ab54781d65126045e.md) |
| [3-3. 공지사항_아우누리 바로가기_클릭](pages/3310221954bc83f48d500138f0d9b2a6.md) | fields_and_images_preserved_elsewhere | [a460221954bc82aa8e1881676f81d484](pages/a460221954bc82aa8e1881676f81d484.md), [d540221954bc83ba95c7015aa20d2937](pages/d540221954bc83ba95c7015aa20d2937.md) |
| [11-10.분실물_분실물신고_물품추가_클릭](pages/2a10221954bc82a5bd43813af587afdc.md) | fields_and_images_preserved_elsewhere | [d1e0221954bc8256aa1381a13a98a332](pages/d1e0221954bc8256aa1381a13a98a332.md), [36f0221954bc837c87c001c99b06e9f6](pages/36f0221954bc837c87c001c99b06e9f6.md) |
| [11-11.분실물_분실물신고_작성완료_클릭](pages/5210221954bc82468b3d0197ae387fd6.md) | fields_and_images_preserved_elsewhere | [9f00221954bc83a59b7b81fce0b079f0](pages/9f00221954bc83a59b7b81fce0b079f0.md), [6b40221954bc8318aa0981a19910b6a7](pages/6b40221954bc8318aa0981a19910b6a7.md) |
| [8-1. 더보기_클릭](pages/14f0221954bc83e092950105fc8e4bc2.md) | fields_and_images_preserved_elsewhere | [0d70221954bc8297bbe48128dcf74499](pages/0d70221954bc8297bbe48128dcf74499.md), [e2e0221954bc839b917881b69ef3a9e8](pages/e2e0221954bc839b917881b69ef3a9e8.md) |
| [7-1. 키워드 관리_클릭](pages/6a30221954bc838285eb81810120abd5.md) | fields_and_images_preserved_elsewhere | [fc10221954bc83ae903381da469052e9](pages/fc10221954bc83ae903381da469052e9.md), [21b0221954bc83df9625811c79c56819](pages/21b0221954bc83df9625811c79c56819.md) |
| [8-3. 키워드 관리 진입 배너_클릭](pages/de10221954bc8300b30d8107e140ad3e.md) | fields_and_images_preserved_elsewhere | [fa20221954bc8295ab7101d34c0e80c9](pages/fa20221954bc8295ab7101d34c0e80c9.md), [4bf0221954bc83c78b7081fd636e4039](pages/4bf0221954bc83c78b7081fd636e4039.md) |
| [6-2. 많이 검색되는 키워드_클릭](pages/2920221954bc839a967901009c062649.md) | fields_and_images_preserved_elsewhere | [aca0221954bc82c1b591815722e03b52](pages/aca0221954bc82c1b591815722e03b52.md), [5570221954bc8242ad13016e7163ad53](pages/5570221954bc8242ad13016e7163ad53.md) |
| [4-1. 탭 메뉴바_클릭](pages/6f80221954bc83aba7a6013fe9d9dfc3.md) | fields_and_images_preserved_elsewhere | [52b0221954bc833bb32a018370533c49](pages/52b0221954bc833bb32a018370533c49.md), [f380221954bc83319946015c7d177803](pages/f380221954bc83319946015c7d177803.md) |
| [11-16.쪽지리스트_대화창_클릭](pages/3d30221954bc8340af35815fad5295d0.md) | fields_and_images_preserved_elsewhere | [d830221954bc82c6a9cb01cafff6884f](pages/d830221954bc82c6a9cb01cafff6884f.md), [cb20221954bc8335977e012e2347e4ee](pages/cb20221954bc8335977e012e2347e4ee.md) |
| [11-6.분실물_습득물신고_삭제확인_클릭](pages/4e90221954bc832cb85f81b714e29903.md) | fields_and_images_preserved_elsewhere | [9170221954bc83f2851481fa2a35103c](pages/9170221954bc83f2851481fa2a35103c.md), [1bb0221954bc82a5969f811385bd96b5](pages/1bb0221954bc82a5969f811385bd96b5.md) |
| [7-8. 키워드 알림받기_토글](pages/a2d0221954bc8348921281e04f3f75c5.md) | fields_and_images_preserved_elsewhere | [6980221954bc839e8d5581928e4ca5c0](pages/6980221954bc839e8d5581928e4ca5c0.md), [b190221954bc83039ca4016d14761051](pages/b190221954bc83039ca4016d14761051.md) |
| [10-1. 헤더_교내 시설물 정보_클릭](pages/6ce0221954bc83a8bd120133314da21e.md) | fields_and_images_preserved_elsewhere | [5500221954bc8259a82b0163fc55fa7c](pages/5500221954bc8259a82b0163fc55fa7c.md), [1290221954bc8311bea00172cdc03d3a](pages/1290221954bc8311bea00172cdc03d3a.md) |
| [7-9. 알림설정_공지사항 키워드 알림_클릭](pages/af30221954bc83cf83db0147d223ce81.md) | fields_and_images_preserved_elsewhere | [44b0221954bc83669fd4013b52482bfb](pages/44b0221954bc83669fd4013b52482bfb.md), [bc70221954bc82ebb8a001134a251684](pages/bc70221954bc82ebb8a001134a251684.md) |
| [11-7.분실물_잃어버렸어요_클릭](pages/f810221954bc83d0809e01628492c45e.md) | fields_and_images_preserved_elsewhere | [a950221954bc82baaea681c164cecea6](pages/a950221954bc82baaea681c164cecea6.md), [2930221954bc83208259814d626d19f4](pages/2930221954bc83208259814d626d19f4.md) |
| [6-3. [검색 키워드] 입력값 >> DB저장](pages/24f0221954bc83f8bb4f81a9445c3c8d.md) | empty_page | [7c30221954bc832ab4ec012abb278477](pages/7c30221954bc832ab4ec012abb278477.md), [65b0221954bc8262a13801a3da7ac8e2](pages/65b0221954bc8262a13801a3da7ac8e2.md) |
| [11-8.분실물_주인을찾아요_클릭](pages/93e0221954bc829a9dd00113c5de6123.md) | fields_and_images_preserved_elsewhere | [a950221954bc82baaea681c164cecea6](pages/a950221954bc82baaea681c164cecea6.md), [2930221954bc83208259814d626d19f4](pages/2930221954bc83208259814d626d19f4.md) |
| [11-15.햄버거_쪽지_클릭](pages/b6a0221954bc82a5b60a8120f0d08237.md) | fields_and_images_preserved_elsewhere | [0dc0221954bc8316be7a815e4460791f](pages/0dc0221954bc8316be7a815e4460791f.md), [f330221954bc83579bf5816e70758bb1](pages/f330221954bc83579bf5816e70758bb1.md) |
| [6-4. 공지글 검색_검색하기_클릭](pages/e070221954bc8233817181646b5e6df1.md) | fields_and_images_preserved_elsewhere | [82b0221954bc8273abbe81b4fc39095e](pages/82b0221954bc8273abbe81b4fc39095e.md), [9ee0221954bc8247badd01d88c248db9](pages/9ee0221954bc8247badd01d88c248db9.md) |
| [새 페이지](pages/79f0221954bc821ab0108136b0cb721e.md) | empty_page | [4970221954bc829a950681f7c1ef78db](pages/4970221954bc829a950681f7c1ef78db.md), [8cc0221954bc825db3f9017791290291](pages/8cc0221954bc825db3f9017791290291.md), [00a0221954bc837e830881248b6c5502](pages/00a0221954bc837e830881248b6c5502.md), [37d0221954bc82d390d781f04dd23c7b](pages/37d0221954bc82d390d781f04dd23c7b.md) |
| [11-14.분실물_게시글신고하기_신고하기_클릭](pages/5bc0221954bc83588753017d0bdae4ff.md) | fields_and_images_preserved_elsewhere | [ad60221954bc8236855581b2e7057454](pages/ad60221954bc8236855581b2e7057454.md), [ea90221954bc8334a6f301da1af7a7ae](pages/ea90221954bc8334a6f301da1af7a7ae.md) |
| [11-17.헤더_쪽지_클릭](pages/84c0221954bc825ea826812c72c0eb8d.md) | fields_and_images_preserved_elsewhere | [6610221954bc83c794e60155ecc5d6fc](pages/6610221954bc83c794e60155ecc5d6fc.md), [84c0221954bc820392b5018ecce7d80a](pages/84c0221954bc820392b5018ecce7d80a.md) |
| [10-3. 햄버거_교내 시설물 정보_클릭](pages/96d0221954bc82e38b8601cfacc06256.md) | fields_and_images_preserved_elsewhere | [9750221954bc822c80b3810a4c62bba8](pages/9750221954bc822c80b3810a4c62bba8.md), [13a0221954bc82fa9bed81d79975357f](pages/13a0221954bc82fa9bed81d79975357f.md) |
| [11-3.분실물_습득물신고_물품추가_클릭](pages/6b00221954bc827c856a0175553bf08c.md) | fields_and_images_preserved_elsewhere | [bb30221954bc83a0aba1015810eb5709](pages/bb30221954bc83a0aba1015810eb5709.md), [4890221954bc82ba95db01b93ecfeea0](pages/4890221954bc82ba95db01b93ecfeea0.md) |
| [11-19.푸터_쪽지_클릭](pages/8f40221954bc82bdba648191e2954c8e.md) | fields_and_images_preserved_elsewhere | [1a70221954bc83408a1381789c552b4f](pages/1a70221954bc83408a1381789c552b4f.md), [05d0221954bc82c8a85b8139b750cbb8](pages/05d0221954bc82c8a85b8139b750cbb8.md) |
| [7-4. [알림받을 키워드] 입력값 >> DB저장](pages/1aa0221954bc83ec8ad301c1d54bb2f4.md) | text_preserved_elsewhere | [e0c0221954bc83d2b094017a952ec735](pages/e0c0221954bc83d2b094017a952ec735.md) |
| [11-18.분실물_게시물종류_클릭](pages/c900221954bc827daf8a81b63360cb8c.md) | fields_and_images_preserved_elsewhere | [e7c0221954bc82e194200103d9b04e18](pages/e7c0221954bc82e194200103d9b04e18.md), [bd00221954bc82628f2e01006b5fd031](pages/bd00221954bc82628f2e01006b5fd031.md) |
| [11-5.분실물_습득물신고_삭제_클릭](pages/3c00221954bc835f816d8121b59607eb.md) | needs_content_review | [eb20221954bc832981c081c4c9f7b5ce](pages/eb20221954bc832981c081c4c9f7b5ce.md), [b4d0221954bc8391b13f010fc3d6a83f](pages/b4d0221954bc8391b13f010fc3d6a83f.md), [1190221954bc83939928017b5b644090](pages/1190221954bc83939928017b5b644090.md), [15e0221954bc835a969901001f9897ae](pages/15e0221954bc835a969901001f9897ae.md) |
| [2-1 가게 정보 수정](pages/a380221954bc833eba8081e730085961.md) | fields_and_images_preserved_elsewhere | [ba10221954bc82949df8014e7c173c89](pages/ba10221954bc82949df8014e7c173c89.md) |
| [2-2 가게 정보 수정 - 확인](pages/4bd0221954bc8387b0f481849725421a.md) | fields_and_images_preserved_elsewhere | [8f60221954bc838bb94801fe9da49bd7](pages/8f60221954bc838bb94801fe9da49bd7.md) |
| [2-3 가게 정보 수정 - 시간 수정 ](pages/0c80221954bc833095a881666fb2b657.md) | fields_and_images_preserved_elsewhere | [bb00221954bc82ea86b18188d013eb8c](pages/bb00221954bc82ea86b18188d013eb8c.md) |
| [2-4 가게 정보 수정 - 이미지 추가 ](pages/dd30221954bc836a86b881430dc548be.md) | fields_and_images_preserved_elsewhere | [5fc0221954bc83278bde019a22c5d462](pages/5fc0221954bc83278bde019a22c5d462.md) |
| [2-5 가게 정보 수정 - 취소 ](pages/a0a0221954bc82189a08815020757a91.md) | fields_and_images_preserved_elsewhere | [8360221954bc836c8c650163d19c77e6](pages/8360221954bc836c8c650163d19c77e6.md) |
| [2-6 가게 정보 수정 - 닫기 ](pages/5470221954bc82058c3e01c7314a0e2b.md) | fields_and_images_preserved_elsewhere | [f870221954bc82319aa1819f58ae8b05](pages/f870221954bc82319aa1819f58ae8b05.md) |
| [3-1 메뉴추가 ](pages/d740221954bc832f896e814a681758c8.md) | fields_and_images_preserved_elsewhere | [6010221954bc822fad650108832d38f4](pages/6010221954bc822fad650108832d38f4.md) |
| [3-2 메뉴추가 - 확인](pages/7e90221954bc826d9a6e01b6d8446089.md) | fields_and_images_preserved_elsewhere | [c1e0221954bc82f081088170326fde2e](pages/c1e0221954bc82f081088170326fde2e.md) |
| [3-3 메뉴추가 - 취소](pages/d2a0221954bc8342ad4981c2b2799f2f.md) | fields_and_images_preserved_elsewhere | [c840221954bc82f6ac96814ed5b53c23](pages/c840221954bc82f6ac96814ed5b53c23.md) |
| [3-4 메뉴추가 - 메뉴사진](pages/4030221954bc82c8a1030122f97693f3.md) | fields_and_images_preserved_elsewhere | [7a20221954bc82a3ba17013c053c01d9](pages/7a20221954bc82a3ba17013c053c01d9.md) |
| [[레거시] 메인_식단_더보기버튼_클릭(확인필요)](pages/9990221954bc832e91d3018d74d3477a.md) | fields_and_images_preserved_elsewhere | [3d50221954bc8228a8ed81c51f8aa5d6](pages/3d50221954bc8228a8ed81c51f8aa5d6.md) |
| [1-1.메인_식단_더보기버튼_클릭 (홈화면 리디자인 로깅으로 찍히고 있음) → 따라서  1-1부터 1-7까지 전부 다 수정할 필요 없음 (레거시)](pages/3df0221954bc833a9f6381766084d23b.md) | needs_content_review | [7090221954bc828fa8bc813fab79d534](pages/7090221954bc828fa8bc813fab79d534.md), [3d50221954bc8228a8ed81c51f8aa5d6](pages/3d50221954bc8228a8ed81c51f8aa5d6.md), [5a80221954bc8265a92e01bcddeea491](pages/5a80221954bc8265a92e01bcddeea491.md), [1f10221954bc82f6a17401f823455276](pages/1f10221954bc82f6a17401f823455276.md) |
| [1-2.메인_식단_클릭](pages/77e0221954bc82b7b9030139d648368f.md) | needs_content_review | [5a80221954bc8265a92e01bcddeea491](pages/5a80221954bc8265a92e01bcddeea491.md), [3d50221954bc8228a8ed81c51f8aa5d6](pages/3d50221954bc8228a8ed81c51f8aa5d6.md), [f450221954bc8321ab2e8140e800c375](pages/f450221954bc8321ab2e8140e800c375.md), [1e10221954bc8268a989013ec93c6966](pages/1e10221954bc8268a989013ec93c6966.md) |
| [1-3.메인_식단_A코너_클릭 (레거시)](pages/1560221954bc83afacc8015e25700762.md) | needs_content_review | [c250221954bc8318b85201e8c22f915d](pages/c250221954bc8318b85201e8c22f915d.md), [3220221954bc83549c970136b8786c33](pages/3220221954bc83549c970136b8786c33.md), [03a0221954bc82988da80160ab26ee4c](pages/03a0221954bc82988da80160ab26ee4c.md), [1830221954bc82da965501008d23f1f3](pages/1830221954bc82da965501008d23f1f3.md) |
| [1-4.메인_식단_B코너_클릭](pages/5b00221954bc82988ba401c3aff2571a.md) | fields_and_images_preserved_elsewhere | [f710221954bc8339b99a01063004ac17](pages/f710221954bc8339b99a01063004ac17.md) |
| [1-5.메인_식단_C코너_클릭](pages/a5e0221954bc83a9bbbf013df21f523a.md) | fields_and_images_preserved_elsewhere | [d360221954bc8393ac29812a0a2efd7a](pages/d360221954bc8393ac29812a0a2efd7a.md) |
| [1-6.메인_식단_능수관_클릭](pages/9b90221954bc82a6957101e87e1224c4.md) | fields_and_images_preserved_elsewhere | [b4d0221954bc8339aaa881e1205affec](pages/b4d0221954bc8339aaa881e1205affec.md) |
| [1-7.메인_식단_2캠퍼스_클릭](pages/1ae0221954bc834388268145704074e0.md) | fields_and_images_preserved_elsewhere | [15e0221954bc835a969901001f9897ae](pages/15e0221954bc835a969901001f9897ae.md) |
| [2-1. 헤더_식단_클릭](pages/3ab0221954bc8252aa2a8162a7fecc97.md) | needs_content_review | [d160221954bc83abb8618181d83f8ae1](pages/d160221954bc83abb8618181d83f8ae1.md), [5db0221954bc82bd9ef801061752b129](pages/5db0221954bc82bd9ef801061752b129.md), [86c0221954bc8205af0a0111a26a89d9](pages/86c0221954bc8205af0a0111a26a89d9.md), [c630221954bc82e48ff8810a80d6f1f0](pages/c630221954bc82e48ff8810a80d6f1f0.md) |
| [2-2. 푸터_식단_클릭](pages/ea00221954bc82db852e810195c314ce.md) | needs_content_review | [5db0221954bc82bd9ef801061752b129](pages/5db0221954bc82bd9ef801061752b129.md), [d160221954bc83abb8618181d83f8ae1](pages/d160221954bc83abb8618181d83f8ae1.md), [ec80221954bc835b8b0b81b7005069a3](pages/ec80221954bc835b8b0b81b7005069a3.md), [7bb0221954bc826ba4d9011b5a841e45](pages/7bb0221954bc826ba4d9011b5a841e45.md) |
| [2-3. 햄버거_식단_클릭 (삭제)](pages/66c0221954bc83e9af9b81f1151285a6.md) | fields_and_images_preserved_elsewhere | [b7f0221954bc83a9af4f010f5b5b8c95](pages/b7f0221954bc83a9af4f010f5b5b8c95.md) |
| [3-1. 식단_식사시간 선택 (클릭) - 3-2·3-3 통합](pages/8320221954bc82e0b41d8128f2e0b302.md) | fields_and_images_preserved_elsewhere | [1830221954bc82da965501008d23f1f3](pages/1830221954bc82da965501008d23f1f3.md) |
| [3-4. 식단_아침_스크롤](pages/dc00221954bc83f5923e01ff8270898e.md) | needs_content_review | [51f0221954bc821cb2648147bef8d890](pages/51f0221954bc821cb2648147bef8d890.md), [1830221954bc82da965501008d23f1f3](pages/1830221954bc82da965501008d23f1f3.md), [3740221954bc8299aee60160f0b07426](pages/3740221954bc8299aee60160f0b07426.md), [58e0221954bc82829b4e8199df6dde60](pages/58e0221954bc82829b4e8199df6dde60.md) |
| [3-5. 식단_점심_스크롤](pages/7c30221954bc8241a6ad812f7ce564ec.md) | fields_and_images_preserved_elsewhere | [47b0221954bc83c5984881b7d24ddad5](pages/47b0221954bc83c5984881b7d24ddad5.md) |
| [3-6. 식단_저녁_스크롤](pages/0dd0221954bc8381bf850126bf46c6e4.md) | fields_and_images_preserved_elsewhere | [a230221954bc8369b994016a3caafcaf](pages/a230221954bc8369b994016a3caafcaf.md) |
| [3-7. 식단_학생식당정보_클릭](pages/a680221954bc837e9c988117a7e8499d.md) | fields_and_images_preserved_elsewhere | [1370221954bc82008ede81bb956111a7](pages/1370221954bc82008ede81bb956111a7.md) |
| [3-8. (Android / iOS) 식단_카카오톡_공유하기_클릭](pages/9bb0221954bc82f6b4e301a447d0894e.md) | fields_and_images_preserved_elsewhere | [9610221954bc82d09b750118aa5dc7aa](pages/9610221954bc82d09b750118aa5dc7aa.md) |
| [3-9. (Android / iOS) 식단_카카오톡_코인이동_클릭 (카카오톡)](pages/75a0221954bc8271ad76810365b94708.md) | needs_content_review | [7b80221954bc826aa9ea01960bfe1fa6](pages/7b80221954bc826aa9ea01960bfe1fa6.md), [9610221954bc82d09b750118aa5dc7aa](pages/9610221954bc82d09b750118aa5dc7aa.md), [1190221954bc83939928017b5b644090](pages/1190221954bc83939928017b5b644090.md), [3d50221954bc8228a8ed81c51f8aa5d6](pages/3d50221954bc8228a8ed81c51f8aa5d6.md) |
| [4-1. 식단_코너 사진_클릭](pages/ae70221954bc83039c5401fa69a8ab05.md) | fields_and_images_preserved_elsewhere | [b3d0221954bc828fbdf7014674efb010](pages/b3d0221954bc828fbdf7014674efb010.md) |
| [5-1. (Android / iOS) 알림설정_클릭](pages/6970221954bc82d29e6301ca89419c5c.md) | fields_and_images_preserved_elsewhere | [1190221954bc83939928017b5b644090](pages/1190221954bc83939928017b5b644090.md) |
| [5-2. (Android / iOS) 알림설정_품절_토글](pages/8330221954bc8287b8be01c95c019076.md) | fields_and_images_preserved_elsewhere | [2ed0221954bc830ca8f3812a30d0063f](pages/2ed0221954bc830ca8f3812a30d0063f.md) |
| [5-3. (Android / iOS) 알림설정_품절_식사시간_토글](pages/e220221954bc82b5b4e0816e7122803a.md) | fields_and_images_preserved_elsewhere | [bfe0221954bc829dac0501c57175d4e1](pages/bfe0221954bc829dac0501c57175d4e1.md) |
| [5-6. (Android / iOS) 알림설정_식단사진 업로드_토글](pages/81a0221954bc82b6bec281c0096d3e42.md) | fields_and_images_preserved_elsewhere | [c7f0221954bc82e4b63f01f4acf751e8](pages/c7f0221954bc82e4b63f01f4acf751e8.md) |
