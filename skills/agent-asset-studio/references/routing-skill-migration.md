# Routing Skill Migration

Reference for moving existing skills into one shallow routing skill without changing discovery or release boundaries accidentally.

## Fit

Migrate skills together only when they share one domain, top-level trigger, resources, permissions, ownership, and release lifecycle. Keep independently installed or versioned skills separate.

Choose one layout:

| Mode | Layout | Use when |
| --- | --- | --- |
| Flat | `workflows/<name>.md` | Resources can be shared or renamed safely |
| Isolated | `workflows/<name>/WORKFLOW.md` | A workflow must retain bundled resources |

## Flat Migration

Prefer a flat workflow with prefixed resources:

```text
workflows/complex-task.md
scripts/complex-task-validate.py
references/complex-task-spec.md
assets/complex-task-template.yaml
```

Rewrite affected relative paths after moving resources. Resolve collisions explicitly; do not overwrite shared files.

## Isolated Migration

Use a non-discoverable `WORKFLOW.md` when isolation is required:

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

Do not leave a nested `SKILL.md`. Nested discovery is client-dependent and can activate the workflow twice.

## Migration Checks

- Every source belongs to the same routing domain and lifecycle.
- Each moved workflow has one exact `id` relative to `INDEX.csv`.
- Rewritten resource paths resolve inside the target skill.
- No source or destination file is overwritten silently.
- The original remains separate when independent discovery is required.

Read `routing-skill-structure.md` only when the target router or index architecture also changes.
