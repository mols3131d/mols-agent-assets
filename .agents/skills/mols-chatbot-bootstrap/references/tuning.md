# Generation and Tuning

Generation creates a factual baseline. Model review improves routing quality.
Neither replaces the canonical Skill or Rule.

## Compatibility First

Do not assume one repository layout or metadata contract is universal.

Before using generation or validation, inspect the target repository for:

- authoritative Skill and Rule roots;
- Skill package shape and entrypoint naming;
- frontmatter syntax and supported fields;
- Rule applicability keys such as `globs`, `applyTo`, or another repository-specific selector;
- local versus remote asset sources;
- existing route files, generators, validators, and CI conventions.

The bundled script is a **reference baseline for a common layout**, not a portable parser for every workspace.

If the target differs, prefer the smallest safe adaptation:

1. pass different roots/output paths when the metadata contract is otherwise compatible;
2. adapt parser/extraction/check logic when frontmatter or selector semantics differ;
3. reuse target-native generation or validation when it is already authoritative;
4. use direct/model generation when adapting a script costs more than the route surface justifies.

Do not force target assets into the bundled script's assumptions.

## Baseline Generation

The bundled generator assumes by default:

```text
.agents/skills/*/SKILL.md
.agents/rules/**/*.md
```

with common frontmatter containing:

- Skill `name` and `description`;
- Rule `globs` or `applyTo` selectors.

Its main options are:

```text
--repo <path>          target repository; default current directory
--skills-root <path>   local Skill root; default .agents/skills
--rules-root <path>    local Rule root; default .agents/rules
--output-dir <path>    route directory; default .agents/routes
--kinds <value>        auto | skills | rules | both; default auto
--check                validate factual route invariants without rewriting
--force                explicit overwrite of existing route files
```

`--kinds auto` uses only kinds with routable local entries. It does not create an empty route file merely because a conventional directory exists.

The baseline should derive only mechanical facts:

- Skills → canonical `name`, `description`, local `source`;
- Rules → authoritative path/glob selectors and local `source`;
- deterministic `_meta` headers and ordering.

Remote assets and semantic routing choices are not inferred by the script. Add them through explicit Skill arguments or model review.

## Generation Strategy

Resolve `generation` conservatively:

- `script` — use a compatible generator or deliberately adapt one;
- `model` — write/update routes directly when scripting adds more machinery than value;
- `<none>` — do not generate routes;
- `<auto>` — inspect compatibility first, reuse existing generation when possible, adapt the bundled script when worthwhile, otherwise prefer the smaller direct edit.

Prefer configuration over code changes when roots/output paths are the only difference.

## Tuning

There are two distinct tuning surfaces.

### Generator tuning

Adapt only what the target requires:

- asset discovery paths;
- package/entrypoint shape;
- frontmatter parsing;
- selector extraction and normalization;
- output locations or route kinds;
- validation logic that depends on those assumptions.

Generator tuning preserves canonical semantics. It does not redefine the asset spec.

### Route tuning

Review the route set as a routing system. Tune only where selection improves.

#### Skill descriptions

Useful tuning includes:

- distinguish Skills with overlapping canonical descriptions;
- expose positive triggers that help selection;
- expose important exclusions that prevent false activation;
- remove wording that does not help routing.

Preserve the Skill's actual capability and trigger boundary. Do not turn `description` into a second Skill body.
If the canonical description already routes well, keep it unchanged.

#### Rule routes

Rule selectors are factual applicability metadata.
Map the target repository's authoritative selector semantics into the route representation.
Do not assume `globs` or `applyTo` exists merely because the bundled script supports them.

Normalize representation only. Do not broaden or narrow selector meaning unless the canonical Rule itself changes.

#### `_meta`

Tune `_meta.instructions` only to clarify consumption of the route file. Keep it short.

## Regeneration Safety

Approved tuning must not be silently destroyed by later generation.

The bundled generator refuses to overwrite existing route files unless `--force` is explicit.
For regeneration or comparison, prefer a separate `--output-dir`. Use `--force` only when the caller actually intends replacement and `overwrite` permits it.

## Drift Validation

When committed routes can drift, validate factual invariants rather than byte-for-byte equality with generated baseline output.

The bundled `--check` mode verifies the common-layout invariants it understands, including:

- `_meta.kind` and JSONL structure;
- valid and unique `source` locators;
- existence of local sources;
- coverage and identity of discovered local Skills;
- coverage and selector equality of discovered local Rules.

It intentionally does **not** require a tuned Skill `description` to equal the generated baseline.
Remote semantic correctness and target-specific metadata still require model or target-native validation.

## CI Example

`examples/github-actions-route-check.yml` is a reference workflow, not an installation side effect.
Create or adapt target CI only when `validation: ci` is actually justified.

Before using the example, adjust as needed:

- workflow trigger paths;
- location of this Skill or another validator;
- `--skills-root`, `--rules-root`, `--output-dir`, and `--kinds`;
- parser/check logic when the target asset specification differs.

Reuse an existing target workflow or validator before adding another one.
Do not copy the example into `.github/workflows/` merely because this Skill is installed.
