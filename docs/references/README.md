---
description: 이 repository와 다른 repository에서 반복해서 참고·적용할 reusable knowledge를 찾고 선택할 때 사용하는 entrypoint입니다.
---

# References

`docs/references/`는 **이 repository와 다른 repository에서 재사용할 가치가 있는 knowledge library**입니다.

Reference는 외부 문서 링크 모음만을 의미하지 않습니다. Agent Asset 설계 지식, reusable pattern, tooling과 specification의 authority routing처럼 여러 context에서 반복해서 설명·구축하기 아까운 지식을 이곳에서 관리합니다.

## Surfaces

| Path | Responsibility |
| --- | --- |
| [`agent-assets/`](agent-assets/) | Agent Asset 자체의 설계 원칙, instruction authoring, naming과 Skill-specific knowledge |
| [`patterns/`](patterns/) | 여러 repository와 harness에서 선택·조합·변형할 수 있는 reusable pattern capsule |
| [`tooling/`](tooling/) | Rulesync, Promptfoo 등 외부 tooling과 specification의 current authority routing 및 필요한 integration knowledge |

## Boundary

- 이 repository에만 적용되는 개발·운영 규칙은 [`development/`](../development/) 또는 [`document/`](../document/) 같은 project-local owner가 소유합니다.
- 개별 asset 또는 family의 maintainer-only knowledge는 `docs/<asset-type>/<owner>/` capsule이 소유합니다.
- Runtime에서 직접 소비하는 Agent Asset source는 `src/`가 소유합니다.
- 이 library의 자산과 reference를 consumer가 가져다 쓰는 방법은 [Consumption](../consumption.md)이 소유합니다.

Reference에 있다는 이유만으로 downstream project의 mandatory policy가 되지는 않습니다. Consumer는 필요한 reference를 명시적으로 채택하거나 자신의 local authority에서 route합니다.

같은 responsibility를 references 내부의 둘 이상의 owner가 중복 소유하지 않습니다. 구체적인 중복 경계는 [Documentation DRY policy](../document/dry.md)를 따릅니다.
