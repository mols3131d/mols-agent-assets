---
title: mols-document family
description: 구조화된 project document와 template 관련 Skill의 maintainer boundary
---

# mols-document

문서의 **의미 구조와 document workflow**를 다루는 Skill family입니다. Markdown이라는 표현 형식 자체와 시각화 문법은 다른 family에 맡깁니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-documents-studio` | ADR, structured project document, document template과 document-level workflow |

## Boundary

- Markdown 표현·가독성·dashboard·Markdown script는 `mols-markdown` family가 소유합니다.
- Mermaid diagram과 chart는 `mols-mermaid` family가 소유합니다.
