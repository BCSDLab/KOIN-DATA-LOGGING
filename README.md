# KOIN-DATA-LOGGING

KOIN의 로깅 계약을 YAML로 관리하고 TypeScript·Kotlin 코드를 생성하는 초기 구현입니다. 기존 노션의 여섯 필드와 라벨을 유지합니다. 명세 PR 검토 → 생성 코드 갱신 → 각 앱에서 검증하는 흐름을 제공합니다.

## 현재 범위

- 강제 업데이트 5개 계약: 초기 코드 생성 대상은 Android입니다. iOS·웹은 지원 미확인으로 생성에서 제외합니다. **2026-11-12 사용자 결정에 따라 DA1**입니다. `main`의 다른 화면은 DA2를 유지합니다.
- 모바일 WEB 카테고리 4개 계약: 식단·버스 시간표·교통편 조회·코인 for Business. 2026-11-08 네이밍 확정본에서 가져왔습니다.
- 명세 검사, 검색, 플랫폼별 코드 생성, 자동 생성 목차, 생성물 불일치 검사 및 PR CI.
- 노션 전체 이관·앱 코드 연결·SDK 배포·실수집 검증은 완료하지 않았습니다. iOS 코드 생성과 PNG 후보 추출·영역 표시도 후속 범위입니다.

`approved`는 명세 계약 확정을 뜻합니다. 해당 플랫폼의 구현·배포·수집 완료를 뜻하지 않습니다. WEB(PC)과 WEB(모바일), 네이티브 앱의 지원 범위를 사진만 보고 확대하지 않습니다.

## 실행

Node.js 22 이상을 사용합니다.

```sh
npm ci
npm run check
npm test
npm run gen
npm run verify
npm run find -- forced_update
```

`npm run gen`은 approved 계약만 `generated/`에 생성합니다. `node cli/koin-log.mjs gen --preview`는 draft도 포함한 검토용 파일을 `generated-preview/`에 생성합니다. 미리보기는 앱에 배포하지 않습니다. legacy·frozen 계약은 생성 대상에서 제외합니다.

## 저장소 구조

```text
rules/                  공통 DA 배정·화면 예외·카테고리·예약 키
specs/<service>/*.yaml   공통 명세 원본
cli/                    check · find · gen
generated/              생성된 TS·Kotlin·목차·버전 해시 (커밋)
docs/                   도입 절차·이관 범위·확정 사항
tests/                  잘못된 명세 거절·타입 검사·전송 객체 검증
.github/workflows/      PR과 main 변경 검사
```

명세 목록은 [자동 생성 목차](generated/catalog.md), 적용 절차는 [앱 통합 가이드](docs/integration.md), 근거와 미해결 항목은 [이관 기록](docs/migration.md)을 참고합니다.

## 로깅 작성 양식

기존 노션 필드의 대응은 다음과 같습니다.

| 노션 | YAML |
| --- | --- |
| 설명 | events[].description — 전송 시점과 제외 조건 |
| screen_view | 문서의 screen_view — label 두 번째 구간과 동일 |
| event_name | events[].event_name — 기존 DA1/DA2 보존 |
| event_label | events[].event_label — 고유 라벨 |
| value | events[].value — 타입·필수 여부·고정값·허용값 |
| event_category | events[].event_category — 마지막 구간과 동일 |

아래는 **양식 설명용 가상 예시**이며 운영 계약이 아닙니다. `specs/`에 복사하기 전에 실제 원문·값·플랫폼을 확정하세요.

```yaml
schema_version: 1
service: board
screen_view: notice
events:
  - description: 공지 목록의 게시글을 직접 클릭할 때 1회 전송
    event_name: DA2
    event_label: board__notice__article__entry__click
    event_category: click
    value:
      type: string
      required: true
      description: 클릭한 게시글 ID의 문자열 표현
    params: {}
    platforms: [WEB, ANDROID]
    platform_support:
      WEB:
        state: confirmed
        evidence: 실제 원문과 웹 화면 확인 근거로 교체
      WEB (모바일):
        state: unknown
        evidence: 지원 여부 미확인
      ANDROID:
        state: confirmed
        evidence: 실제 원문과 Android 화면 확인 근거로 교체
      IOS:
        state: unknown
        evidence: 지원 여부 미확인
    status: draft
    source: notion/pages/실제문서ID.md
```

값은 `string`, `number`, `boolean`을 지원합니다. `const`는 고정 전송값, `enum`은 허용 값 목록입니다. 고정값은 호출자가 덮어쓸 수 없습니다. 동적 값은 기존 의미를 확인한 뒤 타입을 정하며, 기존 value를 임의로 새 params로 분해하지 않습니다. `params: {}`는 추가 키가 없다는 뜻입니다. `event_label` 등 공통 키와 사용자 속성은 params로 지정할 수 없습니다.

라벨은 `service__screen__feature[__detail]__category`의 4~5구간입니다. 승인 카테고리는 click/select/scroll/swipe/submit/fail/exposure/toggle입니다. 기존 접미 예외·동결 계약은 일반 명세로 강제 개명하지 말고 원문 보관 및 예외 설계를 먼저 진행합니다.

## 변경 절차

1. 현행 노션 원문·실제 화면·대표 계약 확인. 과거/새 로깅을 분리합니다.
2. YAML 초안을 `status: draft`로 작성하고 발생 조건·플랫폼·value 의미를 기록합니다.
3. `check`와 `find`로 중복·기존 계약 재사용 여부를 확인합니다.
4. 담당자가 의미·플랫폼·데이터 연속성을 검토한 후 `approved`로 바꿉니다. 신·구 이중 전송은 금지합니다.
5. `gen`으로 생성물을 갱신하고 명세와 함께 PR에 커밋합니다. `verify`가 실패하면 수정합니다.
6. 앱은 명세 커밋 SHA를 고정해 생성물을 가져오고, 별도 앱 PR에서 호출과 SDK 어댑터를 연결합니다.
7. 배포 후 실제 도착 값·전송 횟수·앱 버전을 대조합니다.

이 CI는 잘못된 명세와 생성물 불일치를 검출합니다. 사람이 `approved`로 바꾼 판단의 적절성, 실제 클릭 시점, 중복 발화, GA4 도착은 앱과 수집 단계에서 검증해야 합니다. 필수 리뷰·merge 차단은 조직의 branch protection/ruleset 설정이 필요합니다.

## event_label 작성 규칙과 예시

형식은 `service__screen__feature[__detail]__category`입니다. `__`는 구간 사이, `_`는 한 구간 안의 단어 사이에 씁니다. 영문 소문자·숫자의 lower_snake_case만 사용하며 총 4~5구간입니다. detail은 선택이며 한 구간까지만 둡니다.

| 구간 | 작성 기준 | 예시 |
| --- | --- | --- |
| service | 이벤트가 속한 서비스. 담당 DA 이름이나 플랫폼 이름이 아님 | cafeteria, callvan, main |
| screen | 이벤트의 고정 논리 화면. screen_view와 정확히 일치 | main_category, forced_update |
| feature | 기능 사전의 기존 어휘를 우선 재사용 | category_navigation, app_update |
| detail | 필요할 때 대상·동작을 구분하는 고정 어휘 | cafeteria_entry, store_entry |
| category | event_category와 일치하는 마지막 구간 | click, exposure |

실제 파일럿 계약 예시:

- `cafeteria__main_category__category_navigation__cafeteria_entry__click`: 카테고리 화면의 식단 진입. service=cafeteria, screen_view=main_category, event_name=DA1, value=식단.
- `main__forced_update__app_update__store_entry__click`: 강제 업데이트 본문 업데이트하기 버튼. event_name=DA1(2026-11-12 사용자 확정 예외), value=업데이트하기.
- `main__forced_update__update_popup__store_entry__click`: 확인 팝업의 스토어 가기. 같은 목적지여도 클릭 위치·기능이 달라 위 계약과 구분.
- `main__forced_update__app_update__exposure`: detail이 없는 4구간. 화면이 실제 표시될 때 기록하며 클릭으로 바꾸지 않음.

### label에 넣지 않는 값

사용자 ID, 가게 이름, 게시글 ID, 검색어, 연도·학기, 버전, 플랫폼·운영체제명 등 변하는 값은 label에 연결하지 않습니다. value/params의 타입·필수 여부·허용값을 명세로 정합니다. 단, 민감하거나 자유 입력인 값은 필요성·수집 정책을 먼저 검토합니다. 기존 value의 의미를 임의로 바꾸거나 params로 분해하지 않습니다.

`shop__shop_list__가게이름__click`, `main___forced_update__app_update__click`, 끝이 category와 다른 라벨, detail을 여러 구간으로 늘린 라벨은 사용하지 않습니다. 미등록 screen/feature는 철자만 검사에 통과했다고 채택하지 말고 사전에 등록·검토합니다.

### 같은 기능과 다른 기능 구분

IOS·ANDROID·WEB에서 같은 계약은 같은 label을 사용합니다. label에 ios/android/web을 붙이지 않습니다. UI 차이는 설명·사진·플랫폼 지원 범위에 남깁니다. WEB PC와 모바일 웹의 적용 범위는 따로 확인합니다.

같은 label을 여러 설명 페이지에서 참조할 수 있지만 구조화된 원본 계약은 하나로 두고 source들을 연결합니다. 서로 다른 발생 시점·value 의미를 가진 계약을 이름만 같다는 이유로 합치지 않습니다. 이미 대표 계약이 있는 동작은 재사용하며 한 번의 클릭에 구라벨·새 라벨·대응 페이지별 로그를 함께 전송하지 않습니다.

### category와 전송 시점

현재 파일럿의 허용 목록은 click/select/scroll/swipe/submit/fail/exposure/toggle입니다. 최종 구간과 event_category가 같아야 합니다. click은 사용자 클릭 시도이며 자동으로 처리 성공을 뜻하지 않습니다. API 성공 콜백에서 클릭 로그를 추가 전송하지 않습니다. exposure·lifecycle에는 해당 발생 조건과 중복 방지 조건을 별도로 적습니다.

`page_exit`와 접미 없는 품절 동결 계약은 일반 규칙으로 자동 변환하지 않습니다. `forced_update_exit`는 이관 목록에 보존하되 새 공통 category·발생 조건 확정 전 코드 생성에서 제외합니다. 레거시·동결은 원문·이력·이미지를 보관하고 새 생성 대상으로 자동 승격하지 않습니다.

### 공통 작성 양식

1. 설명: 발생 화면·사용자 동작·전송 시점·제외 조건·중복 방지 조건.
2. screen_view: label 두 번째 구간과 같은 고정 화면명.
3. event_name: 서비스별 DA1/DA2. main/forced_update만 DA1 예외이며 다른 main은 DA2.
4. event_label: 위 구간 규칙과 기능 사전에 따른 고정 문자열.
5. value: 의미·타입·필수 여부·고정값 또는 허용값. 추가 params도 동일하게 정의.
6. event_category: 마지막 구간과 일치.
7. 검토사항: 미확정 의미·동결·플랫폼 차이·출처와 결정 근거.
8. 참고사진: WEB PC / 모바일 웹 / 네이티브 앱을 구분. 원본 출처·이미지 파일·영역 표시를 기록. 다른 서비스 참고사진을 실제 서비스 캡처로 표기하지 않음.

## 이전·지원 상태와 앱 적용 완료 기준

현재는 9개 계약의 생성 파일럿이며 전체 Notion 이전이 아닙니다. `docs/migration-inventory.json`은 생성 계약 9개와 검토 중 이탈 1개의 초기 목록입니다. 원문 문서 1,521개와 이미지 1,472개를 보관했으며, 숨겨진 DB 행을 포함한 전체 원본 총수는 미확정이므로 완료율을 계산하지 않습니다.

`platform_support`는 각 플랫폼의 confirmed/unsupported/unknown과 evidence를 기록합니다. `platforms`에는 confirmed인 생성 대상만 넣습니다. 미확인을 미지원으로 해석하지 않습니다. 승인된 계약도 구현·배포·실수집 완료를 뜻하지 않습니다. iOS는 공통 계약 범위로 보존하되 지원 근거와 Swift 생성·앱 검증은 후속입니다.

전체 이전 시 Event Log의 하위 페이지·DB 행·첨부를 목록화하고 원본 ID·편집 시각·현행/레거시/동결/검토 상태를 보존합니다. 이미지 파일 해시·출처·상대 경로, 원본→이관 파일 대조 및 내부 링크 누락을 확인합니다. 누락·접근 불가·deleted를 완료로 처리하지 않습니다.

이전 대조와 담당자 승인 전에는 Notion이 원문이고 YAML은 파일럿 사본입니다. 승인 후 YAML을 단일 기준으로 전환하고 Markdown·목차를 생성합니다. Notion과 YAML을 따로 편집하지 않습니다.

앱 CI의 생성물 비교와 직접 Firebase/문자열 로거 호출 제한은 후속입니다. 타입 생성만으로 기존 API 우회를 막을 수 없습니다. 기존 호출부 이관·컴파일·어댑터 검증 후 상수/API를 제거합니다. 유사 이름은 재사용 검토 경고 대상이며 현재 유사도 경고는 미구현입니다. 실제 충돌·필수값 누락·예약 키 덮어쓰기는 차단합니다. 앱 SHA 고정·생성물 비교·실제 한번 전송·수집 도착을 별도로 검증합니다.


## 전체 Event Log 문서·사진 이전

[전체 명세 목차](notion/README.md)에서 1,521개 문서와 1,472개 이미지 파일을 확인합니다. 사진은 저장소 assets 파일로 직접 표시하며 Notion 외부 링크는 제외했습니다. 문서 간 참조도 GitHub 내부 경로입니다. 원문 식별은 URL 대신 ID만 보존합니다.

원문 이전 문서가 모두 코드 생성 대상으로 승인된 것은 아닙니다. 생성은 기존 9개 파일럿만 유지합니다. 후속 대조에서 41개 데이터 소스 중 실제 무필터 보기를 확인한 소스는 14개였습니다. 나머지는 필터 보기 합집합 또는 저장된 보기 없음으로 숨겨진 행의 전수 여부가 미확인입니다. 모든 이미지의 UI 일치 여부를 육안 전수 검토한 것도 아닙니다. [검증 결과](notion/validation.json)와 [DB별 수집 근거](notion/database-coverage.json)를 참고하세요.


### 누락 원본 복구 및 이미지 표시 수정

이미지 태그 274개를 Markdown으로 고쳤습니다. 누락 원본 ID 87개는 중복·빈 페이지도 개별 보존하고 원본 이미지 16개를 추가했습니다. [내용 차이 8개와 복구 내역](notion/recovery-review.md)을 참고하세요. 기존 명세를 덮어쓰거나 자동 생성 범위를 확대하지 않았습니다.
