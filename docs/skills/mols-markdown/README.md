---
title: mols-markdown family
description: Markdown 표현·가독성·dashboard·script 관련 Skill의 maintainer boundary
---

# mols-markdown

Markdown을 **표현 surface**로 다루는 Skill family입니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-markdown-for-human` | 사람이 빠르게 읽고 이해할 수 있는 Markdown 표현과 가독성 |
| `mols-markdown-dashboard` | Markdown 기반 dashboard와 상태 projection |
| `mols-markdown-scripts` | Markdown quality check, validation, formatting과 deterministic generation |

## Boundary

- 문서의 의미 구조, ADR, project document template 자체는 `mols-document` family가 소유합니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family가 소유합니다.
- Markdown formatter, linter, parser와 renderer 같은 backend mechanics는 repository가 선택한 tooling을 사용하고 family Skill마다 복제하지 않습니다.
