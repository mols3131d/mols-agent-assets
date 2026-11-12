# PR #294 — 독립 리뷰 보고서

> 검토일: 2026-11-10. **검토 기준:** base `fa5be3bd63e9c29c30017b9e8c833018c092b9a7`, head `49b594ca8a5962cd2db01ba9c9bed3781be6a895`. 이후 문서 커밋은 이 코드 리뷰의 대상이 아니며, 최신 상태는 다시 확인해야 한다. 이 문서는 `.inbox/`의 비정본 작업 근거다.

## 판정

**조건부 보류 — Draft 유지.** 기존 generator를 재사용해 작업 브랜치의 파생 파일만 커밋하는 구현에는 새로운 확정 코드 결함이 발견되지 않았다. 그러나 기본 `GITHUB_TOKEN`으로 생성 파일을 push한 뒤 최신 PR 후보의 required `PR Gate`가 갱신되는지 불명확하며, 신규 write workflow의 실제 E2E와 사람의 독립 승인이 없다. 현재 CI 통과를 write 경로의 성공으로 해석하지 않는다.

- 대상: [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294), `mols3131d/mols-agent-assets`; head branch `mols/chore/generated-sync-on-push`.
- 변경: [generated-sync.yml](../../.github/workflows/generated-sync.yml) 1개와 `.inbox/github-294/` 문서 4개. 기존 generator, validator, Branch Check, PR Gate와 Ruleset은 변경하지 않았다.
- 강제 조건: Ruleset `protect-main`의 `PR Gate` required check 및 squash merge. 이와 별개로 [GitHub 정책](../../docs/development/github.md)은 쓰기 가능한 통제 표면의 독립 근거와 사람의 명시적 승인을 요구한다.

## Findings 및 처분

### F1 — High · 미해결 운영 제약: 봇 커밋 이후 최신 PR Gate 확인

- **근거:** `generated-sync.yml` 62–73행은 `github.token`을 이용해 생성 결과를 원본 작업 브랜치로 push한다. 기존 [pr-gate.yml](../../.github/workflows/pr-gate.yml)은 `pull_request` 이벤트에서만 실행한다.
- **영향:** 원본 push에 대한 검사 성공이 그 이후 발생한 봇 커밋의 최종 PR 후보까지 검증했다고 보장할 수 없다. `GITHUB_TOKEN`에 의한 일반 `push`는 후속 workflow 실행을 트리거하지 않는다.
- **2026-06 변경사항의 정확한 범위:** GitHub는 `GITHUB_TOKEN`으로 **PR을 생성하거나 갱신**하여 발생하는 `pull_request: opened/synchronize/reopened` 이벤트에서 *승인 대기* workflow run을 허용한다. 하지만 현재 YAML의 동작은 **브랜치에 `git push`**하는 것이다. 이 예외가 본 경로에서 최신 required check를 만들어 준다고 추론하지 않는다. 실제 PR의 run/approval 상태를 관찰해야 한다.
- **처분:** 코드 결함으로 자동 판정하거나 새 인증 방식을 강제하지 않는다. 현재 P0는 **원본 push → 생성 봇 커밋 완료 → 최초 PR 생성**을 기본 운영 순서로 유지한다. 이미 열린 PR에서 봇 커밋이 발생하면 최신 head/merge candidate의 검사 상태를 확인하고, 필요 시 동일 사용자의 승인된 후속 이벤트로 재검증한다. 완전 무인 운영이 필수면 별도 설계 결정이 필요하다.
- **근거:** [GitHub: Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [2026-06-11 GitHub Changelog](https://github.blog/changelog/2026-06-11-bot-created-pull-requests-can-run-workflows-if-approved/), [Required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

### F2 — Medium · 코드 수정 완료: 수동 실행 시 태그 ref 허용

- 이전 조건은 `refs/tags/*`에서 job을 차단하지 못했다.
- 현 구현은 `startsWith(github.ref, 'refs/heads/') && github.ref != 'refs/heads/main'`으로 브랜치에 한정하고, `HEAD:refs/heads/${GITHUB_REF_NAME}`으로 push ref를 지정한다.
- **처분:** 정적 수정 확인. 태그/main 차단, 실제 수동 실행은 E2E 검증과 구분한다. 이미 해결된 문제를 신규 수정 과제로 재발행하지 않는다.

### G1 — High · 승인 게이트: 권한 있는 Actions

- 신규 workflow는 `permissions: contents: write`를 갖는다. 분리된 write workflow, `persist-credentials: false`, no-force push, 단계별 `GH_TOKEN` 제공은 합리적인 제한이다.
- 다만 통제 표면의 독립 검토와 사람 승인은 **미확인**이다. 자동 검사·AI 리뷰·이 문서는 승인 근거가 아니다.
- **처분:** 사람의 명시적 승인 이전에는 새 write workflow를 테스트 명목으로도 실행하지 않는다.

### G2 — High · 검증 게이트: 신규 write 경로 E2E

- 실제 원본 변경 → generator → generated-only bot commit, no-op에서 무커밋, 오류/경합 및 최신 PR 후보 검증의 원격 실행 근거가 없다.
- **처분:** 승인 뒤 격리된 브랜치에서 검증한다. `workflow_dispatch`는 이 workflow가 기본 브랜치에 없을 때 수동 실행 엔트리로 기대하지 말고, 병합 전에는 일반 작업 브랜치 `push` 경로로 검증한다.
- 검증 실패는 정상적으로 실패로 기록하고, 필수 check를 면제하거나 성공 상태를 꾸미지 않는다.

## 구현 검토 결과

| 항목 | 확인한 사실 | 평가 |
| --- | --- | --- |
| 범위 | `main` 제외, branch ref 조건, source path filter | 정적 Pass |
| 생성 | 기존 `scripts.generated_artifacts sync` / `validate --all`, `uv --locked` | 정적 Pass |
| 쓰기 | `docs/**/INDEX.tsv`, `catalog/INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl`만 stage | 정적 Pass |
| 무변경 | `git diff --cached --quiet`이면 커밋 생략 | 정적 Pass |
| 안전성 | 강제 push·추가 PAT/App/secret·`main` 직접 push 없음 | 정적 Pass |
| 범위 확대 | 현 generator source-to-projection mapping과 필터에서 확정 누락 발견되지 않음 | 정적 검토, 미래 경로 추가 시 재검토 |
| 경합 | branch tip이 전진하면 non-fast-forward 실패 가능 | 복구 절차 필요, 데이터 덮어쓰기 없음 |

## 증거 및 미검증

| 구분 | 결과 | 근거·한계 |
| --- | --- | --- |
| Branch Check | **Pass** | [run 42673980412](https://github.com/mols3131d/mols-agent-assets/actions/runs/42673980412), 기준 head `49b594ca` |
| PR Gate | **Pass** | [run 42673991539](https://github.com/mols3131d/mols-agent-assets/actions/runs/42673991539), 기준 head `49b594ca` |
| 기존 코드 검증 기록 | 이전 스냅샷에서 `mise check`, `mise test`(434 passed), generated validation 보고 | 해당 커밋의 기록이며 이번 리뷰에서 재실행하지 않음 |
| Write workflow no-op/커밋/notice | **Not Verified** | 해당 head의 실행 목록에 신규 workflow 결과 없음 |
| 봇 커밋 후 최신 required check | **Not Verified** | 후속 PR 이벤트/approval/run 실제 관찰 필요 |
| 사람 독립 승인 | **Not Verified** | 이 보고서와 GitHub Checks는 승인 아님 |

## 다음 결정

1. **사람 검토·승인:** YAML의 실행 권한·토큰·쓰기 대상·호출하는 generator를 독립적으로 검토하고 테스트 승인 여부를 명시한다.
2. **격리 E2E:** [handoff.md](handoff.md)의 테스트 순서에 따라 no-op, 생성 변경, 오류/경합과 최신 PR 검증 근거를 수집한다.
3. **운영 선택:** 열린 PR에 대한 추가 수동 검증을 수용할지 결정한다. 수용하면 이 제약과 복구 절차를 인계한다. 자동 갱신까지 필수라면 별도 설계를 진행한다.
4. **병합 판정:** 최신 head와 base의 required check 및 사람 승인 조건을 다시 확인한 뒤에만 Draft 해제·squash merge를 검토한다.

**범위:** 본 보고서는 read-only 코드·설정·CI 상태 검토 결과다. 새 Actions 실행, 실행 권한 승인, 자동화 활성화, 병합은 수행하지 않았다.
