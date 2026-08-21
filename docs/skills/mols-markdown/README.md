---
title: mols-markdown family
description: Markdown 표현·가독성·dashboard·script 관련 Skill이 공유하는 maintainer boundary
---

# mols-markdown

Markdown을 **표현 surface**로 다루는 Skill family입니다. 공유 원칙과 family-level decision은 이 capsule이 한 번만 소유하고, 각 Skill의 runtime behavior와 type-specific resource는 각 Skill package가 소유합니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-markdown-for-human` | 사람이 빠르게 읽고 이해할 수 있는 Markdown 표현과 가독성 |
| `mols-markdown-dashboard` | Markdown 기반 dashboard와 상태 projection |
| `mols-markdown-scripts` | Markdown 처리에 필요한 deterministic script 작업 |

## Boundary

- 문서의 의미 구조, ADR, project document template 자체는 `mols-document` family의 책임입니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family의 책임입니다.
- Markdown formatter, linter, renderer 같은 backend mechanics는 repository가 선택한 tooling을 사용하고 family Skill마다 복제하지 않습니다.
- 하나의 Skill에만 필요한 maintainer 지식은 기존 Skill-specific capsule에 둘 수 있습니다. 둘 이상의 member가 공유하게 되면 이 family capsule로 올립니다.
