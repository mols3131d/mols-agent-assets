---
title: Rule Management Specification
description: Lifecycle control plane for agentic rules
categories:
  - requirements
draft: false
date: 2026-02-27
lastmod: 2026-02-27T11:50:12.686Z
tags:
  - rule-management
  - lifecycle
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# OVERVIEW

rule_management ::= {Lifecycle_Control | Quality_Engineering | Evaluation_Logic}

# PROTOCOL

- Beyond_Archive: We manage the evolution of rules, not just their collection.
- Impact_Driven: Success is defined by the measurable improvement of agent behavior.

# TOPOLOGY

- [Rule Lifecycle Specification](/docs/requirements/rule/rule.md) :: The core standard for RLM.

# CONSTRAINT

- Core_Logic: Follow `{Creation | Improvement | Evaluation}` cycle.
- Adhere: .agents/rules/
