---
description: 저장소의 change lifecycle, branch validation, main admission, blocking·deferred evidence, projection 검증과 local·agent·API write path의 경계를 설계·운영할 때 사용하는 정책입니다.
---

# Continuous Integration

CI는 단순한 `PR Gate`나 GitHub Actions workflow가 아니라, **변경이 만들어져 통합될 때까지 repository state에 필요한 근거를 점진적으로 확보하는 integration evidence system**입니다.

이 저장소는 local Git뿐 아니라 `gh` CLI, GitHub API, MCP, ChatGPT/GitHub Plugin, 웹 UI와 agent automation을 통해 branch가 직접 변경될 수 있습니다. CI는 특정 authoring path가 hook이나 local command를 실행했을 것이라고 가정하지 않습니다.

이 정책은 GPPC의 Goal, Principles, Patterns, Contracts로 CI의 본질과 실행 계약을 구분합니다.

## Authority

- change lifecycle의 validation placement, branch validation, `PR Gate`, blocking·deferred evidence, projection gate와 local feedback의 관계 → 이 문서
- working tree, branch, ref, commit과 history 안전성 → [VCS / Git](vcs-git.md)
- GitHub permission, Ruleset, Pull Request, Actions trigger와 Merge → [GitHub](github.md)
- 파일 표현의 정규화와 formatter write path → [Formatting](formatting.md)
- 구조·파생 계약의 의미 → [Validation](validation.md)
- repository-owned executable behavior의 deterministic test → [Testing](testing.md)
- model/runtime behavior evidence → [Evaluation](evaluation.md)
- canonical source와 derived output의 권한 → [작성 원본과 권한](source-authority.md)

Workflow filename, step 이름과 tool invocation 같은 구현 세부는 `.github/workflows/`와 repository-native 실행 entrypoint가 소유합니다. 이 문서는 어떤 시점에 어떤 근거가 필요한지와 그 blocking boundary를 정의합니다.

## Goal

변경을 만든 도구나 실행 환경과 무관하게 **지속되는 repository change가 검증 가능한 integration path를 갖고, `main`에는 알고 있다면 merge를 거부했을 실패가 남지 않도록** 합니다.

`main` admission은 최종 경계지만 CI는 그 직전 한 번만 실행되는 gate가 아닙니다. Hook을 우회하는 remote write도 가능한 한 branch 단계에서 조기에 검증하고, Pull Request에서는 merge candidate를 authoritative하게 다시 검증합니다.

## Principles

### Authoring Path Is Not Evidence

Local Git, `gh`, API, MCP, Plugin, 웹 UI와 agent automation은 모두 유효한 변경 경로일 수 있지만 그 경로 자체는 correctness evidence가 아닙니다.

`pre-commit`이나 `pre-push`가 실행됐다고 추정하지 않습니다. 특히 GitHub Contents API나 connector가 branch에 직접 commit하면 local hook이 존재해도 실행되지 않습니다.

### Progressive Integration

가능한 한 실패를 값싼 단계에서 일찍 발견하되, 앞 단계의 성공이 뒤 단계의 근거를 대체하지 않습니다.

```text
authoring / local feedback
→ branch update validation
→ pull request admission
→ deferred / post-merge evidence
```

각 단계는 같은 검증을 무조건 반복하는 것이 아니라 그 시점에 필요한 claim을 가장 싼 근거로 확인합니다.

### Strict Admission, Proportional Evidence

알려진 실패가 `main`의 상태를 받아들일 수 없게 만든다면 merge 전에 blocking evidence가 있어야 합니다. 반대로 merge 판단을 바꾸지 않는 진단, 광범위한 confidence check와 유지보수 작업은 admission gate를 불필요하게 무겁게 만들지 않습니다.

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

### Shared Check Semantics

Local hook, branch CI와 PR CI가 같은 계약을 확인한다면 별도의 의미를 다시 구현하지 않고 repository-native command, validator, generator와 test를 재사용합니다.

실행 위치가 다르다는 이유로 세 개의 서로 다른 validator를 만들지 않습니다. CI YAML은 orchestration을 소유하고 검증 의미는 기존 owner에 둡니다.

### Read-only Integration Evidence

검증 workflow는 repository maintenance automation이 아닙니다. Runner의 ephemeral working tree에서 formatter check, generator나 projection 작업을 실행할 수 있지만 검증 결과를 commit·push하거나 base branch에 write-back하지 않습니다.

### Fail-safe and Diagnosable

영향 범위를 확실히 판단할 수 없으면 관련 검증을 넓히거나 실패시킵니다. 중요한 검증을 조용히 생략하지 않습니다.

CI 단계는 failure class가 드러나도록 나누고 가능한 경우 실패 원인과 repository-native 복구 entrypoint를 함께 보여줍니다.

## Patterns

### Change Entry Paths

CI 설계는 최소한 다음 경로를 구분합니다.

| Change path | Local hook 보장 | CI 관점 |
| --- | --- | --- |
| local Git commit/push | 설치·실행 상태에 따라 가능 | 빠른 feedback으로 활용하되 신뢰 경계로 삼지 않음 |
| `gh` CLI | 사용 방식에 따라 다름 | local Git인지 API mutation인지 추정하지 않고 실제 branch state를 검증 |
| GitHub API / Contents API | 없음 | server-side branch validation 대상 |
| GitHub MCP / Plugin / connector | 없음으로 간주 | server-side branch validation 대상 |
| GitHub web UI | 없음 | server-side branch validation 대상 |
| coding agent / automation | runtime마다 다름 | agent self-report나 runtime hook을 admission evidence로 간주하지 않음 |

특정 tool을 위한 별도 quality standard를 만들지 않습니다. 모든 경로는 같은 repository contract에 수렴합니다.

### Local Feedback

Local hook과 explicit local command는 commit이나 push 전에 문제를 빠르게 발견하고, 필요한 경우 projection을 작성 원본에서 동기화하는 보조 장치입니다.

```text
local edit
→ format / sync / fast checks
→ commit / push
```

이 단계의 성공은 branch 또는 PR의 server-side evidence를 대체하지 않습니다. API·MCP·Plugin 경로가 이 단계를 건너뛰어도 integration contract가 깨지지 않아야 합니다.

### Branch Update Validation

Remote branch에 지속되는 commit이 생기면 PR 존재 여부와 무관하게 가능한 한 server-side에서 빠른 검증을 제공합니다. 이 surface의 목적은 **hookless write를 조기에 발견하고 다음 integration 단계로 넘기기 전에 branch 상태를 진단하는 것**입니다.

대표적으로 다음과 같은 값싼 검증을 배치할 수 있습니다.

```text
remote branch update
→ representation / source checks
→ cheap deterministic validation
→ projection generation + drift check
→ branch feedback
```

Branch validation은 required merge admission 자체가 아닙니다. Open PR이 있는 branch update는 PR validation과 실행을 공유하거나 중복 비용을 줄일 수 있지만, 최종 merge candidate 검증을 생략해서는 안 됩니다.

### PR Admission Gate

`main` admission의 authoritative server-side boundary는 required `PR Gate`입니다. Open Pull Request의 head가 바뀌면 base와 결합된 merge candidate를 다시 검증합니다.

Local hook, branch validation, agent self-review나 API mutation 성공은 이 gate를 대체하지 않습니다. Ruleset은 최종적으로 required check를 강제합니다.

### Evidence Pipeline

Merge-critical evidence는 failure class가 드러나는 순서로 실행합니다.

```text
representation / source validation
→ deterministic behavior tests
→ projection generation
→ projection drift / cross-surface validation
→ admission decision
```

- **Representation / source validation**은 formatter contract, syntax, frontmatter, config처럼 projection 전에 판정할 수 있는 상태를 빠르게 거릅니다.
- **Deterministic behavior tests**는 generator, sync, validator, adapter와 repository-owned script의 동작을 검증합니다.
- **Projection generation**은 canonical source에서 공식 generator를 runner working tree에 실행합니다.
- **Projection drift / cross-surface validation**은 생성 결과와 committed output의 정합성, source와 derived surface 사이의 계약을 확인합니다.

각 단계가 같은 claim을 중복해서 검증하지 않습니다. 특히 committed projection freshness는 generic pytest failure에 숨기기보다 projection stage에서 직접 드러내는 것을 우선합니다.

### Failure to Evidence

| Failure class | Cheapest sufficient evidence | Default boundary |
| --- | --- | --- |
| explicit representation contract 위반 | formatter/static check | blocking if repository contract |
| malformed frontmatter·config·schema | static validator | blocking PR |
| generator·sync·validator 동작 regression | deterministic test | blocking PR |
| committed projection drift | official generation + diff/status | branch feedback + blocking PR |
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

### Deferred Evidence

비용이 크거나 stochastic한 검증, 광범위한 provider/runtime matrix, exhaustive diagnostics와 maintenance write는 merge 판단에 필요하지 않다면 manual, scheduled 또는 별도 non-blocking surface로 둡니다.

어떤 deferred check의 실패를 알았다면 현재 변경을 merge하지 않았을 것이라면 그 check는 deferred에 둘 수 없습니다. 필요한 최소 scope로 줄여 blocking evidence로 승격합니다.

### Maintenance Automation

Formatting write, projection regeneration, index synchronization처럼 repository state를 실제 수정하는 automation은 validation과 분리합니다.

자동 maintenance가 필요하더라도 write permission, canonical source, trigger와 loop 방지 계약을 별도로 정의합니다. Admission workflow에 write capability를 섞지 않습니다.

### Impact Routing

Repository 규모나 검증 비용이 실제로 커졌을 때만 change-impact routing을 도입합니다. Path filter, naming convention, 작은 router 순으로 단순한 방법을 우선하고 영향 판정이 불확실하면 더 넓은 검증으로 fallback합니다.

Routing 자체가 merge-critical evidence를 누락시킬 수 있다면 router도 deterministic하게 검증합니다.

## Contracts

- `main`에 허용할 수 없는 알려진 실패는 required `PR Gate`에서 blocking pre-merge evidence를 가져야 합니다.
- Local Git, `gh`, API, MCP, Plugin, 웹 UI와 agent automation은 동일한 repository contract를 적용받으며 특정 authoring path 자체를 validation evidence로 간주하지 않습니다.
- Remote branch에 직접 지속되는 write를 자주 사용하는 저장소이므로 branch update validation을 first-class CI surface로 취급합니다. 이는 early feedback이며 `PR Gate`를 대체하지 않습니다.
- PR Gate와 branch validation은 local `pre-commit`, `pre-push`, developer machine의 uncommitted state나 agent별 실행 절차에 의존하지 않습니다.
- 같은 contract를 여러 CI surface에서 확인할 때 repository-native command와 validator를 재사용하고 validation semantics를 workflow마다 복제하지 않습니다.
- 검증 workflow는 repository write 권한을 기본으로 요구하지 않으며 commit·push·base branch write-back을 하지 않습니다.
- Runner working tree의 일시적인 생성·검사 작업은 허용하지만 그 결과로 committed drift를 자동 수정하지 않습니다.
- CI에서 project Python을 사용할 때는 lock state를 암묵적으로 변경하지 않는 `uv --locked` 경로를 사용합니다.
- Source-level failure는 가능하면 projection generation 전에 판정하고, projection freshness는 이름 있는 projection 검증으로 직접 보고합니다.
- Projection generator 자체의 correctness는 deterministic test가, committed projection freshness는 generation + comparison이 소유합니다.
- Deferred 또는 optional check는 그 실패가 현재 변경의 `main` admission 결정을 바꾸지 않을 때만 non-blocking일 수 있습니다.
- Deterministic test나 structural validation의 성공을 model/runtime behavior 검증으로 해석하지 않습니다.
- Impact routing이 관련 merge-critical check를 선택했는지 확신할 수 없으면 검증을 넓히거나 gate를 실패시킵니다.
- Branch와 history의 생성·격리 규칙은 [VCS / Git](vcs-git.md), GitHub-side permissions와 required check enforcement는 [GitHub](github.md)가 소유합니다.
- GitHub Actions workflow처럼 권한이나 agent 실행 방식을 바꾸는 control surface 변경은 [GitHub](github.md)의 독립 근거와 사람의 명시적 승인 경계를 따릅니다.
- 실제 required check와 merge 강제 조건의 최종 enforcement는 GitHub Ruleset과 repository settings가 소유하며, 문서와 설정이 다르면 drift로 취급합니다.

## Boundary

이 문서는 formatter 규칙, validation schema, test case, eval rubric, Git 명령 semantics나 GitHub의 일반 기능을 다시 정의하지 않습니다. 각각 [Formatting](formatting.md), [Validation](validation.md), [Testing](testing.md), [Evaluation](evaluation.md), [VCS / Git](vcs-git.md), [GitHub](github.md)의 owner를 따릅니다.
