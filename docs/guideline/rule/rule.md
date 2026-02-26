---
title: Rule Lifecycle Management Guideline
description: Standards for creating, improving, and evaluating agentic rules
categories:
  - guideline
draft: false
date: 2026-02-27
lastmod: 2026-02-26T21:34:41.203Z
tags:
  - rule-management
  - lifecycle
  - evaluation
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# Rule Lifecycle Management (RLM)

This document defines the professional standards for managing the entire lifecycle of rules within the `mols-agent` ecosystem. We do not just store rules; we engineer their evolution.

---

## 1. Definition of "Elite Rules" (Quality Standards)

A rule is considered high-quality only if it satisfies the following criteria:

- **Logic Density**: Maximum information conveyed with minimum tokens. Use symbols and structured definitions.
- **Actionability**: Must provide a clear directive or constraint that an agent can immediately follow.
- **Atomicity**: One rule should address one logical concept or boundary to avoid side effects during improvement.
- **Consistency**: Must align with `.agents/rules/constitution.md` and other root-level policies.
- **Evolvability**: Structured to allow versioning and incremental updates without breaking the core intent.

## 2. Creation Protocol (Rule Engineering)

When initializing a new rule:

1.  **Requirement Analysis**: Identify the gap in the current rule set. Avoid redundancy.
2.  **Drafting (TAS Approach)**:
    *   **Thesis**: Propose the initial rule structure.
    *   **Antithesis**: Challenge the rule with edge cases and potential agent failures.
    *   **Synthesis**: Refine the rule to balance flexibility and strictness.
3.  **Validation**: Test the rule against specific scenarios in `studio/`.

## 3. Improvement & Evolution (The Loop)

Rules are living assets. They must be improved based on execution logs and failure analysis.

- **Refinement**: Clarify ambiguous language found during agent tasks.
- **Optimization**: Increase logic density by replacing verbose descriptions with symbols (::=, |, {}).
- **Integration**: Merge related sub-rules into a unified framework if patterns emerge.
- **Versioning**: Reflect updates in `lastmod` and documentation history.

## 4. Evaluation Metrics (QA)

How we measure the success of a rule:

- **Adherence Rate**: Percentage of times the agent correctly applied the rule in complex tasks.
- **Hallucination Reduction**: Did the rule successfully prevent a known failure mode?
- **Logic Clarity**: Can another agent (or human) reproduce the intended behavior without ambiguity?
- **Stability**: Does the rule remain valid across different task types and LLM models?

---

# SYNOPSIS

RLM ::= {Design | Creation | Improvement | Evaluation}

# PROTOCOL

- **Management_Over_Storage**: Every rule must be active, evaluated, and improved.
- **Asset_Value**: A rule's value is determined by its impact on execution quality.
