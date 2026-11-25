# PR #294 — 작업 인계 진입점

[PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)의 **GitHub Actions 생성 파일 자동 동기화 + GitHub App 단기 인증 + 최종 PR Gate 재검증**을 위한 비정본 작업 번들. 이 문서와 연결된 인계는 실행·보안 승인 또는 CI 검증 통과를 의미하지 않는다.

## 다음에 누가 무엇을 하는가

1. **로컬 에이전트:** [12 — 실행 순서와 인계 계약](12-next-steps-handoff.md)에서 시작한다. #294의 읽기 전용 Producer와 #308의 기본 비활성 Writer를 검증하고, 사람 승인 전에는 원격 쓰기를 활성화하지 않는다.
2. **사람:** 준비된 코드를 검토한 뒤 [13 — GitHub App 설정·승인 체크리스트](13-owner-setup-runbook.md)에 따라 bootstrap 승인, App 설치, `main` 제한 Environment Secret, 격리 E2E와 최종 merge를 단계적으로 결정한다.
3. **로컬 에이전트:** 승인된 환경에서 E2E 증거를 수집하고 PR #294의 오래된 설명을 실제 구현에 맞춰 갱신한다. 실제 필수 체크와 사람 승인 전까지 Draft를 유지한다.

## 필요할 때 읽을 상세 자료

- [09 — 기술 설계](09-github-app-design.md): 읽기 전용 Producer / 신뢰된 Writer / 필수 PR Gate 경계.
- [10 — 구현 세부 인계](10-implementation-handoff.md): 작업 단위·검증 명령·변경 범위·중단 조건.
- [11 — 검증 행렬](11-verification-plan.md): ChatGPT API 연속 수정, no-op, stale SHA, App commit 및 required check 증거.
- [08 — 기술 적합성 조사](08-generated-sync-architecture-research.md): 기본 `GITHUB_TOKEN` 방식의 한계와 원래 위험 평가.

초기 리뷰와 [01 인계](01-handoff.md)·[07 목표 기록](07-status-and-goals-2026-11-16.md)에 나오는 기본 `GITHUB_TOKEN` 직접 push, “GitHub App·Secret 금지”와 수동 후속 push 방식은 **후속 설계 선택 이전의 기록**이다. 현재 권한·실행 절차는 [12 인계 계약](12-next-steps-handoff.md)과 [13 설정 런북](13-owner-setup-runbook.md)을 따른다.

## 변경할 수 없는 경계

- 대상: `mols3131d/mols-agent-assets`, source branch `mols/chore/generated-sync-on-push`, base `main`. **실행 때 실제 PR HEAD·계정·권한을 다시 확인**한다.
- 금지: 다른 계정 전환, Secret의 Git/PR/채팅 노출, `main` 직접 push, Ruleset 우회, force push, 자동 merge, 미실행 테스트를 통과로 보고.
- 통제 정본은 [CI 정책](../../docs/development/ci.md), [GitHub 정책](../../docs/development/github.md), [VCS 정책](../../docs/development/vcs-git.md) 및 실제 GitHub 설정이다. `.inbox/`는 임시 조사·인계 자료로 정본이 아니다.
