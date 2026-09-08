---
description: DualVantage composable review subagent family를 이해하거나 변경할 때 문서 선택과 ownership boundary를 찾는 maintainer entrypoint입니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 outer caller가 선택한 review 단계에 삽입되는 **portable composable review subagent family**다. Outer workflow, review policy, artifact 또는 response format을 소유하지 않고 bounded target을 두 독립 관점으로 검토해 evidence-backed handoff를 돌려준다.

Family를 변경할 때는 **[goal.md](goal.md)를 먼저 읽는다.** 이 문서는 첫 진입과 문서 선택만 맡고 실행 동작은 대응 subagent 정의가 정본이다.

## Architecture

```text
outer caller / review Skill / workflow
owns Goal · Scope · review policy · artifacts · final response
                         │
                         ▼
                DualVantage Root
            inject review context
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
                 outer caller
```

Root는 현재 review에 적용되는 Skill, Rule, instruction, contract와 document 중 필요한 의미만 시작 컨텍스트로 주입한다. Root가 implementation/source/test를 미리 탐색해 defect 후보나 evidence path를 만들어 주는 구조가 아니다.

Verifier와 Challenger는 주입된 context를 출발점으로 자기 failure lens에 필요한 target, source, test, configuration, related document와 evidence를 각각 독립적으로 탐색한다.

Caller나 review Skill이 admission, severity, blocking, disposition 또는 completion policy를 갖고 있으면 DualVantage는 그 의미를 보존해 사용한다. 그런 policy가 없으면 자체 PASS/FAIL, clear/blocked, severity 또는 disposition 체계를 만들지 않는다.

병렬 실행을 실제 지원하는 runtime에서는 context package만 먼저 확정한 뒤 Verifier와 Challenger를 같은 delegation wave에서 시작한다. 병렬 실행을 제공하지 않을 때만 독립성을 보존한 sequential fallback을 사용한다.

## Read next

| Need | Canonical document |
| --- | --- |
| 존재 이유, composability, caller/review-policy ownership, identity invariant, non-goal, 성공 기준 | **[goal.md](goal.md)** |
| evidence layer, candidate adjudication, convergence와 caller-owned review-policy handoff semantics | [review-model.md](review-model.md) |
| ownership, context injection, child-owned exploration, parallel delegation, capability, invocation budget와 runtime 변화 | [maintenance.md](maintenance.md) |

Runtime tool, permission과 target-specific field는 maintainer 문서에 복제하지 않고 대응 Agent Asset과 authoritative runtime contract에서 확인한다.
