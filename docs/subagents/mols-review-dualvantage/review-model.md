---
description: DualVantage의 evidence layer, candidate adjudication, convergence와 caller-owned review policy handoff 의미를 유지보수할 때 사용합니다.
---

# DualVantage Review Model

이 문서는 specialist output을 **candidate claim에서 caller가 소비할 evidence-backed review signal까지** 좁히는 내부 review semantics를 소유한다. 존재 이유와 identity invariant는 [goal.md](goal.md), delegation과 capability mechanics는 [maintenance.md](maintenance.md), 실행 동작은 각 subagent 정의가 정본이다.

여기의 evidence state는 artifact schema나 user-facing response format이 아니다. Severity, blocking, disposition, completion status와 required-action policy는 caller 또는 governing review asset이 소유한다.

## Review flow

```text
independent specialist output
            │
            ▼
       candidate claim
            │
            ▼
      evidence gate
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
confirmed rejected merged
     │
     └──── unresolved
            │
            ▼
caller-owned review policy / handoff
```

Specialist 수나 agreement는 evidence gate를 건너뛰게 하지 않는다.

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
2. **Caller criteria and authority** — Goal/Scope/acceptance와 caller가 제공한 admission, severity, blocking 또는 disposition policy가 있으면 그 기준에 맞는가?
3. **Evidence** — decisive observed fact가 authoritative source에서 확인되는가?
4. **Reasoning and reachability** — evidence에서 trigger/path/impact로 가는 추론이 실제 reachable한가?
5. **Attribution** — current target/change가 문제를 만들거나 materially 악화했는가, 또는 acceptance가 dependency를 요구하는가?
6. **Counter-evidence** — guard, invariant, validation, permission, serialization, rollback/retry, compatibility layer 또는 stronger contract가 claim을 무효화하는가?
7. **Decision relevance** — caller-provided criteria가 있으면 그 기준으로, 없으면 current Goal/acceptance에 실제 영향을 주는가?
8. **Deduplication** — 같은 root cause, reachable path 또는 correction으로 닫히는 candidate와 중복되는가?

Root는 이 과정을 위해 caller policy를 소비할 수 있지만 대체 review policy를 발명하지 않는다. Supporting context를 읽는 것도 scope expansion authority가 아니다.

Finding 수는 admission criterion이 아니다. Review effort, depth, disagreement 또는 specialist 수를 정당화하기 위해 약한 candidate를 살려두지 않는다. 모든 candidate가 탈락하는 것도 정상 결과다.

## Claim state

| State | Meaning |
| --- | --- |
| `confirmed` | evidence, reasoning, reachability와 attribution이 충분함 |
| `rejected` | false, contradicted, unreachable, unsupported 또는 caller-provided review basis와 무관함 |
| `merged` | 다른 candidate와 같은 root cause로 통합됨 |
| `unresolved` | caller decision에 영향을 줄 수 있으나 decisive evidence가 부족함 |

이 state는 **epistemic accounting**이다. Caller의 PASS/FAIL, clear/blocked, severity, blocking 또는 completion state를 대신하지 않는다.

## Caller policy boundary

DualVantage는 review policy engine이 아니다.

Caller나 governing review asset이 다음을 제공하면 Root는 그 의미를 보존해 적용한다.

- admission 또는 materiality criteria
- severity convention
- blocking / non-blocking policy
- disposition 또는 status vocabulary
- acceptance / completion rule
- required-action policy

제공되지 않았다면 DualVantage가 자체 taxonomy를 만들어 빈자리를 채우지 않는다. 대신 evidence-backed candidate와 decision-relevant unknown을 최소 형태로 반환한다.

## Evidence convergence

다음 evidence step 전에 묻는다.

> 이 evidence가 candidate state 또는 caller decision을 materially 바꿀 credible path가 있는가?

있으면 가장 작은 필요한 context/validation만 추가한다. 없으면 saturation으로 보고 멈춘다.

- 같은 evidence를 다른 표현으로 반복하지 않는다.
- finding 수나 confidence를 높이기 위한 no-op 탐색을 하지 않는다.
- 한 source/method가 saturated여도 아직 보지 않은 distinct material lens가 결과를 바꿀 수 있으면 그 lens만 확인한다.
- decisive evidence에 접근할 수 없으면 `unresolved` 또는 coverage limitation으로 남긴다.
- 이 convergence는 evidence refinement이며 specialist 재호출 loop가 아니다.

## Handoff semantics

Root → caller handoff의 형식과 review-policy vocabulary는 caller가 소유한다. Review model은 presentation이 아니라 decision-relevant meaning 보존만 요구한다.

필요한 경우 다음 의미를 전달한다.

- reviewed target과 current state basis
- confirmed material candidate와 decisive evidence
- decision-relevant `unresolved`
- validation / coverage / state-basis limitation
- caller가 제공한 status, severity 또는 disposition 체계가 있을 때 그 체계에 따른 mapping

`rejected`, `merged`, reviewer vote와 reasoning transcript는 기본 handoff로 강제하지 않는다. Material candidate가 없으면 만들지 않는다.

## Specialist evidence shape

Verifier는 defect claim을 좁히고, Challenger는 counterexample hypothesis를 좁힌다. 두 worker의 세부 handoff schema는 각각의 runtime source가 소유한다.

Challenger의 핵심 reasoning chain은 다음과 같다.

```text
Assumption → Trigger → Reachable path → Expected defense → Observed gap → Impact → Falsifier
```

Chain이 evidence 없이 끊기거나 existing defense가 path를 충분히 차단하면 confirmed claim처럼 승격하지 않는다.
