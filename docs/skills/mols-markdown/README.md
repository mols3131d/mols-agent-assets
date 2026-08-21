---
title: mols-markdown family
description: Markdown 표현·가독성·specialized projection·deterministic tooling Skill의 maintainer boundary
---

# mols-markdown

Markdown을 **표현 surface와 Markdown-specific maintenance surface**로 다루는 Skill family입니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-markdown-for-human` | 사람이 빠르게 읽고 이해할 수 있는 Markdown 표현과 가독성 |
| `mols-markdown-dashboard` | Markdown 기반 engineering dashboard와 상태 projection |
| `mols-markdown-tooling` | formatting, validation, frontmatter index 같은 deterministic Markdown mechanics |

## Structure

- Family는 runtime router가 아니라 shared maintainer boundary입니다.
- Human authoring, specialized artifact semantics, deterministic mechanics를 서로 다른 member responsibility로 유지합니다.
- Backend 이름(`script`, 특정 formatter/linter 이름)을 member identity로 사용하지 않습니다. Member 이름은 사용자가 요청하는 책임을 설명해야 합니다.
- Tooling member는 기존 repository-native tooling이 같은 behavior를 소유하면 그것을 우선하고 bundled utility를 강제하지 않습니다.
- 다른 member의 세부 규칙이나 backend 사용법을 family 문서에 복제하지 않습니다.

## Boundary

- 문서의 의미 구조, ADR/decision record, project document workflow는 `mols-document` family가 소유합니다.
- Mermaid diagram/chart의 시각적 의미와 type 선택은 `mols-mermaid` family가 소유합니다.
- 일반 reader-centered writing guidance를 Markdown-specific 규칙처럼 재소유하지 않습니다.
