---
name: progressive-help-pattern
description: >
  USE WHEN: designing optional progressive disclosure (--help) workflows or handling advanced option schemas in skills.
  EXCLUDES: core procedure definitions, CSV index routing, or script validation.
---

# Progressive Help Pattern Reference (`--help`)

## Goal

Define the architecture, anti-patterns, and appropriate use cases for `--help` in agent assets.

## Core Philosophy

`--help` is an **optional progressive disclosure mechanism**. It must never be required for normal execution.

> ⚠️ **Anti-Pattern: Forced Help Resolution**
> Requiring an agent or user to read `--help` before a skill or workflow can function correctly is an anti-pattern. Every asset must operate deterministically with its primary instructions (`SKILL.md` or workflow module). `--help` is strictly for optional, deep, or specialized context.

## When to Use `--help`

Implement `--help` (e.g., `workflows/--help.md` or `<action>--help.md`) strictly for:

1. **Deep Architectural & Operational Explanations**: Internal mechanisms, algorithm details, or design decisions that would otherwise bloat the main prompt.
2. **Edge Cases & Complex Scenarios**: Rare failure modes, complex parameter combinations, recovery steps, or edge-case handling.
3. **Advanced Option Schemas**: Complete JSON schemas, advanced configuration flags, or optional parameter references (`--config--help.md`, `--init--help.md`).
4. **Explicit Guidance Requests**: When a user or agent explicitly appends `--help` to request general documentation or usage clarification.

## Design Rules

1. **Self-Contained Primary Workflows**: Primary workflows must contain sufficient goals, procedures, and validation steps to run without opening `--help`.
2. **Zero Prompt Bloat**: Keep high-density secondary information in `--help` files so main prompt contexts remain lightweight.
3. **Explicit Triggers**: Map `--help` in `INDEX.csv` to explicit `--help` triggers (`use_when: "Explicit --help argument..."`).
