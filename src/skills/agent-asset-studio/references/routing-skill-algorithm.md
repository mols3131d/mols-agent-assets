# Routing Skill Algorithm

Canonical selection, ambiguity, and loading behavior for a routing skill.

## Router Template

```markdown
## Routing

1. Read `workflows/INDEX.csv` once.
2. Identify the requested outcome, operation, object, and constraints.
3. Eliminate routes matching `excludes`.
4. Select the minimum route set matching `use_when`.
5. Resolve material ambiguity with one targeted question.
6. Resolve selected IDs from the index directory and load only those files.
7. Load referenced resources only when a selected workflow requires them.
8. Run each selected workflow's validation before completion.

Route by semantic intent, not keyword overlap. Do not scan `workflows/` to discover routes.

## Ambiguity

- Select one route when it fully covers the request.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when remaining routes imply materially different actions.
- If no route matches, state that the skill does not cover the request.
```

## Selection Rules

- Treat `excludes` as a hard negative signal before comparing positive conditions.
- Use representative and implicit intent in `use_when`; keywords are tie-breakers only.
- Prefer the smallest route set that covers the full request.
- Resolve each `id` relative to the directory containing `INDEX.csv`.

## Loading Rules

- Keep routing depth to one layer; workflows do not route recursively.
- The selected workflow acts as the entry point for its specific task; load only the resources it explicitly requires.
- Do not replace exact IDs with directory scans.
- Preserve workflow order only when the request or procedure requires it.
