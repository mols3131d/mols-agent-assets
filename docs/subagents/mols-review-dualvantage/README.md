---
description: DualVantage review family를 이해하거나 변경할 때 Goal, review model, maintenance 문서 중 무엇을 먼저 볼지 선택하는 maintainer entrypoint입니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 **서로 다른 두 decision-relevant review vantage를 독립적으로 만든 뒤, 별도 evidence gate에서 하나의 bounded assessment로 수렴시키는 review family**다.

Family를 변경할 때는 **[goal.md](goal.md)를 가장 먼저 읽는다.** `goal.md`는 왜 이 구조가 존재하는지와 무엇을 잃으면 더 이상 DualVantage가 아닌지를 정의한다.

Runtime behavior의 canonical source는 각 subagent 정의다. 이 디렉터리는 실행 prompt를 복제하지 않고 설계 의도와 유지보수 판단을 보존한다.

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
                            │
                            ▼
              clear | changes_required | blocked
```

Root는 세 번째 full reviewer가 아니라 **reviewer-of-reviewers**다. Specialist output은 final finding이 아니라 candidate claim이며, Root가 current evidence와 authority를 기준으로 판정한다.

## Read by need

| Need | Read |
| --- | --- |
| 존재 이유, 최상위 목표, identity invariant, non-goal, 성공 기준 | **[goal.md](goal.md)** |
| Observed/Inferred/Unknown, candidate lifecycle, scope disposition, convergence, final gate semantics | [review-model.md](review-model.md) |
| 역할 경계, independent brief, handoff, capability, 호출 예산, runtime 변화와 specialist evolution | [maintenance.md](maintenance.md) |

`goal.md`는 선택 문서가 아니다. Family asset의 behavior, 역할, tool/capability, delegation, stop condition 또는 review semantics를 바꾸려면 먼저 확인한다.

## Family roles

| Role | Responsibility |
| --- | --- |
| `mols-review-dualvantage` | bounded brief, 두 specialist delegation, candidate adjudication, scope/authority와 final assessment |
| `mols-review-dualvantage-verifier` | intended behavior와 governing contract를 evidence-first로 검증하고 focused non-mutating validation을 수행 |
| `mols-review-dualvantage-challenger` | material assumption을 challenge-first로 깨고 reachable counterexample과 falsifier를 제시 |

세 역할의 상세 runtime contract, target-specific fields와 tool configuration은 대응 Agent Asset에서 확인한다.

## Maintainer rule

문서를 실행 정본처럼 키우지 않는다. 공통 설계 의도는 이 디렉터리에서 한 번만 설명하고, 실제 agent behavior는 runtime source가 소유한다.

변경이 [goal.md](goal.md)의 identity invariant를 보존하면 구현 개선으로 진행할 수 있다. Invariant를 바꿔야 한다면 조용한 tuning이 아니라 명시적인 family redesign으로 취급한다.
