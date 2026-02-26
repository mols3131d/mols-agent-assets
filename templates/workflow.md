---
title: "Flow-T"
description: "Proc-Sync"
categories: ["requirements"]
draft: true
date: 2026-02-27
lastmod: ISO-8601
tags: ["workflow", "wlm"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

Flow ::= SCAN -> PLAN -> EXEC -> VERIFY

# FLOW (WLM)

- **[SCAN]**: State-Detect {Delta | Env}
- **[PLAN]**: Logic-Synth {Reference-Docs | Goal}
- **[EXEC]**: Asset-Mutation {Precision | Atomicity}
- **[VERIFY]**: Logic-Check {Requirements | Standards}

# REFERENCE DOCUMENTS

- [Workflow-Lifecycle-Management](/docs/requirements/workflow/workflow.md)
- [Agent-Operational-Standard](/docs/standards/agent.md)

# CONSTRAINT

- Adhere: **REFERENCE DOCUMENTS**
- Sync: Maintain DPS pair