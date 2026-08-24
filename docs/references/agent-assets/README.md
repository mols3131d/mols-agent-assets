---
description: Agent Asset 자체의 공통 설계 의미와 Skill-specific specification·authoring convention 중 어떤 reference를 볼지 선택할 때 사용합니다.
---

# Agent Asset Design

`docs/references/agent-assets/`는 **Agent Asset 자체를 설계하고 작성할 때 재사용하는 durable design knowledge**를 소유합니다.

이 repository의 작업 절차는 `docs/development/`가 소유하고, 반복되는 설계·운용 문제에 대한 reusable solution pattern과 tooling reference는 같은 `docs/references/` library의 sibling surface가 소유합니다.

## Surfaces

| Path | Responsibility |
| --- | --- |
| [`common/`](common/) | asset type에 종속되지 않는 설계 원칙, instruction authoring과 naming |
| [`skills/`](skills/) | Skill-specific specification routing과 mols authoring convention |

이 README는 child inventory를 복제하지 않습니다. 구체적인 지식은 해당 문서가 소유합니다.

## Ownership

- Asset type에 종속되지 않는 durable design meaning은 `common/`이 소유합니다.
- Skill에만 적용되는 durable design meaning은 `skills/`가 소유합니다.
- 같은 의미를 `common/`과 `skills/`가 함께 소유하지 않습니다. 다른 surface에서 필요하면 authoritative owner를 link합니다.
- Agent Asset을 자주 설계할 때 쓰인다는 이유만으로 recurring solution을 이 surface가 소유하지 않습니다. 여러 repository나 harness에서 선택·조합·변형할 수 있는 해결 방식이면 [Patterns](../patterns/README.md)가 소유합니다.

## Boundary

- 여러 repository와 harness에서 재사용할 설계 pattern → [Patterns](../patterns/README.md)
- 이 repository를 개발·변경·검증하는 방법 → [Development](../../development/README.md)
- reusable knowledge library의 공통 contract → [References](../README.md)
- 이 library의 자산과 지식을 consumer가 사용하는 방법 → [Using This Repository](../../using-this-repository.md)

Agent Asset reference와 pattern의 경계는 **대상 파일 형식이 아니라 책임**으로 판단합니다. Asset 자체의 의미·authoring convention·authority routing은 이 surface에 남기고, 반복되는 문제에 대한 구성 방식이나 solution shape는 pattern으로 둡니다.
