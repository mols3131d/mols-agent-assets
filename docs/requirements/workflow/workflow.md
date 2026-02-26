---
title: Workflow Lifecycle Management Specification
description: Standards for engineering, optimizing, and evaluating agentic workflows
categories:
  - requirements
draft: false
date: 2026-02-27
lastmod: 2026-02-26T22:05:42.194Z
tags:
  - workflow-management
  - optimization
  - evaluation
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# Workflow Lifecycle Management (WLM)

Workflows in `mols-agent` are not static instructions; they are **executable algorithmic assets**. This document defines the standards for managing their entire lifecycle to ensure peak agent performance.

---

## 1. Quality Standards (What is a High-Value Workflow?)

A workflow must be engineered to meet these high-density criteria:

- **Executability**: Every step must be clear enough for an agent to run without human intervention.
- **Structural Integrity**: Must follow the `[SCAN] -> [PLAN] -> [EXEC] -> [VERIFY]` sequence or a specialized variant.
- **Logic Density**: Minimize prose; maximize symbolic directives and structural markers.
- **DRY (Don't Repeat Yourself)**: Leverage existing rules (`@rule`) and sub-workflows to avoid logic duplication.
- **Resilience**: Include basic error-handling or verification gates within the steps.

## 2. Engineering & Design (Creation)

1.  **Scope Definition**: Define the exact input, process, and expected output (Artifact).
2.  **Modular Design**: Break complex tasks into atomic, reusable steps.
3.  **Symbolic Mapping**: Use standard headers to signal task types:
    *   **`[SCAN]`**: Environment and state reconnaissance.
    *   **`[PLAN]`**: Strategy synthesis and mapping.
    *   **`[EXEC]`**: Actual mutation or creation of assets.
    *   **`[VERIFY]`**: Quality assurance and logic checking.
4.  **Reference Integration**: Explicitly link to `.agents/rules/` to enforce policy during execution.

## 3. Optimization Loop (Improvement)

Workflows must evolve based on execution telemetry and bottlenecks.

- **Friction Reduction**: Identify steps where agents frequently stall or ask for clarification, then simplify.
- **Precision Tuning**: Sharpen the language of `[PLAN]` and `[VERIFY]` to reduce variance in output quality.
- **Automation (Turbo)**: Annotate steps with `// turbo` only when they are highly stable and safe for auto-execution.
- **Pattern Extraction**: If multiple workflows share a similar sequence, extract that sequence into a "Core Workflow Asset".

## 4. Evaluation Criteria (Success Metrics)

- **Success Rate**: Frequency of "First-Time Success" without manual correction.
- **Cycle Time**: Efficiency of task completion from `[SCAN]` to `[REPORT]`.
- **Token Efficiency**: Achieving the goal with the minimal necessary instructions.
- **Transferability**: Ability for the workflow to be used across different sub-tasks within the same category.

---

# SYNOPSIS

WLM ::= {Standardization | Execution | Optimization | Assessment}

# PROTOCOL

- **Workflow_as_Code**: Treat workflows like source code—versioned, tested, and refactored.
- **Feedback_Driven**: Improvement is mandatory if execution data shows inefficiency.
