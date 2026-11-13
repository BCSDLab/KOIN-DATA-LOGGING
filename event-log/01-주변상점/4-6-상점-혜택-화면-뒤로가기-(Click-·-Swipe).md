# 4-6 상점 혜택 화면 뒤로가기 (Click · Swipe)

[← 주변상점 로깅 목록](README.md)

플랫폼: IOS · ANDROID  
원문 상태: 로깅 필요

과거 로깅·새 로깅과 각 참고사진은 원문의 구간별 연결을 유지합니다.

<!-- logging-section:past:start -->
## 과거 로깅

- event\_label: <code>shop_benefit_back</code>
- value: \{상점이름\}
- event\_category: click

<!-- logging-section:past:end -->

<!-- logging-section:new:start -->
## 새 로깅

### 뒤로가기 버튼

- 설명: 특정 상점의 혜택 화면에서 뒤로가기 버튼 또는 뒤로가기 스와이프로 이전 화면으로 돌아가는 전환이 완료되었을 때 기록한다. 취소된 스와이프는 포함하지 않는다.
- screen\_view: <code>shop_benefit</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_benefit__navigation__back__click</code>
- value: \{상점이름\}
- event\_category: <code>click</code>

### 뒤로가기 스와이프

- 설명: 특정 상점의 혜택 화면에서 뒤로가기 버튼 또는 뒤로가기 스와이프로 이전 화면으로 돌아가는 전환이 완료되었을 때 기록한다. 취소된 스와이프는 포함하지 않는다.
- screen\_view: <code>shop_benefit</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_benefit__navigation__back__swipe</code>
- value: \{상점이름\}
- event\_category: <code>swipe</code>

### 참고사진

PC 웹: 이벤트/공지 탭 방식이며 별도 혜택 화면의 뒤로가기 버튼 없음.

<b>모바일</b>

![참고 이미지](../../assets/917bb4dd-2097-4707-8e5f-f1e3c0163ba7.png)

Stage 모바일 웹 · 해당 상점의 이벤트/공지 화면 뒤로가기

<!-- logging-section:new:end -->

---

<details>
<summary>원문 정보</summary>

원본 ID: `4ab0221954bc82e5b7d981ebcc544220`  
[보존 원문](../../_archive/original/notion/pages/4ab0221954bc82e5b7d981ebcc544220.md)

</details>
