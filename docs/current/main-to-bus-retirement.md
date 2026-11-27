# PC 교통 제목 main_to_bus — 레거시

[← 현행 문서와 참고 자료](README.md)

[Notion 기준 원문](https://app.notion.com/p/4250221954bc817f85c0dbed4e2f5d55) · 원문 편집 시각: 2026-11-27T16:31:57.590Z

조회·동기화 기준일: 2026-11-28. 구현·배포·실수집 검증과 구분합니다.

<!-- notion-body:start -->
2026-11-28 확정.

- 대상: PC 홈 ‘교통’ 제목 링크에서 사용하던 <code>main_to_bus</code>.
- 분류: 과거 로깅. 과거 명세·수집 데이터는 보존하고, 신규 전송은 중단한다.
- PC ‘교통’ 제목 링크에는 대체 이벤트를 추가하지 않는다. 기능 링크 삭제를 의미하지 않는다.
- <a href="https://app.notion.com/p/93c0221954bc82a5b20701ce5f75c697">1-8 버스 노선 클릭</a>의 <code>bus__main__bus_entry__search_entry__click</code>은 버스 노선 조회 카드 클릭만 대상으로 유지하며 PC ‘교통’ 제목 링크를 포함하지 않는다.
- 기존 카드 계약의 ANDROID·IOS·WEB, DA1, screen\_view=main, event\_category=click, value=버스 노선 조회는 유지한다.
- 이 문서는 명세 결정이다. 실제 WEB 코드의 main\_to\_bus 호출 제거·배포·신규 수집 중단 확인은 웹 담당자가 수행한다. 이번 문서 작업에서는 외부 앱·웹 저장소나 운영 데이터를 변경하지 않았다.
<!-- notion-body:end -->
