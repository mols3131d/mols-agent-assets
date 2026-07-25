---
name: trigger-guide
description: >
  USE WHEN: writing or validating trigger/activation descriptions for agent assets.
  EXCLUDES: strict validation templates or routing details.
---

# Agent Asset Trigger Guide

> Guidelines for writing activation triggers that help models decide when to invoke/reference assets.

## Recommended Template

```text
{summary}. {use_when}. [{use_case}.] [{exclusions}.]
```

- `{summary}`: (Required) Intro & core capability.
- `{use_when}`: (Required) Key scenarios, objectives, or tasks when asset should run.
- `{use_case}`: (Optional) Sample prompts, user requests, or queries triggering asset.
- `{exclusions}`: (Optional) Scope limits, near misses, or explicit boundaries.

## Examples

```yaml
description: >
  Refactor Python source code to improve readability. Use when cleaning up code structure, removing unused imports, or fixing linter warnings, such as running ruff check --fix. Does not apply to non-Python configurations or system-level setups.
```
