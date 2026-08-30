---
description: RPI, adaptive control, recursive resolution이라는 이 Skill의 핵심 설계를 보존하기 위한 maintainer 문서입니다.
---

# RPI

이 문서는 이 Skill의 고유한 RPI 설계만 기록합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## RPI

- 기본 계약은 **Research → Plan → Implementation → Review**입니다.
- 이는 고정 pipeline이 아니라 prerequisite 관계입니다. 유효한 Research나 Plan은 재사용할 수 있습니다.
- 하나의 Loop는 같은 단계를 반복하는 횟수가 아니라, 필요한 가장 이른 prerequisite에서 시작해 Review로 닫히는 substantive attempt입니다.
- Evidence before Plan, Plan before Work, Review before acceptance를 유지합니다.

## Adaptive

- Review가 현재 evidence와 state를 보고 다음 Loop의 시작점을 결정합니다.
- Research, Plan, Work를 매번 처음부터 반복하지 않습니다. stale한 prerequisite만 다시 엽니다.
- Scope, evidence direction, replanning과 continuation은 material uncertainty와 expected gain에 맞춰 조정합니다.
- Convergence, saturation 또는 blocker가 확인되면 불필요한 Loop를 만들지 않습니다.

## Recursive

- 더 작은 문제를 분리하는 편이 materially 유리할 때만 Review에서 child Scope로 내려갑니다.
- Child Scope는 parent의 strict subset이며 Goal, authority, safety boundary를 넓히지 않습니다.
- Parent와 모든 child는 하나의 Run과 Loop budget을 공유하며 recursion으로 budget을 reset하지 않습니다.
- Child는 parent에 필요한 evidence, decision과 impact만 반환하고 parent state를 다시 검증합니다.
- Recursion은 multi-agent debate나 subagent 생성을 의미하지 않습니다.

## Preserve

이 Skill을 변경할 때 **Review-driven adaptation, prerequisite reuse, strict-subset recursion, shared Loop accounting, parent reintegration**을 고정 반복, 고정 depth 또는 무조건적인 recursive descent로 바꾸지 않습니다.
