---
title: "Flow_T"
description: "Proc_Sync"
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

- **[SCAN]**: State_Detect {Delta | Env}
- **[PLAN]**: Logic_Synth {Reference_Docs | Goal}
- **[EXEC]**: Asset_Mutation {Precision | Atomicity}
- **[VERIFY]**: Logic_Check {Requirements | Standards}

# REFERENCE DOCUMENTS

- [/docs/requirements/workflow/workflow.md](/docs/requirements/workflow/workflow.md) :: WLM
- [/docs/standards/agent.md](/docs/standards/agent.md) :: AOS

# CONSTRAINT

- Adhere: **REFERENCE DOCUMENTS**
- Sync: Maintain DPS pair