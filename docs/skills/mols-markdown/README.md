---
title: mols-markdown family
description: mols-markdown family에서 사람이 읽는 Markdown, dashboard, deterministic maintenance 중 어느 Skill이 책임지는지 선택하거나 family boundary를 유지보수할 때 사용하는 entrypoint입니다.
---

# mols-markdown

Markdown을 **표현 surface와 Markdown-specific maintenance surface**로 다루는 Skill family입니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-documentation` | 사람이 읽고 유지보수하는 문서의 구조·가독성과 Markdown 표현 |
| `mols-markdown-dashboard` | Markdown 기반 engineering dashboard와 상태 projection |
| `mols-markdown-maintenance` | formatting, validation, frontmatter index 같은 deterministic Markdown maintenance |

## Boundary

- 일반 문서 구조·가독성과 Markdown 표현은 `mols-documentation`이 소유합니다.
- engineering dashboard의 집계·gap·projection semantics는 `mols-markdown-dashboard`가 소유합니다.
- 반복 가능한 formatting, validation, index mechanics는 `mols-markdown-maintenance`가 소유합니다.
- Markdown maintenance에서 repository-native equivalent가 없으면 portable fallback backend로 rumdl을 사용합니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family가 소유합니다.
