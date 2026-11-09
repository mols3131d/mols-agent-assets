# PR #294 — 재개·검증·운영 인계

## 2026-11-10 코딩 에이전트 작업 지시

**목표:** [리뷰 보고서](review-report.md)의 F2를 최소 수정으로 해결하고 F1의 제한적 자동화 결정을 유지하면서, 검증 근거와 남은 승인 경계를 정리한다. 구현 범위는 기존 PR #294에 한정하며 Draft·사람 승인 요건을 해제하지 않는다.

**작업 대상:** `mols3131d/mols-agent-assets` / PR #294 / branch `mols/chore/generated-sync-on-push`. GitHub 연결은 `main-dev`(`mols3131d`)만 사용한다. 이 문서 작성 당시 정적 리뷰 기준 head는 `0e9905b3f3ceb4ce8a4b76453471ee4d358294ff`이며 **현재 head로 가정하지 않는다**.

### 필수 작업 순서

1. PR의 최신 base/head, diff, Checks, 사람의 후속 변경·리뷰를 새로 조회한다. 루트 `CHATBOT.md`·`AGENTS.md` 및 적용 지침, [GitHub 정책](../../docs/development/github.md)·[CI 정책](../../docs/development/ci.md)·[리뷰 보고서](review-report.md)를 확인하고 기존 작업을 보존한다.
2. **F2 / 코드 수정:** `.github/workflows/generated-sync.yml`의 `jobs.sync.if`를 브랜치 전용 + `main` 제외로 제한한다. 예: `startsWith(github.ref, 'refs/heads/') && github.ref != 'refs/heads/main'`. Push ref도 `HEAD:refs/heads/${GITHUB_REF_NAME}`처럼 명시해 태그 dispatch가 브랜치 대상으로 오인되지 않게 한다.
3. **F1 / 운영 결정 유지:** 기본 `GITHUB_TOKEN`의 bot commit 후 PR Gate 재실행을 자동으로 약속하지 않는다. 현재 P0는 최초 PR을 열기 전 생성 commit 완료, 열린 PR의 후속 갱신은 사람이 승인한 정상 push/PR 이벤트로 최신 required check를 검증하는 **제한적 자동화**다. 완전 무인 요구가 새로 확인되면 임의 구현하지 말고 결정·권한을 인계한다.
4. **회귀 검증:** workflow 문법과 job 조건의 branch/main/tag 분기, generated-only stage, no-op commit 생략, `git push` 대상, `contents: write` 범위, `uv --locked` 사용을 확인한다. 저장소의 결정적 검증 및 `generated validate`를 실행할 수 있다면 실행하고, 수행하지 못한 검사는 Not Verified로 기록한다. 변경 후 최신 HEAD의 `Branch Check`·`PR Gate` 결과를 확인한다.
5. **승인 뒤 E2E:** 신규 write-capable Actions의 독립적 사람 검토와 명시적 승인 **전에는** 안전한 테스트 명목으로도 write workflow를 실행하지 않는다. 승인 후 본 문서의 '완료 판정용 시나리오'를 별도 전용 브랜치에서 테스트해 no-op, source→generated-only bot commit, 최신 PR Gate의 실제 상태를 run URL·commit SHA로 남긴다. 테스트 실패 시 증거를 기록하고 복구한다.
6. 검증 결과·미완료 항목·최신 revision 정보를 PR 설명 또는 적절한 PR 기록에 반영하고, 본 인계 내용을 필요 최소한으로 갱신한다. 기존 `Branch Check`, `PR Gate`, generator, Ruleset을 변경하거나 별도 자동화·App/PAT/Secret을 추가하지 않는다.

### 완료 판정

- [ ] F2: `main`과 `refs/tags/*`에서 sync job이 실행되지 않으며 일반 작업 브랜치에서만 실행된다. 브랜치 대상 push가 명시된다.
- [ ] generated-only stage 및 무변경 no-op 동작이 유지되고, 실패·경합 시 강제 push 없이 원인 파악이 가능하다.
- [ ] 수정 이후 최신 PR head·merge candidate의 필수 `PR Gate` 성공을 GitHub 실제 Checks로 확인한다. 과거 SHA의 pass로 대체하지 않는다.
- [ ] F1의 수동 재검증 제약을 사람이 수용했는지, 아니면 설계 변경이 필요한지 구분해 기록한다.
- [ ] 사람의 독립 검토·승인과 write E2E 결과를 각각 Pass / Not Verified로 구분한다. 미완료라면 Draft와 인계를 유지한다.

**중단 조건:** 연결 계정이 다르거나, 예상 밖 source 변경·보호 규칙 충돌·write workflow 승인 부재가 발견되면 해당 외부 쓰기/실행을 중단한다. 대체 계정, 강제 push, `main` 직접 수정, Ruleset 우회, 자동 merge를 하지 않는다. 이 작업 지시는 코딩 에이전트의 구현 인계이며 병합·운영 활성화 승인이 아니다.

---

## 지금 어디까지 진행됐나

- 대상: [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294), Draft, base=`main`, head branch=`mols/chore/generated-sync-on-push`.
- 도입물: `.github/workflows/generated-sync.yml` 한 개. 기존 generator/validator/PR Gate는 유지한다. 인계 문서인 이 파일과 [review-brief.md](review-brief.md)는 noncanonical 작업 기록이다.
- 선택: **GitHub Actions + 기본 `GITHUB_TOKEN`**. GitHub App, PAT, repository secret, Issue 생성은 요구하지 않는다.
- 검증 근거: 코드·문서 수정 후 PR head `ae51d7ac2a860a59bad0e7594c32fe3502fc3442`에서 **Branch Check와 PR Gate 성공**을 확인했다. 이후 본 인계 파일을 수정하면 새 head의 체크를 **반드시 다시 확인**해야 한다. 이 성공은 신규 write workflow의 E2E 성공을 의미하지 않는다.
- 아직 수행하지 않은 일: 생성 결과가 실제로 다른 source push로 end-to-end 테스트, 사람이 workflow를 독립 리뷰해 승인, Draft 해제, merge, 운영 활성화 확인. 위 항목을 완료 상태로 간주하지 않는다.

## 2026-11-09 수행 루프 결과

**상태: HANDOFF (운영 설계·워크플로 보완 완료 / E2E·사람 승인 미완료).**

- Research: GitHub 공식 문서에서 `GITHUB_TOKEN` push의 후속 workflow 억제와 `workflow_dispatch` 검사에 의한 required check 충족 불가를 확인. 기존 Ruleset의 required check는 `PR Gate`.
- Plan: App/PAT/추가 workflow 없이 **봇 커밋 완료 후 PR 최초 생성**을 기본 운영 경로로 선택. 열린 PR에는 검증 재트리거를 위한 사용자의 후속 이벤트가 필요하다는 한계 인정.
- Work: `generated-sync.yml`에 봇 커밋 후 Actions notice 추가, [리뷰 브리프](review-brief.md)와 본 인계의 운영 절차, PR 본문을 동기화.
- Review: `main` 직접 write 없음, generated-only staging, `uv --locked` 생성·검증, `contents: write`, no-force push 등 **11개 정적 불변식** 확인. 변경 직후의 `Branch Check`와 `PR Gate` 통과 관찰.
- 미완료: 사람의 **독립적 write-capable workflow 리뷰/승인**, 원본 push로 실제 신규 workflow 실행, no-op/변경 발생 시 봇 커밋, 최신 required PR Gate 이벤트 통합 확인. 이는 **미검증**으로 유지한다.
- 최종 경계: PR은 Draft이고 병합하지 않았다. 본 루프는 사람 승인 전에 write-capable Actions를 의도적으로 실행하지 않았다.

## 재개하는 사람이 먼저 확인할 것

1. 같은 GitHub 주 계정과 저장소 `mols3131d/mols-agent-assets`가 맞는지 확인한다. 다른 연결 계정은 사용하지 않는다.
2. PR의 최신 base/head SHA, 파일 목록, 새 커밋·리뷰·체크·충돌을 새로 읽는다. 이 문서의 특정 SHA를 최신으로 가정하지 않는다.
3. `AGENTS.md`, [GitHub 정책](../../docs/development/github.md), [VCS 정책](../../docs/development/vcs-git.md), [CI 정책](../../docs/development/ci.md), [review-brief.md](review-brief.md)를 확인한다.
4. PR에 별도의 사용자 변경이나 동시 작업이 있으면 보호한다. 강제 push, 임의 reset/rebase, main 직접 수정 없이 이번 작업을 격리한다.
5. 가장 먼저 **기본 토큰 커밋 후 required check 공백을 수용할지** 결정한다. 완전 무인 PR 검증이 요구된다면 현재 구현을 그대로 merge하지 않는다.

## Actions-only 권장 실행 순서 (P0 운영 결론)

이 저장소에서는 **작업 브랜치에 원본을 먼저 push하고 생성 파일 커밋이 끝난 뒤 PR을 생성**하는 순서가 가장 단순하다. 별도 App·PAT·Secret 없이 첫 PR의 latest head를 정상적인 `pull_request: opened` 이벤트로 검증할 수 있다.

1. 사용자의 기존 `mols3131d` 계정에서 전용 브랜치에 원본 파일을 commit/push한다. `main`에 직접 쓰지 않는다.
2. `Sync Generated Artifacts`의 실행 완료 및 성공, 브랜치 head의 generated-only commit 유무를 확인한다. 실패하거나 실행 중이면 PR을 만들지 않는다. `paths`가 선택되지 않은 변경은 생성 작업을 실행하지 않을 수 있으므로 필요한 경우 `generated validate`로 drift를 확인한다.
3. 최신 브랜치 head가 생성 결과를 포함한 것을 확인한 뒤 PR을 **처음 생성**한다. 그러면 기존 `PR Gate`는 그 head와 base를 대상으로 실행된다.
4. 열린 PR에서 나중에 원본을 수정한 경우에는 동기화 Actions가 `GITHUB_TOKEN`으로 커밋하더라도 `PR Gate`가 자동 갱신되지 않을 수 있다. 자동 커밋 후 **사람 계정의 정상 push로 `pull_request: synchronize`를 유발**하고 최신 head/merge candidate의 required check를 직접 확인한다. 단순 과거 run 재실행이나 `workflow_dispatch`는 이 해결책을 대체하지 않는다.
5. 이 수동 단계가 반복적인 운영 부담이 된다는 증거가 쌓일 때만, 별도 기술 검토 및 사람 승인 아래 다른 인증/워크플로 방식을 검토한다. 현재 PR은 완전 무인 PR 검증을 약속하지 않는다.

`generated-sync.yml`은 봇 커밋 직후 후속 체크 공백에 대한 Actions notice를 출력한다. Notice는 경고이자 운영 안내일 뿐 검증 실행이나 합격 근거가 아니다.

### 실행 제한

- 신규 write-capable workflow는 **사람이 변경된 실행 권한과 스크립트를 독립 검토하고 명시적으로 승인하기 전까지** 원본 push로 활성화해서는 안 된다. 이 PR 자체의 `Branch Check`/`PR Gate` 통과는 독립 승인이나 E2E 검증이 아니다.
- 현재 draft PR #294는 이미 열린 PR이므로 위의 'PR 생성 전 동기화' 순서를 소급 적용했다고 주장하지 않는다.
- E2E 테스트는 사람 승인 후 별도 전용 테스트 브랜치와 독립적인 확인 경로에서 수행한다. 테스트 완료 전에는 미검증 상태를 유지한다.

## 구현 계약과 실제 사용

- Trigger: 작업 브랜치의 `push` 중 현재 workflow의 source path filter에 맞는 변경이 있을 때. `main`은 제외한다.
- Run: 잠긴 `uv` 의존성으로 `python -m scripts.generated_artifacts sync` → `validate --all`.
- Write: `docs/**/INDEX.tsv`, `catalog/INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl`에 한정해 stage; `git diff --cached --quiet`가 변경 없다고 판단하면 commit/push 생략.
- Commit: `github-actions[bot]` 명의, `chore(generated): sync indexes and routes`; 기본 `GITHUB_TOKEN`에서 `contents: write` 사용. `main`이나 다른 브랜치로 쓰지 않는다.
- 기존 `PR Gate`는 별도 read-only validation이며 generator를 자동 반영하지 않는다.

## 완료 판정용 시나리오

| 시나리오 | 실행 방법 | 기대 증거 |
| --- | --- | --- |
| No-op | 원본과 생성 결과가 이미 일치하는 작업 브랜치에서 원본 파일 push 또는 병합 후 workflow 수동 실행 | `sync`·`validate` 성공, 자동 커밋 없음 |
| 원본 변경 | PR head를 기반으로 별도 임시 작업 브랜치 준비 후 기존 문서/Skill의 승인된 작은 source 변경을 push | workflow 실행, 예상 `INDEX.tsv`/`route/*.jsonl`만 변경된 bot commit |
| 생성 검증 | `uv run --locked --no-default-groups --group test python -m scripts.generated_artifacts validate --all` | 변경 결과의 정합성 성공 |
| PR 재검증 | 자동 커밋 직후 최신 PR head의 Checks 조회 | 필수 `PR Gate`가 생성됐는지 직접 확인. 기본 토큰 한계로 **생성되지 않을 가능성을 예상**하고 성공이라고 쓰지 않음 |
| 변경 영향 제외 | 생성 출력만 다른 커밋으로 push된 경우 | `paths` 필터로 동기화 workflow가 재실행되지 않음 |
| 오류/경합 | 실패 로그 또는 branch 이동 상황 조사 | 데이터 손실·강제 push·무조건 성공 처리 없이 명확히 실패하고 원인 확인 가능 |

실제 검증 시 작업 브랜치와 임시 브랜치를 혼동하지 않고, 자동 생성 결과 외의 원본 수정은 작업 범위에 맞게 별도 PR로 유지한다. 테스트를 위해 `main`에 실험용 커밋을 하지 않는다.

## 자동 커밋 이후 PR Gate가 없는 경우

기본 `GITHUB_TOKEN` push가 후속 `push`/`pull_request` workflow를 자동 시작하지 않는 것이 핵심 제약이다. 따라서 **과거 체크 재실행만으로 다른 SHA의 required check가 충족된다고 추정하지 않는다**.

- 우선 PR의 최신 head 및 merge commit 대상 required check를 확인한다. `PR Gate`가 최신 후보를 검증했는지 GitHub가 표시하는 정보를 근거로 판단한다.
- 현재 구조를 수용한 경우 사람이 기존 계정으로 새 정상 push를 수행해 `pull_request` synchronize와 `PR Gate` 재검증을 유도한다. 예: 전용 테스트 브랜치에서 리뷰 가능한 실제 소규모 후속 커밋. 불가피할 때만 `git commit --allow-empty -m "chore(ci): revalidate generated artifacts"` 후 push를 사용한다. 이는 **수동 우회**이지 완전 자동화의 증거가 아니다.
- 빠짐없이 무인 실행되어야 한다면 인증 전환 또는 CI orchestration을 별도 설계·검토한다. Ruleset 우회, required check 면제, 성공 상태를 임의로 만드는 방법은 허용하지 않는다.

## 실패 시 복구

- `sync`/검증 실패: 실패한 Actions run의 step 로그 확인 → 해당 source/lock/네트워크 의존성 확인 → 전용 브랜치에서 원인을 수정하고 정상 push. 검증을 끄지 않는다.
- `403 Resource not accessible by integration`: 해당 workflow에 부여된 `contents: write`와 저장소/조직 정책을 확인한다. 토큰이나 저장소 권한을 무조건 확대하지 않는다.
- `non-fast-forward`: runner checkout 이후 브랜치가 이동했는지 비교하고 최신 ref에서 다시 실행/동기화한다. 강제 push하지 않는다.
- `nothing to commit`: 정상 no-op이면 커밋 없이 종료되는 것이 맞다. 기대했던 생성 결과가 빠졌다면 `paths`와 source-to-projection mapping을 점검한다.
- PR 체크 미보고: 위 'PR Gate가 없는 경우' 절차로 원인을 분류하고 최신 SHA 체크를 얻기 전 병합하지 않는다.

## 리뷰·병합 인계 기준

1. [review-brief.md](review-brief.md)의 High 항목 두 개(쓰기 권한, PR Gate 공백)를 사람 검토자가 이해·판단한다. 필요하면 Draft를 유지하고 설계를 변경한다.
2. PR 최신 diff 범위, 검증 결과, 해당 commit의 `revision.base`/`revision.head`를 PR 설명과 일치시킨다.
3. Required `PR Gate`가 최신 대상에서 성공하고 별도 승인 조건을 만족하면 사람의 명시적 승인 아래 **squash merge**한다. 인계자가 merge를 자동 수행하지 않는다.
4. 병합 후 임시 브랜치로 실제 no-op/source-change smoke test를 실행한다. 성공·실패 각각의 run 링크/commit SHA를 PR comment 또는 후속 PR에 기록한다.
5. 운영 단계에서 비슷한 문제가 반복되면 생성기/동기화 로직은 `scripts/generated_artifacts.py`, CI 의미는 `docs/development/ci.md`와 기존 PR Gate를 정본으로 유지한다. 이 인계 문서를 새 정책 정본처럼 취급하지 않는다.

## 근거 링크

- [GitHub: workflow를 다른 workflow에서 시작하는 경우](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub: required checks의 최신 commit 기준](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
- [Workflow 구현](../../.github/workflows/generated-sync.yml)
- [Generator entrypoint](../../scripts/generated_artifacts.py)
- [PR Gate](../../.github/workflows/pr-gate.yml)
