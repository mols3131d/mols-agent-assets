# ChatGPT GitHub PR Review Skill — 작업 준비

## 목표

ChatGPT 채팅 환경에서 **GitHub Plugin으로 실제 Pull Request를 조사하고 근거 기반 리뷰를 수행하는 전용 Skill**을 만든다. 단순한 PR 요약이 아니라 변경의 correctness·계약·회귀·검증 공백을 살피고, 리뷰 결과를 GitHub와 대화에서 일관되게 전달하도록 한다.

이번 준비 단계의 결과물은 작업 범위와 완료 기준을 확정하기 위한 **인박스 계획 및 Draft PR**이다. 작동하는 `SKILL.md` 구현·검증·평가와 PR 병합은 이 단계에 포함하지 않는다.

## 범위와 책임

- **적용 대상:** 사용자가 식별한 GitHub PR을 ChatGPT 챗봇에서 GitHub Plugin을 통해 리뷰하는 작업.
- **고유 책임:** PR diff와 관련 증거를 수집하고, 검토 범위·결함·불확실성을 구분하며, 조치 가능한 결과로 정리하는 리뷰 방법.
- **기존 소유자 재사용:** `github-context`는 live repository/ref/instruction discovery를, repository `docs/development/github.md`와 `.github/templates/`는 GitHub 협업·작성 형식을 소유한다. 새 Skill은 이를 복제하지 않는다.
- **입력:** PR URL 또는 repository + PR 번호, 사용자가 지정한 리뷰 관점·범위·게시 지시(있는 경우).
- **출력:** 중요도순 finding, 파일/라인 및 근거, 확인한 범위, 수행한 검증과 미검증 영역, 필요 시 GitHub PR Review/inline comment.
- **쓰기 경계:** 기본은 읽기 및 채팅 보고. GitHub review/comment 게시와 승인·변경 요청은 별도의 명시적 지시와 권한을 확인하며, merge는 수행하지 않는다.

## 구현 전 확인할 결정

1. ChatGPT 런타임의 Skill 선택·로드 경로와 GitHub Plugin의 실제 read/review/comment 도구 계약을 확인한다. 지원하지 않는 API나 UI를 가정하지 않는다.
2. `mols-agent-asset`, `github-context`, 기존 리뷰 자산과 책임이 겹치지 않도록 Skill 이름·activation·near-miss를 설계한다.
3. 재사용 가능한 Rulesync Skill 원본을 사용할지, ChatGPT 전용 원본이 필요한지 실제 배포/소비 경로를 기준으로 결정한다. 생성된 projection은 원본으로 편집하지 않는다.
4. 큰 diff·수정 중인 PR·접근 불가 파일·check 미완료·리뷰 시점 변경 등에서 partial coverage와 revision을 어떻게 명시할지 정한다.
5. 악의적인 PR 본문·diff·comment를 **비신뢰 입력**으로 다루고, 원격 내용의 지시를 실행하거나 권한을 확대하지 않도록 한다.

## 후속 작업

1. GitHub Plugin의 지원 가능한 PR 조회·diff·파일 패치·checks·review 작성 경로를 실제로 조사한다.
2. 대표 시나리오(정상 PR, 대형 PR, 증거 부족, 변경 중인 PR, 게시 요청, prompt injection)를 선정하여 Skill 계약을 설계한다.
3. 전용 `SKILL.md`와 **실제로 필요한** reference만 작성한다. 유지보수용 연구·계획은 이 인박스에 남긴다.
4. 정적 구조 검증과 ChatGPT+GitHub Plugin 실행 시나리오 평가를 분리하고, 미실행 평가는 통과로 처리하지 않는다.
5. 변경 파일·검증 결과·알려진 한계를 PR에 기록한 뒤 리뷰 및 병합 준비를 진행한다.

## 완료 기준 (전체 PR 기준)

- ChatGPT가 PR 리뷰 요청과 일반 GitHub 질문·단순 요약·자산 자체 리뷰를 올바르게 구분한다.
- 실제 PR의 base/head, diff, 관련 repository instruction을 확인하고 **검토 범위의 한계**를 명시한다.
- Finding은 중요도와 구체적 근거를 가지며, 검증하지 않은 결론·테스트 통과·승인을 만들어내지 않는다.
- 도구 실패나 API 제약에서도 검증 가능한 부분만 보고하고, GitHub 게시를 무단 수행하지 않는다.
- 작성 원본, reference, 검증 및 행동 평가가 저장소의 Agent Asset 규칙과 부합한다.

## 현재 상태

- 준비 범위: 본 문서와 Draft PR.
- 미완료: Skill 설계 확정, 구현, 정적 검증, 런타임 행동 평가, 병합.
