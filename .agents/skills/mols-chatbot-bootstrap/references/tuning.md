# Generation and Tuning

Generation creates a factual baseline. Model review improves routing quality.

Neither replaces the canonical Skill or Rule.

## Compatibility First

Do not assume one repository layout or metadata contract is universal.

Before using any generator, inspect the target repository for:

- authoritative Skill and Rule roots;
- Skill package shape and entrypoint naming;
- frontmatter syntax and supported fields;
- Rule applicability keys such as `globs`, `applyTo`, or another repository-specific selector;
- local versus remote asset sources;
- existing route files, generators, and conventions.

The bundled script is a **reference baseline for a common layout**, not a portable parser for every workspace.

If the target differs, prefer the smallest safe adaptation:

1. pass different roots/output paths when the metadata contract is otherwise compatible;
2. adapt the parser or extraction logic when frontmatter or selector semantics differ;
3. reuse a target-native generator when it is already authoritative;
4. use direct/model generation when adapting a script costs more than the route surface justifies.

Do not force target assets into the bundled script's assumptions.

## Baseline Generation

The bundled generator's default assumptions are:

```text
.agents/skills/*/SKILL.md
.agents/rules/**/*.md
```

and common frontmatter containing:

- Skill `name` and `description`;
- Rule `globs` or `applyTo` selectors.

The script is configurable where simple path differences are sufficient:

```text
--repo <path>          target repository; default current directory
--skills-root <path>   local Skill root; default .agents/skills
--rules-root <path>    local Rule root; default .agents/rules
--output-dir <path>    route output; default .agents/routes
--kinds <value>        auto | skills | rules | both; default auto
--force                explicit overwrite of existing route files
```

`--kinds auto` emits only kinds with routable local entries. It does not create an empty route file merely because a conventional directory exists.

The baseline generator should extract only mechanical facts:

- Skills → canonical `name`, `description`, local `source`;
- Rules → authoritative path/glob selectors and local `source`;
- deterministic `_meta` headers and ordering.

Remote assets and semantic routing choices are not inferred by the script. Add them through explicit Skill arguments or model review.

Do not make the generator infer new capabilities, rewrite Rule semantics, or summarize asset bodies.

## Generation Strategy

Resolve the Skill's `generation` argument conservatively:

- `script` — use a compatible generator or deliberately adapt one;
- `model` — write/update routes directly when scripting adds more machinery than value;
- `<none>` — do not generate routes;
- `<auto>` — inspect compatibility first, reuse existing generation when possible, adapt the bundled script when worthwhile, otherwise prefer the smaller direct edit.

Configuration is preferred over code changes when roots/output paths are the only difference. Parser changes are appropriate when the target's asset spec is materially different.

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

Map the target repository's authoritative selector semantics into the route representation. Do not assume `globs` or `applyTo` exists merely because the bundled script supports them.

You may normalize equivalent representation for routing, but do not broaden or narrow selector meaning unless the canonical Rule itself is changed.

### `_meta`

Tune `_meta.instructions` only to clarify how the route file should be consumed. Keep it short.

## Regeneration Safety

Approved tuning must not be silently destroyed by later generation.

The bundled generator refuses to overwrite existing route files unless `--force` is explicit.

For regeneration or comparison, prefer a separate `--output-dir`. Use `--force` only when the caller actually intends replacement and the Skill's `overwrite` argument permits it.

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
