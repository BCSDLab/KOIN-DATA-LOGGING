# [레거시] 3-5-4 상점상세 뒤로 가기 (Logo) - 레거시

> **레거시 문서** · 과거 구현과 로깅을 확인하기 위한 보존 자료입니다.

[← 주변상점 로깅 목록](README.md)

플랫폼: WEB  
원문 상태: 완료

과거 로깅·새 로깅과 각 참고사진은 원문의 구간별 연결을 유지합니다.

원문 미기재 항목: `event_name`, `screen_view`, `event_category`. 값을 추정하지 않았습니다.

<!-- logging-section:past:start -->
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

<ol>

- 상점 상세보기 페이지에서 어떠한 행위를 해도 상관이 없음. <br />즉 상점 상세보기를 들어온 시간부터 상점 상세보기를 떠난 시간까지 측정 

</ol>

---

### 오류사항

햄버거로 나가는걸 측정하지 못하고 있음. 

웹: 

상점 목록으로 나가면 swipe 이벤트가 찍히고 있음. 

안드: 

swipe → click 

---

[해결 (3)](../../_archive/original/notion/pages/3e40221954bc8208908581ee82812066.md)

<!-- logging-section:past:end -->

<!-- logging-section:new:start -->
## 새 로깅

- 레거시: 상점 상세 뒤로가기를 나가는 방법(click / swipe / logo)별로 나눠 두었던 로깅이다. 3-5-1 논의대로 하나의 라벨로 합치고 나가는 방법은 value로 구분하므로 새 로깅을 만들지 않는다.
- 대체 로깅: 3-5-1 상점상세 뒤로 가기 (ShopList) (shop\_\_shop\_detail\_\_back\_\_click)

해당 없음 (레거시)

해당 없음 (레거시)

<!-- logging-section:new:end -->

---

<details>
<summary>원문 정보</summary>

원본 ID: `cf60221954bc82f8a2e501f1efb91a7b`  
[보존 원문](../../_archive/original/notion/pages/cf60221954bc82f8a2e501f1efb91a7b.md)

</details>
