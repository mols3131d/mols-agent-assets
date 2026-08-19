# Generation and Tuning

Generation creates a factual baseline. Model review improves routing quality.

Neither replaces the canonical Skill or Rule.

## Baseline Generation

Use the bundled generator when the target repository follows the default local layout:

```text
.agents/skills/*/SKILL.md
.agents/rules/**/*.md
```

Run it from the Skill package or adapt the smallest necessary part for the target repository.

The baseline generator should extract only mechanical facts:

- Skills → canonical `name`, `description`, local `source`;
- Rules → authoritative path/glob selectors and local `source`;
- deterministic `_meta` headers and ordering.

Do not make the generator infer new capabilities, rewrite Rule semantics, or summarize asset bodies.

## Tuning

Review the route set as a routing system, not as isolated entries.

Tune only where it improves selection.

### Skill descriptions

Useful tuning includes:

- distinguish Skills with overlapping canonical descriptions;
- expose positive triggers that help selection;
- expose important exclusions that prevent false activation;
- remove wording that does not help routing.

Preserve the Skill's actual capability and trigger boundary. Do not invent capabilities, narrow away intended use, or turn `description` into a second Skill body.

If the canonical description already routes well, keep it unchanged.

### Rule routes

Rule selectors are factual applicability metadata.

You may normalize equivalent representation for routing, but do not broaden or narrow selector meaning unless the canonical Rule itself is changed.

### `_meta`

Tune `_meta.instructions` only to clarify how the route file should be consumed. Keep it short.

## Regeneration Safety

Approved tuning must not be silently destroyed by later generation.

The bundled generator therefore should not overwrite existing route files unless overwrite is explicitly requested.

For regeneration or comparison, use a separate output directory or explicit overwrite only when the caller intends to replace current route files.

## Drift Validation

When route files are committed and sources change often, validate factual invariants rather than requiring byte-for-byte equality with generated baseline output.

Useful invariants include:

- referenced local sources still exist;
- Skill identity still matches the canonical Skill;
- Rule selectors still match canonical applicability metadata;
- every route entry has a valid `source`;
- the first JSONL line remains `_meta`.

Do not fail CI merely because an approved Skill route description is semantically tuned away from the generator's copied baseline.

Reuse existing CI and repository tooling before adding new machinery.
