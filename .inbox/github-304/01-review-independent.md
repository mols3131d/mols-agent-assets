# PR #304 Independent Review Report

> [!NOTE]
> `.inbox/` 비정본 독립 리뷰 기록입니다. 저장소 정책이나 GitHub PR 승인·검증을 대신하지 않습니다.

**후속 상태:** 아래는 `e8af238` 독립 리뷰 당시의 판정입니다. 이후 F1을 해결하고 최신 `main` 기준 CI를 통과한 뒤 사용자 승인으로 squash merge했습니다. 최종 근거는 이 문서 끝의 `Merge Outcome`에 구분해 기록합니다.

**판정: 검토 범위에서 코드 변경을 요구하는 결함은 발견하지 못했습니다.** `Critical`·`High`·`Medium` finding은 없고, PR 본문 `Validation`의 현행 규약 불일치(`Low` F1) 1건이 남아 있습니다. 구조·결정론적 검증은 통과했지만 Hook·Command 런타임 실행은 검증하지 않았습니다. 이 로컬 검토 권고는 GitHub의 `Approve` 제출이나 사람의 병합 승인이 아닙니다.

| 항목 | 값 |
| --- | --- |
| 대상 | [PR #304 — `feat(rulesync): subagents·hooks·commands 지원 확장`](https://github.com/mols3131d/mols-agent-assets/pull/304) |
| 브랜치 / 범위 | `mols3131d/feat/rulesync-subagents-hooks-commands` (`c39d094f72cfb331217bc70abb303c738493dd4c..e8af2387212df3c730f0ec553325bdb8d7b1ef1e`) |
| `origin/main` 비교 | `016439fe20b7e12f443e61252cc32bc624329010` (#307·#302 병합 후에도 3-dot diff는 동일한 3파일 `+16 / -11`) |
| 검토 방법 | `mols-review-dualvantage` 절차에 따른 독립 `Verifier`·`Challenger` 병렬 위임 + Root 직접 대조·로컬 검증 |

## Findings

### 🔵 Low · F1 — PR 본문 `Validation` 표기가 #307 병합 이후의 현재 `main` 템플릿 규약과 다름

- **영향:** 기능·검증 결함은 아니지만, PR #304 생성 이후 `main`에 병합된 #307(`6de7f6c`)이 PR 본문 `Validation`의 상태 아이콘(`✅ Pass` / `⚪ Not Verified`) 표기를 체크박스(`[x]` / `[ ]`) 단일 표기로 통일하고 미검증 사유를 텍스트로 적도록 변경했습니다. 현재 PR #304 본문은 #307 이전 형식(`- ⚪ Not Verified — ...`, `- ✅ Pass — ...`)을 유지하고 있습니다.
- **권고 조치:** 원격 PR 본문의 `Validation`을 현행 체크박스 형식으로 정리합니다. 실제 통과한 검증만 `[x]`로 표시하고, 미검증 항목에는 이유를 남깁니다. 코드 수정은 필요 없으며 non-blocking finding으로 분류하지만, 이전 base에서 작성됐다는 이유로 현재 규약의 예외를 부여하지는 않습니다. 이 후속 작업에서는 원격 본문을 수정하지 않았습니다.
- **근거:** [PR #304 본문](https://github.com/mols3131d/mols-agent-assets/pull/304), `origin/main`의 [GitHub 정책](https://github.com/mols3131d/mols-agent-assets/blob/016439fe20b7e12f443e61252cc32bc624329010/docs/development/github.md#authoring)과 [PR 템플릿](https://github.com/mols3131d/mols-agent-assets/blob/016439fe20b7e12f443e61252cc32bc624329010/.github/pull_request_template.md). 현재 체크아웃의 해당 파일은 #307 이전 버전이므로 이 finding의 비교 기준과 구분합니다.

## DualVantage Adjudication Summary

- **`Verifier` (`mols-review-dualvantage-verifier`):** `No material candidate` 반환. Rulesync `v43.2.0` 계약과 관련 소스·검증을 확인한 범위에서 material candidate를 보고하지 않았습니다. 모든 입력·런타임에서 회귀가 없다는 보증으로 확대하지 않습니다.
- **`Challenger` (`mols-review-dualvantage-challenger`):** 가설 `C1` 1건 제기 — 향후 `src/rulesync/.rulesync/hooks.jsonc`에서 `antigravity-ide.hooks`와 `antigravity-cli.hooks`를 서로 다르게 정의할 경우, `HooksProcessor`가 별도 경고 없이 target 순서대로 `.agents/hooks.json`을 덮어써 `mise run rulesync-validate`가 이를 걸러내지 못한다는 점.
  - **Root 판정 (`rejected` as defect / 잔여 운영 위험으로 유지):**
    1. 현재 `src/rulesync/.rulesync/`에는 Hook 원본이 없으며, [`src/rulesync/rulesync.jsonc`](../../src/rulesync/rulesync.jsonc)는 개별 자산이 아닌 라이브러리의 vendor support ceiling을 선언합니다.
    1. [`docs/tools/rulesync.md`](../../docs/tools/rulesync.md)가 *"Antigravity IDE·CLI는 프로젝트 `.agents/` 경로를 공유하고 Hook 파일을 전체 교체합니다. 상충하는 target별 Hook 구성을 같은 출력 루트에 생성하지 않습니다."*라고 해당 제약을 정확히 명시하고 있고, PR 본문 `Risks`에도 이미 `🟡 Medium`으로 기록되어 있습니다.
    1. [Agent Asset Design Principles](../../docs/development/agent-assets/design-principles.md)의 **YAGNI** 및 [Validation 정책](../../docs/development/validation.md)("Schema나 projection semantics를 별도 validator에서 다시 구현하지 않습니다")에 따라, 아직 존재하지 않는 Hook 원본을 위해 `rulesync_validate.py`에 커스텀 파서를 추가하는 것은 불필요합니다.

## Contract Verification Matrix

| 검토 영역 | 결과 | 확인 근거 |
| --- | --- | --- |
| Target / Feature ceiling (`src/rulesync/rulesync.jsonc`) | ✅ Verified | Rulesync `v43.2.0` `supported-tools` 및 processor 구현 대조 완료: 6개 타깃 모두 project-scope `rules`·`skills`·`subagents`·`hooks` 지원; `commands`는 `claudecode`·`copilot`·`antigravity-ide`·`antigravity-cli`만 project-scope 지원(`codexcli`는 global-only, `copilotcli`는 미지원으로 제외 정당) |
| Root self-consumer 분리 (`rulesync.jsonc`) | ✅ Verified | `8484886`에서 루트 `rulesync.jsonc` 변경을 원복해 `origin/main`과 diff 0. 루트의 미사용 feature 활성화는 최종 변경에서 제외됐으며, 라이브러리 출력에 대한 모든 `--delete` 부작용을 검증한 것은 아님 |
| `preserveUnownedHooks` 및 `.rulesync-hooks-lock.json` (`docs/tools/rulesync.md`) | ✅ Verified | `v43.2.0` `ConfigParamsSchema`의 `"preserveUnownedHooks": true` 유효성 확인. 6개 타깃 중 `claudecode`·`codexcli`만 `supportsPreserveUnowned() === true`로 동작하며 `copilot`·`copilotcli`·`antigravity-ide`·`antigravity-cli`는 파일 전체를 교체함(문서의 *"일부 target에만 적용"* 및 lock 설명과 정확히 부합) |
| Antigravity 공유 출력 경로 (`docs/tools/rulesync.md`) | ✅ Verified | `AntigravityIdeCommand`·`AntigravityCliCommand`는 `.agents/skills/<name>/SKILL.md`로 생성되며 동명 Skill 우선(`rulesyncSkillTakesPrecedence` + warning, `rulesync_validate.py`가 warning을 실패 처리). `AntigravityIdeHooks`·`AntigravityCliHooks`는 `.agents/hooks.json`을 공유·전체 교체함 |
| 소비자 안내 및 문서 정합성 (`docs/using-this-repository.md`) | ✅ Verified | `src/rulesync/.rulesync/`에 현재 `skills/`·`subagents/`만 존재하고 `commands/`·`hooks/` 원본이 없음을 명시. 두 문서의 frontmatter `description`이 유지되어 #302의 `docs/INDEX.tsv`·`docs/tools/INDEX.tsv`와 무충돌 |

## Validation

- ✅ Pass — `mise run rulesync-validate`: `PASS config`, `PASS configured-projection` (`rulesync 43.2.0` 기준 `doctor --strict` 및 `generate --dry-run` 245 files: 41 subagents + 204 skills, warning 0)
- ✅ Pass — `mise doctor project`: `PASS python-lock`, `PASS rulesync-root` (`2 passed, 0 failed`)
- ✅ Pass — `mise run test`: **`438 passed in 9.59s`**
- ✅ Pass — `uv run --locked --no-default-groups --group test python scripts/docs_frontmatter_validate.py`: `PASS documentation frontmatter`
- ✅ Pass — `uv run --locked --no-default-groups --group test python -m scripts.generated_artifacts validate --all`: `PASS docs-indexes`, `PASS catalog-indexes`, `PASS distribution-routes`, `PASS repository-routes` (`--changed-from origin/main` 포함)
- ✅ Pass — `mise exec -- biome check src/rulesync/rulesync.jsonc rulesync.jsonc`: `Checked 2 files in 25ms. No fixes applied.`
- ✅ Pass — `mise exec -- rumdl check --no-cache docs/tools/rulesync.md docs/using-this-repository.md`: `Success: No issues found`
- ✅ Pass — 원격 GitHub Actions (HEAD `e8af238`): [PR Gate (run 43714619991)](https://github.com/mols3131d/mols-agent-assets/actions/runs/43714619991), [Branch Check (run 43714617757)](https://github.com/mols3131d/mols-agent-assets/actions/runs/43714617757)
- ⚪ Not Verified — 실제 Hook·Command 작성 원본의 생성·호출·런타임 실행 smoke test (이 PR에는 해당 원본이 없으며 범위 밖)

## Residual Risks and Merge Gate

- **🟡 Medium (문서화된 운영 경계):** 추후 `src/rulesync/.rulesync/hooks.jsonc`를 실제로 도입할 때는 (1) `preserveUnownedHooks`가 `claudecode`·`codexcli`에만 적용된다는 점과 `.rulesync-hooks-lock.json` 관리, (2) `antigravity-ide`와 `antigravity-cli`에 서로 다른 Hook override를 주면 `.agents/hooks.json`이 무경고 덮어써진다는 점을 preview diff로 확인해야 합니다.
- **통합 조건:** [GitHub 정책](../../docs/development/github.md)상 [`src/rulesync/rulesync.jsonc`](../../src/rulesync/rulesync.jsonc)는 에이전트 제어 표면 변경입니다. 실제 병합 시 최신 head·merge candidate의 required checks와 GitHub 조건을 다시 확인하고 **사람의 명시적 승인**을 받아 `squash` merge합니다. #302·#307 이후 `main`과 결합한 후보를 이 로컬 검토에서 실행했다고 주장하지 않습니다.

## Follow-up Verification

2026-11-18 후속 확인에서 로컬 HEAD와 원격 PR head는 모두 `e8af2387212df3c730f0ec553325bdb8d7b1ef1e`로 유지됐고, 별도로 조회한 원격 `main`도 위 비교 SHA(`016439fe`)와 같았습니다. GitHub 상태는 `OPEN`·`MERGEABLE`·`CLEAN`이며 기존 `PR Gate`·`Branch Check`는 성공, 제출된 리뷰·리뷰 요청·일반 코멘트는 각각 0건입니다. 위 실행 결과는 앞선 독립 리뷰 당시 해당 head의 근거이며, 문서 정합성만 다룬 후속 확인에서 전체 테스트를 중복 실행하지 않았습니다.

F1은 두 reviewer가 공통으로 보고한 코드 결함이 아니라 코디네이터가 `origin/main`의 작성 규약과 대조해 기록한 본문 finding입니다. 비교 기준과 승인 경계를 명확히 했으며, 이전에 실패한 리뷰 호출은 독립 검토 근거에 포함하지 않았습니다. 두 인박스 문서는 로컬 미커밋 파일이고, 이 작업에서는 GitHub 리뷰 제출·PR 본문 수정·커밋·푸시·병합을 수행하지 않았습니다.

## Merge Outcome

2026-11-18 사용자가 명시적으로 merge를 요청했습니다. 이전 리뷰 결과는 위 기준 head의 기록으로 보존하고, 후속 조치를 다음과 같이 확인했습니다.

- **F1 해결:** 현재 `main`의 PR 템플릿을 확인하고 원격 본문 `Validation`을 체크박스로 정리했습니다. 미검증 런타임 항목은 unchecked로 남겼고 최신 CI 링크·명령·결과와 정확한 base/head provenance를 추가했습니다.
- **최신 후보 준비:** `main`(`016439fe20b7e12f443e61252cc32bc624329010`)을 PR 브랜치에 GitHub native update-branch로 병합했습니다. 새 head는 `89f67cf1343efd672ad2e1dc5c0a77e645c5d91f`이며 원래 3개 변경 파일은 독립 리뷰 head `e8af238`과 동일합니다. History를 재작성하거나 커스텀 validator를 추가하지 않았습니다.
- **새 CI 통과:** [PR Gate 44140165201](https://github.com/mols3131d/mols-agent-assets/actions/runs/44140165201)은 candidate `cf94358ee90c19b6f69e83c5fbe8f46fdfd27662`를 checkout해 `uv run --locked --no-default-groups --group test pytest -q tests` **473 passed**, frontmatter·docs-indexes·mise Doctor·Rulesync 검증을 통과했습니다. [Branch Check 44140153169](https://github.com/mols3131d/mols-agent-assets/actions/runs/44140153169)도 **473 passed**와 local projection 검증을 통과했습니다.
- **Squash merge 확인:** `--match-head-commit 89f67cf...`를 지정해 merge했습니다. GitHub는 `MERGED`, 병합 시각 `2026-11-17T17:47:34Z`(KST 2026-11-18 02:47:34), 계정 `mols3131d`, `main`의 squash commit [`df82086d0fac43f96dea17ff92a64466605e9402`](https://github.com/mols3131d/mols-agent-assets/commit/df82086d0fac43f96dea17ff92a64466605e9402)를 반환했습니다. 보호 우회 없이 수행했고 실제 commit tree는 CI 후보와 동일한 `c2bb0c6d840641ff88847ca3602a3ced2d19cb57`입니다.
- **로컬 보존·범위:** 이 리뷰를 GitHub `Approve`로 제출하지 않았습니다. 인박스 두 문서는 여전히 로컬 미커밋 상태이며 최종 3파일 변경에 포함하지 않았습니다. 실제 Hook·Command 런타임 실행은 여전히 범위 밖·미검증입니다.
