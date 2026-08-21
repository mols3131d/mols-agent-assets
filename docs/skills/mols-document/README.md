---
title: mols-document family
description: 구조화된 project document의 의미 구조와 책임을 관리하는 Skill family
---

# mols-document

문서의 **의미 구조와 document-level responsibility**를 다루는 Skill family입니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-document-decisions` | 기술·프로젝트 의사결정 기록과 lightweight decision workflow |

## Boundary

- `mols-document-decisions`는 decision record만 소유하며 일반 project document authoring까지 확장하지 않습니다.
- Consumer repository에 accepted ADR 또는 decision format이 있으면 그 local owner를 우선합니다.
- Markdown 표현·가독성·dashboard·deterministic maintenance는 `mols-markdown` family가 소유합니다.
- Mermaid diagram과 chart는 `mols-mermaid` family가 소유합니다.
- 일반 reader-centered prose와 audience 판단은 active writing capability가 소유합니다.
