---
title: mols-markdown family
description: mols-markdown family에서 사람이 읽는 Markdown, dashboard, deterministic maintenance 중 어느 Skill이 책임지는지 선택하거나 family boundary를 유지보수할 때 사용하는 entrypoint입니다.
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
- Markdown maintenance에서 repository-native equivalent가 없으면 portable fallback backend로 rumdl을 사용합니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family가 소유합니다.
