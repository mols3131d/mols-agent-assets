---
description: DualVantage review family를 이해하거나 변경할 때 Goal, review model, maintenance 문서 중 무엇을 먼저 볼지 선택하는 maintainer entrypoint입니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 **caller가 선택한 review 단계에 삽입되는 composable subagent family**다. 서로 다른 두 decision-relevant review vantage를 독립적으로 만들고, 그 candidate를 evidence gate에서 판정해 caller에게 bounded review handoff를 돌려준다.

Family를 변경할 때는 **[goal.md](goal.md)를 가장 먼저 읽는다.** `goal.md`는 왜 이 구조가 존재하는지와 무엇을 잃으면 더 이상 DualVantage가 아닌지를 정의한다.

Runtime behavior의 canonical source는 각 subagent 정의다. 이 디렉터리는 실행 prompt를 복제하지 않고 설계 의도와 유지보수 판단을 보존한다.

## Architecture

```text
         caller / outer Skill / workflow / instruction
          owns Goal · Scope · phase/loop · artifacts
                 · user-facing response · mutation
                              │
                              ▼
                     DualVantage subagent
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
                    bounded review handoff
                              │
                              ▼
                            caller
```

Root는 세 번째 full reviewer도 outer engine도 아니다. Specialist output은 final finding이 아니라 candidate claim이며, Root는 caller-provided review basis 안에서 evidence/authority admission만 소유한다.

병렬 실행을 실제 지원하는 runtime에서는 Verifier와 Challenger를 같은 delegation wave에서 시작하는 것이 기본이다. 순차 실행은 runtime 또는 current capability가 병렬 실행을 제공하지 않을 때의 fallback이다.

## Read by need

| Need | Read |
| --- | --- |
| 존재 이유, composability, 최상위 목표, identity invariant, non-goal, 성공 기준 | **[goal.md](goal.md)** |
| Observed/Inferred/Unknown, candidate lifecycle, scope disposition, convergence, review-state semantics | [review-model.md](review-model.md) |
| 역할 경계, caller ownership, independent brief, handoff, capability, 병렬 실행, 호출 예산, runtime 변화 | [maintenance.md](maintenance.md) |

`goal.md`는 선택 문서가 아니다. Family asset의 behavior, 역할, tool/capability, delegation, stop condition 또는 review semantics를 바꾸려면 먼저 확인한다.

## Family roles

| Role | Responsibility |
| --- | --- |
| caller / outer owner | outer Goal/Scope, workflow/loop, artifact policy, user-facing response, implementation/mutation |
| `mols-review-dualvantage` | bounded review brief, 두 specialist delegation, candidate adjudication, scope/authority relation, review handoff |
| `mols-review-dualvantage-verifier` | intended behavior와 governing contract를 evidence-first로 검증하고 focused non-mutating validation을 수행 |
| `mols-review-dualvantage-challenger` | material assumption을 challenge-first로 깨고 reachable counterexample과 falsifier를 제시 |

세 subagent의 상세 runtime contract, target-specific fields와 tool configuration은 대응 Agent Asset에서 확인한다.

## Maintainer rule

DualVantage를 더 편리한 outer workflow로 키우지 않는다. 공통 설계 의도는 이 디렉터리에서 한 번만 설명하고, 실제 agent behavior는 runtime source가 소유한다.

변경이 [goal.md](goal.md)의 identity invariant를 보존하면 구현 개선으로 진행할 수 있다. Invariant를 바꿔야 한다면 조용한 tuning이 아니라 명시적인 family redesign으로 취급한다.
