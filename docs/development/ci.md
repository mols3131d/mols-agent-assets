---
description: 저장소의 CI admission, PR Gate, blocking·deferred evidence, projection 검증과 local hook·agent/API write path의 경계를 설계·운영할 때 사용하는 정책입니다.
---

# Continuous Integration

CI는 **어떤 write path로 만들어진 변경이든 `main`에 들어가기 전에 repository state 자체를 검증하는 admission evidence system**입니다. 이 문서는 CI의 orchestration과 blocking boundary를 소유하고, formatter·validator·test·eval의 의미는 각 owner에 둡니다.

이 정책은 GPPC의 Goal, Principles, Patterns, Contracts로 CI의 본질과 실행 계약을 구분합니다.

## Authority

- CI admission, `PR Gate`, trigger, stage order, blocking·deferred evidence, projection gate와 local hook의 관계 → 이 문서
- GitHub permission, Ruleset, Pull Request와 Merge → [GitHub](github.md)
- 파일 표현의 정규화와 formatter write path → [Formatting](formatting.md)
- 구조·파생 계약의 의미 → [Validation](validation.md)
- repository-owned executable behavior의 deterministic test → [Testing](testing.md)
- model/runtime behavior evidence → [Evaluation](evaluation.md)
- canonical source와 derived output의 권한 → [작성 원본과 권한](source-authority.md)

Workflow filename, step 이름과 tool invocation 같은 구현 세부는 `.github/workflows/`와 실행 entrypoint가 소유합니다. 이 문서는 admission 의미와 책임 경계를 정의하고 구현을 불필요하게 복제하지 않습니다.

## Goal

`main`에는 **알고 있다면 merge를 거부했을 실패가 blocking pre-merge evidence로 검출되는 repository state만** 들어가야 합니다.

이 기준은 변경을 만든 방식과 무관합니다. Local Git, `gh` CLI, GitHub MCP, GitHub Plugin, 웹 UI, API나 다른 agent automation이 local hook을 거치지 않아도 같은 admission standard를 적용합니다.

## Principles

### Repository State over Authoring Path

CI는 개발자의 로컬 절차가 아니라 commit된 repository state를 검증합니다. `pre-commit`과 `pre-push`는 빠른 피드백과 자동 보조를 제공할 수 있지만 CI correctness의 전제나 신뢰 경계가 아닙니다.

### Strict Admission, Proportional Evidence

알려진 실패가 `main`의 상태를 받아들일 수 없게 만든다면 그 evidence는 merge 전에 blocking이어야 합니다. 반대로 merge 판단을 바꾸지 않는 진단, 광범위한 confidence check, 유지보수 작업은 PR Gate를 불필요하게 무겁게 만들지 않습니다.

검증 비용과 범위는 줄일 수 있지만 admission standard 자체를 낮추지는 않습니다.

### Cheapest Sufficient Evidence

필요한 claim을 증명할 수 있는 가장 저렴하고 결정적인 evidence를 우선합니다.

```text
static
→ deterministic
→ projection / harness
→ semantic
→ live runtime
```

낮은 tier의 성공을 더 높은 tier의 근거로 확대 해석하지 않습니다. Deterministic assertion으로 충분하면 model/runtime eval을 추가하지 않습니다.

### Read-only Admission

PR Gate는 repository를 수정하는 maintenance automation이 아닙니다. 검증을 위해 runner의 ephemeral working tree에서 formatter check, generator나 projection 작업을 실행할 수 있지만 commit, push나 base branch write-back은 하지 않습니다.

### Fail-safe and Diagnosable

영향 범위를 확실히 판단할 수 없으면 관련 검증을 넓히거나 실패시킵니다. 중요한 검증을 조용히 생략하지 않습니다.

CI 단계는 failure class가 드러나도록 나누고, 가능한 경우 실패 원인과 repository-native 복구 entrypoint를 함께 보여줍니다.

## Patterns

### PR Admission Gate

`main` admission의 server-side 정본은 required `PR Gate`입니다. Open Pull Request의 head가 바뀌면 merge candidate를 다시 검증해야 하며, PR이 없는 branch push는 `main` admission evidence로 간주하지 않습니다.

PR Gate는 가능한 경우 PR head만이 아니라 base와 결합된 merge candidate를 검증합니다. Local hook 성공이나 agent의 self-report는 이 gate를 대체하지 않습니다.

### Evidence Pipeline

Merge-critical evidence는 책임이 드러나는 순서로 실행합니다.

```text
change
→ representation / source validation
→ deterministic behavior tests
→ projection generation
→ projection drift / cross-surface validation
→ main admission
```

- **Representation / source validation**은 formatter contract, syntax, frontmatter, config처럼 projection을 만들기 전에 판정할 수 있는 상태를 빠르게 거릅니다.
- **Deterministic behavior tests**는 generator, sync, validator, adapter와 repository-owned script의 동작을 검증합니다.
- **Projection generation**은 canonical source에서 공식 generator를 runner working tree에 실행합니다.
- **Projection drift / cross-surface validation**은 생성 결과와 committed output의 정합성, source와 derived surface 사이의 계약을 확인합니다.

각 단계가 같은 claim을 중복해서 검증하지 않습니다. 특히 committed projection freshness는 generic pytest failure에 숨기기보다 projection stage에서 직접 드러내는 것을 우선합니다.

### Failure to Evidence

| Failure class | Cheapest sufficient evidence | Default boundary |
| --- | --- | --- |
| explicit representation contract 위반 | formatter/static check | blocking PR |
| malformed frontmatter·config·schema | static validator | blocking PR |
| generator·sync·validator 동작 regression | deterministic test | blocking PR |
| committed projection drift | official generation + diff/status | blocking PR |
| Rulesync-managed source의 structural incompatibility | repository-owned structural validation | 해당 변경이 `main`을 invalid하게 만들면 blocking |
| model routing·runtime behavior regression | semantic/runtime eval | 기본은 deferred, admission risk일 때만 blocking |
| explicit contract가 아닌 pure style preference | local formatting/maintenance | non-blocking |

### Projection Gate

Projection의 canonical source와 generator는 해당 domain owner가 정합니다. CI는 별도 projection semantics를 구현하지 않고 공식 generator를 재사용합니다.

```text
canonical source
→ official generator
→ ephemeral working tree
→ committed projection과 비교
```

차이가 생기면 stale projection으로 실패합니다. CI가 생성 결과를 자동 commit하거나 push해서 drift를 숨기지 않습니다. Repository-wide generated projection을 갱신하는 기본 local entrypoint는 `mise run generated-sync`입니다.

### Local Acceleration

Local hook은 같은 문제를 더 일찍 발견하거나 projection을 commit 전에 동기화하기 위한 보조 장치입니다.

```text
local commit / push
→ optional fast feedback

Pull Request
→ authoritative PR Gate
```

CI는 hook 설치 여부, shell 환경, local cache나 staged state에 의존하지 않습니다.

### Deferred Evidence

비용이 크거나 stochastic한 검증, 광범위한 provider/runtime matrix, exhaustive diagnostics와 maintenance write는 merge 판단에 필요하지 않다면 manual, scheduled 또는 별도 non-blocking surface로 둡니다.

어떤 deferred check의 실패를 알았다면 현재 변경을 merge하지 않았을 것이라면 그 check는 deferred에 둘 수 없습니다. 필요한 최소 scope로 줄여 blocking evidence로 승격합니다.

### Impact Routing

Repository 규모나 검증 비용이 실제로 커졌을 때만 change-impact routing을 도입합니다. Path filter, naming convention, 작은 router 순으로 단순한 방법을 우선하고, 영향 판정이 불확실하면 더 넓은 검증으로 fallback합니다.

Routing 자체가 merge-critical evidence를 누락시킬 수 있다면 router도 deterministic하게 검증합니다.

## Contracts

- `main`에 허용할 수 없는 알려진 실패는 required `PR Gate`에서 blocking pre-merge evidence를 가져야 합니다.
- PR Gate는 local `pre-commit`, `pre-push`, developer machine의 uncommitted state나 agent별 실행 절차에 의존하지 않습니다.
- PR Gate는 repository write 권한을 기본으로 요구하지 않으며 base branch에 commit·push·write-back하지 않습니다.
- Runner working tree의 일시적인 생성·검사 작업은 허용하지만 그 결과로 committed drift를 자동 수정하지 않습니다.
- CI에서 project Python을 사용할 때는 lock state를 암묵적으로 변경하지 않는 `uv --locked` 경로를 사용합니다.
- Source-level failure는 가능하면 projection generation 전에 판정하고, projection freshness는 이름 있는 projection 검증으로 직접 보고합니다.
- Projection generator 자체의 correctness는 deterministic test가, committed projection freshness는 generation + comparison이 소유합니다.
- Deferred 또는 optional check는 그 실패가 현재 변경의 `main` admission 결정을 바꾸지 않을 때만 non-blocking일 수 있습니다.
- Deterministic test나 structural validation의 성공을 model/runtime behavior 검증으로 해석하지 않습니다.
- Impact routing이 관련 merge-critical check를 선택했는지 확신할 수 없으면 검증을 넓히거나 gate를 실패시킵니다.
- GitHub Actions workflow처럼 권한이나 agent 실행 방식을 바꾸는 control surface 변경은 [GitHub](github.md)의 독립 근거와 사람의 명시적 승인 경계를 따릅니다.
- 실제 required check와 merge 강제 조건의 최종 enforcement는 GitHub Ruleset과 repository settings가 소유하며, 문서와 설정이 다르면 drift로 취급합니다.

## Boundary

이 문서는 formatter 규칙, validation schema, test case, eval rubric이나 GitHub의 일반 기능을 다시 정의하지 않습니다. 각각 [Formatting](formatting.md), [Validation](validation.md), [Testing](testing.md), [Evaluation](evaluation.md), [GitHub](github.md)의 owner를 따릅니다.
