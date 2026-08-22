---
description: 문서 작업 전에 consumption, agent-assets, patterns, development, document, references, asset capsule 중 읽을 docs surface를 선택할 때 사용합니다.
---

# Documentation Layout

`docs/`는 문서의 책임과 portability에 따라 다음 surface로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`consumption.md`](consumption.md) | 이 repository가 관리하는 Agent Asset을 외부 consumer가 발견하고 가져다 쓰는 방법 |
| [`agent-assets/`](agent-assets/) | Agent Asset 자체를 설계·작성할 때 재사용하는 공통 지식과 Skill 관행 |
| [`patterns/`](patterns/) | 여러 repository와 harness에서 재사용할 수 있는 design pattern capsule |
| [`development/`](development/) | 이 repository의 개발 규칙과 관행 |
| [`document/`](document/) | 이 repository의 문서 규칙과 관행 |
| [`references/`](references/) | 외부 specification과 tooling의 authoritative source routing |
| `<asset-type>/<asset>/` | 한 자산에 대한 portable maintainer documentation capsule |

구체적인 문서 배치와 중복 경계는 [Documentation](document/README.md)이 소유합니다.
