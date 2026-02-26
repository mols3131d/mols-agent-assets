---
title: "Templates Root"
description: "Standard blueprints for consistent document and rule creation"
categories: ["templates"]
draft: false
date: 2026-02-27
lastmod: 2026-02-27
tags: ["templates", "governance"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

templates ::= {Markdown_Blueprints | Rule_Blueprints | Workflow_Blueprints}

# TOPOLOGY

- /templates/doc.md :: Standard knowledge/standard blueprint.
- /templates/rule.md :: Agentic rule (RLM) blueprint.
- /templates/workflow.md :: Agentic workflow (WLM) blueprint.

# CONSTRAINT

- Compliance: All new ACE assets MUST derive from these templates.
- Pairing: Adhere to DPS policy (/docs/standards/document.md).