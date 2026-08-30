---
description: Adaptive recursive RPI에서 Plan이 각 Loop와 Scope 변화에 맞춰 어떻게 갱신되는지 보존할 핵심 결정사항입니다.
---

# RPI Plan

RPI의 Plan은 한 번 만들고 끝나는 문서가 아니라 **현재 Research와 Active Scope를 다음 Work로 연결하는 revisable control artifact**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Essence

- Consequential Work에는 Research에 근거한 Plan이 선행합니다.
- Review가 material gap을 찾으면 전체를 다시 만들지 않고 earliest stale prerequisite부터 필요한 Plan만 갱신합니다.
- Scope가 좁아지거나 확장되면 affected Plan coverage를 다시 검증합니다.
- Recursive child는 parent의 strict subset 안에서 필요한 좁은 Plan만 가집니다.
- Child가 돌아오면 그 결과가 parent Research, Scope 또는 Plan을 stale하게 만들었는지 확인합니다.
- 이미 유효한 Plan은 재사용하고 Loop를 채우기 위한 ceremony로 다시 만들지 않습니다.

## Preserve

Plan을 고도화할 때 **Research-before-Plan, delta replanning, Scope-aware planning, child-to-parent reintegration**을 고정된 one-shot 계획이나 전체 재작성으로 바꾸지 않습니다.
