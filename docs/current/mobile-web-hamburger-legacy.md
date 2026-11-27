# 모바일 WEB 햄버거 패널 로깅 — 레거시

[← 공통 문서 목록](README.md)

플랫폼:   
원문 상태:   
[Notion 기준 명세](https://app.notion.com/p/4250221954bc8179ad6ddc9414495902)  
원본 ID: `4250221954bc8179ad6ddc9414495902`

<!-- notion-body:start -->
- 분류: 레거시
- 결정일: 2026-11-28
- 적용 범위: 모바일 WEB의 구형 헤더에서 여는 햄버거 패널.
- 처리: 구형 패널의 로그 전송을 제거한다. 메뉴 이동·로그인·로그아웃·내 정보 기능은 유지한다. 현재 홈 하단 카테고리와 그 현행 계약은 별개다.
- 과거 명세·사진·수집 데이터는 보존한다. 새 DA1/DA2 라벨로 이관하거나 신·구 이중 전송하지 않는다.

## 보존하는 과거 로깅

| event\_name | event\_label | event\_category | value |
| --- | --- | --- | --- |
| CAMPUS | hamburger | click | 공지사항 / 분실물 / 교통편 조회하기 / 버스 시간표 / 식단 / 교내 시설물 정보 / 쪽지 / 동아리 / 콜밴팟 모집 / 팀원 모집 |
| BUSINESS | hamburger | click | 복덕방 |
| BUSINESS | hamburger\_shop | click | 주변상점 |
| USER | hamburger | click | 시간표 / 내정보 / 로그아웃 / 로그인 시도 |
| USER | timetable\_back | click | 햄버거 |

표의 슬래시는 여러 과거 고정값을 나열한 것이며 합쳐 전송하는 값이 아니다. <code>timetable_back</code>은 value=<code>햄버거</code>인 이 패널 경로만 대상이다.

- 기존 관련 명세: [1-2 햄버거 → 상점 카테고리 (클릭) - 레거시](https://app.notion.com/p/b150221954bc8281b86e81d96cf14724).
- [기존 웹 호출 위치](https://github.com/BCSDLab/KOIN_WEB_RECODE/blob/9b6b7a2a29e70f59409bb1136cf2ec7bb9765ab6/src/components/layout/Header/MobileHeader/Panel/index.tsx).
- 적용 상태: 명세 폐기 결정. 웹 코드 제거는 리뷰용 PR로 진행하며, 병합·배포·실수집 종료는 아직 확인하지 않았다.

## 플랫폼 대조 — 코드 기준

- WEB: 이 문서의 제거 대상. 구형 패널의 로그 호출 17곳을 제거하는 리뷰용 변경이며 메뉴 동작은 유지한다.
- Android: 5.2.4 소스의 구형 메뉴 12곳·설정 1곳에서 HAMBURGER 계열 호출이 남아 있다. 현재 develop에서도 두 파일의 호출을 확인했다. 설정의 비밀번호 변경은 <code>hamburger / 정보수정 시도</code>를 사용하므로 일괄 삭제하지 않고 현행 기능 계약 이관 여부를 별도로 검토한다. 이 WEB 폐기 결정으로 Android 호출을 삭제하지 않는다.
- iOS: develop <code>5f7800fbbc607b9c48c3e8d2fa61004141515d88</code>의 Swift 소스에서 hamburger·hambuger 문자열은 발견하지 못했다. 카테고리의 새 <code>category_navigation</code> 라벨은 유지한다. 전체 버전의 실수집 종료를 검증한 결과는 아니다.

[Android 메뉴 코드](https://github.com/BCSDLab/KOIN_ANDROID/blob/fe0462438f9a807ebcf2a5d307988d17884ec7a5/koin/src/main/java/in/koreatech/koin/ui/navigation/KoinNavigationDrawerActivity.kt) · [Android 설정 코드](https://github.com/BCSDLab/KOIN_ANDROID/blob/fe0462438f9a807ebcf2a5d307988d17884ec7a5/koin/src/main/java/in/koreatech/koin/ui/setting/SettingActivity.kt) · [iOS 카테고리 라벨](https://github.com/BCSDLab/KOIN_iOS/blob/5f7800fbbc607b9c48c3e8d2fa61004141515d88/Koin/Core/Logger/EventParameter.swift)
<!-- notion-body:end -->

<details>
<summary>Notion 원문 속성 전체</summary>

```json
{
  "title": "모바일 WEB 햄버거 패널 로깅 — 레거시"
}
```

</details>
