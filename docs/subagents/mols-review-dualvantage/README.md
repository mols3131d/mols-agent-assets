---
description: DualVantage composable review subagent family를 이해하거나 변경할 때 문서 선택과 ownership boundary를 찾는 maintainer entrypoint입니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 caller가 선택한 review 단계에 삽입되는 **portable composable review subagent family**다. Outer workflow를 운영하거나 결과 형식을 소유하지 않고, 이식된 host repository/runtime의 실제 지침·Skill·Rule·문서 semantics를 존중하면서 bounded target을 두 독립 관점으로 검토해 caller가 소비할 review handoff를 돌려준다.

Family를 변경할 때는 **[goal.md](goal.md)를 먼저 읽는다.** 이 문서는 첫 진입과 문서 선택만 맡고, 실행 동작은 대응 subagent 정의가 정본이다.

## Architecture

```text
outer caller / host Skill / workflow
owns Goal · Scope · lifecycle · artifacts · final response
                         │
                         ▼
                DualVantage Root
      resolve applicable host review context
   Skill · Rule · instruction · contract · document
                         │
               shared bounded basis
               ┌────────┴────────┐
               ▼                 ▼
           Verifier          Challenger
        own exploration      own exploration
        evidence-first      challenge-first
               └────────┬────────┘
                        ▼
              candidate adjudication
                        │
                        ▼
               bounded handoff
                        │
                        ▼
                 outer caller
```

Root는 current host에서 실제 적용되는 context를 resolve해 **시작 컨텍스트로 주입**한다. 특정 MOLS/Rulesync path나 asset taxonomy를 전제로 하지 않으며, external catalog에서 새 review capability를 고르는 generic finder도 아니다. Root가 implementation/source/test를 미리 탐색해 defect 후보나 evidence path를 만들어 주는 구조도 아니다.

Verifier와 Challenger는 주입된 context를 출발점으로 자기 failure lens에 필요한 target, source, test, configuration, related document와 evidence를 각각 독립적으로 탐색한다. 새 path에서 추가 scoped instruction이 적용되면 host repository/runtime의 native scope·precedence semantics에 따라 직접 준수한다.

Outer Skill이나 workflow가 있으면 한 specialist invocation에 필요한 review-local constraint, criterion, evidence rule, check와 question만 합성한다. 그 owner의 loop, lifecycle, transition, artifact와 response ownership은 그대로 남는다.

병렬 실행을 실제 지원하는 runtime에서는 context package만 먼저 확정한 뒤 Verifier와 Challenger를 같은 delegation wave에서 시작한다. 병렬 실행을 제공하지 않을 때만 독립성을 보존한 sequential fallback을 사용한다.

## Read next

| Need | Canonical document |
| --- | --- |
| 존재 이유, portability, composability, identity invariant, non-goal, 성공 기준 | **[goal.md](goal.md)** |
| evidence layer, candidate adjudication, scope relation, convergence, review-state/handoff semantics | [review-model.md](review-model.md) |
| ownership, host-context composition, child-owned exploration, parallel delegation, capability, invocation budget와 runtime/host 변화 | [maintenance.md](maintenance.md) |

Runtime tool, permission, host-specific routing field와 실제 instruction은 maintainer 문서에 복제하지 않고 이식된 environment의 authoritative contract와 대응 Agent Asset에서 확인한다.
