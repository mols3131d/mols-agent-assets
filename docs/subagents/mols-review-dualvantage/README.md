---
description: mols-review-dualvantage family의 목적, 본질, 역할 분리, evidence convergence와 유지보수 원칙에 사용합니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 **서로 다른 두 review vantage를 독립적으로 만든 뒤 별도 evidence gate에서 하나의 bounded assessment로 수렴시키는 review family**다.

목적은 reviewer 수를 늘리는 것이 아니다. 하나의 reasoning path와 failure mode에 과도하게 의존하지 않으면서, specialist의 discovery bias와 final judgment를 분리하고, 추가 탐색이 더 이상 판정을 바꾸지 않을 때 멈추는 것이 핵심이다.

이 문서는 실행 prompt를 복제하지 않는다. Tool, target, output contract와 runtime semantics는 각 Agent Asset이 소유하고, 여기서는 구현이 바뀌어도 보존할 설계 본질과 유지보수 기준만 기록한다.

## Architecture

```text
                       DualVantage
                            │
                 same bounded review brief
                  ┌─────────┴─────────┐
                  ▼                   ▼
             Verifier             Challenger
          evidence-first         challenge-first
          precision bias          recall bias
                  │                   │
                  └─────────┬─────────┘
                            ▼
                     Evidence Gate
          scope / authority / evidence / reachability
        attribution / counter-evidence / materiality
                            │
                            ▼
              clear | changes_required | blocked
```

기본 shape는 **independent specialist discovery → evidence-gated adjudication → bounded final assessment**다.

`DualVantage`의 `dual`은 agent 수가 아니라 같은 target 판단을 바꿀 수 있는 **두 decision-relevant vantage**를 뜻한다.

- **Verifier** — 관찰 가능한 근거로 입증되는 material defect가 있는가?
- **Challenger** — 현재 동작의 전제를 realistic trigger로 깨면 reachable failure가 생기는가?
- **Evidence gate** — candidate를 current Goal의 remediation/blocker로 주장할 근거와 권한이 있는가?

Root reviewer는 세 번째 vantage가 아니라 두 vantage를 판정하는 owner다.

## Core principles

### Two lenses, one gate

Verifier는 precision, Challenger는 useful recall에 편향된다. 같은 checklist를 다른 문구로 반복하면 별도 execution의 가치가 사라진다. Final gate는 다시 precision과 authority boundary를 우선한다.

### Candidate is not a finding

Specialist output은 **falsifiable candidate claim**이다. Subagent가 final admission까지 소유하면 discovery bias, anchoring과 overclaim이 그대로 외부 결과가 된다.

`subagent output = candidate claim`, never proof by itself.

### Evidence beats consensus

Reviewer agreement나 majority는 correctness proof가 아니다. Disagreement도 어느 쪽의 evidence를 자동으로 약하게 만들지 않는다. 최종 판정은 governing contract, current state, reachability, attribution, counter-evidence, materiality와 authority로 결정한다.

### Authority before impact

High-impact issue가 곧 current remediation은 아니다. 해결하려면 Goal/Scope/Acceptance 또는 authorized contract boundary 확대가 필요한지 먼저 판단한다. Severity는 impact를 설명할 뿐 scope authority를 만들지 않는다.

### Independence before parallelism

병렬 실행은 latency optimization이고 independence는 quality mechanism이다. 순차 실행이어도 sibling 결과를 다음 brief에 넣지 않으면 독립 관점을 상당 부분 보존할 수 있다. 반대로 병렬 실행이어도 같은 speculative diagnosis를 주입하면 독립성은 약해진다.

### Single-pass delegation

한 review run의 자동 specialist invocation은 **총 2회 이하: Verifier 최대 1회, Challenger 최대 1회**다. 실패, timeout, incomplete result, disagreement, uncertainty 또는 refinement 필요도 자동 재호출 사유가 아니다.

새 2회 budget은 caller가 명시적으로 새 review pass를 요청한 경우에만 생긴다. Root가 스스로 pass를 갱신하지 않는다.

### Refine evidence, not agents

반복이 필요한 곳은 subagent invocation이 아니라 evidence adjudication이다.

```text
candidate
   │
   ▼
smallest decisive evidence
   │
   ├─ next evidence can change disposition? ─ yes ─► inspect narrowly
   │                                                │
   └─ no / saturated / decisive blocker ◄───────────┘
   │
   ▼
terminal claim state
```

추가 작업은 disposition 또는 assessment를 바꿀 credible information gain이 있을 때만 수행한다. 같은 evidence 재표현, no-op search와 finding 수를 채우는 탐색은 refinement가 아니다.

### Freshness is evidence quality

Evidence가 다른 revision/version/stale observable state를 가리키면 current finding 근거가 아닐 수 있다. Candidate와 handoff는 가능한 범위에서 state basis를 포함한다.

## Role boundaries

| Role | Owns | Does not own |
| --- | --- | --- |
| `mols-review-dualvantage` | bounded brief, independent delegation, evidence gate, scope/authority, reconciliation, deduplication, final assessment | third full review, 새 defect/counterexample hunting, scope expansion, implementation/approval/merge |
| `mols-review-dualvantage-verifier` | intended behavior/contract/correctness 검증, reachability, counter-evidence, smallest decisive non-mutating validation | broad hypothesis generation, final disposition/authority |
| `mols-review-dualvantage-challenger` | material assumption, realistic trigger, reachable counterexample, expected defense와 falsifier | general correctness checklist, active attack/reproduction, final disposition/authority |

Coverage가 부족하면 Root가 그 perspective를 대신 수행하지 않고 gap을 드러낸다.

### Challenger reasoning chain

```text
Assumption
→ Trigger
→ Reachable path
→ Expected defense
→ Observed gap
→ Impact
→ Falsifier
```

이 chain의 중간이 evidence 없이 끊기면 confirmed defect처럼 다루지 않는다.

## Evidence model

Family 전체에서 세 층을 구분한다.

| Layer | Meaning |
| --- | --- |
| **Observed** | source, configuration, contract, test, output 또는 current state에서 직접 확인한 사실 |
| **Inferred** | observed evidence에서 도출한 root cause, trigger, reachability, attribution 또는 impact |
| **Unknown** | 필요한 runtime, state, contract, permission 또는 context가 없어 확인하지 못한 조건 |

Unknown을 Observed처럼 표현하지 않고, Inference를 source fact처럼 포장하지 않는다.

Candidate admission 전에 가장 가까운 counter-evidence를 먼저 본다. Stronger contract, guard, permission, validation, serialization, transaction/rollback/retry semantics, compatibility layer 또는 unreachable-state constraint가 candidate를 무효화하면 final gate에 올리지 않는다.

## Claim lifecycle

| State | Meaning |
| --- | --- |
| `confirmed` | evidence, reasoning, reachability와 attribution이 충분함 |
| `rejected` | false, contradicted, unreachable, unsupported 또는 immaterial |
| `merged` | 다른 candidate와 같은 root cause로 통합됨 |
| `unresolved` | gate에 영향을 줄 수 있으나 decisive evidence가 부족함 |

Confidence label과 reviewer agreement는 이 state를 대신하지 않는다.

## Scope disposition

| Disposition | Meaning |
| --- | --- |
| `current_required` | authorized boundary 안에서 해결할 수 있고 current Goal acceptance에 반드시 필요함 |
| `scope_decision` | 해결하려면 Goal/Scope/Acceptance/authorized contract boundary 확대 결정이 필요함 |
| `follow_up` | valid하지만 current Goal completion에 필수적이지 않은 독립 요구사항 |
| `unrelated` | current target과 causal/material relation이 없음 |
| `unknown` | relation 또는 impact를 확정할 evidence가 부족함 |

`current_required`만 직접 `changes_required` 근거가 된다. `scope_decision`과 `unknown`은 그 결정/evidence 없이는 Goal acceptance를 판단할 수 있을 때만 blocker다. `follow_up`과 `unrelated`는 impact가 커도 current remediation authority를 만들지 않는다.

## Final assessment

Final output은 정확히 하나의 gate state를 가진다. Precedence는 `blocked > changes_required > clear`다.

1. `blocked` — required coverage, decisive evidence, review basis 또는 scope authority가 부족해 independent gate를 닫을 수 없음
2. `changes_required` — blocker가 없고 confirmed `current_required` finding이 하나 이상 있음
3. `clear` — 위 둘이 모두 없음

이 assessment는 absolute correctness proof가 아니다. 명시한 review basis, scope, coverage와 evidence에 대한 bounded independent assessment다.

## Maintenance rules

- **역할 차이를 보존한다.** Verifier와 Challenger가 같은 checklist로 수렴하면 separate agent justification을 다시 검토한다.
- **Root를 third reviewer로 키우지 않는다.** Root quality는 더 많은 defect hunting이 아니라 더 강한 admission gate에서 나온다.
- **Handoff는 최소 충분하게 유지한다.** Target/location, state basis, decisive observed evidence, inference, counter-evidence, validation/falsifier와 material unknown이면 충분하다. Full repository summary나 reasoning transcript를 복제하지 않는다.
- **Capability는 responsibility에 맞춘다.** Verifier만 focused validation 실행이 필요할 수 있고, Challenger는 read/search 중심, Root는 read/search/delegation 중심이다.
- **Failure를 성공으로 흡수하지 않는다.** Unavailable capability, incomplete specialist result와 stale basis를 coverage/limitation으로 드러낸다.
- **Signal density를 최적화한다.** Finding 수, agent 수, source 수와 token 수 자체는 quality metric이 아니다.
- **새 specialist를 쉽게 추가하지 않는다.** 기존 두 vantage와 다른 decision-relevant failure lens, 실제 isolation benefit, independent activation/reuse 가치가 coordination/token cost보다 클 때만 고려한다.

## Success criteria

DualVantage가 잘 작동하면 다음이 성립한다.

- Verifier와 Challenger가 실제로 다른 failure mode를 탐색한다.
- initial specialist analysis가 independent하다.
- candidate가 current state basis와 observable evidence를 가진다.
- Challenger hypothesis가 trigger/path/defense/falsifier를 가진다.
- Verifier validation이 smallest decisive check에 집중한다.
- Root가 third full review 없이 candidate를 adjudicate할 수 있다.
- scope authority와 issue impact가 섞이지 않는다.
- false positive와 duplicate가 final output에서 억제된다.
- final gate가 `clear | changes_required | blocked`로 명확하다.
- specialist invocation은 run당 최대 2회에서 종료된다.
- saturation 이후 no-op review churn이 발생하지 않는다.

## Preserve across runtime changes

Vendor, model, tool alias, runtime API와 projection format이 바뀌어도 다음은 보존한다.

1. 서로 다른 두 decision-relevant review vantage
2. 가능한 한 독립적인 initial discovery
3. specialist output = candidate claim
4. 별도 evidence gate의 final judgment ownership
5. Root는 third full review가 아니라 validation/authority/admission owner
6. Observed / Inferred / Unknown 분리
7. authority boundary를 severity보다 먼저 판정
8. reviewer agreement를 correctness proof로 사용하지 않음
9. run당 Verifier 1회 + Challenger 1회의 hard invocation budget
10. additional work는 credible information gain이 있을 때만 수행하고 saturation에서 종료
11. material coverage/evidence gap을 성공으로 흡수하지 않음
12. false-positive suppression과 actionable signal을 finding 수보다 우선

이 조건이 사라지면 파일명이나 agent 수가 같아도 더 이상 DualVantage라고 보기 어렵다.
