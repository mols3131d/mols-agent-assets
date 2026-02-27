---
title: Markdown Standards
description: Technical specification for Markdown assets in MOLS Agent
categories:
  - standards
draft: false
date: 2026-02-26
lastmod: 2026-02-27T16:50:27.315Z
tags:
  - markdown
  - standards
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# OVERVIEW

Markdown_Spec ::= {Frontmatter_Schema | Linking_Protocol | Dual_Target_Layout}

# STANDARDS

## 1. Frontmatter (Hugo-Compatible)

Every document MUST include a YAML frontmatter for governance and metadata.

```yaml
---
title: "Title"
description: "Brief summary"
categories: ["standard", "requirement"]
draft: false
date: YYYY-MM-DD
lastmod: ISO-8601-Timestamp
tags: ["tag1"]
id: "prefix-001" # Optional. e.g., adr-001, rfc-001
agent-readable: true|false
agent-editable: true|false
agent-moveable: true|false
agent-deletable: true|false
agent-friendly: true|false
---
```

## 2. Agent Control Fields

- **`agent-readable`**: Visibility to the LLM.
- **`agent-editable`**: Permission for the LLM to mutate content.
- **`agent-moveable`**: Permission for location change.
- **`agent-deletable`**: Permission for removal (Soft Delete via AOS).
- **`agent-friendly`**: Optimized structure (Logic-dense).

## 3. Linking Protocol

- **Root-Relative Only**: Links MUST start with `/` referencing the workspace root.
- **Format**: `[Label]( /path/to/asset.md )`

# CONSTRAINT

- **Pairing Required**: Adhere to DPS (`/docs/standards/document.md`).
