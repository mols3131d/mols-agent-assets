---
title: mols-markdown family
description: Markdown 표현·specialized projection·deterministic maintenance Skill의 maintainer boundary
---

# mols-markdown

Markdown을 **표현 surface와 Markdown-specific maintenance surface**로 다루는 Skill family입니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-markdown-for-human` | 사람이 빠르게 읽고 이해할 수 있는 Markdown 표현과 가독성 |
| `mols-markdown-dashboard` | Markdown 기반 engineering dashboard와 상태 projection |
| `mols-markdown-maintenance` | formatting, validation, frontmatter index 같은 deterministic Markdown maintenance |

## Boundary

- 일반 Markdown 표현과 독자 가독성은 `mols-markdown-for-human`이 소유합니다.
- engineering dashboard의 집계·gap·projection semantics는 `mols-markdown-dashboard`가 소유합니다.
- 반복 가능한 formatting, validation, index mechanics는 `mols-markdown-maintenance`가 소유합니다.
- 문서의 의미 구조와 decision record는 `mols-document` family가 소유합니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family가 소유합니다.
