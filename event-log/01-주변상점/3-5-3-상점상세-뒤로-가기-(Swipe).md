# 3-5-3 상점상세 뒤로 가기 (Swipe)

[← 주변상점 목록](README.md)

플랫폼: WEB, ANDROID, IOS  
원문 상태: 완료  
[Notion 기준 명세](https://app.notion.com/p/4220221954bc8218826a0190e9857ccb)  
원본 ID: `4220221954bc8218826a0190e9857ccb`

<!-- notion-body:start -->
## 과거 로깅

event\_params.key

- event\_label : shop\_detail\_view\_back
- value : \{상점이름\}
- event\_category :

  - swipe

- current\_page : \{돌아간 카테고리\}
- duration\_time : 상점 상세보기에서 카테고리로 돌아간 시간.

---

카테고리 의미 

- 뒤로가기 버튼을 눌러 상점 카테고리 페이지로 돌아가는 것.

시간 관련 주의 사항: 

- 상점 상세보기 페이지에서 어떠한 행위를 해도 상관이 없음. <br />즉 상점 상세보기를 들어온 시간부터 상점 상세보기를 떠난 시간까지 측정

---

### 오류사항

햄버거로 나가는걸 측정하지 못하고 있음. 

웹: 

상점 목록으로 나가면 swipe 이벤트가 찍히고 있음. 

안드: 

swipe → click 

---

[해결 (4)](https://app.notion.com/p/3ca0221954bc836fadf401d7f03dd980)

## 새 로깅

- 설명: 상점 상세 화면에서 나가는 경우
- screen\_view: <code>shop_detail</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_detail__navigation__back__swipe</code>
- value: 스와이프
- event\_category: <code>swipe</code>

### 참고사진 (상점 상세 뒤로가기)

<b>웹</b>

<b>참고사진 · 웹</b>

웹 - 없음

<b>모바일</b>

<b>참고사진 · 모바일</b>

모바일 — 뒤로가기 클릭 (출처: stage 실제 캡처, 빨간 네모 = 클릭 위치)

![참고사진](../../assets/6b532818-8efd-497f-8315-b81aab095673.png)
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "platform": [
    "WEB",
    "ANDROID",
    "IOS"
  ],
  "url": "https://app.notion.com/p/4220221954bc8218826a0190e9857ccb",
  "상태": "완료",
  "생성일": "2026-11-23T13:38:16.622Z",
  "이벤트 이름": "3-5-3 상점상세 뒤로 가기 (Swipe)",
  "태그": [
    "3. 상점 상세 페이지"
  ]
}
```

</details>
