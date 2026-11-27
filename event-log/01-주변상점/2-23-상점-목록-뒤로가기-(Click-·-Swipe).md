# 2-23 상점 목록 뒤로가기 (Click · Swipe)

[← 주변상점 목록](README.md)

플랫폼: ANDROID, IOS  
원문 상태: 로깅 필요  
[Notion 기준 명세](https://app.notion.com/p/4c30221954bc82b5afb4016b1b3be6a7)  
원본 ID: `4c30221954bc82b5afb4016b1b3be6a7`

<!-- notion-body:start -->
### 플랫폼별 계약 범위

2026-11-27 사용자 확정: <b>swipe는 IOS 전용</b>이다. Android·Web의 기존 swipe 수집은 지원 범위 밖 전송으로 검수하며, 과거 기록을 개명하거나 click으로 자동 치환하지 않는다. 아래 표는 이 페이지의 개별 계약 범위이며 페이지 platform 속성은 확정된 범위의 합집합이다. 문서 수정은 SDK 배포·실수집 정상 완료를 뜻하지 않는다.

| event\_label | platform |
| --- | --- |
| <code>shop__shop_list__navigation__back__click</code> | ANDROID, IOS |
| <code>shop__shop_list__navigation__back__swipe</code> | IOS |

## 과거 로깅

- event\_label: <code>shop_categories_back</code>
- value: 기존 명세 미기재
- event\_category: click / swipe

## 새 로깅

### 뒤로가기 버튼

- 설명: 상점 목록에서 뒤로가기 버튼 또는 뒤로가기 스와이프로 이전 화면으로 돌아가는 전환이 완료되었을 때 기록한다. 취소된 스와이프와 하단 홈 탭 클릭은 포함하지 않는다.
- screen\_view: <code>shop_list</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_list__navigation__back__click</code>
- value: 메인
- event\_category: <code>click</code>

### 뒤로가기 스와이프

- 설명: 상점 목록에서 뒤로가기 버튼 또는 뒤로가기 스와이프로 이전 화면으로 돌아가는 전환이 완료되었을 때 기록한다. 취소된 스와이프와 하단 홈 탭 클릭은 포함하지 않는다.
- screen\_view: <code>shop_list</code>
- event\_name: <code>DA1</code>
- event\_label: <code>shop__shop_list__navigation__back__swipe</code>
- value: 메인
- event\_category: <code>swipe</code>

### 참고사진

<b>웹</b>

PC 웹: 상점 목록에 대응하는 뒤로가기 버튼 없음.

<b>모바일</b>

![참고사진](../../assets/2d945e53-8693-470f-b94b-502c9a911b53.png)
Stage 모바일 웹 · 상점 목록 뒤로가기 버튼
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "platform": [
    "ANDROID",
    "IOS"
  ],
  "url": "https://app.notion.com/p/4c30221954bc82b5afb4016b1b3be6a7",
  "상태": "로깅 필요",
  "생성일": "2026-11-23T13:38:19.511Z",
  "이벤트 이름": "2-23 상점 목록 뒤로가기 (Click · Swipe)",
  "태그": [
    "2. 상점 카테고리"
  ]
}
```

</details>
