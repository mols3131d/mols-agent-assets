# CI redesign

이 설계는 [`research.md`](research.md)의 조사 결과를 입력으로 한다. 목표는 CI를 하나의 PR workflow가 아니라 **local → remote branch → pull request → deferred evidence**로 이어지는 integration system으로 만드는 것이다.

## Design summary

```text
Authoring
├─ local Git
├─ gh
├─ GitHub API / MCP / Plugin
├─ web UI
└─ coding agent / automation
        │
        ├─ Local Feedback            optional acceleration
        │
        └─ remote branch update
                ↓
          Branch Check               early server-side feedback
                ↓
          Pull Request
                ↓
          PR Gate                    authoritative merge-candidate admission
                ↓
          strict main integration
                ↓
          Deferred Evidence          only when it does not change admission
```

핵심 결정은 다음과 같다.

1. `PR Gate`는 유지하되 CI 전체와 동일시하지 않는다.
2. 모든 non-`main` branch push에 non-required `Branch Check`를 추가한다.
3. `Branch Check`는 hookless remote write를 빠르게 잡는 값싼 검증만 실행한다.
4. `PR Gate`는 `main`과 결합된 merge candidate에서 merge-critical evidence를 다시 전부 확보한다.
5. Projection freshness를 generic pytest assertion에서 이름 있는 projection check로 분리한다.
6. Local hook은 유지하지만 CI correctness의 prerequisite로 사용하지 않는다.
7. `main` required check를 strict mode로 바꿔 최신 base와 검증되지 않은 상태의 merge를 허용하지 않는다.
8. Pure formatting preference는 기본적으로 merge-blocking evidence로 승격하지 않는다.
9. Rulesync structural validation을 blocking으로 승격하려면 먼저 CI에서 사용할 Rulesync version을 고정한다.
10. 현재 규모에서는 matrix, test router, merge queue, CI write-back을 도입하지 않는다.

## Goals

### Admission goal

`main`에는 다음 상태만 들어간다.

- source/structural contract가 유효하다.
- repository-owned deterministic behavior가 통과한다.
- 영향받는 committed projection이 canonical source와 일치한다.
- Rulesync-managed surface가 repository가 지원하는 projection contract를 만족한다.
- 현재 `main`과 결합된 상태가 required check를 통과한다.

### Feedback goal

API/MCP/Plugin처럼 local hook을 우회하는 변경도 PR을 열기 전에 branch 수준에서 대표적인 오류를 빠르게 발견할 수 있어야 한다.

### Operational goal

같은 contract를 local hook, branch workflow, PR workflow가 각각 다시 구현하지 않는다. Existing generator, validator와 tests를 재사용하고 CI는 execution placement만 소유한다.

## Non-goals

이번 설계에서는 다음을 도입하지 않는다.

- CI의 generated artifact auto-commit/push
- merge queue
- provider/model matrix
- PR별 semantic/runtime model eval
- third-party path-filter action
- 복잡한 dependency/impact router
- pure style만을 이유로 한 required merge gate

필요성이 관찰되면 별도 evidence로 다시 검토한다.

## Integration surfaces

### 1. Local Feedback

Local feedback은 가장 빠른 개발 보조 수단이다. 강제 경계가 아니다.

현재 구조를 유지한다.

```text
edit
→ optional `mise run format-changed`
→ pre-commit generated projection sync
→ commit message validation
→ pre-push deterministic tests
```

`pre-push` 전체 test는 현재 약 1초 수준이므로 branch CI가 생겨도 당장 제거할 근거가 없다. 반복 비용이 실제 문제가 되면 그때 축소한다.

API/MCP/Plugin path가 이 surface를 건너뛰는 것은 정상이며 server-side validation이 이를 보완한다.

### 2. Branch Check

새 workflow를 추가한다.

Suggested workflow name/file:

```text
Branch Check
.github/workflows/branch-check.yml
```

Trigger:

```yaml
on:
  push:
    branches-ignore:
      - main
```

Role:

- remote branch에 지속된 commit의 early feedback
- API/MCP/Plugin/web/coding-agent direct write에서 local hook omission 발견
- merge admission 자체는 아님

Properties:

- `permissions: contents: read`
- secret 없음
- branch ref 자체 checkout
- `concurrency`를 branch ref 기준으로 두고 superseded run 취소
- workflow-level path filter 없음
- failure가 `main` merge 자체를 직접 차단하지 않음

#### Branch Check pipeline

```text
Checkout pushed commit
↓
Set up Python/test dependencies
↓
Source validation
↓
Full deterministic tests
↓
Local projection check
↓
Branch feedback
```

현재 deterministic suite가 매우 작으므로 branch용 test subset을 새로 만들지 않고 전체 `tests/`를 실행한다.

Source validation에는 최소한 docs frontmatter처럼 network나 external tool 없이 바로 판정할 수 있는 repository contract를 둔다.

Local projection check는 **network-free projection만** 대상으로 한다.

```text
docs indexes
+ distribution routes
```

이 두 projection은 API/Plugin commit에서 가장 흔한 stale-generated-state를 빠르게 발견하면서 external dependency availability에 branch feedback을 묶지 않는다.

`.agents/route`의 repository route는 external raw GitHub fetch가 필요하므로 Branch Check 기본 범위에서는 제외한다. PR Gate에서 authoritative하게 확인한다.

### 3. PR Gate

현재 required check 이름 `PR Gate`를 유지한다. Ruleset migration과 check-name drift를 불필요하게 만들지 않는다.

Suggested filename:

```text
.github/workflows/pr-gate.yml
```

현재 `targeted-tests.yml`은 실제로 targeted test가 아니므로 rename한다.

Trigger:

```yaml
on:
  pull_request:
    branches:
      - main
```

Workflow-level `paths`/`paths-ignore`는 두지 않는다. Required workflow가 skip되어 Pending 상태로 남는 경우를 피한다.

Properties:

- `permissions: contents: read`
- secret 없음
- default `pull_request` merge ref checkout
- PR number 기준 concurrency + `cancel-in-progress: true`
- 하나의 required `PR Gate` job을 유지
- step을 failure class별로 나눠 diagnosis를 명확히 함
- repository write-back 없음

#### PR Gate pipeline

```text
Checkout PR merge candidate
↓
Source / representation contract validation
↓
Deterministic behavior tests
↓
Affected projection generation + freshness validation
↓
Rulesync structural validation
↓
PR Gate success
```

각 단계의 의미는 다음과 같다.

#### Source / representation contract validation

Projection 전에 판정 가능한 merge-critical source contract만 둔다.

초기 대상:

- documentation frontmatter
- syntax/config parse처럼 기존 validator가 소유하는 contract

Pure formatting preference를 이 단계에 넣지 않는다. 정확한 representation 자체가 parseability나 explicit contract인 경우만 blocking으로 둔다.

#### Deterministic behavior tests

```text
pytest -q tests
```

현재 suite가 작으므로 full suite를 유지한다.

다만 다음 종류의 test는 projection gate로 책임을 이전한다.

```text
committed generated output == generator output
```

Generator의 parsing, ordering, failure semantics와 render logic unit test는 그대로 tests에 남긴다.

#### Projection generation + freshness validation

새로운 repository-native read-only validation entrypoint를 둔다.

Suggested semantic interface:

```text
validate generated projections
  -- local-only
  -- all
  -- affected paths when supplied
```

정확한 script 이름은 구현 시 결정하되 다음 contract를 가진다.

- 기존 generator 함수를 호출해 projection을 계산한다.
- projection semantics를 별도로 재구현하지 않는다.
- committed output과 비교한다.
- stale path를 짧게 출력한다.
- 실패 시 recovery entrypoint `mise run generated-sync`를 안내한다.
- repository를 commit/push하지 않는다.

PR Gate에서는 모든 **영향받는** projection을 확인한다.

```text
docs indexes
+ distribution routes
+ repository routes
```

Repository route가 외부 GitHub fetch를 필요로 하므로 불필요한 PR에서 항상 network call을 하지 않는 것을 선호한다.

영향 판정은 workflow YAML에 path table을 복제하지 않고 `scripts/generated_artifacts_sync.py`가 이미 가진 projection source/output ownership을 재사용한다. PR base/head의 changed paths를 validation entrypoint에 넘기면 해당 registry가 projection을 선택한다.

불확실하거나 changed-path 정보를 정상적으로 계산할 수 없으면 fail-safe하게 **all projections**를 검증한다.

이 정도의 routing은 이미 존재하는 projection ownership을 재사용하므로 별도 generic CI router를 만드는 것보다 작다.

#### Rulesync structural validation

Rulesync-managed Agent Asset source가 invalid한 상태는 이 repository의 핵심 deliverable을 깨뜨리므로 장기적으로 blocking evidence가 되어야 한다.

그러나 현재 `mise.toml`의 `npm:rulesync = "latest"`를 그대로 required CI에 넣으면 upstream release가 repository commit과 무관하게 PR admission을 바꿀 수 있다.

따라서 순서는 다음으로 고정한다.

```text
1. CI-compatible Rulesync version pin
2. existing `npm run rulesync:validate` 재사용
3. PR Gate blocking step으로 승격
```

Validator는 이미 `doctor --strict`, configured projection dry-run, declared-target projection dry-run을 read-only로 실행한다. 새로운 Rulesync semantics를 CI에 만들 필요가 없다.

초기 구현에서 version pin을 함께 완료하지 못하면 Rulesync validation은 기존 `Optional Validation`에 남기고 `PR Gate` 승격을 완료된 것으로 간주하지 않는다.

### 4. Main admission freshness

현재 `protect-main` Ruleset의 required status check는 loose mode다 (`strict_required_status_checks_policy=false`). GitHub 공식 문서상 loose mode는 topic branch가 최신 base와 동기화되지 않아도 merge할 수 있고, incompatible change가 merge 후 실패할 수 있다.

이 repository는 병렬 agent/PR 작업이 흔하므로 이 trade-off가 맞지 않는다.

설계 결정:

```text
strict_required_status_checks_policy = true
```

즉 PR은 최신 `main`을 기준으로 required evidence가 유효한 상태에서만 merge한다.

현재 규모에서는 merge queue를 추가하지 않는다. Strict mode의 branch-update 비용이 실제 병목이 될 정도로 PR concurrency가 증가하면 그때 merge queue를 검토한다.

Ruleset 변경은 workflow 변경과 마찬가지로 control-surface change이므로 구현 시 explicit human approval을 별도로 확보한다.

### 5. Deferred Evidence

다음은 기본적으로 required PR Gate 밖에 둔다.

- Promptfoo/model runtime eval
- broad provider/model matrix
- repeated stochastic sampling
- exhaustive diagnostics
- pure formatting normalization
- repository write maintenance

단, 어떤 check의 실패를 미리 알았다면 해당 PR을 merge하지 않았을 것이라면 deferred로 유지할 수 없다. 최소 representative scope를 찾아 blocking evidence로 승격한다.

## Formatting boundary

Formatting은 두 종류를 구분한다.

```text
explicit representation contract
→ validation / blocking 가능

pure style normalization
→ local formatting / maintenance
```

현재 `mise run format`과 `format-changed`는 write-oriented다. CI가 이를 실행해 working tree를 고쳐서 PASS시키지 않는다.

현재 단계에서는 pure formatting을 required PR check로 추가하지 않는다. 향후 exact format 자체를 repository contract로 정한다면 `ruff format --check`, `rumdl check`, Biome read-only check를 조합한 별도 canonical read-only entrypoint를 먼저 만든 뒤 CI가 재사용한다.

## Workflow architecture

최종적으로 유지할 workflow surface는 다음 세 개를 목표로 한다.

| Workflow | Trigger | Blocking | Responsibility |
| --- | --- | --- | --- |
| `Branch Check` | non-main `push` | No | hookless remote write early feedback |
| `PR Gate` | PR → `main` | Yes | latest-base merge candidate admission |
| `Optional/Deferred Validation` | manual | No | expensive/stochastic/diagnostic evidence only |

현재 Optional Validation의 `docs_frontmatter`, `docs_indexes`, `asset_routes`는 PR Gate로 승격한 뒤 제거한다. 같은 contract의 수동 복제본을 유지하지 않는다.

Rulesync input은 blocking promotion이 끝날 때까지만 Optional Validation에 남긴다.

## Failure ownership

| Failure | Branch Check | PR Gate | Deferred |
| --- | --- | --- | --- |
| malformed docs frontmatter | fail early | block | — |
| deterministic script regression | fail early | block | — |
| stale docs index | fail early | block | — |
| stale distribution route | fail early | block | — |
| stale repository route | optional/no network | block when affected | — |
| Rulesync structural incompatibility | omit initially | block after version pin | manual until promoted |
| pure formatting drift | local feedback | non-blocking by default | maintenance |
| semantic/model regression | — | only if explicitly merge-critical | default |

## Duplicate execution policy

Open PR branch에 push하면 `Branch Check`와 `PR Gate`가 모두 실행될 수 있다. 이를 첫 구현에서 제거하지 않는다.

이유:

- branch check는 head commit feedback이다.
- PR Gate는 base와 결합된 merge candidate evidence다.
- tests는 현재 매우 빠르다.
- 중복 제거를 위한 PR lookup, API permission, cross-workflow coordination이 더 복잡하다.

실제 Actions 사용량이나 latency가 문제가 되었을 때만 deduplication을 설계한다.

## Security and permissions

Branch Check와 PR Gate 모두 기본값:

```yaml
permissions:
  contents: read
```

- secret 없음
- `persist-credentials: false`
- generated artifact write-back 없음
- `pull_request_target` 사용 안 함
- untrusted event field를 shell command로 직접 interpolation하지 않음

Workflow 자체를 수정하는 PR은 수정된 workflow가 자기 자신을 검증할 수 있다는 한계가 있다. 따라서 repository GitHub policy대로 workflow/control-surface 변경에는 수정된 workflow success와 별개의 inspection/review evidence와 explicit human approval을 요구한다.

## Implementation plan

### Phase 1 — Projection validation boundary

1. committed projection freshness를 검사하는 first-party read-only entrypoint를 만든다.
2. existing projection ownership registry를 재사용한다.
3. concise stale-path + recovery message를 제공한다.
4. pytest에서 committed-output byte equality만 소유하는 test를 projection validation으로 이동한다.
5. generator behavior tests는 유지한다.

### Phase 2 — Branch Check

1. `branch-check.yml`을 추가한다.
2. non-main push를 trigger로 한다.
3. source validation → full deterministic tests → local projection validation 순으로 실행한다.
4. read-only/secretless/concurrency contract를 검증한다.

이 단계부터 API/MCP/Plugin direct branch commit이 PR 이전에 server-side feedback을 받는다.

### Phase 3 — PR Gate restructure

1. `targeted-tests.yml`을 `pr-gate.yml`로 rename한다.
2. required job/check name `PR Gate`는 유지한다.
3. source validation, deterministic tests, projection validation을 named step으로 분리한다.
4. affected projection check를 사용하되 uncertainty는 all-projection fallback으로 처리한다.
5. workflow-level path filters는 추가하지 않는다.

### Phase 4 — Rulesync promotion

1. CI에 사용할 Rulesync version을 고정한다.
2. existing `rulesync:validate`를 PR Gate에 blocking으로 추가한다.
3. 안정적으로 통과함을 확인한 뒤 Optional Validation의 중복 Rulesync surface를 정리한다.

### Phase 5 — Strict main admission

1. 새 PR Gate가 안정적으로 required check를 제공하는지 확인한다.
2. `protect-main`의 strict required-status policy를 활성화한다.
3. 최신 `main`과 결합되지 않은 PR은 merge할 수 없음을 확인한다.

### Phase 6 — Optional Validation cleanup

PR Gate로 승격된 deterministic/structural checks를 manual workflow에서 제거한다. Optional workflow는 실제 deferred evidence만 소유하게 한다.

## Acceptance criteria

구현 완료 판단은 다음으로 한다.

- GitHub API/MCP/Plugin으로 feature branch에 직접 commit하면 PR이 없어도 `Branch Check`가 실행된다.
- Branch Check 실패가 main Ruleset의 required admission check로 오인되지 않는다.
- PR을 열거나 head를 갱신하면 `PR Gate`가 merge ref를 검증한다.
- Required PR Gate는 path filtering 때문에 Pending 상태로 남지 않는다.
- stale `route/skills.jsonl` 같은 오류는 generic JSON assertion이 아니라 projection name/path와 `mise run generated-sync` 복구 경로를 보고한다.
- generator regression과 committed projection drift의 failure ownership이 분리된다.
- unchanged unrelated PR은 repository-route external fetch를 불필요하게 수행하지 않거나, 영향 판정 불확실 시 명시적으로 all-validation fallback한다.
- Rulesync가 blocking이 되기 전에 CI tool version이 고정된다.
- Branch Check와 PR Gate는 repository write permission과 secrets 없이 동작한다.
- CI가 generated output을 자동 commit/push하지 않는다.
- `PR Gate` success만으로 semantic/runtime behavior까지 검증했다고 주장하지 않는다.
- required status check는 최신 `main`을 기준으로 유효해야 merge할 수 있다.
- workflow/ruleset 변경은 CI self-success 외의 independent review evidence와 explicit human approval을 거친다.

## Expected steady state

```text
local authoring
  ├─ format/sync/test when available
  └─ no correctness dependency on hooks

remote branch write
  └─ Branch Check
       ├─ source validation
       ├─ deterministic tests
       └─ local projection freshness

pull request → main
  └─ PR Gate [required]
       ├─ source validation
       ├─ deterministic tests
       ├─ affected full projection freshness
       └─ pinned Rulesync structural validation

main Ruleset
  └─ PR + PR Gate + strict latest-base + squash

manual / deferred
  └─ semantic/runtime/exhaustive/maintenance evidence
```

이 구조는 `PR Gate`를 약화하지 않으면서도 CI를 PR 직전의 한 번짜리 검사에서 **여러 authoring path가 동일한 repository contract로 수렴하는 integration system**으로 확장한다.
