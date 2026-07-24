---
name: command-flag-workflows
description: >
  USE WHEN: defining architectural semantics or naming conventions for CLI-style entry points (like --init or --config) in routing skills.
  EXCLUDES: natural language router selection, general asset optimization, or markdown formatting rules.
---

# Command Flag Workflows Reference

## Goal

Define architectural semantics and naming conventions for CLI-style command flag workflows (`--init`, `--config`, and action flags) in routing skills.

## Core Flag Semantics

Command flags are optional entry-point mechanisms that override fuzzy natural language matching when explicitly invoked.

- **`--init` (`workflows/--init.md`)**: Workspace initialization (`.configs/<skill>.cfg.json`, `.tmp/`).
- **`--config` (`workflows/--config.md`)**: View, locate, or edit active skill configuration.
- **Action Flags**: Action-specific CLI entry points (`workflows/<action>.md`).

> For `--help` architectural philosophy and anti-patterns, see [references/progressive-help-pattern.md](progressive-help-pattern.md).

## Naming & Index Conventions

| Flag | Workflow File | Sub-Help File (`*--help`) |
| --- | --- | --- |
| Init | `workflows/--init.md` | `workflows/--init--help.md` |
| Config | `workflows/--config.md` | `workflows/--config--help.md` |
| Custom Action | `workflows/<action>.md` | `workflows/<action>--help.md` |

- **Router Priority**: Direct flag inputs (`--init`, `--config`) take priority over ambiguous natural language.
- **Combination Resolution**: Multi-flag inputs (e.g. `--init --help`) route directly to the sub-help module (`--init--help.md`).
