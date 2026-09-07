# CI redesign

이 설계는 [`research.md`](research.md)의 조사 결과를 입력으로 한다. CI를 하나의 PR workflow가 아니라 **local → remote branch → pull request → deferred evidence**로 이어지는 integration system으로 정의한다.

## Goal

변경을 만드는 도구가 local Git, `gh`, GitHub API, MCP, Plugin, web UI, coding agent 중 무엇이든 persisted repository state가 동일한 contract로 수렴하게 한다.

`main` admission은 required `PR Gate`가 소유하지만, hookless remote write의 오류를 PR 생성 전에도 발견할 수 있어야 한다.

## Architecture

```text
Authoring
├─ local Git
├─ gh
├─ GitHub API / MCP / Plugin
├─ web UI
└─ coding agent / automation
        │
        ├─ Local Feedback           optional acceleration
        │
        └─ remote branch update
                ↓
          Branch Check              early server-side feedback
                ↓
          Pull Request
                ↓
          PR Gate                   authoritative merge-candidate admission
                ↓
          main Ruleset
                ↓
          Deferred Evidence         only when admission does not depend on it
```

## Decisions

1. `PR Gate`는 유지하지만 CI 전체와 동일시하지 않는다.
2. 모든 non-`main` branch push에 `Branch Check`를 실행한다.
3. Local hook은 feedback/maintenance 수단이며 CI correctness prerequisite가 아니다.
4. Branch Check와 PR Gate는 같은 repository-native validator와 tests를 재사용한다.
5. Generator behavior와 committed projection freshness를 분리한다.
6. CI는 generated output을 commit·push하지 않는다.
7. Pure formatting preference는 기본적으로 merge-blocking evidence가 아니다.
8. Rulesync structural validation은 version을 고정한 뒤 PR Gate에서 blocking한다.
9. 현재 규모에서는 matrix, generic impact router, merge queue, CI write-back을 도입하지 않는다.
10. Optional Validation에 있던 deterministic/structural checks는 새 CI와 중복되므로 제거한다.

## 1. Local Feedback

Local path는 가능한 경우 빠른 feedback과 projection sync를 제공한다.

```text
edit
→ optional format
→ pre-commit generated projection sync
→ commit message validation
→ pre-push deterministic tests
```

API/MCP/Plugin 같은 write path가 이 단계를 건너뛰는 것은 정상이다. Server-side CI가 correctness를 보완해야 한다.

## 2. Branch Check

Workflow: `.github/workflows/branch-check.yml`

Trigger:

```yaml
on:
  push:
    branches-ignore:
      - main
```

Purpose:

- hookless remote write 조기 검출
- PR 생성 전 branch feedback
- main admission과 분리된 non-required check

Pipeline:

```text
Checkout pushed commit
→ source contract validation
→ full deterministic tests
→ network-free projection validation
```

Network-free projection은 다음 둘이다.

- documentation indexes
- distribution routes

Repository routes는 external GitHub fetch가 필요하므로 Branch Check 기본 범위에서 제외한다.

Properties:

- `permissions: contents: read`
- secrets 없음
- branch ref 자체 checkout
- branch ref 기준 concurrency
- superseded run 취소
- write-back 없음

## 3. PR Gate

Workflow: `.github/workflows/pr-gate.yml`

Required check 이름은 기존 Ruleset과 호환되도록 `PR Gate`를 유지한다.

Trigger:

```yaml
on:
  pull_request:
    branches:
      - main
```

PR Gate는 GitHub의 PR merge ref를 checkout해 현재 base와 head가 결합된 merge candidate를 검증한다.

Pipeline:

```text
Checkout PR merge candidate
→ source contract validation
→ full deterministic tests
→ affected generated projection validation
→ pinned Rulesync structural validation
→ PR Gate success
```

### Projection impact

Projection impact는 PR event payload의 base SHA가 아니라 **실제로 checkout한 merge commit의 first parent (`HEAD^1`)**를 기준으로 계산한다.

```text
HEAD^1 = merge candidate가 사용한 실제 base
HEAD   = merge candidate
```

이 기준으로 changed paths를 계산한 뒤 기존 projection ownership registry가 영향을 받은 projection을 선택한다.

영향 판정을 계산할 수 없으면 all-projection validation으로 fail-safe하게 넓힌다.

## 4. Projection validation

새 read-only entrypoint:

```text
python -m scripts.generated_artifacts_validate
```

지원 범위:

- docs indexes
- distribution routes
- repository routes

Contract:

- 기존 generator 함수를 재사용한다.
- projection semantics를 새로 구현하지 않는다.
- repository file을 수정하지 않는다.
- committed output과 expected output을 비교한다.
- missing/outdated/stale path를 직접 표시한다.
- drift 시 `mise run generated-sync` 복구 경로를 안내한다.
- impact가 불확실하면 검증 범위를 넓힌다.

Generator의 parsing, ordering, rendering, failure semantics는 pytest가 계속 소유한다. Committed projection freshness만 projection validation이 소유한다.

## 5. Rulesync structural validation

Rulesync는 `mise.toml`에서 `16.24.1`로 고정한다.

PR Gate는 repository-owned `npm run rulesync:validate`를 재사용한다.

현재 structural evidence는 두 check로 구성한다.

```text
doctor --strict
configured generate --dry-run
```

`src/rulesync/rulesync.jsonc`가 유지 target과 feature의 support ceiling을 선언하고, configured generation이 asset별 `targets`를 존중하므로 별도 wildcard target generation을 반복하지 않는다.

Rulesync validation의 성공은 structural compatibility만 의미하며 semantic quality, routing quality, runtime behavior까지 증명하지 않는다.

## 6. Formatting boundary

Formatting은 다음을 구분한다.

```text
explicit representation contract
→ blocking validation 가능

pure style normalization
→ local formatting / maintenance
```

현재 formatter entrypoint는 write-oriented이므로 pure formatting을 required PR check로 추가하지 않는다.

향후 exact formatting 자체를 repository contract로 만들 경우 먼저 canonical check-only entrypoint를 만든 뒤 CI가 재사용한다.

## 7. Deferred evidence

다음은 기본적으로 required PR Gate 밖에 둔다.

- Promptfoo/model runtime eval
- broad provider/model matrix
- repeated stochastic sampling
- exhaustive diagnostics
- pure formatting normalization
- repository state를 실제 수정하는 maintenance automation

어떤 check의 실패를 미리 알았다면 해당 변경을 merge하지 않았을 것이라면 deferred로 둘 수 없다. 그 경우 최소한의 representative blocking evidence로 승격한다.

별도의 `Optional Validation` workflow는 유지하지 않는다. 필요한 deferred evidence는 실제 독립 목적이 생겼을 때 별도 surface로 추가한다.

## 8. Security and permissions

Branch Check와 PR Gate의 기본 계약:

- `permissions: contents: read`
- secrets 없음
- `persist-credentials: false`
- `pull_request_target` 사용 안 함
- generated artifact write-back 없음
- base branch commit/push 없음

Workflow 변경은 수정된 workflow가 자기 자신을 검증하는 한계가 있으므로 CI success와 별도의 review evidence 및 사람의 명시적 approval이 필요하다.

## 9. Main admission freshness

현재 별도 enforcement 작업으로 남겨 둔 목표:

```text
strict_required_status_checks_policy = true
```

이 변경은 repository CI 파일이 아니라 GitHub Ruleset 자체를 수정하는 control-surface operation이다. 새 CI가 안정적으로 merge된 뒤 명시적 승인 하에 별도로 적용한다.

현재 PR의 완료 조건에 Ruleset mutation을 포함하지 않는다.

## Implemented state

현재 구현된 steady state:

```text
remote branch write
  └─ Branch Check
       ├─ source validation
       ├─ deterministic tests
       └─ network-free projection freshness

pull request → main
  └─ PR Gate [required]
       ├─ source validation
       ├─ deterministic tests
       ├─ merge-ref 기준 affected projection freshness
       └─ pinned Rulesync structural validation

local authoring
  └─ hooks / formatting / projection sync as optional acceleration

deferred
  └─ semantic/runtime/exhaustive evidence only when justified
```

## Acceptance criteria

- API/MCP/Plugin으로 feature branch에 직접 commit해도 `Branch Check`가 실행된다.
- Branch Check는 main Ruleset의 required admission check가 아니다.
- PR head가 바뀌면 `PR Gate`가 merge candidate를 검증한다.
- Required PR Gate는 workflow-level path filtering으로 skip되지 않는다.
- stale projection은 projection 이름/path와 `mise run generated-sync` 복구 경로를 보고한다.
- generator regression과 committed projection drift의 failure ownership이 분리된다.
- repository-route external fetch는 영향받은 PR에서만 실행하거나 impact 계산 실패 시 fail-safe하게 실행된다.
- Rulesync version이 고정되어 있다.
- Branch Check와 PR Gate는 read-only permission으로 동작한다.
- CI는 generated output을 commit/push하지 않는다.
- PR Gate success를 semantic/runtime behavior evidence로 확대 해석하지 않는다.
- strict latest-base enforcement는 CI merge 후 별도 Ruleset change로 수행한다.
