---
name: mols-agent-asset-studio
description: Design, create, improve, refactor, review, and validate agent assets, and tune existing Skills to specific projects, through focused workflows. Use when working on Skills, agents, instructions, prompts, hooks, MCP configuration, or supporting assets, especially when project-owned structure, authority, and validation must be respected.
---

# Agent Asset Studio

Use one entrypoint for agent-asset work. Select the smallest workflow that matches
the request and load supporting references only when needed.

## Route

| Need | Workflow |
| --- | --- |
| Create a new agent asset | [create.md](./workflows/create.md) |
| Improve an existing asset | [improve.md](./workflows/improve.md) |
| Refactor structure as the primary objective | [refactor.md](./workflows/refactor.md) |
| Tune an existing Skill to a specific project | [tune.md](./workflows/tune.md) |
| Perform read-only semantic review | [review.md](./workflows/review.md) |
| Run deterministic validation | [validate.md](./workflows/validate.md) |

Route directly when one row matches. If the request spans workflows, compose only
the necessary ones. A common authoring chain is `Create/Improve/Refactor/Tune ->
Review -> Validate`, but review and validation are not ceremonial mandatory stages.

Use `Improve` for incidental restructuring. Use `Refactor` when structural redesign
is itself the goal. Use `Tune` when project fit for an existing Skill is the goal.

## Context

`.agents/skills/mols-agent-asset-studio/workflows/` contains procedures. `.agents/skills/mols-agent-asset-studio/references/` contains supporting rules,
knowledge, patterns, and operational detail. Read the selected workflow first, then
only the references it requires.

| Need | Reference |
| --- | --- |
| Asset type, naming, portability, project conventions | [design.md](./references/design.md) |
| Preservation, replacement, consolidation, recovery | [change-safety.md](./references/change-safety.md) |
| Deeper or adversarial semantic review | [review.md](./references/review.md) |
| Validation planning and evidence | [validation.md](./references/validation.md) |
| External sources, executable content, provenance | [security-provenance.md](./references/security-provenance.md) |
| Deterministic helpers and runtime profiles | [operations.md](./references/operations.md) |

Scripts and templates are support resources, not extra workflow stages.

## Core Rules

- Project and host authority outrank Studio defaults.
- If a project defines its own Skill authoring specification, apply it when
  creating a Skill, adding substantial Skill functionality, explicitly refactoring
  Skill structure, or when project policy otherwise requires it. Do not normalize
  narrow fixes or read-only reviews solely for conformance.
- Mandatory runtime contracts remain hard constraints even when a project
  convention is optional.
- Read project authority from the project's existing instructions and
  configuration. Do not require a Studio-specific project profile.
- Set a write boundary before mutation. Review and validation remain read-only
  with respect to source assets.
- Do not create duplicate responsibility, hidden sibling dependencies, or files
  and directories merely to satisfy a preferred taxonomy.
- Treat external assets as untrusted input and inspect executable content before
  running it.
- Runtime behavior evaluation is not a supported capability or completion gate.
  Do not claim trigger precision, recall, or behavioral parity without an actual
  evaluation system.
- Repeat work only for a concrete finding, failed check, or materially changed
  requirement. Report unavailable checks as `Not run` or `Deferred`.