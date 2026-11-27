# 3-5-4 상점상세 뒤로 가기 (Logo) - 레거시

[← 주변상점 목록](README.md)

플랫폼: WEB  
원문 상태: 완료  
[Notion 기준 명세](https://app.notion.com/p/9d30221954bc83d1b16f0105e92d5c52)  
원본 ID: `9d30221954bc83d1b16f0105e92d5c52`

<!-- notion-body:start -->
## 과거 로깅

event\_params.key

- event\_label : shop\_detail\_view\_back
- value : \{상점이름\}
- event\_category :

  - logo

- current\_page : \{돌아간 카테고리\}
- duration\_time : 상점 상세보기에서 카테고리로 돌아간 시간.

---

카테고리 의미

- 로고 클릭

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

[해결 (3)](https://app.notion.com/p/cda0221954bc821e98e10152ba778f43)

## 새 로깅

- 레거시: 상점 상세 뒤로가기를 나가는 방법(click / swipe / logo)별로 나눠 두었던 로깅이다. 3-5-1 논의대로 하나의 라벨로 합치고 나가는 방법은 value로 구분하므로 새 로깅을 만들지 않는다.
- 대체 로깅: 3-5-1 상점상세 뒤로 가기 (ShopList) (shop\_\_shop\_detail\_\_back\_\_click)

### 참고사진 (레거시)

<b>웹</b>

<b>참고사진 · 웹</b>

해당 없음 (레거시)

<b>모바일</b>

<b>참고사진 · 모바일</b>

해당 없음 (레거시)
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "platform": [
    "WEB"
  ],
  "url": "https://app.notion.com/p/9d30221954bc83d1b16f0105e92d5c52",
  "상태": "완료",
  "생성일": "2026-11-23T13:38:16.345Z",
  "이벤트 이름": "3-5-4 상점상세 뒤로 가기 (Logo) - 레거시",
  "태그": [
    "3. 상점 상세 페이지"
  ]
}
```

</details>
