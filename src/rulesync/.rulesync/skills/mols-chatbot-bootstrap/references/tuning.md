# Generation and Tuning

Use this reference only when route generation, regeneration, semantic tuning, or drift
validation is materially justified. Generation creates a factual baseline; model review may
improve routing quality. Neither replaces the canonical Skill or Rule.

## Compatibility First

Do not assume one repository layout or metadata contract is universal.

Before using generation or validation, inspect only the target facts that can change the
mechanism:

- authoritative Skill and Rule roots;
- package/entrypoint shape and supported frontmatter;
- Rule applicability keys such as `globs`, `applyTo`, or another target selector;
- local versus remote sources;
- existing route files, generators, validators, and CI conventions.

Prefer target-native or already-established generation and validation when they are
sufficient. The bundled script is a **reference baseline for a common local layout**, not a
portable parser for every workspace.

If the target differs, choose the smallest safe path:

1. configure an existing compatible mechanism;
1. make a small deliberate adaptation when repeatable mechanics justify it;
1. use a direct/model edit when adapting automation costs more than the route surface;
1. skip generation entirely when no durable generated surface is needed.

Do not force target assets into the bundled script's assumptions.

## Baseline Generator

The bundled generator assumes by default:

```text
.agents/skills/*/SKILL.md
.agents/rules/**/*.md
```

with common frontmatter containing:

- Skill `name` and `description`;
- selector-based Rule `globs` or `applyTo` metadata.

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

`--kinds auto` uses only kinds with routable local entries for generation. In check mode it
can also discover existing route files, including remote-only route sets.

The baseline derives only mechanical facts:

- Skills → canonical `name`, `description`, local `source`;
- selector-based Rules → authoritative path/glob selectors and local `source`;
- deterministic `_meta` headers and ordering.

Remote assets and semantic routing choices are not inferred by the script. Add them only
from explicit source information or review evidence.

## Choosing the Mechanism

Use the bundled script only when its deterministic regeneration/checking value exceeds the
cost of carrying or adapting it. Otherwise prefer the smaller target-native or direct path.

Typical choices:

- existing target generator/checker → reuse it;
- compatible repeated local route generation → bundled script may be useful;
- small or one-off route surface → direct/model edit is usually simpler;
- no separate route asset → no generation work.

Prefer configuration over code changes when roots or output paths are the only difference.

## Tuning

Tune only where routing behavior materially improves.

### Generator adaptation

Adapt only mechanics the target actually requires, such as discovery paths, entrypoint
shape, selector extraction, output location, or factual validation. Generator adaptation
preserves canonical semantics; it does not redefine the asset specification.

### Route tuning

For Skill descriptions, distinguish overlapping capabilities, expose useful positive or
negative triggers, and remove wording that does not help selection. Preserve the Skill's
actual capability and trigger boundary; do not turn the route description into a second
Skill body.

For Rules, map authoritative selector semantics without broadening or narrowing them. Do
not invent selectors for non-path Rules merely to fit the fallback representation.

Keep `_meta.instructions` short and limited to consumption of the route file.

## Regeneration Safety

Approved tuning must not be silently destroyed by later generation.

The bundled generator refuses to overwrite existing route files unless `--force` is
explicit. Prefer a separate output directory for comparison or regeneration experiments.
Use `--force` only when replacement is actually intended and current authority permits it.

## Drift Validation

When committed routes can drift, validate factual invariants rather than byte-for-byte
equality with generated baseline output.

The bundled `--check` mode verifies the common-layout invariants it understands, including:

- `_meta.kind`, routing instructions, and JSONL structure;
- valid and unique `source` locators;
- existence of local sources;
- coverage and identity of discovered local Skills;
- coverage and selector equality of discovered local selector-based Rules;
- basic structure of remote-only or hybrid route entries.

It intentionally does **not** require a tuned Skill `description` to equal the generated
baseline. Remote semantic correctness and target-specific metadata still require model or
target-native validation.

## CI Example

`examples/github-actions-route-check.yml` is a reference workflow, not an installation side
effect.

Use or adapt it only when committed route metadata has a meaningful recurring drift risk
and the target lacks an equivalent check. Reuse an existing workflow or validator first.
When the example is justified, adapt its trigger paths, asset locations, roots, output path,
route kinds, and parser/check assumptions to the actual target.

Do not copy the example into `.github/workflows/` merely because this Skill is available.
