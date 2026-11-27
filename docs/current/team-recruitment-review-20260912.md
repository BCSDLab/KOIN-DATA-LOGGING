# 팀원모집 로깅 검수 (09.12)

[← 현행 문서와 참고 자료](README.md)

> 과거 검수 참고문서입니다. 원문의 2026-09-01~12 관측 범위와 9월 13일 문서 정리 설명을 그대로 보존하며 오늘의 수집 결과로 해석하지 않습니다. 팀원 모집의 SDK 동결·네이밍 전환 정책을 변경하지 않습니다.

[Notion 기준 원문](https://app.notion.com/p/2d30221954bc820eac2001262e4505e9) · 원문 편집 시각: 2026-10-21T12:29:26.417Z  
조회·동기화 기준일: 2026-11-27. [조회되지 않은 참고 링크와 확인 범위](reference-status.md).

<!-- notion-body:start -->
# 팀원모집 로깅 검수 — 수정·확인할 항목

## 검수 기준과 처리 방법

- 데이터 범위: 2026년 9월 1일부터 12일 최초 검수 시점. 9월 13일에는 문서만 정리했으며 로그를 재조회하지 않았습니다.
- 대상 데이터셋: <code>koin-stage-438512.analytics_427218788</code>. stage는 <code>stage.koreatech.in</code>, 로컬은 <code>localhost</code>입니다.
- PC·모바일은 GA4 기기 분류 기준입니다. 반응형 화면 너비를 구분한 결과는 아닙니다.
- <b>조치 단위는 event\_label + 기기 + 환경입니다.</b> 정상 표본은 조치 표에서 제외하고, 같은 라벨의 미관측 기기나 불일치 환경만 남겼습니다.
- 0건은 테스트 미수행일 수도 있습니다. 해당 기기에서 명세 동작을 재현한 뒤 수집 여부와 값을 확인하세요.
- 정상으로 확인된 value의 기대값·실제값은 생략했습니다. 미관측 항목의 기대값은 재현 테스트 기준으로 남겼습니다.
- 처리한 행은 해당 표에서 제거하세요. 토글 안의 범주를 모두 처리했다면 토글 전체를 제거해도 됩니다.

## (수정 필요) stage에서 로깅 명세와 로그가 다른 항목

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
기기
</td>
<td>
stage 발생
</td>
<td>
불일치 건수
</td>
<td>
기대 value
</td>
<td>
실제 value
</td>
</tr>
<tr>
<td>
<code>team_recruitment_apply_activity_modify_complete</code>
</td>
<td>
6. 지원서 작성 → ⑥ 활동 이력 수정 완료
</td>
<td>
PC
</td>
<td>
1건
</td>
<td>
1건
</td>
<td>
수정하기
</td>
<td>
완료
</td>
</tr>
</table>

모바일은 stage·로컬 모두 0건이므로 아래 미관측 표에서 별도로 확인합니다.

## (확인 필요) stage에는 안 찍혔지만 로컬에서는 찍힌 항목

아래 표에는 <b>로컬에서만 관측된 기기</b>만 표시했습니다. 다른 기기의 정상 stage 로그는 제외했습니다. stage에서 관측됐어도 동적 value 확인이 남은 로그는 다음 절의 별도 stage 표에 두었습니다.

<b>할 일:</b> 표의 기기로 stage에 접속해 명세 위치의 동작을 실행하세요. 이벤트 수집이 확인되면 이 표에서 제외하고, 값이 다르면 수정 필요 항목으로 옮기세요.

### 로컬 value가 일치한 항목 — 11개

## (확인 필요) stage에 찍혔지만 동적 value의 의미 확인이 남은 항목

<details>
<summary>상세보기</summary>

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
stage 재검수 기기
</td>
<td>
stage 건수
</td>
<td>
로컬 건수
</td>
<td>
로컬 판정
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_status</code>
</td>
<td>
2-1. 필터 내부 → ① 모집 상태
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_method</code>
</td>
<td>
2-1. 필터 내부 → ④ 진행 방식
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
2
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_apply</code>
</td>
<td>
2-1. 필터 내부 → ⑥ 필터 적용하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
2
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_delete_cancel</code>
</td>
<td>
4-1. 모집글 상세 및 삭제 → ③ 게시글 삭제 취소하기
</td>
<td>
PC
</td>
<td>
0
</td>
<td>
3
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_next</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ③ 다음 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_activity_modify</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ⑦ 활동 이력 수정
</td>
<td>
PC
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_activity_modify_complete</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ⑧ 활동 이력 수정 내용 저장
</td>
<td>
PC
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_submit_cancel</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ⑪ 프로필 작성 취소
</td>
<td>
PC
</td>
<td>
0
</td>
<td>
2
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant</code>
</td>
<td>
9. 내가 작성한 모집글 → ① 지원자 관리 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
7
</td>
<td>
일치 
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_close</code>
</td>
<td>
9. 내가 작성한 모집글 → ② 모집 마감 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치 
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_select</code>
</td>
<td>
10. 지원자 관리 → ① 지원자 선택
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
4
</td>
<td>
일치
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_applicant_check</code>
</td>
<td>
4. 모집글 상세 → ② 지원자 확인하기 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
일치
</td>
</tr>
</table>

</details>

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
기기
</td>
<td>
stage 건수
</td>
<td>
기대 value
</td>
<td>
stage 실제 value
</td>
<td>
확인할 내용
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_applicant_check</code>
</td>
<td>
4. 모집글 상세 → ② 지원자 확인하기 버튼 클릭
</td>
<td>
PC
</td>
<td>
9
</td>
<td>
확인한 게시글 이름
</td>
<td>
현재 페이지에 stage 실제값 미기재
</td>
<td>
stage 값 조회 후 실제 클릭한 게시글 제목과 비교
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant</code>
</td>
<td>
9. 내가 작성한 모집글 → ① 지원자 관리 클릭
</td>
<td>
PC
</td>
<td>
1
</td>
<td>
선택한 모집글 이름
</td>
<td>
현재 페이지에 stage 실제값 미기재
</td>
<td>
stage 값 조회 후 실제 클릭한 게시글 제목과 비교
</td>
</tr>
</table>

## (확인 필요) 해당 기기에서 stage와 로컬 둘 다 찍히지 않은 항목.

<details>
<summary>PC·모바일 모두 양쪽 환경에서 미관측 — 21개 라벨</summary>

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
재현할 기기
</td>
<td>
stage 건수
</td>
<td>
로컬 건수
</td>
<td>
재현 후 기대 value
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_role</code>
</td>
<td>
4-2. 모집글 편집 → ③ 역할
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
역할 구분 없이 모집하기 / 역할 추가
</td>
</tr>
<tr>
<td>
<code>team_recruitment_apply_activity_modify</code>
</td>
<td>
6. 지원서 작성 → ⑤ 활동 이력 수정
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
수정
</td>
</tr>
<tr>
<td>
<code>team_recruitment_apply_submit_cancel</code>
</td>
<td>
6. 지원서 작성 → ⑪ 지원 취소
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_major_select</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ② 학과·학부 선택
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
선택한 학부
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_activity_modify</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑤ 활동 이력 수정
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
수정
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_activity_modify_complete</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑥ 활동 이력 수정 저장
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
수정하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_submit_cancel</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑪ 프로필 최종 수정 취소하기
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_filter_sort</code>
</td>
<td>
8-1. 필터 내부 → ② 정렬 방식 선택
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
최신순 / 마감 임박순
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_filter_reset</code>
</td>
<td>
8-1. 필터 내부 → ③ 필터 초기화
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
초기화
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_chat</code>
</td>
<td>
8-2. 채팅 클릭
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
채팅을 선택한 모집글 이름
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_filter_status</code>
</td>
<td>
9-1. 필터 클릭 및 내부 → ② 모집 상태 선택
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
전체 / 모집 중 / 모집 마감
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_filter_sort</code>
</td>
<td>
9-1. 필터 클릭 및 내부 → ③ 정렬 방식 선택
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
최신순 / 마감 임박순
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_filter_reset</code>
</td>
<td>
9-1. 필터 클릭 및 내부 → ④ 필터 초기화
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
초기화
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_filter_apply</code>
</td>
<td>
9-1. 필터 클릭 및 내부 → ⑤ 필터 적용
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
적용하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_chat</code>
</td>
<td>
10. 지원자 관리 → ② 지원자 채팅 클릭
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
채팅
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_approve</code>
</td>
<td>
11. 지원자 상세 → ① 지원자 승인
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
승인하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_approve_confirm</code>
</td>
<td>
11. 지원자 상세 → ② 지원자 승인 확정
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
승인하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_approve_cancel</code>
</td>
<td>
11. 지원자 상세 → ③ 지원자 승인 취소
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_reject</code>
</td>
<td>
11. 지원자 상세 → ④ 지원자 거절
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
거절하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_reject_confirm</code>
</td>
<td>
11. 지원자 상세 → ⑤ 지원자 거절 확정
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
거절하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_applicant_reject_cancel</code>
</td>
<td>
11. 지원자 상세 → ⑥ 지원자 거절 취소
</td>
<td>
PC·모바일
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
PC 0 / 모바일 0
</td>
<td>
취소하기
</td>
</tr>
</table>

</details>

<details>
<summary>특정 기기가 양쪽 환경에서 미관측 — 27개 라벨</summary>

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
재현할 기기
</td>
<td>
stage 건수
</td>
<td>
로컬 건수
</td>
<td>
재현 후 기대 value
</td>
</tr>
<tr>
<td>
<code>team_recruitment_apply_activity_modify_complete</code>
</td>
<td>
6. 지원서 작성 → ⑥ 활동 이력 수정 완료
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
수정하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_delete_cancel</code>
</td>
<td>
4-1. 모집글 상세 및 삭제 → ③ 게시글 삭제 취소하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_submit_cancel</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ⑪ 프로필 작성 취소
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_close</code>
</td>
<td>
9. 내가 작성한 모집글 → ② 모집 마감 버튼 클릭
</td>
<td>
PC
</td>
<td>
0
</td>
<td>
0
</td>
<td>
마감하려는 모집글 이름
</td>
</tr>
<tr>
<td>
<code>team_recruitment_search</code>
</td>
<td>
1. 검색 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
사용자가 입력한 검색어
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_sort</code>
</td>
<td>
2-1. 필터 내부 → ② 정렬
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
최신순 / 마감 임박순
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_category</code>
</td>
<td>
2-1. 필터 내부 → ③ 카테고리
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
전체 / 공모전 / 대외활동 / 스터디 / 프로젝트 / 기타
</td>
</tr>
<tr>
<td>
<code>team_recruitment_filter_reset</code>
</td>
<td>
2-1. 필터 내부 → ⑤ 필터 초기화
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
초기화
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_delete</code>
</td>
<td>
4-1. 모집글 상세 및 삭제 → ① 게시글 삭제 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
삭제하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_delete_confirm</code>
</td>
<td>
4-1. 모집글 상세 및 삭제 → ② 게시글 삭제하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
삭제하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit</code>
</td>
<td>
4-2. 모집글 편집 → 게시글 편집 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
편집하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_category</code>
</td>
<td>
4-2. 모집글 편집 → ① 카테고리 선택
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
공모전 / 대외활동 / 스터디 / 프로젝트 / 기타
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_method</code>
</td>
<td>
4-2. 모집글 편집 → ② 진행 방식 선택
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
온라인 / 오프라인 / 온·오프라인
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_submit</code>
</td>
<td>
4-2. 모집글 편집 → ④ 수정 완료 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
수정 완료
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_submit_cancel</code>
</td>
<td>
4-2. 모집글 편집 → ⑤ 수정 취소하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
취소하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_post_edit_submit_confirm</code>
</td>
<td>
4-2. 모집글 편집 → ⑥ 수정하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
수정하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_apply_activity_add</code>
</td>
<td>
6. 지원서 작성 → ④ 활동 이력 추가
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
활동 이력 추가
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_skill_add</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ④ 기술 / 자격증 추가 버튼 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
기술 / 자격증 추가
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_activity_add</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑦ 활동 이력 추가
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
활동 이력 추가
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_activity_complete</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑧ 활동 내용 추가 작성 완료
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
완료
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_submit</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑨ 프로필 수정하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
수정하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_modify_submit_confirm</code>
</td>
<td>
7-1-1. 프로필 수정하기 내부 → ⑩ 프로필 최종 수정하기
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
수정하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_major</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ② 학과·학부 선택
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
선택한 학과·학부
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_filter</code>
</td>
<td>
8. 필터 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
필터
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_filter_status</code>
</td>
<td>
8-1. 필터 내부 → ① 지원 상태 선택
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
전체 / 승인 / 대기 / 거절
</td>
</tr>
<tr>
<td>
<code>team_recruitment_applied_post_filter_apply</code>
</td>
<td>
8-1. 필터 내부 → ④ 필터 적용
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
적용하기
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_chat</code>
</td>
<td>
9. 내가 작성한 모집글 → ⑤ 채팅 클릭
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
0
</td>
<td>
채팅을 선택한 모집글 이름
</td>
</tr>
</table>

</details>

## (확인 필요) 과거 로컬 불일치 이력

stage 정상 표본은 제외했습니다.

<details>
<summary>현재 로컬에서도 재현되는지 확인 — 2개 라벨</summary>

<b>할 일:</b> 현재 로컬에서 같은 동작을 실행하세요. 정상 값이면 과거 이력으로 처리하고 이 토글에서 제외하세요. 불일치가 재현되면 구현 또는 명세를 수정하세요.

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
기기
</td>
<td>
로컬 전체 발생
</td>
<td>
불일치 건수
</td>
<td>
불일치 필드
</td>
<td>
기대값
</td>
<td>
실제값
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile</code>
</td>
<td>
7. 프로필 클릭
</td>
<td>
PC
</td>
<td>
24건
</td>
<td>
12건
</td>
<td>
value
</td>
<td>
프로필
</td>
<td>
내 프로필
</td>
</tr>
<tr>
<td>
<code>team_recruitment_profile_create_submit_confirm</code>
</td>
<td>
7-1-2. 프로필 작성하기 내부 → ⑫ 프로필 작성 저장
</td>
<td>
PC
</td>
<td>
1건
</td>
<td>
1건
</td>
<td>
event_category
</td>
<td>
click
</td>
<td>
result
</td>
</tr>
</table>

프로필 작성 최종 확인의 value는 일치하므로 기대·실제 value는 생략했습니다. 프로필 수정 최종 확인의 category=result는 정상이며 수정 대상에 포함하지 않았습니다.

</details>

## (확인 필요) 공용 알림·명세 대응·웹 적용 범위

<details>
<summary>공용 알림을 모바일 stage에서 재현</summary>

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
기기
</td>
<td>
stage 건수
</td>
<td>
로컬 건수
</td>
<td>
기대 value
</td>
<td>
로컬 실제 value
</td>
<td>
할 일
</td>
</tr>
<tr>
<td>
<code>notification_list</code>
</td>
<td>
0. 알림 클릭 → 1-2 알림 클릭 내부
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
클릭한 알림 제목
</td>
<td>
팀원모집 새 지원
</td>
<td>
모바일 stage에서 팀원모집 알림 클릭 후 수집·제목 일치 확인
</td>
</tr>
</table>

</details>

<details>
<summary>명세에서 찾지 못한 라벨의 대응 확인</summary>

<table>
<tr>
<td>
event_label
</td>
<td>
기기
</td>
<td>
stage 건수
</td>
<td>
로컬 건수
</td>
<td>
로컬 실제 value
</td>
<td>
할 일
</td>
</tr>
<tr>
<td>
<code>team_recruitment_group_chat</code>
</td>
<td>
모바일
</td>
<td>
0
</td>
<td>
1
</td>
<td>
모집글 테스트
</td>
<td>
발생 화면·구현 확인 후 명세 추가 또는 기존 채팅 라벨과의 대응 결정
</td>
</tr>
</table>

</details>

<details>
<summary>명세의 ‘web 로깅 X’ 적용 범위 결정 — 2개 라벨</summary>

<b>할 일:</b> ‘web 로깅 X’가 PC만 의미하는지 모바일 웹도 포함하는지 명세 담당자가 결정하세요. 적용 대상이면 재현 검수로 옮기고, 제외 대상이면 이 토글을 제거하세요. 이번 검수에서는 두 항목 모두 웹 계열 필수 집계에서 제외했습니다.

<table>
<tr>
<td>
event_label
</td>
<td>
명세 위치
</td>
<td>
stage PC / 모바일
</td>
<td>
로컬 PC / 모바일
</td>
<td>
현재 판정
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_close_cancel</code>
</td>
<td>
9. 내가 작성한 모집글 → ③ 모집 마감 취소
</td>
<td>
0 / 0
</td>
<td>
0 / 1
</td>
<td>
로컬 value 일치. 웹 적용 범위 확인 필요
</td>
</tr>
<tr>
<td>
<code>team_recruitment_created_post_close_confirm</code>
</td>
<td>
9. 내가 작성한 모집글 → ④ 모집 마감 확인
</td>
<td>
0 / 0
</td>
<td>
0 / 0
</td>
<td>
미관측. 적용 대상이면 value=마감하기 검수
</td>
</tr>
</table>

</details>
<!-- notion-body:end -->
