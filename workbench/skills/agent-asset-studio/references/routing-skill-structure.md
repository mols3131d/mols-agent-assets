# Routing Skill Architecture

Terse reference for building one skill that routes requests to task-specific workflows while loading minimal context.

> **Status:** Routing skills are a custom pattern built on the Agent Skills specification. `INDEX.csv` and `workflows/` are conventions, not standard Agent Skills primitives.

## 1. Purpose and Fit

A routing skill exposes one coherent domain capability and loads only the workflow required for the current request.

Benefits:

- one catalog entry instead of many narrow skills;
- selective workflow loading;
- shared policies, scripts, references, and assets;
- explicit routing boundaries; and
- centralized maintenance.

Use a routing skill when workflows share a domain, resources, and top-level activation description. Use separate skills when capabilities have unrelated triggers, permissions, ownership, or release lifecycles.

| Situation | Design |
| --- | --- |
| Variants within one domain | Routing skill |
| Workflows frequently compose | Routing skill |
| Unrelated intents or permissions | Separate skills |
| Only a few short workflows | One regular `SKILL.md` |

The main optimization target is model catalog and context usage, not filesystem scanning.

## 2. Recommended Structure

```text
routing-skill/
├── SKILL.md          # Activation metadata and router
├── workflows/        # Routed workflow modules
│   ├── INDEX.csv     # Route registry (default location)
│   ├── ingest-data.md
│   ├── transform-data.md
│   └── validate-quality.md
├── scripts/          # Reusable executable logic
├── references/       # Shared knowledge and specifications
└── assets/           # Templates and static resources
```

Terminology:

- whole package: **Routing Skill** or **Composite Skill**;
- root `SKILL.md`: **Skill Router**;
- `INDEX.csv`: **Route Index**;
- routed Markdown files: **Workflow Modules**.

Avoid “sub-skill” for modules that are not independently discoverable skills.

## 3. `SKILL.md`: The Router

`SKILL.md` is the only skill entry point. Keep it small because it loads on every activation.

Include:

- frontmatter describing the coherent domain scope;
- routing and ambiguity rules;
- global constraints; and
- conditions for loading shared resources.

Exclude full workflows, long references, and instructions to scan every module.

```markdown
---
name: data-engineering
description: Use this skill for data ingestion, transformation, quality validation, and pipeline orchestration.
---

# Data Engineering Router

## Routing

1. Read `workflows/INDEX.csv`.
2. Compare the request with each route's `use_when` and `excludes`.
3. Select the smallest route set that covers the request.
4. Resolve each selected `id` relative to `INDEX.csv` and read that file.
5. Load additional resources only when a workflow requires them.

Do not route from keyword overlap alone.
Do not scan all files under `workflows/`.

## Ambiguity

- Select one route when it is the clear semantic match.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when remaining routes imply materially different actions.
- If no route matches, state that the skill does not cover the request.
```

## 4. `INDEX.csv`: The Route Index

Use the minimum fields required for semantic routing:

```csv
id,use_when,excludes
```

| Field | Purpose |
| --- | --- |
| `id` | Workflow file path relative to the directory containing `INDEX.csv` |
| `use_when` | Positive selection conditions |
| `excludes` | Near misses and out-of-scope requests |

Example:

```csv
id,use_when,excludes
ingest-data.md,"Extraction, source connectors, CDC, or incremental loading","Data already loaded and only transformation is needed"
transform-data.md,"SQL modeling, joins, aggregation, normalization, or dbt","Source extraction or destination loading is primary"
validate-quality.md,"Quality checks, schema validation, anomaly detection, or reconciliation","Only scheduling or infrastructure health is requested"
```

Registry rules:

- one workflow per row;
- `id` is a relative file path resolved from the directory containing `INDEX.csv`;
- `id` must not be absolute, contain `..`, or resolve outside the skill;
- concise single-line fields;
- quoted fields when commas are present;
- exact file paths instead of directory search;
- semantic intent as the primary signal;
- keywords only as an optional tie-breaker.

Keep representative and implicit requests in `use_when`. Do not add a separate `includes` field; it duplicates the positive routing condition and increases index cost.

Use `id` as both the stable routing key and workflow location. Default to `workflows/INDEX.csv`; sibling workflows then use IDs such as `ingest-data.md`. Use a root or different subdirectory only when the user requests it. Always resolve IDs from the directory containing that index. Add `name` only when a separate human-facing label is required. Add `type` only when rows require different loading semantics, and first consider splitting heterogeneous entries into separate skills.

Use JSONL or YAML when fields require multiline or complex structured data.

## 5. Workflow Modules

Each module contains one executable workflow and follows a consistent contract:

```markdown
# Workflow Name

## Goal
State the required outcome.

## Required inputs
List inputs needed before execution.

## Procedure
Provide concise ordered steps.

## Validation
Define the completion check.

## Resources
State when to load references or run scripts.

## Stop conditions
Define when to clarify, stop, or avoid mutation.
```

Do not repeat global rules from `SKILL.md`. Put passive knowledge in `references/`, deterministic repeated logic in `scripts/`, and templates in `assets/`.

## 6. Routing Algorithm

1. Read `INDEX.csv` once.
2. Identify the requested outcome, operation, object, and constraints.
3. Eliminate routes matching `excludes`.
4. Select the minimum route set matching `use_when`.
5. Resolve material ambiguity with one targeted question.
6. Resolve selected IDs from the index directory and load only those files.
7. Load referenced resources on demand.
8. Run each workflow's validation before completion.

Do not add recursive routers. Keep routing depth to one layer.

## 7. Complex and Migrated Workflows

Do not embed nested `SKILL.md` files by default:

```text
# Avoid
workflows/complex-task/SKILL.md
```

Nested skill discovery is not defined by the core specification and can cause client-dependent activation or duplicate discovery.

Prefer a flat entry point with prefixed resources:

```text
workflows/complex-task.md
scripts/complex-task-validate.py
references/complex-task-spec.md
assets/complex-task-template.yaml
```

If migration requires an isolated directory, keep it under `workflows/`, use a non-discoverable file such as `WORKFLOW.md`, and use its exact relative path as `id` in `INDEX.csv`:

```text
workflows/
├── INDEX.csv
└── complex-task/
    ├── WORKFLOW.md
    ├── scripts/
    ├── references/
    └── assets/
```

```csv
id,use_when,excludes
complex-task/WORKFLOW.md,"Complex multi-step processing","Simple single-step requests"
```

The router resolves the exact `id` path from `INDEX.csv`, so a separate layout `type` is unnecessary. Verify that target clients can resolve the nested path.

Keep the original as a separate skill instead when it must remain independently installed or versioned.

## 8. Efficiency Boundaries

Expected context for a single-route request:

```text
metadata + SKILL.md + INDEX.csv + selected workflow + required resources
```

The pattern becomes inefficient when:

- the index becomes a detailed manual;
- the router repeats workflow content;
- most requests load most workflows;
- the router covers unrelated domains;
- workflows route recursively; or
- exact paths are replaced by directory scans.

If most workflows load together, consolidate them. If requests rarely match cleanly, split the routing skill.

## 9. Validation

Structural checks:

- workflow identifiers are unique;
- every `id` is a safe relative path whose file exists inside the skill directory;
- resource paths resolve from the skill root;
- no workflow requires discovery scans; and
- nested `SKILL.md` files are absent unless intentionally separate.

Routing tests should include:

- clear and indirect positive requests;
- near-miss negative requests;
- multi-workflow requests;
- out-of-scope requests; and
- ambiguous requests.

Measure correct-route rate, false-route rate, unnecessary workflow loads, clarification frequency, and average context loaded.

## 10. Recommended Defaults

| Decision | Default |
| --- | --- |
| Module directory | `workflows/` |
| Workflow path | `workflows/<workflow-name>.md` |
| Registry | `workflows/INDEX.csv`; custom location only when requested |
| Registry schema | `id,use_when,excludes` |
| Selection | Minimum route set |
| Ambiguity | One targeted clarification question |
| Embedded complex workflow | `WORKFLOW.md`, not `SKILL.md` |
| Resource loading | Explicit and on demand |
| Routing depth | One layer |

## Summary

An efficient routing skill uses one small router, one compact semantic index whose IDs are exact relative workflow paths, and on-demand resources.

> Route from metadata, select from the index, load the minimum workflow set, and avoid recursive discovery.

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
