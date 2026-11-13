# 앱 통합 가이드

이 저장소는 전송할 객체를 생성합니다. SDK 호출, 화면 이벤트 바인딩, 사용자 속성 및 debug 정책은 기존 앱의 어댑터가 담당합니다. 생성 파일만 추가해도 로그가 전송되는 구조가 아닙니다.

## 웹

`generated/logging.ts`를 앱에 가져옵니다. 현재 WEB 생성물은 `WEB` 또는 `WEB (모바일)` 명세를 포함합니다. 모바일 전용 계약을 PC에 바인딩하지 않도록 `contracts[label].platforms`도 확인합니다.

```ts
import {createEvent} from './generated/logging';

const event = createEvent(
  'cafeteria__main_category__category_navigation__cafeteria_entry__click',
  {}, // 고정 value '식단'은 명세에서 자동 적용
);
// 기존 SDK 호출 지점에서 event.event_name과 event.params를 사용합니다.
// 예: SDK 어댑터가 준비된 뒤 analytics.send(event.event_name, event.params)
```

등록되지 않은 label과 필수 동적 값 누락은 타입 검사 대상입니다. 런타임에도 알 수 없는 label·추가 키·타입·허용값을 검사합니다. JS의 any/cast로 타입 검사를 우회한 호출도 이 검사 대상입니다. 기존 로거가 params를 다시 덮어쓰지 않는지 대조하세요.

## Android

`generated/KoinEvents.kt`를 소스에 추가하고 `KoinEvent`를 받는 어댑터 하나를 연결합니다.

```kotlin
val event = Event_main__forced_update__app_update__store_entry__click()
// 기존 Firebase 어댑터가 event.eventName과 event.params를 변환하여 전송

val exposure = Event_main__forced_update__app_update__exposure(value = "v4.0.0")
```

Kotlin의 `number`는 Double입니다. JSON/Firebase 어댑터도 같은 표현을 유지해야 합니다. 이 초기 도구는 Kotlin 원본을 생성하며 프로젝트의 Gradle·Kotlin 버전에서 컴파일과 어댑터 변환을 확인해야 합니다. iOS 계약도 명세에 보존되지만 Swift 생성기는 아직 없습니다.

## 명세 버전 고정과 앱 CI

1. 검토된 명세 commit SHA를 앱에 고정합니다. 처음에는 이 커밋의 generated 파일과 manifest를 함께 복사할 수 있습니다.
2. 앱 CI에서 그 커밋을 checkout하고 `npm ci`, `npm run gen`을 실행합니다.
3. 재생성한 파일과 앱에 커밋한 파일을 비교하여 불일치 시 실패시킵니다.
4. 앱 타입/컴파일 검사와 SDK 전송 객체 검사를 수행합니다.

`manifest.json`의 revision은 규칙·명세 전체 내용의 SHA-256이며 릴리스 태그가 아닙니다. 커밋 SHA로 다운로드 대상을 고정하고 revision으로 생성물 대응을 확인합니다. 앱 CI는 아직 이 저장소에서 수정하지 않았습니다.

## 강제 업데이트 검증

- 모든 새 계약은 DA1, screen_view=forced_update입니다.
- 실제 화면 표시 1회마다 exposure 1회. 단순 재렌더에는 추가 발화하지 않습니다.
- 업데이트하기/팝업 스토어 가기는 이동 시도입니다. 설치·완료 여부와 분리합니다.
- 팝업 닫기 값은 새 계약의 '닫기'. 과거 iOS '확인'·Android '닫기'의 차이는 이관 기록으로 보존하며 과거 데이터를 소급 변경하지 않습니다.
- 기존 `forced_update_exit`은 lifecycle 동작이므로 신규 click으로 바꾸지 않습니다.
- 한 동작에서 과거·새 로그를 동시에 보내지 않습니다.
- 전환 전후 원천 이벤트의 label·value·category·event_name을 확인하고 앱 버전·적용일을 남깁니다.
