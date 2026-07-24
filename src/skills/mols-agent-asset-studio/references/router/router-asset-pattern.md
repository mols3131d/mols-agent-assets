---
name: router-asset-pattern
description: >
  USE WHEN: designing or validating dedicated router assets, separating router responsibilities from task-specific workflows.
  EXCLUDES: directory structure layouts, CLI action-flag specs, or markdown headings.
---

# Router Asset Pattern Reference

## Goal

Define the concept, structure, boundaries, and rules for **Router** assets—assets dedicated exclusively to request routing and workflow dispatching.

## Overview & Definition

A **Router Asset** (or simply **Router**) is a specialized agent asset pattern whose sole responsibility is **routing and dispatching**.

While many agent assets may contain incidental routing capabilities (e.g., `--help` workflows that catalog and suggest sub-workflows), a **Router Asset** is dedicated exclusively to evaluating incoming requests and selecting/loading the appropriate workflow module without performing domain work itself.

### Key Distinction: Dedicated Router vs. Incidental Routing

| Aspect | Dedicated Router Asset | Incidental Routing Asset |
| --- | --- | --- |
| **Primary Role** | Pure dispatch & workflow resolution | Task execution, help disclosure, or configuration |
| **Examples** | Root `SKILL.md` (Composite Skill), `workflows/INDEX.csv`, child `INDEX.csv` | `workflows/--help.md`, `--config.md` |
| **Domain Logic** | Zero domain execution; purely routing | Contains domain instructions, explanations, or edits |
| **Context Footprint** | Extremely minimal (loads quickly on every trigger) | Medium to large context (loaded on demand) |

## Core Structure & Components

A Router Asset package typically consists of:

1. **Skill Router (`SKILL.md`)**: The lightweight entry point. Defines activation scope (`description`), global constraints, ambiguity handling, and index parsing logic.
2. **Route Index (`INDEX.csv`)**: The declarative registry mapping request conditions (`use_when`, `excludes`) to child indexes or workflow module paths (`id`).
3. **Workflow Modules (`workflows/*.md`)**: The target workflow files dispatched by the router.

```text
routing-skill/
├── SKILL.md          # Router Entry Point
└── workflows/
    ├── INDEX.csv     # Route Index Registry
    ├── task-a.md     # Dispatched Workflow Module
    └── task-b.md     # Dispatched Workflow Module
```

## Architectural Rules & Boundaries

1. **Zero Direct Execution**: A Router must never contain task execution procedures, heavy reference prose, or code/script logic. It delegates 100% of execution to routed modules.
2. **Hierarchical Index Evaluation**: The Router reads one nearest index at a time, selects a child index or workflow, and dispatches it without loading unrelated route metadata.
3. **Strict Context Boundary**: Keep `SKILL.md` as small as possible. High context costs in a Router degrade performance across every activation.
4. **Explicit Exclusions**: Exclude non-matching or near-miss routes early using the `excludes` column of the Route Index.
5. **No Recursive Routing**: A Router must dispatch directly to executable workflow modules or scripts, avoiding nested router chains.

## Router Asset Check & Validation

When validating a Router Asset (e.g., using `validate_asset.py`):

- Confirm `SKILL.md` delegates work to `workflows/` via a root Route Index (`INDEX.csv`).
- Verify every `id` entry in every `INDEX.csv` resolves relative to its index location.
- Ensure no nested `SKILL.md` files exist under `workflows/`.
