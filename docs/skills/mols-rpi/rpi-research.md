---
description: Adaptive recursive RPI에서 Research가 uncertainty와 다음 Loop 방향을 어떻게 줄이는지 보존할 핵심 결정사항입니다.
---

# RPI Research

RPI의 Research는 일반적인 자료 수집 단계가 아니라 **다음 판단과 Loop 방향을 바꾸는 uncertainty reduction**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Essence

- Research는 Plan보다 먼저 필요한 evidence를 확보합니다.
- 고정된 조사 순서보다 현재의 material uncertainty와 information gain에 따라 source, breadth, depth와 관점을 바꿉니다.
- Review에서 evidence gap이 확인되면 다음 Loop는 필요한 Research 지점부터 다시 시작할 수 있습니다.
- 더 작은 문제가 parent 진행을 막는다면 Review를 거쳐 strict-subset child Scope로 내려가 Research할 수 있습니다.
- Child Research는 parent를 대체하지 않습니다. 필요한 evidence와 parent impact만 돌려주고 parent state를 다시 검증합니다.
- 추가 Research가 downstream 판단을 materially 바꾸지 못하면 멈춥니다.

## Preserve

Research를 고도화할 때 **adaptive search, Review-driven reopening, recursive narrowing, evidence-before-Plan**을 고정된 checklist나 source quota로 바꾸지 않습니다.
