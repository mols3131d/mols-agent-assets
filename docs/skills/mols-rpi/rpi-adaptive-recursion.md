---
description: RPI의 핵심 특징인 adaptive recursive Loop와 child Scope의 본질을 보존하기 위한 maintainer 결정사항입니다.
---

# RPI Adaptive Recursion

RPI의 큰 특징은 **고정 반복이 아니라 Review가 다음 경로를 선택하는 adaptive recursive Loop**라는 점입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Essence

- 매 Loop는 같은 단계를 기계적으로 반복하지 않습니다. Review가 가장 이른 stale prerequisite를 찾아 다음 시작점을 정합니다.
- 더 작은 문제를 분리하는 편이 유리할 때만 Review에서 strict-subset child Scope로 내려갑니다.
- Recursion은 child Scope를 만드는 제어 방식이지 multi-agent debate나 subagent 생성을 뜻하지 않습니다.
- Parent와 모든 child는 하나의 Run과 Loop budget을 공유하며 recursion으로 budget을 reset하지 않습니다.
- Child는 parent의 Goal, Scope boundary와 authority를 넓힐 수 없습니다.
- Child 결과는 parent에 필요한 evidence, decision과 impact만 반환하고 parent state를 다시 검증합니다.
- Convergence, saturation 또는 blocker가 확인되면 불필요한 Loop나 recursion을 만들지 않습니다.

## Preserve

RPI를 고도화할 때 **Review-driven adaptation, strict-subset recursion, shared Loop accounting, parent reintegration**을 단순 반복 횟수, 고정 depth 또는 무조건적인 recursive descent로 바꾸지 않습니다.
