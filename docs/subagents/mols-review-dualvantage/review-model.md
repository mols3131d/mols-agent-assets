---
description: DualVantage의 evidence layer, candidate lifecycle, scope disposition, convergence와 final gate semantics를 유지보수할 때 사용하는 문서입니다.
---

# DualVantage Review Model

이 문서는 DualVantage가 specialist output을 어떤 의미 단위로 받아 final assessment까지 좁히는지 설명한다. 존재 이유와 최상위 불변 목표는 [goal.md](goal.md)가 소유하고, 실제 runtime instruction은 각 subagent 정의가 소유한다.

## Review flow

```text
independent specialist output
           │
           ▼
     candidate claim
           │
           ▼
  evidence adjudication
           │
           ├─ confirmed
           ├─ rejected
           ├─ merged
           └─ unresolved
           │
           ▼
    scope disposition
           │
           ▼
clear | changes_required | blocked
```

Specialist 수나 agreement는 이 flow의 단계를 건너뛰게 하지 않는다.

## Evidence layers

Family 전체에서 세 층을 구분한다.

| Layer | Meaning |
| --- | --- |
| **Observed** | source, configuration, governing contract, test, output 또는 current state에서 직접 확인한 사실 |
| **Inferred** | observed evidence에서 도출한 root cause, trigger, reachability, attribution 또는 impact |
| **Unknown** | 필요한 runtime, state, contract, permission 또는 context가 없어 확인하지 못한 조건 |

Unknown을 Observed처럼 표현하지 않고, Inferred를 source fact처럼 포장하지 않는다. Evidence가 current revision/version/state와 맞지 않으면 stale basis로 취급한다.

## Candidate admission

Specialist output은 candidate다. Root는 material candidate를 다음 축으로 판정한다.

1. **State basis** — candidate가 current review basis를 가리키는가?
2. **Scope relation** — current Goal/target과 어떤 causal 또는 acceptance relation이 있는가?
3. **Evidence** — 핵심 observed fact가 authoritative source에서 확인되는가?
4. **Reasoning and reachability** — evidence에서 trigger/path/impact로 가는 추론이 실제 reachable한가?
5. **Attribution** — current target/change가 문제를 만들거나 materially 악화했는가, 또는 Goal acceptance가 dependency를 요구하는가?
6. **Counter-evidence** — guard, invariant, validation, permission, serialization, rollback/retry, compatibility layer 또는 stronger contract가 claim을 무효화하는가?
7. **Materiality** — correctness, reliability, security, compatibility 또는 운영 판단에 의미 있는가?
8. **Action and authority** — 사실성과 impact와 별개로 current remediation 권한이 있는가?
9. **Deduplication** — 같은 root cause/path/correction으로 닫히는 candidate와 중복되는가?

Supporting context를 읽는 것은 scope expansion이 아니다. 그 context의 문제를 current remediation으로 승격하려면 current target과 causal/acceptance relation이 있어야 한다.

## Scope relation

필요하면 다음 관계를 사용해 candidate와 current Goal의 연결을 설명한다.

| Relation | Meaning |
| --- | --- |
| `explicit_target` | 명시된 target 자체의 결함 |
| `direct_regression` | current change가 만든 reachable regression |
| `contract_dependency` | Goal acceptance에 직접 필요한 caller/consumer/dependency contract |
| `acceptance_gap` | 명시된 acceptance condition을 충족하지 못함 |
| `scope_change` | 해결하려면 authorized boundary 확대가 필요함 |
| `independent_requirement` | 유용하지만 current Goal과 독립된 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | 관계를 확정할 evidence가 부족함 |

Scope relation은 remediation disposition과 같은 개념이 아니다. Relation은 **문제가 Goal과 어떻게 연결되는지**, disposition은 **현재 작업에서 어떻게 처리할 권한이 있는지**를 나타낸다.

## Claim lifecycle

Root의 내부 claim state는 다음과 같다.

| State | Meaning |
| --- | --- |
| `confirmed` | evidence, reasoning, reachability와 attribution이 충분함 |
| `rejected` | false, contradicted, unreachable, unsupported 또는 immaterial |
| `merged` | 다른 candidate와 같은 root cause로 통합됨 |
| `unresolved` | gate에 영향을 줄 수 있으나 decisive evidence가 부족함 |

Reviewer confidence, agreement 또는 반복 주장은 이 state를 대신하지 않는다.

## Scope disposition

Confirmed 또는 unresolved item은 current Goal과 authority에 따라 분류한다.

| Disposition | Meaning |
| --- | --- |
| `current_required` | authorized boundary 안에서 해결할 수 있고 Goal acceptance에 반드시 필요한 confirmed defect/regression/acceptance gap |
| `scope_decision` | 해결하려면 Goal/Scope/Acceptance/authorized contract boundary 확대 결정이 필요함 |
| `follow_up` | valid하지만 current Goal completion에 필수적이지 않은 독립 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | relation 또는 impact를 확정할 evidence가 부족함 |

`current_required`만 직접 `changes_required` 근거가 된다. `scope_decision`이나 `unknown`은 그 결정/evidence 없이는 Goal acceptance를 판단할 수 있을 때만 blocker다. `follow_up`과 `unrelated`는 impact가 커도 current remediation authority를 만들지 않는다.

## Evidence convergence

추가 evidence step은 다음 질문으로 제한한다.

> 이 evidence가 candidate disposition 또는 final assessment를 materially 바꿀 credible path가 있는가?

있으면 가장 작은 필요한 context/validation만 추가한다. 없으면 saturation으로 보고 멈춘다.

- 같은 evidence를 다른 표현으로 반복하지 않는다.
- finding 수나 confidence를 높이기 위한 no-op 탐색을 하지 않는다.
- 한 method가 saturation이어도 아직 보지 않은 distinct material lens가 결과를 바꿀 수 있으면 그 lens만 확인할 수 있다.
- decisive evidence에 접근할 수 없고 그 gap이 Goal 판단을 막으면 `blocked` 후보다.

이 convergence는 **evidence refinement**이며 specialist 재호출 loop가 아니다.

## Final assessment

Final output은 정확히 하나의 gate state를 가진다. Precedence는 `blocked > changes_required > clear`다.

1. `blocked` — required specialist coverage, decisive evidence, review basis 또는 scope authority가 부족해 independent gate를 신뢰성 있게 닫을 수 없음
2. `changes_required` — blocker가 없고 confirmed `current_required` finding이 하나 이상 있음
3. `clear` — 위 둘이 모두 없음

Confirmed defect가 있어도 전체 gate를 신뢰성 있게 닫지 못하면 `blocked`가 우선한다. `clear`는 absolute correctness proof가 아니라 명시한 review basis, scope, coverage와 evidence 안에서 current blocker/current-required finding이 남지 않았다는 bounded assessment다.

## Specialist-specific evidence shape

Verifier는 **defect claim**을 좁힌다. 핵심은 observed evidence, reachable impact, checked counter-evidence, focused validation과 falsifier다.

Challenger는 **counterexample hypothesis**를 좁힌다.

```text
Assumption
→ Trigger
→ Reachable path
→ Expected defense
→ Observed gap
→ Impact
→ Falsifier
```

Chain이 evidence 없이 끊기거나 existing defense가 path를 충분히 차단하면 confirmed defect처럼 승격하지 않는다.
