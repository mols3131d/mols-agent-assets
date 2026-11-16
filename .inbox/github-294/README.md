# PR #294 — 작업 인계 진입점

[PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)의 생성 파일 자동 동기화와 GitHub App 기반 최신 PR 검증을 위한 **비정본 작업 번들**이다. 문서 내용은 실제 repository policy, 현재 GitHub 설정, 사용자의 실행 승인과 별개다.

## 로컬 에이전트의 시작 경로

1. [구현 인계](10-implementation-handoff.md) — 현재 branch/ref 재확인, 작업 순서·권한 경계·중단 조건.
2. [GitHub App 설계](09-github-app-design.md) — Producer/Trusted Writer/PR Gate 책임, 기본 브랜치 선행 배포, API/ChatGPT 호환성.
3. [검증 행렬](11-verification-plan.md) — unit/E2E/경합/보안 테스트, required check의 증거·최종 합격 기준.

판단 근거가 더 필요할 때는 [기존 기술 조사](08-generated-sync-architecture-research.md), [원래 목표·상태 기록](07-status-and-goals-2026-11-16.md), [심층 리뷰](05-review-report-deep-2026-11-12.md)를 읽는다. **이전 인계의 “GitHub App·Secret 금지”, 수동 후속 push 제안은 후속 설계 선택 이전 기록이며 현재 구현 기준이 아니다.**

## 핵심 상태와 경계

- 대상: `mols3131d/mols-agent-assets`, source branch `mols/chore/generated-sync-on-push`, base `main`. 실제 head 및 Draft/check 상태는 **작업 시작 때 GitHub에서 다시 읽는다**.
- 도착 목표: GitHub Contents API·ChatGPT GitHub Plugin과 로컬 에이전트가 모두 source를 변경할 수 있고, 생성 파일은 자동 동기화되며 최신 PR candidate에 **실제 required `PR Gate`**가 작동한다.
- 선행 조건: write-capable workflow의 독립 보안 리뷰·사람 승인, 기본 브랜치에 trusted writer bootstrap, 사용자 소유 GitHub App/Secret 등록, 승인된 격리 E2E.
- 금지: 다른 계정/명의로 자동 전환, Secret을 repo/PR/채팅에 복제, `main` 직접 변경, Ruleset 우회, 자동 merge, 미실행 검증을 Pass로 기록.
- 이 번들의 문서는 실행 승인이나 정본 정책이 아니다. 변경의 최종 통제는 [CI 정책](../../docs/development/ci.md), [GitHub 정책](../../docs/development/github.md), [VCS 정책](../../docs/development/vcs-git.md), 실제 GitHub 권한·Rulesets가 소유한다.
