# 로깅 명세 목록

자동 생성. approved 계약만 포함. 앱 적용·배포·실수집 검증 완료를 뜻하지 않는다.

| event_label | event_name | screen_view | 발생 조건 | 플랫폼 | 원문 |
| --- | --- | --- | --- | --- | --- |
| bus__main_category__category_navigation__search_entry__click | DA1 | main_category | 모바일 WEB 카테고리에서 교통편 조회하기 항목을 클릭할 때 한 번 기록한다. 단순 노출·초기 렌더·자동 이동 제외. | WEB (모바일) | [원문](https://www.notion.so/4000221954bc81469ea6dbe19c7d8be7) |
| bus__main_category__category_navigation__timetable_entry__click | DA1 | main_category | 모바일 WEB 카테고리에서 버스 시간표 항목을 클릭할 때 한 번 기록한다. 단순 노출·초기 렌더·자동 이동 제외. | WEB (모바일) | [원문](https://www.notion.so/4000221954bc81469ea6dbe19c7d8be7) |
| cafeteria__main_category__category_navigation__cafeteria_entry__click | DA1 | main_category | 모바일 WEB 카테고리에서 식단 항목을 클릭할 때 한 번 기록한다. 단순 노출·초기 렌더·자동 이동 제외. | WEB (모바일) | [원문](https://www.notion.so/4000221954bc81469ea6dbe19c7d8be7) |
| main__forced_update__app_update__already_done__click | DA1 | forced_update | 강제 업데이트 화면의 이미 업데이트를 하셨나요? 링크를 클릭해 안내 팝업을 열 때 1회 기록한다. | ANDROID | [원문](https://www.notion.so/4150221954bc81a28e0fc946e1e57c27) |
| main__forced_update__app_update__exposure | DA1 | forced_update | 강제 업데이트 화면이 사용자에게 실제 표시될 때 화면 표시 1회당 기록한다. 단순 재렌더에는 중복 전송하지 않는다. | ANDROID | [원문](https://www.notion.so/4150221954bc8126ab91fa403975d406) |
| main__forced_update__app_update__store_entry__click | DA1 | forced_update | 강제 업데이트 화면 하단 업데이트하기 버튼을 클릭해 스토어 이동을 시도할 때 1회 기록한다. | ANDROID | [원문](https://www.notion.so/4150221954bc81abb0fff0dc3714fcee) |
| main__forced_update__update_popup__close__click | DA1 | forced_update | 안내 팝업의 닫기 버튼을 클릭할 때 1회 기록한다. 배경 터치·OS 뒤로가기·제스처는 제외한다. | ANDROID | [원문](https://www.notion.so/4150221954bc81eda804ff10d5d301bf) |
| main__forced_update__update_popup__store_entry__click | DA1 | forced_update | 안내 팝업의 스토어 가기 버튼을 클릭해 스토어 이동을 시도할 때 1회 기록한다. | ANDROID | [원문](https://www.notion.so/4150221954bc81c4bd1ec8bb60a227e2) |
| owner__main_category__category_navigation__owner_entry__click | DA1 | main_category | 모바일 WEB 카테고리에서 코인 for Business 항목을 클릭할 때 한 번 기록한다. 단순 노출·초기 렌더·자동 이동 제외. | WEB (모바일) | [원문](https://www.notion.so/4000221954bc81469ea6dbe19c7d8be7) |
