---
name: section
description: >
  USE WHEN: understanding essential roles, semantic purpose, and structural concepts of agent asset sections and headers.
  EXCLUDES: directory structure specifications, naming conventions, or trigger description details.
---

# Agent Asset Structural Concepts & Essential Roles

Markdown headers in an agent asset are semantic boundaries that guide model reasoning and execution flow. Header names are flexible as long as their intent and purpose remain clear.

## Essential Roles & Concepts

### 1. Scope & Intent Boundary

- **Role**: Define core responsibility and prevent scope creep.
- **Intent**: Establish what the asset must achieve and explicit out-of-scope areas.
- **Header Examples**: `Goal`, `Non-Goal`, `Purpose`, `Overview`, `Scope`

### 2. Activation & Termination Control

- **Role**: Control when the asset starts, passes control, or halts execution.
- **Intent**: Prevent unnecessary token usage, wrong invocations, or silent failures on negative conditions.
- **Header Examples**: `When to Use`, `When NOT to Use`, `When to STOP`, `Triggers`, `Exit Criteria`

### 3. Execution Guardrails & Rules

- **Role**: Provide positive directives and absolute negative constraints.
- **Intent**: Direct model behavior deterministically and enforce strict safety boundaries.
- **Header Examples**: `Instructions`, `Constraints`, `Rules`, `Guiding Principles`

### 4. Deterministic Workflow Execution

- **Role**: Guide multi-step procedures, environment state, and verification steps.
- **Intent**: Break down execution into clear context, ordered steps, and outcome checks.
- **Header Examples**: `Workflow`, `Context` (`Arguments`/`Parameters`), `Procedure` / `Steps`, `Validation` / `Checks`

### 5. Context & Resource References

- **Role**: Link to external knowledge, sub-workflows, or reference files loaded on demand.
- **Intent**: Keep prompt lightweight by deferring deep context to dedicated reference files.
- **Header Examples**: `References`, `Resources`, `Dependencies`

## Design Heuristics

- Header names can be flexibly adapted (e.g., `Procedure` vs `Steps`, `Constraints` vs `Rules`) as long as semantic meaning is preserved.
- Omit headers that add no actionable value for the target task. Keep only essential structural boundaries.
