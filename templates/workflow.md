---
title: "Workflow Name"
description: "Brief summary of the target artifact and procedure"
categories:
  - requirements
draft: true
date: 2026-02-27
lastmod: 2026-02-27
tags:
  - workflow
  - wlm
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

Workflow_Process ::= {SCAN | PLAN | EXEC | VERIFY}

# STEPS (WLM)

## 1. [SCAN]
- Environment and state reconnaissance. Identify the current delta.

## 2. [PLAN]
- Strategy synthesis. Explicitly link to @rules and requirements.

## 3. [EXEC]
- Actual mutation or creation of assets. Focus on precision.

## 4. [VERIFY]
- Quality assurance. Check against requirements and standards.

# REFERENCE DOCUMENTS

- [/docs/requirements/workflow/workflow.md](/docs/requirements/workflow/workflow.md) :: Workflow Lifecycle Management (WLM)
- [/docs/standards/agent.md](/docs/standards/agent.md) :: Agent Operational Standard (AOS)

# CONSTRAINT

- **Protocol**: Mandatorily follow the WLM protocol linked in **REFERENCE DOCUMENTS**.
- **Turbo**: Use `// turbo` sparingly only for safe, routine steps.
