# PR #304 Status Briefing

> [!NOTE]
> `.inbox/` 비정본 작업 브리핑입니다. 저장소 정책·실행 지침이나 GitHub 승인 상태를 대신하지 않습니다.

**Squash merge 완료:** [PR #304](https://github.com/mols3131d/mols-agent-assets/pull/304)(`feat(rulesync): subagents·hooks·commands 지원 확장`)가 사용자 명시적 승인과 최신 `main` 기준 CI 통과 후 `main`의 [`df82086`](https://github.com/mols3131d/mols-agent-assets/commit/df82086d0fac43f96dea17ff92a64466605e9402)에 반영됐습니다(2026-11-18 02:47:34 KST). PR 본문을 현행 체크박스 형식으로 갱신해 `Low` F1도 해결했습니다. 로컬 인박스 문서는 미커밋 상태로 보존했습니다.

| 항목 | 상태 (2026-11-18 기준) |
| --- | --- |
| 브랜치 / 로컬 | `mols3131d/feat/rulesync-subagents-hooks-commands` (`e8af238`, `--no-track` 체크아웃, `.inbox/github-304/` 외 clean) |
| 최종 PR base / head | `016439fe20b7e12f443e61252cc32bc624329010` / `89f67cf1343efd672ad2e1dc5c0a77e645c5d91f` (`main` 반영용 merge commit 추가) |
| PR 상태 / 병합 | `MERGED` · squash commit `df82086d0fac43f96dea17ff92a64466605e9402` · 병합 계정 `mols3131d` |
| 리뷰 상태 | 로컬 [독립 리뷰 보고서](01-review-independent.md) 완료, 코드 수정 요구 없음 · 본문 `Low` F1 해결 · GitHub `Approve`는 별도 제출하지 않음 |
| 변경 규모 / 범위 | 최종 `main` 반영 3 files (`+16 / -11`); 로컬 인박스 문서는 포함하지 않음 |

## Changes

초기 커밋(`65c2d0a`)에서 루트 [`rulesync.jsonc`](../../rulesync.jsonc)까지 확장했으나, 소비 원본 없이 기능을 켜면 `generate --delete` 시 기존 산출물이 정리될 위험이 있어 `8484886`에서 원복했습니다. **라이브러리 support ceiling과 루트 self-consumer를 분리**한 원래 7커밋에 최신 `main` 반영용 merge commit(`89f67cf`)을 추가한 뒤 squash merge했습니다. 실제 변경 범위는 3개 파일(`+16 / -11`)로 유지됐습니다.

### [`src/rulesync/rulesync.jsonc`](../../src/rulesync/rulesync.jsonc) (`+8 / -7`)

`"preserveUnownedHooks": true`를 추가하고, 기존 6개 런타임의 `subagents` 지원을 유지한 채 `hooks`·`commands` 지원 범위를 확장했습니다(`b22871e`).

| Target | 변경 | 최종 Feature 구성 |
| --- | --- | --- |
| `claudecode`, `copilot` | `+hooks` | `rules`, `skills`, `subagents`, `commands`, `hooks` |
| `antigravity-ide`, `antigravity-cli` | `+commands`, `+hooks` | `rules`, `skills`, `subagents`, `commands`, `hooks` |
| `codexcli` | `+hooks` (`commands` 미포함: global-only) | `rules`, `skills`, `subagents`, `hooks` |
| `copilotcli` | `+hooks` (`commands` 미포함: project 미지원) | `rules`, `skills`, `subagents`, `hooks` |

### Documentation (`+8 / -4`)

- **[`docs/tools/rulesync.md`](../../docs/tools/rulesync.md) (`+5 / -1`, `9cd8ad6`·`fd18ba3`·`e8af238`):** 라이브러리 ceiling·루트 self-consumer 분리와 미보유 원본 기능 사전 활성화 금지, project-scope `commands` 제한(`codexcli`·`copilotcli` 미활성화, Antigravity `Commands→Skills` 이름 충돌 확인), Hook 생성 위험(`preserveUnownedHooks` 부분 적용, `.rulesync-hooks-lock.json` 보존, Antigravity IDE·CLI `.agents/` 공유 경로 전체 교체)을 명시했습니다.
- **[`docs/using-this-repository.md`](../../docs/using-this-repository.md) (`+3 / -3`, `ab8104e`):** `Import Subagents, Commands, and Hooks` 섹션으로 확장하고, 현재 [`src/rulesync/.rulesync/`](../../src/rulesync/.rulesync/)에는 `skills`·`subagents`(7개)만 있고 Command·Hook 원본은 없음을 밝혔습니다. Feature 활성화·route 등재만으로 설치/실행되지 않으며 preview 후 명시 적용이 필요함을 안내합니다.

## Validation and Constraints

| 구분 | 결과 | 근거 및 세부 내용 |
| --- | --- | --- |
| 최종 `PR Gate` (`89f67cf`) | ✅ Pass | [run 44140165201](https://github.com/mols3131d/mols-agent-assets/actions/runs/44140165201): 최신 `main`(`016439fe`)과 결합한 candidate `cf94358` checkout, `pytest -q tests` **473 passed**, frontmatter·docs-indexes·mise Doctor·Rulesync `config`·`configured-projection` 통과 |
| 최종 `Branch Check` (`89f67cf`) | ✅ Pass | [run 44140153169](https://github.com/mols3131d/mols-agent-assets/actions/runs/44140153169): `pytest -q tests` **473 passed**, frontmatter·docs-indexes·catalog-indexes·distribution-routes 통과 |
| 기존 로컬 검증 (`e8af238`) | ✅ Pass | `mise run rulesync-validate` (`PASS config`, `PASS configured-projection`, 245 files dry-run, warning 0), `mise doctor project` (`2 passed`), `mise run test` (**438 passed**), frontmatter·generated artifacts 4종·Biome·rumdl. 최신 head 결과와 혼동하지 않으며, 최종 후보는 위 CI로 검증 |
| 독립 다관점 리뷰 (`e8af238`) | 검토 완료 | [01-review-independent.md](01-review-independent.md): 코드 수정 요구 없음. 최종 head에서도 원래 3개 변경 파일의 바이트 동일성 확인; 본문 `Low` F1은 체크박스 형식과 provenance 갱신으로 해결 |
| 실물 Hook·Command 런타임 | ⚪ Not Verified | [`src/rulesync/.rulesync/`](../../src/rulesync/.rulesync/)에 `commands/`·`hooks/` 원본이 없어 생성·실행 smoke test는 PR 범위 밖 |

- **최종 후보 정합성:** candidate `cf94358`과 실제 squash commit `df82086`의 Git tree는 모두 `c2bb0c6d840641ff88847ca3602a3ced2d19cb57`입니다. #302·#307 반영 후 실제 병합된 파일 내용이 통과한 CI 후보와 동일함을 확인했습니다.
- **승인·권한:** 사용자의 명시적 merge 요청에 따라 [GitHub 정책](../../docs/development/github.md)을 적용했습니다. `--match-head-commit 89f67cf...`로 head를 고정하고 required checks·GitHub 조건을 확인했으며, `--admin`·보호 우회·force push는 사용하지 않았습니다.

## Completion and Remaining Boundary

- **완료:** PR 본문 정리, 최신 `main` 반영, 최종 CI 통과, expected-head squash merge, GitHub `MERGED` 및 `main` commit 확인.
- **보존:** 로컬 checkout은 `e8af238`에 그대로 두고 인박스 두 문서를 미커밋 상태로 유지했습니다. 자동으로 stage·push하거나 로컬 브랜치·파일을 삭제하지 않았습니다.
- **미검증 경계:** 실제 Hook·Command 작성과 런타임 smoke test는 범위 밖으로 남깁니다. 신규 원본을 도입할 때 문서화된 보존·공유 출력 제약을 별도로 검증합니다.

---

*병합 확인(2026-11-18): 최종 PR base `016439fe20b7e12f443e61252cc32bc624329010`, head `89f67cf1343efd672ad2e1dc5c0a77e645c5d91f`, squash/main `df82086d0fac43f96dea17ff92a64466605e9402`. 원격 본문 provenance는 기존 `mols3131d:openai-chatgpt`를 보존하고 `mols3131d:github-copilot`을 추가했습니다.*
