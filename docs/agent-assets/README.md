---
description: Agent Asset 설계 원칙, 공통 지식과 Skill 관행 중 어떤 documentation surface를 볼지 선택할 때 사용합니다.
---

# Agent Asset Design

`docs/agent-assets/`는 **Agent Asset 자체를 설계하고 작성할 때 재사용하는 지식**을 소유합니다.

이 repository의 작업 절차는 `development/`, 범용 reusable pattern은 `patterns/`, 외부 specification과 tooling의 current authority routing은 `references/`가 소유합니다.

## Surfaces

| Path | Responsibility |
| --- | --- |
| [`common/`](common/) | asset type에 종속되지 않는 설계 원칙, instruction authoring, naming과 compatibility |
| [`skills/`](skills/) | Skill-specific specification routing, authoring convention과 reusable template knowledge |

이 README는 child inventory를 복제하지 않습니다. 구체적인 지식은 해당 문서가 소유합니다.

## Boundary

- 여러 repository와 harness에서 재사용할 설계 pattern → [Patterns](../patterns/README.md)
- 이 repository를 개발·변경·검증하는 방법 → [Development](../development/README.md)
- 외부 tool과 specification의 authoritative source routing → [References](../references/README.md)
- 이 library의 자산을 consumer가 가져다 쓰는 방법 → [Consumption](../consumption.md)
