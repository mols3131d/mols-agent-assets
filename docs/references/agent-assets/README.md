---
description: Agent Asset 설계 원칙, 공통 지식과 Skill 관행 중 어떤 documentation surface를 볼지 선택할 때 사용합니다.
---

# Agent Asset Design

`docs/references/agent-assets/`는 **Agent Asset 자체를 설계하고 작성할 때 재사용하는 지식**을 소유합니다.

이 repository의 작업 절차는 `docs/development/`가 소유하고, 범용 reusable pattern과 tooling reference는 같은 `docs/references/` library의 sibling surface가 소유합니다.

## Surfaces

| Path | Responsibility |
| --- | --- |
| [`common/`](common/) | asset type에 종속되지 않는 설계 원칙, instruction authoring, naming과 compatibility |
| [`skills/`](skills/) | Skill-specific specification routing, authoring convention과 reusable template knowledge |

이 README는 child inventory를 복제하지 않습니다. 구체적인 지식은 해당 문서가 소유합니다.

## Ownership

- Asset type에 종속되지 않는 durable design meaning은 `common/`이 소유합니다.
- Skill에만 적용되는 durable design meaning은 `skills/`가 소유합니다.
- 같은 의미를 `common/`과 `skills/`가 함께 소유하지 않습니다. 다른 surface에서 필요하면 authoritative owner를 link합니다.

## Boundary

- 여러 repository와 harness에서 재사용할 설계 pattern → [Patterns](../patterns/README.md)
- 이 repository를 개발·변경·검증하는 방법 → [Development](../../development/README.md)
- reusable knowledge library의 공통 contract → [References](../README.md)
- 이 library의 자산과 지식을 consumer가 사용하는 방법 → [Consumption](../../consumption.md)
