---
title: "마크다운 관행"
type: "doc"
description: "MOLS Agent의 마크다운 사용 규칙"
created: 2026-02-27
updated: 2026-02-27
tags: ["convention", "markdown"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 마크다운 관행

- 마크다운 작성 관행을 다루는 문서.

## Frontmatter

```yaml
---
title: "Title"
type: "doc" # 문서의 종류 ("", "doc", "agent-rule", "agent-workflow")
description: "문서의 설명" # 250자 이내
created: YYYY-MM-DD # 문서의 생성일
updated: YYYY-MM-DD # 문서의 수정일
tags: ["tag1", "tag2", ...]
# === agent 관련 ===
agent-readable: true # bool, 에이전트가 읽을 수 있는지 여부
# agent-readable이 true일 때만 의미가 있음
agent-editable: false # bool, 에이전트가 수정할 수 있는지 여부
agent-moveable: false # bool, 에이전트가 이동할 수 있는지 여부
agent-deletable: false # bool, 에이전트가 삭제할 수 있는지 여부
agent-friendly: false # bool, 문서가 에이전트 친화적인지 여부
---
```
