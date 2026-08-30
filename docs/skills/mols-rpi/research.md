---
description: RPI Research를 설계하거나 변경할 때 보존해야 할 핵심 결정사항을 정리한 maintainer 문서입니다.
---

# RPI Research

RPI Skill의 Research를 수정할 때 보존할 본질만 정리합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Decisions

- Research의 목적은 자료 수집이 아니라 **downstream 결정을 바꿀 수 있는 material uncertainty를 줄이는 것**입니다.
- 먼저 Goal, Scope, Plan 또는 acceptance를 바꿀 수 있는 질문과 가정을 찾습니다.
- Evidence source는 고정하지 않습니다. 현재 질문에 맞춰 repository/workspace, external source 또는 둘을 함께 사용합니다.
- 가능한 경우 직접적이고 authoritative하며 current한 evidence를 우선합니다.
- 중요한 결론은 필요할 때 counterevidence나 alternative explanation으로 도전합니다.
- Evidence가 충돌하면 source 수로 결정하지 않고 relevance, authority, directness, freshness를 기준으로 조정합니다.
- 추가 Research가 downstream 판단을 materially 바꾸지 못하면 멈춥니다.

## Output

Research artifact에는 필요한 evidence, findings, material conflict와 residual uncertainty만 남깁니다. 검색 과정 전체나 source 개수 자체를 성과로 취급하지 않습니다.
