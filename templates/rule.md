---
title: "Rule_T"
description: "Logic_Bound"
categories: ["requirements"]
draft: true
date: 2026-02-27
lastmod: ISO-8601
tags: ["rule", "rlm"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

Rule ::= {Context | Logic | Metric}

# LOGIC (RLM)

- **Context**: [Status_Active_When]
- **Directives**:
  - `D0`: [Mandatory_Boundary]
  - `D1`: [Forbidden_Action]
- **Metric**: {Accuracy | Compliance}

# REFERENCE DOCUMENTS

- [/docs/requirements/rule/rule.md](/docs/requirements/rule/rule.md) :: RLM
- [/docs/standards/agent.md](/docs/standards/agent.md) :: AOS

# CONSTRAINT

- Adhere: **REFERENCE DOCUMENTS**
