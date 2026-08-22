---
description: 문서 작업 전에 top-level docs surface와 nested directory의 ownership boundary를 선택할 때 사용합니다.
---

# Documentation Layout

`docs/`는 문서의 책임과 portability에 따라 다음 top-level surface로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`consumption.md`](consumption.md) | 이 repository가 관리하는 Agent Asset과 reusable knowledge를 외부 consumer가 발견하고 사용하는 방법 |
| [`language.md`](language.md) | repository communication과 Agent Asset 역할별 language policy |
| [`development/`](development/) | 이 repository의 개발 규칙과 관행 |
| [`document/`](document/) | 이 repository 전체에 적용되는 문서 원칙과 관행 |
| [`references/`](references/) | 이 repository와 다른 repository에서 재사용할 Agent Asset 설계 지식, pattern, tooling/specification reference |
| `<asset-type>/<asset>/` | 한 자산에 대한 portable maintainer documentation capsule |

## Nested Directory Ownership

`docs/`의 nesting은 고정된 directory taxonomy가 아니라 **필요한 책임 경계를 더 좁은 local owner에게 위임할 수 있는 계층**입니다. Directory depth 자체가 README나 별도 documentation owner를 요구하지 않습니다.

- 이 README는 top-level surface routing과 nested ownership model만 소유하며 descendant의 내부 구조를 직접 소유하지 않습니다.
- Child surface 사이의 responsibility boundary를 filesystem만으로 복구하기 어렵다면, 그 boundary를 설명할 가장 가까운 parent local owner가 이유와 구분을 소유합니다.
- Child에 독립적인 local contract나 navigation responsibility가 실제로 생기면 해당 child의 local owner가 자기 subtree 범위만 소유합니다.
- Ancestor는 deeper child의 세부 구조나 쉽게 재생성되는 inventory를 복제하지 않습니다. Local owner도 필요하지 않은 routing table이나 child 목록을 만들지 않습니다.
- Repository-wide documentation principle은 [`document/`](document/)가 계속 소유합니다. Local owner는 자기 scope를 구체화할 수 있지만 상위 공통 원칙을 중복 소유하거나 재정의하지 않습니다.
- 이 ownership model은 domain별 folder, document bundle, asset capsule 또는 특정 nesting depth를 요구하지 않습니다. 그런 구조는 해당 책임에서 실제로 필요할 때만 local하게 정의합니다.

Directory-level documentation이 필요한 조건과 repository-wide 배치 원칙은 [Documentation Ownership](document/ownership.md)이 소유합니다. 특정 directory나 surface에만 적용되는 contract와 세부 규칙은 가장 가까운 유효한 local owner가 소유합니다.
