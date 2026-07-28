# Abathur

> [!WARNING]
> not a production-ready skill. Abathur is experimental and may have limited or incomplete functionality. Users should verify Abathur's output and manually adjust as needed.

Operator guide for **humans** and **orchestrator agents**. Do **not** inject this file into executor context. Executor rules: [SKILL.md](SKILL.md).

## What

Restructure information shape (n↔m sentences, split/merge/reorder). Full grammar. Drop waste only. Not caveman surface compression.

## When

| Use | Skip |
| --- | --- |
| Verbose or disordered answers; need core front | Token-only trim → caveman |
| Cause / action / evidence need reorder | Code, commits, PR body style |

## Commands

| Action | Command |
| --- | --- |
| Lite (default) | `/abathur`, `/abathur lite`, `like abathur` |
| Full | `/abathur full` |
| Ultra | `/abathur ultra` |
| Off | `/abathur off`, `speak normal` |

| Level | Pick when | Executor loads |
| --- | --- | --- |
| `lite` | Light split/reorder | [SKILL.md](SKILL.md) |
| `full` | Strong n↔m | + [references/full.md](references/full.md) |
| `ultra` | Min sentences + labels | + [references/ultra.md](references/ultra.md) |

## Orchestrator

1. Attach [SKILL.md](SKILL.md) only. Never attach this README.
2. Pass intensity `lite|full|ultra` (default `lite`). Load intensity refs on demand only.
3. With caveman: abathur = structure, caveman = surface. Prefer one primary style rule if they conflict.
4. Do not restyle code, commits, or PRs.
