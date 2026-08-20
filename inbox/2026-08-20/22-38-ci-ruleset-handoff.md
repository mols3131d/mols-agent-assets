---
title: CI / Ruleset 개선 인계
description: mise tooling 도입 이후 PR admission gate와 GitHub Free public repository ruleset을 정리하기 위한 implementation handoff
tags:
  - ci
  - github-actions
  - ruleset
  - handoff
---

# CI / Ruleset 개선 인계

## Context

Repository: `mols3131d/mols-agent-assets`

이 문서는 CI와 repository protection 개선만 인계한다. 현재 tooling migration 구현은 Draft PR #80 `chore(tooling): adopt mise and Biome`에서 진행 중이며, 이 handoff branch는 해당 구현과 분리해 최신 `main`에서 생성한다.

현재 확인된 repository 설정:

- public repository
- default branch: `main`
- squash merge only
- merge commit / rebase merge disabled
- auto-merge disabled
- update branch suggestion disabled
- classic branch protection은 현재 비활성

관련 current workflow:

- `.github/workflows/targeted-tests.yml`
- `.github/workflows/rulesync.yml`
- `.github/workflows/distribution-routes.yml`
- `.github/workflows/rumdl-main-autofix.yml`

PR #80에서 이미 검증된 방향:

- mise를 repository tool version authority로 사용
- Python version/dependencies/environment는 uv가 소유
- PR Python test는 `uv --locked` semantics 사용
- tooling 변경은 `mise run check`로 실제 config/toolchain 검증
- `mise.toml`, `.python-version`, `pyproject.toml`, `uv.lock` 변경은 root `tests/` 전체로 fan-out
- Rulesync는 `@latest` 대신 mise exact pin 사용
- Targeted PR Tests는 stale run cancellation 사용

PR #80 실제 pull_request run에서는 `Targeted PR Tests`, `Rulesync`가 모두 성공했고 root test는 212 passed였다.

## Admission Goal

`main`에 들어가면 안 되는 변경은 PR 전에 blocking evidence로 차단한다.

최소 admission contract:

1. PR 없이 `main` 변경 불가
2. merge-critical deterministic CI 실패 시 merge 불가
3. unresolved review conversation이 있으면 merge 불가
4. force push / branch deletion 차단
5. squash-only + linear history 유지
6. CI가 path filtering 때문에 required check 자체를 생성하지 않는 상태를 만들지 않음

Approval 1개 강제는 단독 maintainer repository에서 불필요한 자기승인 ceremony가 되므로 기본안에서는 요구하지 않는다.

## Main CI Finding

현재처럼 workflow-level `paths:` filter를 사용하는 workflow를 그대로 required status check로 등록하면, 어떤 PR에서는 workflow가 아예 생성되지 않아 required check가 pending으로 남을 수 있다.

따라서 required check는 **항상 모든 `main` 대상 PR에서 생성되는 하나의 stable PR gate**로 만드는 것이 안전하다.

권장 logical architecture:

```text
Pull Request
    |
    v
PR Gate  [required]
    |
    +-- Impact routing
    |     +-- no relevant check -> success
    |     +-- isolated change -> targeted deterministic checks
    |     +-- shared/runtime/tooling change -> broadened checks
    |
    +-- lock/tooling validation when applicable
    |
    +-- merge-critical Rulesync evidence when applicable

Supplemental workflows
    +-- maintenance/write-back
    +-- broader/non-blocking eval
```

## CI Architecture

### PR Gate

Purpose: `main` admission을 대표하는 유일한 required check.

Trigger:

```yaml
on:
  pull_request:
    branches:
      - main
```

Workflow-level `paths:`는 두지 않는다. 모든 PR에서 job/check 자체는 생성하고 내부 impact router가 필요한 evidence만 선택한다.

권장 stable job/check name:

```text
PR Gate
```

다른 workflow/job과 이름을 중복시키지 않는다.

Blocking evidence 후보:

- affected deterministic tests
- `uv lock --check` / `uv --locked` test execution
- tooling 변경 시 `mise run check`
- merge-critical Rulesync canonical validation
- impact routing 자체의 deterministic contract tests

Fail-safe:

- 영향 범위를 확신할 수 없으면 validation을 넓힌다.
- selector가 모르는 merge-critical 파일을 조용히 skip하지 않는다.

### Rulesync

현재 별도 `Rulesync` PR workflow는 유지할 수 있다.

다만 최종 ruleset에서 required check를 여러 개로 늘리기보다 다음 둘 중 하나를 선택한다.

1. Rulesync evidence를 `PR Gate` 내부에 흡수하고 `PR Gate`만 required로 둔다. **권장.**
2. `Rulesync` workflow도 모든 PR에서 check를 생성하도록 바꾼 뒤 별도 required로 둔다.

Rulesync-only path filter를 유지하면서 required로 등록하지 않는다.

### Maintenance workflows

`distribution-routes.yml`, `rumdl-main-autofix.yml`처럼 repository write가 필요한 automation은 admission gate와 분리한다.

Ruleset에서 PR-required를 bypass 없이 강제하려면 **main에 직접 commit하는 post-merge write-back 패턴은 제거 또는 재설계**해야 한다.

권장 방향:

- formatting / generated consistency를 PR에서 검증하거나 PR branch에서 수정
- `main`에는 merge 결과만 들어오게 함
- GitHub Actions 전체에 broad bypass를 부여하지 않음

## Impact Routing

대표 변경 → evidence:

| Change | Blocking evidence |
| --- | --- |
| Skill asset | 해당 Skill tests + source isolation + relevant generated/route contract |
| `evals/skills/**` | eval fixture deterministic validation + 해당 Skill tests |
| normal docs | documentation consistency only |
| `mise.toml` | `mise run check` + root `tests/` |
| `.python-version` | lock/toolchain check + root `tests/` |
| `pyproject.toml` / `uv.lock` | `uv --locked` + root `tests/` |
| `biome.json` / `lefthook.yml` | `mise run check` + tooling tests |
| CI router/workflow | router/tooling regression tests + conservative fan-out |
| Rulesync config/runner | Rulesync deterministic verification + source isolation |

현재 test suite 규모가 작고 빠르므로 runtime/dependency authority가 바뀌는 경우에는 지나친 targeting보다 root `tests/` 전체 실행이 더 안전하다.

## Recommended GitHub Ruleset

Ruleset name:

```text
protect-main
```

Target:

```text
~DEFAULT_BRANCH
```

Enforcement: `Active`

권장 rules:

| Rule | Setting |
| --- | --- |
| Restrict deletions | ON |
| Require linear history | ON |
| Require pull request | ON |
| Required approvals | 0 |
| Require conversation resolution | ON |
| Require status checks | ON |
| Required check | `PR Gate` |
| Require branch up-to-date | OFF initially |
| Block force pushes | ON |
| Require signed commits | OFF |
| Restrict updates | OFF |
| Required deployments | OFF |
| Code scanning gate | OFF initially |

Bypass는 기본적으로 두지 않는다.

`Require branches to be up to date`는 초기에는 OFF를 권장한다. 현재 CI가 빠르더라도 main 이동 때마다 불필요한 branch update/re-run ceremony를 만들 수 있다. 실제 stale-base 문제가 반복되면 그때 강화한다.

## Repository Settings

권장 pull request / merge 설정:

| Setting | Value |
| --- | --- |
| Allow squash merging | ON |
| Allow merge commits | OFF |
| Allow rebase merging | OFF |
| Allow auto-merge | ON |
| Always suggest updating PR branches | ON |
| Automatically delete head branches | ON |

Auto-merge는 repository-wide 자동 merge가 아니라 PR별 opt-in 기능이므로 활성화해도 admission policy를 약화하지 않는다.

## Actions / Security

권장 기본값:

- default `GITHUB_TOKEN`: read-only
- workflow가 write가 필요할 때만 explicit `permissions:` 부여
- Actions가 PR approval을 대신하도록 허용하지 않음
- secret scanning ON
- push protection ON
- Dependabot alerts ON
- Dependabot security updates ON

CI admission workflow에는 repository write permission을 주지 않는다.

## Implementation Plan

### Phase 1 — PR Gate 안정화

1. PR #80 merge 여부와 최신 `main` 상태 재확인
2. `targeted-tests.yml`을 항상 모든 `main` PR에서 생성되는 stable `PR Gate`로 개편
3. workflow-level path filter 제거
4. 내부 impact router는 유지하되 unknown/global change는 fail-safe fan-out
5. required check로 사용할 job name을 고정
6. Rulesync merge-critical evidence를 PR Gate에 흡수할지 결정
7. CI regression tests 추가/갱신

### Phase 2 — write-back 제거

1. `distribution-routes.yml`과 `rumdl-main-autofix.yml`의 main write responsibility 조사
2. PR-required ruleset과 충돌하는 main direct write 제거
3. 가능하면 PR-time validation/fix 또는 explicit maintenance PR로 이동
4. broad bypass 없이 동작하는지 확인

### Phase 3 — ruleset 활성화

1. `protect-main` ruleset 생성
2. `PR Gate` required
3. PR required / conversation resolution / linear history / deletion+force-push block 활성화
4. approvals 0 유지
5. merge path 실제 검증

### Phase 4 — repository convenience

1. auto-merge ON
2. suggest update branch ON
3. auto-delete head branches ON
4. security defaults 확인

## Acceptance Criteria

- 모든 `main` 대상 PR에 `PR Gate` check가 생성된다.
- 관련 변경이 없더라도 required check가 pending으로 남지 않고 정상 success할 수 있다.
- merge-critical failure가 impact routing 때문에 silent skip되지 않는다.
- `pyproject.toml` / `uv.lock` drift는 merge 전에 차단된다.
- tooling config/version drift는 실제 mise toolchain validation으로 차단된다.
- Rulesync merge-critical regression은 deterministic evidence로 차단된다.
- CI admission workflow는 write permission을 요구하지 않는다.
- ruleset 활성화 후 direct push, force push, main deletion이 차단된다.
- unresolved review conversation이 있는 PR은 merge할 수 없다.
- solo maintainer가 자기 approval을 만들기 위한 불필요한 ceremony는 없다.
- maintenance automation 때문에 broad ruleset bypass를 부여하지 않는다.

## Risks / Open Decisions

### Required check topology

`PR Gate` 하나만 required로 둘지, `Rulesync`까지 별도 required로 둘지는 구현 시 최종 결정한다. 기본 추천은 **PR Gate 하나**다.

### Main write-back

현재 maintenance workflows가 ruleset과 가장 크게 충돌할 가능성이 있다. ruleset을 먼저 강제하기보다 이 write path부터 정리한다.

### Repository ruleset capability

GitHub Free public repository를 기준으로 설계한다. 실제 Settings UI에서 제공되는 ruleset/security option은 적용 직전에 다시 확인한다.

## Evidence Boundary

이 handoff는 CI/ruleset의 다음 구현 방향을 정의한다.

다음은 아직 완료됐다고 주장하지 않는다.

- `PR Gate` 통합 구현
- main write-back 제거
- GitHub Ruleset 실제 생성/활성화
- repository security setting 실제 변경

PR #80의 CI 성공은 mise/toolchain migration branch의 evidence이며, future ruleset enforcement의 evidence는 아니다.
