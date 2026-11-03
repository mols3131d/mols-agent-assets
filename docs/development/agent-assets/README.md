---
description: Agent Asset 공통 설계·관리 지식과 Skill 전용 작성 규약 중 필요한 정본을 선택할 때 사용합니다.
---

# Agent Assets

Agent Asset의 설계·작성·관리 판단에 쓰는 재사용 지식을 둡니다. 이 저장소 자체의 개발 정책은 [Development](../README.md)가, 반복되는 해결 패턴은 [Patterns](../../../catalog/patterns/README.md)가 소유합니다.

## 문서 선택

| 판단할 문제 | 정본 |
| --- | --- |
| 자산을 추가·분리하거나 중복·context 비용을 줄일 때 | [Design Principles](design-principles.md) |
| Agent instruction의 행동·권한·중단 조건을 작성할 때 | [Instruction Design](instruction-design.md) |
| 자산 이름을 결정하거나 충돌을 피할 때 | [Naming](naming.md) |
| 신설·검증·제공·폐기, 유지보수 문서와 완료 기준을 선택할 때 | [Agent Asset Management](agent-asset-management.md) |
| Skill package·description·metadata나 공식 명세를 확인할 때 | [Skill-specific guidance](skills/) |

공통 자산 지식은 이 디렉터리가, Skill에만 적용되는 관행은 `skills/`가 소유합니다. 같은 의미를 중복 정의하지 않습니다. 외부 도구·명세의 공식 자료는 [Tooling References](../tooling/README.md), 외부 소비자의 사용법은 [Using This Repository](../../using-this-repository.md)를 따릅니다.
