# 3-5-1 상점상세 뒤로 가기 (shoplist) - 레거시

[← 주변상점 로깅 목록](README.md)

플랫폼: WEB · WEB (모바일) · ANDROID · IOS  
원문 상태: 완료

과거 로깅·새 로깅과 각 참고사진은 원문의 구간별 연결을 유지합니다.

원문 미기재 항목: `event_name`, `screen_view`, `event_category`. 값을 추정하지 않았습니다.



<!-- logging-section:past:start -->
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

[해결 (1)](../../_archive/original/notion/pages/1610221954bc827fbbad81569041f13e.md)

<!-- logging-section:past:end -->


---

<details>
<summary>원문 정보</summary>

원본 ID: `da60221954bc8307916e017ed74a757b`  
[보존 원문](../../_archive/original/notion/pages/da60221954bc8307916e017ed74a757b.md)

</details>
