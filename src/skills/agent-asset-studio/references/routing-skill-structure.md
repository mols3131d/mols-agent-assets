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

Read `routing-skill-algorithm.md` when writing or changing router selection, ambiguity, or loading behavior.

## 4. `INDEX.csv`: The Route Index

A routing skill uses one `INDEX.csv`, defaulting to `workflows/INDEX.csv`. Its fields are `id,use_when,excludes`, and each `id` resolves from the directory containing the index.

Use `workflows/agent-asset-index-write.md` to create or update the index. Keep schema-writing rules out of the router architecture.

## 5. Workflow Modules

Each module acts as the entry point and orchestrator for a specific task, loading shared resources only when needed. It follows a consistent contract:

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

## 6. Recommended Defaults

| Decision | Default |
| --- | --- |
| Module directory | `workflows/` |
| Workflow path | `workflows/<workflow-name>.md` |
| Resource loading | Explicit and on demand |

## Summary

An efficient routing skill uses one small router, one compact semantic index, focused workflow modules, and on-demand resources.

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
