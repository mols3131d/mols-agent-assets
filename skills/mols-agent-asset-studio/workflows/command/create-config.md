---
name: create-config
description: >
  USE WHEN: scaffolding --config.md configuration management workflow for a target skill.
  EXCLUDES: scaffolding workspace initialization or progressive disclosure help workflows.
---

# Create Config Flag Workflow

## Goal

Create `--config.md` (configuration management) workflow module for a target skill following standard command-flag conventions.

## When to Use

Use when a target skill requires active configuration inspection or editing entry points (`.configs/<skill>.cfg.json`).

## Instructions

- Follow [references/router/command-flag-workflows.md](../../references/router/command-flag-workflows.md) for flag semantics.
- Ensure `--config.md` provides steps to locate, view, or update the skill's JSON configuration.
- Automatically scaffold paired sub-help file (`workflows/--config--help.md`) for detailed configuration key references.

## Workflow: Create Config Flag

### Context

#### Arguments

- `--skill <name>`: Target skill folder name.

#### Parameters

- `target_dir`: Path to target skill directory (`src/skills/<skill>/`).

### Procedure

1. Verify target skill directory exists under `src/skills/<skill>/`.
2. Ensure `workflows/` directory exists inside target skill folder.
3. Create `workflows/--config.md` specifying config reading, path resolution, and parameter updates.
4. Create `workflows/--config--help.md` providing detailed configuration key references.
5. Register created flag workflow in target skill's `workflows/INDEX.csv`.
6. Validate created files using `python3 scripts/validate_asset.py <target-skill-dir>`.

### Validation

- Flag file matches exact naming convention (`workflows/--config.md`).
- Sub-help file (`--config--help.md`) is properly referenced.
- Target `workflows/INDEX.csv` contains valid entry for `--config.md`.
