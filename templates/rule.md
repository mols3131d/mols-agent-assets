---
title: "Rule-T"
description: "Logic-Bound"
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

- **Context-Trigger**: [Activate-When-Condition]
- **Directives**:
  - `D0`: [Mandatory-Boundary]
  - `D1`: [Forbidden-Action]
- **Metric**: {Accuracy | Compliance}

# REFERENCE DOCUMENTS

- [Rule-Lifecycle-Management](/docs/requirements/rule/rule.md)
- [Agent-Operational-Standard](/docs/standards/agent.md)

# CONSTRAINT

- Adhere: **REFERENCE DOCUMENTS**
