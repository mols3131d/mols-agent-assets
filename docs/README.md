---
description: 문서 작업 전에 consumption, development, document, references, asset capsule 중 읽을 docs surface를 선택할 때 사용합니다.
---

# Documentation Layout

`docs/`는 문서의 책임과 portability에 따라 다음 surface로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`consumption.md`](consumption.md) | 이 repository가 관리하는 Agent Asset과 reusable knowledge를 외부 consumer가 발견하고 사용하는 방법 |
| [`development/`](development/) | 이 repository의 개발 규칙과 관행 |
| [`document/`](document/) | 이 repository의 문서 규칙과 관행 |
| [`references/`](references/) | 이 repository와 다른 repository에서 재사용할 Agent Asset 설계 지식, pattern, tooling/specification reference |
| `<asset-type>/<asset>/` | 한 자산에 대한 portable maintainer documentation capsule |

구체적인 문서 배치와 중복 경계는 [Documentation](document/README.md)이 소유합니다.
