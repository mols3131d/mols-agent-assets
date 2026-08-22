---
description: 문서 작업 전에 consumption, development, document, references, asset capsule 중 읽을 docs surface를 선택할 때 사용합니다.
---

# Documentation Layout

`docs/`는 문서의 책임과 portability에 따라 다음 surface로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`consumption.md`](consumption.md) | 이 repository가 관리하는 Agent Asset과 reusable knowledge를 외부 consumer가 발견하고 사용하는 방법 |
| [`development/`](development/) | 이 repository의 개발 규칙과 관행 |
| [`document/`](document/) | 이 repository 전체에 적용되는 문서 원칙과 관행 |
| [`references/`](references/) | 이 repository와 다른 repository에서 재사용할 Agent Asset 설계 지식, pattern, tooling/specification reference |
| `<asset-type>/<asset>/` | 한 자산에 대한 portable maintainer documentation capsule |

Repository-wide 문서 배치와 ownership 원칙은 [Documentation](document/README.md)이 소유합니다. 특정 directory나 surface에만 적용되는 contract와 세부 규칙은 해당 directory의 `README.md` 또는 local document가 소유합니다.
