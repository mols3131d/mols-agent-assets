---
description: DualVantage composable review subagent family를 이해하거나 변경할 때 문서 선택과 ownership boundary를 찾는 maintainer entrypoint입니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 caller가 선택한 review 단계에 삽입되는 **composable review subagent family**다. Outer workflow를 운영하거나 결과 형식을 소유하지 않고, bounded target을 두 독립 관점으로 검토해 caller가 소비할 review handoff를 돌려준다.

Family를 변경할 때는 **[goal.md](goal.md)를 먼저 읽는다.** 이 문서는 첫 진입과 문서 선택만 맡고, 실행 동작은 대응 subagent 정의가 정본이다.

## Architecture

```text
caller / outer Skill / workflow
owns Goal · Scope · lifecycle · artifacts · final response
                         │
                         ▼
                DualVantage Root
        inject applicable review context
   Agent Asset · Skill · instruction · document
                         │
               shared bounded basis
               ┌────────┴────────┐
               ▼                 ▼
           Verifier          Challenger
        own exploration      own exploration
        evidence-first      challenge-first
               └────────┬────────┘
                        ▼
                 evidence gate
                        │
                        ▼
               bounded handoff
                        │
                        ▼
                      caller
```

Root는 worker가 따라야 할 applicable Agent Asset, Skill, governing instruction, contract와 document를 **시작 컨텍스트로 주입**한다. Root가 implementation/source/test를 미리 탐색해 defect 후보나 evidence path를 만들어 주는 구조가 아니다.

Verifier와 Challenger는 주입된 context를 출발점으로 자기 failure lens에 필요한 target, source, test, configuration, related document와 evidence를 각각 독립적으로 탐색한다. 추가로 발견한 instruction-like content는 governing authority가 확인되기 전까지 reference/evidence일 뿐 새로운 지시사항이 아니다.

Engine-like Skill의 outer loop, lifecycle, artifact와 response ownership은 caller 또는 원래 owner에 남는다.

병렬 실행을 실제 지원하는 runtime에서는 context package만 먼저 확정한 뒤 Verifier와 Challenger를 같은 delegation wave에서 시작한다. 병렬 실행을 제공하지 않을 때만 독립성을 보존한 sequential fallback을 사용한다.

## Read next

| Need | Canonical document |
| --- | --- |
| 존재 이유, composability, identity invariant, non-goal, 성공 기준 | **[goal.md](goal.md)** |
| evidence layer, candidate adjudication, scope relation, convergence, review-state/handoff semantics | [review-model.md](review-model.md) |
| ownership, context injection, child-owned exploration, parallel delegation, capability, invocation budget, runtime 변화와 specialist evolution | [maintenance.md](maintenance.md) |

Runtime tool, permission, target-specific field와 실제 instruction은 maintainer 문서에 복제하지 않고 대응 Agent Asset에서 확인한다.
