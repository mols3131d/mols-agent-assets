---
name: create-help
description: >
  USE WHEN: scaffolding progressive disclosure --help.md workflow for a target skill.
  EXCLUDES: scaffolding sub-help (*--help.md), --init, or --config workflows.
---

# Create Main Help Workflow

## Goal

Create `--help.md` progressive disclosure workflow module for a target skill.

## When to Use

Use when a target skill needs a root CLI `--help` entry point providing a domain overview, workflow catalog, and general usage patterns.

## Instructions

- Follow [references/router/progressive-help-pattern.md](../../references/router/progressive-help-pattern.md) for help architecture.
- Scaffold `workflows/--help.md` to catalog available workflows and common commands.
- Do not make `--help` mandatory for normal execution.

## Workflow: Create Main Help

### Context

#### Arguments

- `--skill <name>`: Target skill folder name.

#### Parameters

- `target_dir`: Path to target skill directory (`src/skills/<skill>/`).

### Procedure

1. Verify target skill directory exists under `src/skills/<skill>/`.
2. Create `workflows/--help.md` providing overview, domain capabilities, and workflow selection catalog.
3. Register `--help.md` in target skill's `workflows/INDEX.csv`.

### Validation

- File is created at `workflows/--help.md`.
- `INDEX.csv` contains route entry for `--help.md`.
