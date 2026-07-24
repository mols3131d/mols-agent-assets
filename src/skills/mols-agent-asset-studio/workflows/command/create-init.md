---
name: create-init
description: >
  USE WHEN: scaffolding --init.md workspace initialization workflow for a target skill.
  EXCLUDES: scaffolding configuration management or progressive disclosure help workflows.
---

# Create Init Flag Workflow

## Goal

Create `--init.md` (workspace setup) workflow module for a target skill following standard command-flag conventions.

## When to Use

Use when a target skill requires CLI-style workspace initialization (`.configs/<skill>.cfg.json`, `.tmp/`) entry points.

## Instructions

- Follow [references/router/command-flag-workflows.md](../../references/router/command-flag-workflows.md) for flag semantics.
- Ensure `--init.md` sets up `.configs/<skill>.cfg.json` and temporary backup directories.
- Automatically scaffold paired sub-help file (`workflows/--init--help.md`) for detailed initialization options.

## Workflow: Create Init Flag

### Context

#### Arguments

- `--skill <name>`: Target skill folder name.

#### Parameters

- `target_dir`: Path to target skill directory (`src/skills/<skill>/`).

### Procedure

1. Verify target skill directory exists under `src/skills/<skill>/`.
2. Ensure `workflows/` directory exists inside target skill folder.
3. Create `workflows/--init.md` specifying `.configs/<skill>.cfg.json` creation and `.tmp/` directory validation.
4. Create `workflows/--init--help.md` providing advanced initialization flags and schema options.
5. Register created flag workflow in target skill's `workflows/INDEX.csv`.
6. Validate created files using `python3 scripts/validate_asset.py <target-skill-dir>`.

### Validation

- Flag file matches exact naming convention (`workflows/--init.md`).
- Sub-help file (`--init--help.md`) is properly referenced.
- Target `workflows/INDEX.csv` contains valid entry for `--init.md`.
