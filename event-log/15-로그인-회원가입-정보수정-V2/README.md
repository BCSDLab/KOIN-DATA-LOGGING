# 로그인/회원가입/정보수정 V2

[← 전체 서비스](../../README.md)

명세를 누르면 한 페이지에서 로그 정의와 해당 이미지를 함께 확인할 수 있습니다. 과거·새 로깅은 원문 구간대로 구분합니다. 상태는 원문 표기이며 구현·배포 승인을 뜻하지 않습니다.

## 로깅 목록

| 명세 | 원문 상태 | 플랫폼 |
| --- | --- | --- |
| **레거시** [레거시 2-2 로그인 진입(클릭)](%5B%EB%A0%88%EA%B1%B0%EC%8B%9C%5D-2-2-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%A7%84%EC%9E%85%28%ED%81%B4%EB%A6%AD%29.md) | 레거시 | ANDROID · IOS |
| **레거시** [레거시 4-2 로그아웃(클릭)](%5B%EB%A0%88%EA%B1%B0%EC%8B%9C%5D-4-2-%EB%A1%9C%EA%B7%B8%EC%95%84%EC%9B%83%28%ED%81%B4%EB%A6%AD%29.md) | 레거시 | ANDROID · IOS |
| [1-1 헤더_회원가입진입(클릭)](1-1-%ED%97%A4%EB%8D%94_%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EC%A7%84%EC%9E%85%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | WEB |
| **레거시** [1-2 회원가입진입(클릭) - 레거시](1-2-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EC%A7%84%EC%9E%85%28%ED%81%B4%EB%A6%AD%29-%EB%A0%88%EA%B1%B0%EC%8B%9C.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-3 로그인 화면_회원가입진입(클릭)](1-3-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%ED%99%94%EB%A9%B4_%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EC%A7%84%EC%9E%85%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-4 약관동의(클릭)](1-4-%EC%95%BD%EA%B4%80%EB%8F%99%EC%9D%98%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-5 본인인증_인증번호_발송(클릭)](1-5-%EB%B3%B8%EC%9D%B8%EC%9D%B8%EC%A6%9D_%EC%9D%B8%EC%A6%9D%EB%B2%88%ED%98%B8_%EB%B0%9C%EC%86%A1%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-6 본인인증_인증완료](1-6-%EB%B3%B8%EC%9D%B8%EC%9D%B8%EC%A6%9D_%EC%9D%B8%EC%A6%9D%EC%99%84%EB%A3%8C.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-7 정보입력_학생_외부인_구분(클릭)](1-7-%EC%A0%95%EB%B3%B4%EC%9E%85%EB%A0%A5_%ED%95%99%EC%83%9D_%EC%99%B8%EB%B6%80%EC%9D%B8_%EA%B5%AC%EB%B6%84%28%ED%81%B4%EB%A6%AD%29.md) | 대표 명세 · 원문별 상태 참조 | WEB · ANDROID · IOS (원문별 표기) |
| [1-8 학생_외부인_닉네임_중복확인](1-8-%ED%95%99%EC%83%9D_%EC%99%B8%EB%B6%80%EC%9D%B8_%EB%8B%89%EB%84%A4%EC%9E%84_%EC%A4%91%EB%B3%B5%ED%99%95%EC%9D%B8.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-8 학생_외부인_아이디_중복확인](1-8-%ED%95%99%EC%83%9D_%EC%99%B8%EB%B6%80%EC%9D%B8_%EC%95%84%EC%9D%B4%EB%94%94_%EC%A4%91%EB%B3%B5%ED%99%95%EC%9D%B8.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [1-9 학생_외부인_회원가입완료(클릭)](1-9-%ED%95%99%EC%83%9D_%EC%99%B8%EB%B6%80%EC%9D%B8_%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EC%99%84%EB%A3%8C%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [2-1 헤더_로그인 진입(클릭)](2-1-%ED%97%A4%EB%8D%94_%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%A7%84%EC%9E%85%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | WEB |
| [2-3 로그인 시도(클릭)](2-3-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%8B%9C%EB%8F%84%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [2-4 아이디찾기(클릭)](2-4-%EC%95%84%EC%9D%B4%EB%94%94%EC%B0%BE%EA%B8%B0%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [2-5 비밀번호찾기(클릭)](2-5-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EC%B0%BE%EA%B8%B0%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [3-1 헤더_정보수정하기(클릭)](3-1-%ED%97%A4%EB%8D%94_%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95%ED%95%98%EA%B8%B0%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | WEB |
| [3-2 정보수정하기(클릭)](3-2-%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95%ED%95%98%EA%B8%B0%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS |
| [3-3 정보수정완료(클릭)](3-3-%EC%A0%95%EB%B3%B4%EC%88%98%EC%A0%95%EC%99%84%EB%A3%8C%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | ANDROID · IOS · WEB |
| [3-4 비밀번호수정완료(클릭)](3-4-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EC%88%98%EC%A0%95%EC%99%84%EB%A3%8C%28%ED%81%B4%EB%A6%AD%29.md) | 대표 명세 · 원문별 상태 참조 | ANDROID · IOS · WEB (원문별 표기) |
| [4-1 로그아웃(클릭)](4-1-%EB%A1%9C%EA%B7%B8%EC%95%84%EC%9B%83%28%ED%81%B4%EB%A6%AD%29.md) | 로깅 필요 | WEB |

과거 Event Log 전체·템플릿·빈 페이지·수집 검증 기록은 [보존 자료](../../_archive/README.md)에서 확인할 수 있습니다.

중복 원본은 목록에서만 통합했습니다. 대표 명세의 ‘추가 원본과 플랫폼별 자료’에서 기존 정의·사진·원문 상태를 확인하세요.
