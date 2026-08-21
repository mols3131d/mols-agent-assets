---
title: mols-document family
description: 구조화된 project document의 의미 구조와 책임을 관리하는 Skill family
---

# mols-document

문서의 **의미 구조와 document-level responsibility**를 다루는 Skill family입니다. 표현 형식이나 시각화 문법을 다시 소유하지 않습니다.

## Members

| Skill | 책임 |
| --- | --- |
| `mols-document-decisions` | 기술·프로젝트 의사결정 기록과 lightweight decision workflow |

## Structure

- Family는 shared maintainer boundary이지 runtime router가 아닙니다.
- 각 member는 독립 trigger와 명확한 document responsibility를 가져야 합니다.
- `studio`, generic router, workflow index 같은 중간 framework는 실제로 복수의 독립 workflow를 조정해야 할 때만 둡니다.
- 새로운 document member는 기존 member나 프로젝트 고유 문서 owner로 해결할 수 없을 때만 추가합니다.
- Consumer repository에 이미 accepted document format이나 workflow가 있으면 그것을 우선하고 portable member는 local delta만 제공합니다.

## Boundary

- Markdown 표현·가독성·dashboard·deterministic Markdown tooling은 `mols-markdown` family가 소유합니다.
- Mermaid diagram과 chart는 `mols-mermaid` family가 소유합니다.
- 일반 reader-centered prose와 audience 판단을 document family에 복제하지 않습니다.
