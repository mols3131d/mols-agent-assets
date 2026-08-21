---
title: mols-mermaid family
description: Mermaid diagram과 chart Skill이 공유하는 maintainer boundary
---

# mols-mermaid

Mermaid 기반 시각화를 다루는 Skill family입니다. **관계·절차·구조를 설명하는 diagram**과 **수치 구조를 표현하는 chart**를 서로 다른 discoverable 책임으로 유지합니다.

## Members

| Skill | 중심 질문 |
| --- | --- |
| `mols-mermaid-diagram` | 무엇이 어떻게 연결되고, 진행되고, 상태가 바뀌는가? |
| `mols-mermaid-chart` | 값이 얼마나 크고, 변하고, 구성되고, 이동하는가? |

## Routing Boundary

- 관계, procedure, branching, message order, lifecycle, architecture, schema, unweighted hierarchy가 핵심이면 `mols-mermaid-diagram`을 사용합니다.
- magnitude, trend, proportion, quantified flow, weighted hierarchy, numeric profile이 핵심이면 `mols-mermaid-chart`를 사용합니다.
- 하나의 요청에 두 질문이 모두 있으면 하나의 Skill로 억지 통합하지 않고 필요한 표현을 분리합니다.
- Markdown 문서 전체의 표현과 dashboard composition은 `mols-markdown` family가 소유합니다.

## Documentation Boundary

Mermaid 전체에 공통인 durable maintainer 지식만 이 family capsule이 소유합니다. Type 선택, syntax, examples, renderer verification처럼 runtime에 필요한 세부 지식은 `mols-mermaid-diagram`과 `mols-mermaid-chart` package 안에서 각각 소유합니다.
