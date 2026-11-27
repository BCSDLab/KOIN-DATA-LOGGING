# 3-28 상점상세 사진 넘기기 (Swipe)

[← 주변상점 목록](README.md)

플랫폼: IOS, ANDROID  
원문 상태: 로깅 필요  
[Notion 기준 명세](https://app.notion.com/p/40c0221954bc83da9dd401ed9a8cef00)  
원본 ID: `40c0221954bc83da9dd401ed9a8cef00`

<!-- notion-body:start -->
## 과거 로깅

- event\_label: <code>shop_picture_swipe</code>
- value: \{상점이름\}
- event\_category: swipe

## 새 로깅

- 설명: 상점 상세의 사진을 넘겨 현재 사진 인덱스가 다른 사진으로 변경되었을 때 기록한다. 사진 클릭으로 확대 화면만 여는 경우는 포함하지 않는다.
- screen\_view: <code>shop_detail</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_detail__photo_view__slide__swipe</code>
- value: \{상점이름\}
- event\_category: <code>swipe</code>

### 참고사진

<b>웹</b>

PC 웹: 사진 확대 후 화살표 클릭 방식. 모바일 좌우 스와이프와 구분.

<b>모바일</b>

![참고사진](../../assets/3b231400-96e5-45d2-ba27-9fb9ffacca90.png)
Stage 모바일 웹 · 사진 3장의 좌우 넘김 영역
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "platform": [
    "IOS",
    "ANDROID"
  ],
  "url": "https://app.notion.com/p/40c0221954bc83da9dd401ed9a8cef00",
  "상태": "로깅 필요",
  "생성일": "2026-11-23T13:38:15.610Z",
  "이벤트 이름": "3-28 상점상세 사진 넘기기 (Swipe)",
  "태그": [
    "3. 상점 상세 페이지"
  ]
}
```

</details>
