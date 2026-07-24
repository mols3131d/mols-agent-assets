---
name: create-sub-help
description: >
  USE WHEN: scaffolding targeted sub-help (*--help.md) workflows for specific sub-workflows or action flags.
  EXCLUDES: scaffolding root --help.md, --init, or --config workflows.
---

# Create Sub-Help Workflow

## Goal

Create targeted sub-help workflow modules (`<workflow>--help.md`) for specialized progressive disclosure.

## When to Use

Use when a specific workflow or action flag requires deep architectural explanations, full parameter schemas, rare failure recovery steps, or edge-case handling that would otherwise bloat the main prompt.

## Instructions

- Follow [references/router/progressive-help-pattern.md](../../references/router/progressive-help-pattern.md) for sub-help philosophy.
- File naming must follow `workflows/<workflow>--help.md` (e.g., `workflows/--config--help.md` or `workflows/export--help.md`).
- Link sub-help from its parent workflow module.

## Workflow: Create Sub-Help

### Context

#### Arguments

- `--skill <name>`: Target skill folder name.
- `--workflow <name>`: Name of the parent workflow (e.g. `--config`, `export`).

#### Parameters

- `target_dir`: Path to target skill directory (`src/skills/<skill>/`).

### Procedure

1. Verify target skill directory exists under `src/skills/<skill>/`.
2. Create `workflows/<workflow>--help.md` with detailed operational schemas or edge cases.
3. Link `<workflow>--help.md` inside parent workflow's `## References` section.
4. Register sub-help route in target skill's `workflows/INDEX.csv`.

### Validation

- File is created at `workflows/<workflow>--help.md`.
- Parent workflow references the sub-help file properly.
