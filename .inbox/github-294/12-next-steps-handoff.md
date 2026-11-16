# PR #294 — 다음 작업 인계: 로컬 에이전트 → 사람 → 검증

> 2026-11-16 계획 스냅샷. [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)는 조사 시점 Open/Draft, head `b3c965225c0554d37e904cdf56b37a17d9a41ba0`. 새 작업에서는 ref·권한·검증 상태를 다시 조회한다. **이 문서는 설계·작업 인계이며 CI 변경 승인이나 실행 증거가 아니다.**

## 지금 바로 맡길 작업

**로컬 에이전트의 첫 목표는 GitHub App을 설치하는 것이 아니라, 설치 없이 검증 가능한 안전한 구현과 사람의 승인 패키지를 준비하는 것**이다. 그 다음 사람은 [GitHub App 설치·승인 절차](13-owner-setup-runbook.md)에 따라 설정한다. 기존 [상세 기술 설계](09-github-app-design.md), [구현 인계](10-implementation-handoff.md), [검증 행렬](11-verification-plan.md)을 재작성하지 말고 적용한다.

| 단계 | 담당 | 산출물 / 통과 기준 | 다음 단계로 이동하는 조건 |
| --- | --- | --- | --- |
| A0. 현재 상태·권한 파악 | 로컬 에이전트 | 실제 PR head/base, 작업 브랜치, Ruleset/required check, 기존 write workflow 트리거, 승인 공백 정리 | 계정·변경 범위 명확 |
| A1. 최소 안전 구현 준비 | 로컬 에이전트 | 읽기 전용 Producer, 기본 브랜치 trusted Writer의 **비활성 상태** 구현, 검증 스크립트와 테스트; PR/패치로 제안 | 정적·결정적 테스트와 독립 검토 근거 |
| H1. 통제 표면 승인 | 사람 | bootstrap PR의 diff·write boundary·App scope 검토, 승인 여부 명시 | 승인된 bootstrap만 `main`에 squash merge |
| H2. App·Credential 준비 | 사람 | 본인 소유 GitHub App 설치, environment 제한, Client ID/PEM 등록 확인 | 키 노출 없이 trusted writer만 Secret 접근 |
| H3. 격리된 쓰기 E2E 승인 | 사람 | 테스트 대상·브랜치·범위·활성화 상태 승인 | 승인된 테스트 branch/PR에서만 write 가능 |
| A2. 통합 검증과 개선 | 로컬 에이전트 | ChatGPT API/연속 커밋·no-op·race·App push·최신 PR Gate 증거, 실패 수정 | 필수 항목 Pass / 미검증은 Blocked |
| H4. 최종 수용·병합 결정 | 사람 | 전체 PR 리뷰, 현재 SHA의 필수 checks, 병합 승인 | 조건 충족 시 수동 squash merge |

**현시점:** A0~A2 및 H1~H4는 이번 인계에서 완료 처리하지 않는다. 운영 상태가 아니라 계획이다.

## 로컬 에이전트 작업 계약

1. **컨텍스트부터 재확인:** `mols3131d/mols-agent-assets` / `mols/chore/generated-sync-on-push` / PR #294만 대상으로 하며, `git`·`gh` 로그인 계정이 소유자 `mols3131d`인지 먼저 확인한다. 다른 계정·연결·명의로 전환하지 않는다. 루트/경로별 `AGENTS.md`, `docs/development/github.md`, `ci.md`, `vcs-git.md`와 로컬 Skill 선택 규칙을 적용한다.
2. **현재 write-back의 위험부터 제거:** 현행 `.github/workflows/generated-sync.yml`에는 `contents: write` + 기본 `GITHUB_TOKEN` push가 남아 있다. 특히 `scripts/**` 등 trigger 경로의 원격 변경은 **기존 write-capable workflow를 실행할 수 있다**. 승인 전에는 그런 push·dispatch·실험을 하지 말고 local patch/정적 검증부터 준비한다. 변경을 원격 반영해야 한다면 사람의 명시적 범위 승인을 받는다.
3. **변경을 최소화:** 기존 `scripts.generated_artifacts`의 `sync`/`validate --all`, 생성 대상 inventory, `PR Gate`와 `Branch Check`의 읽기 전용 검증은 재사용한다. 재구현할 것은 원격 write의 신뢰 경계뿐이다. `int128/update-generated-files-action`, `autofix.ci`, `gh-aw`, 개인 PAT, 신규 생성 프레임워크는 이번 경로에서 필요하지 않다.
4. **Producer:** source push를 읽기 전용으로 처리하여 generator 실행·검증 후 허용된 projection만 artifact로 전달한다. 실패 시 writer는 커밋하지 않는다. GitHub API/ChatGPT 플러그인의 hookless 연속 커밋과 output-only 변경 범위를 테스트한다.
5. **Writer:** 기본 브랜치의 `workflow_run`으로 실행하되, 처음에는 fail-closed/disabled 상태여야 한다. 신뢰된 default-branch 코드로 run source/repo/ref/SHA/artifact/파일 목록을 검증하고, source branch에서 받은 스크립트를 실행하지 않는다. stale SHA면 폐기, no-op이면 커밋 없이 종료, 변경 시에만 App 단기 토큰으로 generated-only fast-forward push한다.
6. **Secret 경계:** 가능한 경우 `main`만 접근 가능한 GitHub Actions Environment의 Secret을 사용한다. 일반 repository-level Secret은 같은 저장소의 다른 워크플로에서 읽을 수 있으므로 무비판적으로 채택하지 않는다. 지원하지 않는 플랜·저장소라면 **중단하고 사람에게 대안을 검토받는다**. App 개인키 자체를 로컬 에이전트에 제공하거나 실행 로그·PR에 기록하지 않는다.
7. **리뷰와 산출물:** 보안 리뷰 가능한 최소 bootstrap PR(필요 시 별도)과 PR #294 개선안을 준비한다. `PR Gate`의 실제 required 이름·source 확인, unit tests 결과, 비활성 스위치, 복구·키 폐기 절차, 미승인·미검증 사항을 기술한다. 기존 PR 본문의 **App 불필요·수동 후속 push** 문구를 실제 합의와 코드에 맞춰 교체한다. 다만 PR 본문 갱신도 승인된 범위에서 수행한다.
8. **정지 조건:** 승인 없는 privileged workflow 활성화·write E2E, expected ref/actor 불일치, fork/외부 artifact 신뢰 불가, default branch 직접 쓰기, PR 필수 체크 부재, App 키 노출 가능성이 있으면 실행을 중단하고 `BLOCKED`로 인계한다.

## 검증 우선순위

기존 [검증 행렬](11-verification-plan.md)에서 다음 항목은 **필수 P0**다.

- [ ] GitHub App 없이 local/static test: 악성 artifact·경로/타입 우회·stale HEAD·no-op·repo/branch provenance 거부
- [ ] 승인된 격리 E2E: 단일 API source 변경 → generated-only App commit → 열린 PR의 최신 required `PR Gate` 성공
- [ ] 승인된 격리 E2E: API 연속 커밋/동시 실행 → 오래된 artifact의 덮어쓰기 없음
- [ ] App-generated output-only 커밋의 무한 반복 없음, 소스 수정 시 재생성 누락 없음
- [ ] Secret 접근이 신뢰된 default branch writer 외에 허용되지 않음
- [ ] 강제 push, `main` 직접 쓰기, Ruleset bypass, 자동 merge 없음

E2E 근거에는 **source SHA, bot commit SHA, producer/writer/PR Gate run URL, 검사 대상 head/merge SHA, 변경 파일 목록**이 있어야 한다. Draft·기존 CI 성공은 신규 write E2E 통과 근거가 아니다.

## 승인 대기 시 인계 문구

구현을 준비했더라도 사람이 H1~H3을 승인하지 않았다면 다음처럼 보고하고 **실행을 멈춘다**.

> 구현 준비 및 로컬·정적 검증 완료 여부: [실제 결과]. 기본 브랜치 Writer bootstrap/Secret/쓰기 E2E는 사람 승인 전이므로 Not Verified. 다음 사람 작업은 [13-owner-setup-runbook.md](13-owner-setup-runbook.md)의 H1~H3이며, 실행할 계정·브랜치와 승인 범위를 먼저 확인해야 한다.

## 완료와 비목표

- **이 단계 완료:** 코딩 에이전트와 사람이 각자 할 다음 일이 독립적으로 실행 가능하고, 승인·증거 경계가 명확하다.
- **프로젝트 완료:** H4까지의 실제 필수 checks·사람 승인·squash merge가 끝났을 때 별도 판정한다.
- **비목표:** App 서버 호스팅, 여러 프로젝트용 공통 모듈 추출, 범용 PR 자동 수정 서비스, AI 추론 기반 생성, 자동 병합. 재사용화는 첫 저장소 E2E 성공 후에 판단한다.

## 참고

- [기존 GitHub App 설계](09-github-app-design.md) · [상세 구현 인계](10-implementation-handoff.md) · [검증 행렬](11-verification-plan.md)
- [실행을 맡을 사람의 절차](13-owner-setup-runbook.md)
- [Actions 이벤트·`GITHUB_TOKEN` 재귀 억제](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub Environment 권한·Secret 제약](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
