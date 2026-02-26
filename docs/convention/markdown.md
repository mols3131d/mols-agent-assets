---
title: 마크다운 관행
description: MOLS Agent의 마크다운 사용 규칙
categories:
    - convention
draft: false
date: 2026-02-26
lastmod: 2026-02-26T17:59:54.187Z
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
description: "문서의 설명" # 250자 이내
categories: ["category", ...]
draft: false # bool
date: YYYY-MM-DD # date. 문서의 생성일
lastmod: YYYY-MM-DD # date. 문서의 수정일
tags: ["tag1", "tag2", ...]
# === agent 관련 ===
agent-readable: true # bool. 에이전트가 읽을 수 있는지 여부
# === === agent-readable이 true일 때만 의미가 있음 === ===
agent-editable: false # bool. 에이전트가 수정할 수 있는지 여부
agent-moveable: false # bool. 에이전트가 이동할 수 있는지 여부
agent-deletable: false # bool. 에이전트가 삭제할 수 있는지 여부
agent-friendly: false # bool. 문서가 에이전트 친화적인지 여부
# ===
---
```
