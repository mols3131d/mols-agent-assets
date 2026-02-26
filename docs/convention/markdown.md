---
title: 마크다운 관행
description: MOLS Agent의 마크다운 사용 규칙
categories:
    - convention
draft: false
date: 2026-02-26
lastmod: 2026-02-26T18:23:24.135Z
tags:
    - markdown
    - convention
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 마크다운 관행

- 마크다운 작성 관행을 다루는 문서.

## Frontmatter

- Hugo의 Frontmatter를 따름.
- 거기에, agent관련 필드를 추가.

```yaml
---
title: "Title"
description: "문서의 설명"
categories: ["category", ...]
draft: false
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
tags: ["tag1", "tag2", ...]
agent-readable: true
agent-editable: false
agent-moveable: false
agent-deletable: false
agent-friendly: false
---
```
