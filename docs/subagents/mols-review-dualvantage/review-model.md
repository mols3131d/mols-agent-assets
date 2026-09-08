---
description: DualVantage의 evidence layer, candidate adjudication, scope relation, convergence와 caller handoff 의미를 유지보수할 때 사용합니다.
---

# DualVantage Review Model

이 문서는 specialist output을 **candidate claim에서 caller가 소비할 bounded review signal까지** 좁히는 내부 review semantics를 소유한다. 존재 이유와 identity invariant는 [goal.md](goal.md), delegation과 capability mechanics는 [maintenance.md](maintenance.md), 실행 동작은 각 subagent 정의가 정본이다.

여기의 state, disposition과 label은 artifact schema나 user-facing response format이 아니다. Caller는 자신의 workflow와 output contract에 맞게 그대로 사용하거나 매핑하거나 생략할 수 있다.

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
     ┌──────┼──────┐
     ▼      ▼      ▼
confirmed rejected merged
     │
     └──── unresolved
            │
            ▼
      scope disposition
            │
            ▼
   bounded review signal
            │
            ▼
          caller
```

Specialist 수나 agreement는 이 흐름을 건너뛰게 하지 않는다.

## Evidence layers

| Layer | Meaning |
| --- | --- |
| **Observed** | source, configuration, governing contract, test, output 또는 current state에서 직접 확인한 사실 |
| **Inferred** | observed evidence에서 도출한 root cause, trigger, reachability, attribution 또는 impact |
| **Unknown** | 필요한 runtime, state, contract, permission 또는 context가 없어 확인하지 못한 조건 |

Unknown을 Observed처럼 표현하지 않고 Inferred를 source fact처럼 포장하지 않는다. Evidence가 current revision/version/state와 맞지 않으면 stale basis로 취급한다.

## Candidate adjudication

Root는 material candidate를 다음 순서로 확인한다.

1. **State basis** — current caller-provided review basis를 가리키는가?
2. **Scope relation** — caller-provided Goal/target과 causal 또는 acceptance relation이 있는가?
3. **Evidence** — decisive observed fact가 authoritative source에서 확인되는가?
4. **Reasoning and reachability** — evidence에서 trigger/path/impact로 가는 추론이 실제 reachable한가?
5. **Attribution** — current target/change가 문제를 만들거나 materially 악화했는가, 또는 acceptance가 dependency를 요구하는가?
6. **Counter-evidence** — guard, invariant, validation, permission, serialization, rollback/retry, compatibility layer 또는 stronger contract가 claim을 무효화하는가?
7. **Materiality** — correctness, reliability, security, compatibility 또는 운영 판단에 의미 있는가?
8. **Action and authority** — 사실성과 impact와 별개로 current remediation 권한이 있는가?
9. **Deduplication** — 같은 root cause, reachable path 또는 correction으로 닫히는 candidate와 중복되는가?

Supporting context를 읽는 것은 scope expansion이 아니다. 그 context의 문제를 current remediation으로 올리려면 caller-provided target과 causal/acceptance relation이 있어야 한다. Root는 relation을 판정하지만 outer Scope를 변경하지 않는다.

## Scope relation

| Relation | Meaning |
| --- | --- |
| `explicit_target` | 명시된 target 자체의 결함 |
| `direct_regression` | current change가 만든 reachable regression |
| `contract_dependency` | caller-provided acceptance에 직접 필요한 caller/consumer/dependency contract |
| `acceptance_gap` | 명시된 acceptance condition을 충족하지 못함 |
| `scope_change` | 해결하려면 caller-owned authorized boundary 확대가 필요함 |
| `independent_requirement` | 유용하지만 current Goal과 독립된 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | relation을 확정할 evidence가 부족함 |

Relation은 문제가 Goal과 **어떻게 연결되는지**, disposition은 current authority 안에서 **어떻게 처리할 수 있는지**를 나타낸다.

## Claim state

| State | Meaning |
| --- | --- |
| `confirmed` | evidence, reasoning, reachability와 attribution이 충분함 |
| `rejected` | false, contradicted, unreachable, unsupported 또는 immaterial |
| `merged` | 다른 candidate와 같은 root cause로 통합됨 |
| `unresolved` | caller decision에 영향을 줄 수 있으나 decisive evidence가 부족함 |

Reviewer confidence, agreement 또는 반복 주장은 이 state를 대신하지 않는다.

## Disposition

| Disposition | Meaning |
| --- | --- |
| `current_required` | authorized boundary 안에서 해결할 수 있고 caller-provided acceptance에 필요한 confirmed defect/regression/acceptance gap |
| `scope_decision` | 해결하려면 Goal/Scope/Acceptance/authorized contract boundary 확대 결정이 필요함 |
| `follow_up` | valid하지만 current Goal completion에 필수적이지 않은 독립 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | relation 또는 impact를 확정할 evidence가 부족함 |

`current_required`는 current remediation이 필요하다는 가장 강한 review signal이다. `scope_decision`이나 `unknown`은 그 결정/evidence 없이는 acceptance를 판단할 수 있을 때 blocker signal이 된다. `follow_up`과 `unrelated`는 impact가 커도 remediation authority를 만들지 않는다.

## Evidence convergence

다음 evidence step 전에 묻는다.

> 이 evidence가 candidate disposition 또는 caller decision을 materially 바꿀 credible path가 있는가?

있으면 가장 작은 필요한 context/validation만 추가한다. 없으면 saturation으로 보고 멈춘다.

- 같은 evidence를 다른 표현으로 반복하지 않는다.
- finding 수나 confidence를 높이기 위한 no-op 탐색을 하지 않는다.
- 한 source/method가 saturated여도 아직 보지 않은 distinct material lens가 결과를 바꿀 수 있으면 그 lens만 확인한다.
- decisive evidence에 접근할 수 없고 그 gap이 caller decision을 막으면 blocker signal로 남긴다.
- 이 convergence는 evidence refinement이며 specialist 재호출 loop가 아니다.

## Review-state semantics

Caller가 유용하게 소비할 수 있을 때 Root는 다음 내부 의미 상태를 도출할 수 있다. 이는 고정 output schema가 아니다.

1. `blocked` — required specialist coverage, decisive evidence, review basis 또는 scope authority가 부족해 independent review를 신뢰성 있게 닫을 수 없음
2. `changes_required` — blocker가 없고 confirmed `current_required`가 하나 이상 있음
3. `clear` — 위 둘이 모두 없음

Precedence는 `blocked > changes_required > clear`다. `clear`는 absolute correctness proof가 아니라 명시된 basis/scope/coverage/evidence 안에서 current-required finding 또는 blocker가 남지 않았다는 bounded signal이다.

## Handoff semantics

Root → caller handoff의 형식은 caller가 소유한다. Review model은 presentation이 아니라 decision-relevant meaning 보존만 요구한다.

필요한 경우 다음 의미를 전달한다.

- reviewed target과 current state basis
- confirmed `current_required`
- caller decision이 필요한 `scope_decision`
- useful `follow_up`
- material unresolved evidence/coverage limitation
- caller에게 유용한 경우 review-state semantics

`rejected`, `merged`, low-value `unrelated`, reviewer vote와 reasoning transcript는 기본 handoff로 강제하지 않는다.

## Specialist evidence shape

Verifier는 defect claim을 좁히고, Challenger는 counterexample hypothesis를 좁힌다. 두 worker의 세부 handoff schema는 각각의 runtime source가 소유한다.

Challenger의 핵심 reasoning chain은 다음과 같다.

```text
Assumption → Trigger → Reachable path → Expected defense → Observed gap → Impact → Falsifier
```

Chain이 evidence 없이 끊기거나 existing defense가 path를 충분히 차단하면 confirmed defect처럼 승격하지 않는다.
