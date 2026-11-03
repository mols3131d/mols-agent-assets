---
description: Agent Asset의 설계·워크플로·라이프사이클·유지보수 문서 배치와 Skill-specific 작성 규약 중 필요한 지식을 선택할 때 사용합니다.
---

# Agent Asset Design

`docs/development/agent-assets/`는 **Agent Asset의 설계, 변경 절차, 생애주기와 유지보수 문서 책임을 판단할 때 재사용하는 durable knowledge**를 소유합니다.

이 repository의 개발 규칙과 관행은 [Development](../README.md)가 소유하고, 반복되는 설계·운용 문제에 대한 reusable solution pattern은 [`catalog/patterns/`](../../../catalog/patterns/), tooling reference는 sibling인 [Tooling References](../tooling/README.md)가 소유합니다.

## Surfaces

| Path | Responsibility |
| --- | --- |
| [`common/`](common/) | 자산 유형 공통의 설계·instruction·naming, 작업 흐름·라이프사이클과 유지보수 문서 배치 |
| [`skills/`](skills/) | Skill-specific specification routing과 mols authoring convention |

유지보수 문서의 배치·책임은 [Agent Asset Management](common/agent-asset-management.md#유지보수-문서)을 따릅니다. 이 README는 child inventory를 복제하지 않습니다.

## Ownership

- Asset type에 종속되지 않는 설계, 작업 선택, 라이프사이클과 유지보수 문서의 durable knowledge는 `common/`이 소유합니다.
- Skill에만 적용되는 durable design meaning은 `skills/`가 소유합니다.
- 같은 의미를 `common/`과 `skills/`가 함께 소유하지 않습니다. 다른 surface에서 필요하면 authoritative owner를 link합니다.
- Agent Asset을 자주 설계할 때 쓰인다는 이유만으로 recurring solution을 이 surface가 소유하지 않습니다. 여러 repository나 harness에서 선택·조합·변형할 수 있는 해결 방식이면 [Patterns](../../../catalog/patterns/README.md)가 소유합니다.

## Boundary

- 여러 repository와 harness에서 재사용할 설계 pattern → [Patterns](../../../catalog/patterns/README.md)
- 이 repository를 개발·변경·검증하는 방법 → [Development](../README.md)
- 외부 tool과 specification의 공식 source routing → [Tooling References](../tooling/README.md)
- 이 library의 자산과 지식을 consumer가 사용하는 방법 → [Using This Repository](../../using-this-repository.md)

Agent Asset reference와 pattern의 경계는 **대상 파일 형식이 아니라 책임**으로 판단합니다. Asset 자체의 의미·authoring convention·authority routing은 이 surface에 남기고, 반복되는 문제에 대한 구성 방식이나 solution shape는 pattern으로 둡니다.
