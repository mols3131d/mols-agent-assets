---
title: mols-document family
description: 구조화된 project document와 template 관련 Skill이 공유하는 maintainer boundary
---

# mols-document

문서의 **의미 구조와 document workflow**를 다루는 Skill family입니다. Markdown이라는 표현 형식 자체와 시각화 문법은 다른 family에 맡깁니다.

## Members

현재 discoverable member는 `mols-documents-studio`입니다. 기존 identifier는 이번 family-documentation 변경에서 호환성을 위해 유지하며, 새 member는 실제 책임이 분리될 때만 추가합니다.

## Boundary

- ADR, structured project document, document template과 document-level workflow는 이 family가 소유합니다.
- Markdown 표현·가독성·dashboard·Markdown script는 `mols-markdown` family가 소유합니다.
- Mermaid diagram과 chart는 `mols-mermaid` family가 소유합니다.
- 공유 maintainer 지식은 이 family capsule에 한 번만 두고, runtime-required template/reference/workflow는 해당 Skill package에 둡니다.
