---
description: PR #257에서 Rulesync 16.24.1을 40.2.0으로 이전하기 위한 upstream 근거, 변경 범위, 검증 계약과 실행 계획입니다.
---

# PR #257 — Rulesync v40.2.0 업그레이드 조사·계획

> **2026-10-25 후속 상태:** GitHub transport·공식 lock migration·wrapper 제거와 Windows 실제 설치를 완료했다. [후속 실행 결과](rulesync-v40-handoff.md#후속-실행-결과--2026-10-25-kst)에 payload 동등성·hash 변경 사유와 검증을 기록했다. 사용자의 명시적 push 지시로 최소 root frozen CI 변경의 게시·검증이 승인되었다. 아래 조사·실행 절차는 최초 계획이며, 현재 완료 상태는 체크리스트와 PR 본문을 따른다. Draft 해제·merge는 별도 승인 없이는 하지 않는다.

## 결정 및 작업 경계

**목표:** PR #257 안에서 repository toolchain의 Rulesync를 `16.24.1` → `40.2.0`으로 변경하고 실제 root 설치, library validation, generated route, CI 및 PC별 Git 인증을 확인하여 merge 가능한 상태로 만든다. 최신 버전을 동적으로 따라가지 않고 **검증한 정확한 버전으로 고정**한다.

- 시작 GitHub 상태: [PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257), head `c85be45b40c89cc55ca3b7e9ba5bdd9947eedefe`, base `7e595952aba994c46dd4c40cb95238c0eaf2b7f1`. 후속 작업 시 현재 SHA를 다시 조회한다.
- 변경 후보: `mise.toml`, `rulesync.jsonc`, `rulesync.lock`, `scripts/agent_assets/rulesync_install.py`, 해당 tests, `docs/references/tooling/{mise,rulesync}.md`, Rulesync 검증 orchestration 및 현 CI. **lock은 CLI가 소유**한다.
- 이번 대화에서의 작업 분리: GitHub API로 안전하게 편집 가능한 버전 pin·문서·PR 계획은 적용한다. 원격 npm·네이티브 Rulesync·Windows/macOS Git 자격 증명이 필요한 실행과 그 결과에 의존하는 lock 변경은 **로컬 에이전트 검증·후속 구현**으로 인계한다.
- [GitHub transport 복귀 요청](rulesync-github-transport.md)은 여전히 유효하다. `transport: git`를 유지해야 할 실증 근거가 없다면 **40.2.0 실제 설치를 통해 GitHub transport로 단순화**하고, `GIT_CONFIG_*` 보정 래퍼·그 테스트를 제거한다. config와 lock을 임의로 수동 정합화해 성공으로 간주하지 않는다.

## 조사 근거: 고정 버전과 공식 변경점

| 사실·관찰 | 영향 / 판정 |
| --- | --- |
| 2026-10-24 확인 공식 최신 태그 [v40.2.0](https://github.com/dyoshikawa/rulesync/releases/tag/v40.2.0), 발행 2026-10-22 | `mise.toml`의 `npm:rulesync`를 `40.2.0`으로 고정 |
| [v40.2.0 package.json](https://github.com/dyoshikawa/rulesync/blob/v40.2.0/package.json)은 Node `>=22.0.0` 요구 | repo의 Node `24.19.0` pin은 **정적 버전 조건상 충족**. 실제 설치 검증 아님 |
| [v40.2.0 CLI](https://github.com/dyoshikawa/rulesync/blob/v40.2.0/docs/reference/cli-commands.md)에서 `doctor --strict`, `generate --dry-run`, `generate --check`, `install --frozen`, `--json` 유지 | upstream 검증을 재사용. 자체 config schema의 모든 field/type 복제 금지 |
| [v34.0.0](https://github.com/dyoshikawa/rulesync/releases/tag/v34.0.0): lock source entry에 `skillsPath` 추가, legacy lock은 locked ref에서 한 번 재조회 | **현재 root `rulesync.lock`에는 `skillsPath`가 없다**. 40.2.0에서 source 선택·integrity·revision을 유지하며 공식 CLI로 마이그레이션 확인 필요 |
| [v37.0.0](https://github.com/dyoshikawa/rulesync/releases/tag/v37.0.0): frozen 설치가 설치된 curated Skill을 lock integrity와 대조·복원 | 로컬 curated 수정분 보존을 가정하지 말 것. 임시 checkout에서 먼저 테스트 |
| [v39.0.0](https://github.com/dyoshikawa/rulesync/releases/tag/v39.0.0): YAML/YML frontmatter만 허용 | 자산 및 외부 Skill의 frontmatter 파싱 검증 필요 |
| [v40.0.0](https://github.com/dyoshikawa/rulesync/releases/tag/v40.0.0): 외부 symlink 경계·frozen 무결성 실패·npm token 제한 강화 | 로컬 경로·인증·integrity 실패를 warning으로 무시하면 안 됨; 이 PR의 sources는 `git`이며 npm source가 아님 |
| [v40.2.0 Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/v40.2.0/docs/guide/declarative-sources.md) | GitHub transport, `install --frozen` 및 `install --outdated` 지원 확인. `--outdated`는 원격 최신성 검사이며 pinned lock 설치 검증의 대체가 아님 |

## 이미 확인한 저장소 상태

- `main`과 PR head의 `mise.toml`은 모두 Rulesync `16.24.1`이고, PR head는 Python wrapper로 frozen install을 실행한다.
- root `rulesync.jsonc`는 2개 Git source에서 총 **11개** Skill을 선언하고 `transport: git`을 사용한다. `rulesync.lock`은 `lockfileVersion: 1`, 각 source의 `requestedRef`, `resolvedRef`, 개별 integrity를 가진다. 검증 없이는 값을 수동 갱신하거나 `install --update`로 최신 ref를 당기지 않는다.
- `src/rulesync/rulesync.jsonc`는 별개 reusable library의 authoring/projection 설정이다. CI의 `npm run rulesync:validate`는 여기서 `doctor --strict` + `generate --dry-run`을 실행하면서 warning을 실패로 승격한다.
- 기존 PR Gate는 library의 Rulesync 검사와 repository route/projection 검사를 하지만 **root frozen 설치 자체는 실행하지 않는다**. 이전 PR Gate 성공을 40.x 업그레이드의 성공으로 재사용할 수 없다.

## 단계별 구현·검증

### A. 원격에서 안전하게 가능한 작업

1. 현 PR 브랜치에서 `mise.toml`의 Rulesync pin을 `40.2.0`으로 정확히 바꾼다. Node 조건을 충족하는지 정적 확인한다.
1. 기존 v16 조사 문서에 **이전 버전 기준 기록** 표시 및 본 계획 연결. 새 vendor 기능을 무작정 옛 보고서에 덮어쓰지 않는다.
1. PR 설명에 업그레이드를 범위로 넣고 **미실행/기존 버전에서만 실행한 검증**을 분리한다.
1. 이어지는 작업의 증거·결정·검증 상태를 같은 `inbox/github-257/` 아래 유지한다.

### B. 로컬 에이전트: 실제 CLI를 통한 마이그레이션

1. PR head를 최신으로 받아 독립 checkout/worktree에서 `mise install node "npm:rulesync"`, `rulesync --version` → **40.2.0** 확인. `mise run check`도 수행.
1. 변경 전 lock·source config snapshot을 보존하고, **루트**에서 `rulesync doctor --strict`. `src/rulesync`에서도 `rulesync doctor --strict`, `rulesync generate --dry-run`, `npm run rulesync:validate` 실행. warning/exit code를 기록.
1. **기존 `git` transport + frozen lock**으로 `mise run rulesync-install` 또는 `rulesync install --frozen`을 실행하여 40.x와 legacy lock의 호환 여부를 먼저 재현한다. source 재다운로드·수정 여부, 잠긴 11개 Skill과 lock 불변 여부를 검사한다.
1. [transport 변경 요구](rulesync-github-transport.md)에 따라 root source를 `github` transport로 통일한다. **Rulesync CLI 소유 lock을 공식 설치/lock 생성 경로로 갱신**하되 lock `resolvedRef`·`requestedRef`·Skill selection과 integrity를 가능한 한 보존한다. `install --update`는 잠긴 revision을 갱신할 수 있으므로 무분별하게 사용하지 않는다. 사용이 불가피하면 변경 범위와 각 integrity 증거를 먼저 검토한다.
1. 변경 후 `rulesync install --frozen`, lock 불변, 11개 선택 Skill 존재, route/index generator의 config↔lock 대응 및 `mise run generated-validate`를 확인한다.
1. Git transport만을 위한 `rulesync_install.py`와 해당 unit tests가 더는 필요 없으면 `mise run rulesync-install`을 native `rulesync install --frozen`으로 되돌리고 wrapper·테스트 및 관련 문서를 함께 제거한다. `tests/conftest.py` Git hook 격리는 무관한 실제 재현 여부로 별도 판단한다.
1. 최소 CI 보강: PR merge candidate의 **루트 `doctor --strict`**와 루트 source/lock 변경 시 **frozen install**·lock 불변을 검토하되, 새 CI 프레임워크/상시 OS matrix를 추가하지 않는다. 설치 검사는 ephemeral runner에서 네트워크/인증 오류를 분명히 구분한다.
1. `mise run test`, `mise run generated-validate`, `npm run rulesync:validate`, `mise run check`, `mise run setup` 또는 이에 준하는 smoke 및 PR Gate를 **새 HEAD**에서 확인한다. Windows는 PR 원래 LF·Git auth 변경의 영향이 있으므로 최소 한 번 실행한다. Linux/macOS는 영향받는 환경에서 선택 검증한다.

### C. 완료 기준

- [x] Rulesync v40.2.0 설치 및 `rulesync --version` 실제 확인
- [x] 루트·라이브러리의 공식 doctor, library generate/JSON warning fail-closed 통과
- [x] root source + lock이 공식 도구로 일치하며 `install --frozen` 성공·lock 불변·11개 Skill 일치
- [x] GitHub transport 전환과 Git 전용 우회 제거; hash 8개 변경은 동일 98개 파일의 경로 표기 차이로 입증
- [x] repository-owned route/index drift, targeted pytest 64개 및 전체 pytest 237개 통과
- [x] Windows Git auth/LF 대표 smoke 및 임시 HOME의 전체 setup 통과
- [x] 구현 head `d9797a740d5e430788c7df8c72b7ef470c2c4e48`의 PR Gate 및 Branch Check 통과 — [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/40107200255), [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/40107197801)
- [x] Root frozen-install admission — 사용자 push 승인 후 구현 head `0146bab35b24ae52bda517128c9ea88d6a56029a`의 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/40110662690)에서 11개 Skill 실제 설치와 `rulesync.lock: OK` 확인. High thread 해결·셀프 리뷰 완료. Step-only 기본 토큰과 `contents: read` 유지, 10개 로컬 scenario는 failure-path 근거. 최종 exact head의 실행·revision은 PR 본문에서 확인
- [x] 이 보고서 및 [인계 보고서](rulesync-v40-handoff.md)와 PR validation evidence 갱신. 최종 exact revision과 최신 CI 상태는 PR 본문이 소유

## 판정 경계 및 주의

- **정적 공식 문서 대조: 완료.** 네이티브 CLI 설치·실행·Windows 검증·v40 lock 업그레이드는 이 단계에서 수행되지 않았다.
- `rulesync.lock`을 수작업으로 새로운 vendor schema처럼 재구현하거나, `install --update`로 의도하지 않은 upstream revision 변경을 섞지 않는다.
- 원래 PR의 transport/auth 변경과 새 major 업그레이드를 합친 상태이므로 이전 CI 통과는 현재 변경의 통과가 아니다. **실제 설치 검증 전 merge 금지/인계**.
- `rulesync install --frozen`은 단순 정적 검사나 무조건 무변경 작업이 아니다. 임시 curated output을 생성·복원하며 네트워크와 로컬 credential에 의존할 수 있다.
- 변경이 실제로 요구하지 않는 full field/type snapshot, wrapper 상세 포맷별 unit test, 모든 OS×vendor 조합 상시 CI는 피한다.

## 근거

- [Rulesync v40.2.0 release](https://github.com/dyoshikawa/rulesync/releases/tag/v40.2.0), [공식 CLI](https://github.com/dyoshikawa/rulesync/blob/v40.2.0/docs/reference/cli-commands.md), [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/v40.2.0/docs/guide/declarative-sources.md)
- [기존 Rulesync v16 자체 검증 기능 조사](rulesync-native-validation-report.md), [CI 검토](rulesync-ci-test-review.md), [검증 최적화 제안](rulesync-verification-proposal.md)
- [Testing](../../docs/development/testing.md), [Validation](../../docs/development/validation.md), [CI](../../docs/development/ci.md)
