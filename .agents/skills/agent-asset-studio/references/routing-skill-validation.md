# Routing Skill Validation

Reference for checking routing correctness, structural safety, and context efficiency.

## Expected Context

A single-route request should load:

```text
metadata + SKILL.md + INDEX.csv + selected workflow + required resources
```

The routing skill is inefficient when:

- the index becomes a detailed manual;
- the router repeats workflow content;
- most requests load most workflows;
- the router covers unrelated domains;
- workflows route recursively; or
- exact paths are replaced by directory scans.

Consolidate workflows that usually load together. Split the skill when requests rarely match one route cleanly.

## Structural Checks

- One `INDEX.csv` exists at the configured location.
- The schema is `id,use_when,excludes`.
- IDs are unique safe relative paths whose files exist inside the skill.
- `use_when` and `excludes` are non-empty and semantically distinct.
- Resource paths resolve from their documented base.
- No workflow requires a discovery scan.
- No nested discoverable `SKILL.md` exists under `workflows/`.

## Routing Tests

Test at least one case for each category:

- clear direct match;
- indirect or implicit match;
- near miss excluded from a route;
- explicit multi-workflow request;
- out-of-scope request; and
- materially ambiguous request.

Confirm that clear requests load the minimum correct workflow set, excluded requests do not route, and ambiguity produces one targeted question.

## Measures

Track correct-route rate, false-route rate, unnecessary workflow loads, clarification frequency, and average context loaded. Treat regressions in correctness as failures; context savings never justify wrong routing.
