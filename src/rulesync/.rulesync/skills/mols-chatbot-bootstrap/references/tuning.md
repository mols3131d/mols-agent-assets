# Generation and Tuning

Use this reference only when route generation, regeneration, semantic tuning, or drift
validation is materially justified. Generation creates a factual baseline; model review may
improve routing quality. Neither replaces the canonical Skill or Rule.

## Compatibility First

Do not assume one repository layout or metadata contract is universal.

Before using generation or validation, inspect only target facts that can change the
mechanism:

- authoritative Skill and Rule roots;
- package/entrypoint shape and supported frontmatter;
- Rule applicability selectors;
- local versus remote sources;
- existing route files, generators, validators, and CI conventions.

Prefer target-native or established generation and validation when sufficient. The bundled
script is a **reference baseline for a common local layout**, not a portable parser for every
workspace.

If the target differs, choose the smallest safe path:

1. configure an existing compatible mechanism;
1. make a small adaptation when repeatable mechanics justify it;
1. use a direct/model edit when automation costs more than the route surface;
1. skip generation when no durable generated surface is needed.

Do not force target assets into the bundled script's assumptions.

## Baseline Generator

The bundled generator assumes by default:

```text
.agents/skills/*/SKILL.md
.agents/rules/**/*.md
```

with common frontmatter containing Skill `name` and `description`, and selector-based Rule
`globs` or `applyTo` metadata.

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

The baseline derives only mechanical facts:

- Skills → canonical `name`, `description`, local `source`;
- selector-based Rules → authoritative selectors and local `source`;
- deterministic `_meta` headers and ordering.

Remote assets and semantic routing choices are not inferred by the script. Add them only
from explicit source information or review evidence.

Use the bundled script only when deterministic regeneration or checking provides more value
than carrying or adapting it costs. Small or one-off route surfaces usually favor a direct
edit; an established target generator should be reused instead.

## Tuning

Tune only where routing behavior materially improves.

- **Generator adaptation** changes only mechanics the target actually requires, such as
  discovery paths, entrypoint shape, selector extraction, output location, or factual
  validation. It does not redefine asset semantics.
- **Skill route tuning** may clarify positive/negative triggers or distinguish overlapping
  capabilities, but must preserve the Skill's actual responsibility and must not become a
  second Skill body.
- **Rule route tuning** preserves authoritative applicability. Do not invent selectors for
  non-path Rules merely to fit the fallback representation.
- **`_meta.instructions`** stays short and limited to route-file consumption.

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
When justified, adapt the example to the actual target rather than copying it unchanged.
