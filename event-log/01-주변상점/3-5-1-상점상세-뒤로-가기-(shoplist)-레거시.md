# 3-5-1 상점상세 뒤로 가기 (shoplist) - 레거시

[← 주변상점 목록](README.md)

플랫폼: WEB, WEB (모바일), ANDROID, IOS  
원문 상태: 완료  
[Notion 기준 명세](https://app.notion.com/p/6f00221954bc83b480bc81c89b26bfb3)  
원본 ID: `6f00221954bc83b480bc81c89b26bfb3`

<!-- notion-body:start -->
## 과거 로깅

event\_params.key

- event\_label : shop\_detail\_view\_back
- value : \{상점이름\}
- event\_category :

  - ShopList
- current\_page : \{돌아간 카테고리\}
- duration\_time : 상점 상세보기에서 카테고리로 돌아간 시간.

---

 

카테고리 의미 

- ‘상점목록’ 클릭으로 상점카테고리 페이지로 돌아가는 것.

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

[해결 (1)](https://app.notion.com/p/ef30221954bc828e9dcd810b198746b6)
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "platform": [
    "WEB",
    "WEB (모바일)",
    "ANDROID",
    "IOS"
  ],
  "url": "https://app.notion.com/p/6f00221954bc83b480bc81c89b26bfb3",
  "상태": "완료",
  "생성일": "2026-11-23T13:38:18.207Z",
  "이벤트 이름": "3-5-1 상점상세 뒤로 가기 (shoplist) - 레거시",
  "태그": [
    "3. 상점 상세 페이지"
  ]
}
```

</details>
