---
name: mols-chatbot-bootstrap
description: >-
  Bootstrap or update a repository for mols CHATBOT.md compatibility. Use when a
  repository should support chat runtimes that may not automatically load applicable
  AGENTS.md guidance, task-relevant Skills, or path-scoped Rules, including route
  metadata, generation, tuning, or drift validation.
---

# Mols Chatbot Bootstrap

Establish the smallest repository-local compatibility harness for chat runtimes.

## Arguments

```yaml
target: <auto>
mode: <auto>
scope: <auto>
sources: <auto>
route_entry: <auto>
generation: <auto>
tuning: <auto>
validation: <auto>
overwrite: <auto>
```

- `target` — repository or workspace to inspect and modify. `<auto>` uses the active repository/workspace established by the caller or runtime.
- `mode` — `apply`, `refresh`, `audit`, or `<auto>`. `<auto>` resolves to `audit` for review/check-only intent, `refresh` when relevant compatibility assets already exist and the caller asks to update/sync/repair them, otherwise `apply`.
- `scope` — one or more of `chatbot`, `skills`, `rules`, `automation`, or `<auto>`. `<auto>` includes only responsibilities needed by the request or missing/stale in the target.
- `sources` — explicit local asset roots, remote asset URLs, or `<auto>`. `<auto>` uses authoritative asset locations already declared or discoverable in the target plus remote assets explicitly established by the caller; it does not search for unrelated remote sources.
- `route_entry` — an explicit entrypoint path, `direct`, `<none>`, or `<auto>`. `<auto>` reuses an existing entrypoint when suitable; otherwise it prefers `.agents/routes/ROUTE.md` when one link usefully represents the routing surface.
- `generation` — `script`, `model`, `<none>`, or `<auto>`. `<auto>` first checks whether existing or bundled generation matches the target asset layout and metadata contract, adapts it when worthwhile, and otherwise uses the smaller direct/model path.
- `tuning` — `on`, `off`, or `<auto>`. `<auto>` covers both generator compatibility tuning and route-quality tuning, but changes only what materially improves compatibility or selection.
- `validation` — `local`, `ci`, `<none>`, or `<auto>`. `<auto>` performs local validation after writes and adds target CI only when committed route metadata has a meaningful drift risk.
- `overwrite` — `preserve`, `replace`, or `<auto>`. `<auto>` is `preserve`. Existing approved routing/tuning is never replaced without explicit `replace` intent.

`<auto>` means infer independently from evidence, not use one hidden fixed profile. `<none>` explicitly disables that optional behavior. Explicit arguments always win.

## Auto Resolution

Resolve each `<auto>` independently using this evidence order:

1. explicit caller intent and arguments;
1. active target repository/workspace context;
1. applicable repository instructions and established conventions;
1. existing `CHATBOT.md`, route entrypoints, route files, scripts, validators, and CI;
1. authoritative local asset roots and explicitly declared remote assets;
1. this Skill's defaults and bundled resources.

Default behavior is conservative:

- reuse before creating;
- preserve before replacing;
- local validation before new CI;
- `.agents/routes/ROUTE.md` as the default single entrypoint only when useful, never mandatory;
- never assume one asset layout, frontmatter shape, Rule selector key, or package spec is universal;
- generation and validation only after their assumptions match the target or are deliberately adapted;
- tune only when compatibility or routing quality improves.

`mode: audit` is read-only. Do not infer write behavior from another argument while audit is active.

Do not let one inferred value silently authorize another. If a material value cannot be resolved from evidence, leave that behavior disabled or unresolved rather than inventing repository structure.

## Contract

Inspect the repository first. Reuse existing instructions, routes, scripts, validators, and CI.
Create only what is actually needed.

- Keep root `CHATBOT.md` minimal and root-only.
- Recover only harness behavior the runtime does not already provide.
- Keep `AGENTS.md`, Skills, and Rules authoritative; route assets are discovery metadata only.
- Treat bundled scripts and examples as reference baselines, not universal target assets.
- Use generation for mechanical baseline metadata and model review for routing quality.
- Never silently erase approved route tuning.
- Never install `ROUTE.md`, route JSONL, or CI merely because this Skill itself is installed.

## Resources

Read only the resource needed for the current work.

- [Route convention](references/routes.md) — route files, `_meta`, `source`, `ROUTE.md`, Skill and Rule entry shapes.
- [Generation and tuning](references/tuning.md) — compatibility, generation, semantic tuning, validation, overwrite safety, and CI guidance.
- `scripts/generate_routes.py` — reference generator/checker for a common local Skill/Rule layout; inspect and adapt it before use when the target differs.
- `examples/github-actions-route-check.yml` — optional target-side CI example; adapt it and use only when `validation: ci` is justified.

## CHATBOT.md

When compatibility routing is needed, point `CHATBOT.md` at the smallest useful routing entrypoint.

Default to `.agents/routes/ROUTE.md` when one link usefully represents the routing surface.
Reuse another established entrypoint or direct route-file links when simpler.

Recover only missing behavior such as:

- applicable `AGENTS.md` hierarchy loading;
- task-relevant Skill discovery/loading;
- target-path Rule discovery/loading.

Do not copy project policy, Skill bodies, Rule bodies, catalogs, or static path tables into `CHATBOT.md`.

## Workflow

1. Resolve arguments and inspect the target's current state, asset locations, package shapes, frontmatter, selectors, generation, validation, and CI conventions.
1. Determine which compatibility responsibilities are actually missing or stale.
1. Create, update, or audit root `CHATBOT.md` according to `mode` and `scope`.
1. Establish the smallest useful route surface according to `route_entry` and `sources`; create `ROUTE.md` in the target only when that default is useful.
1. Verify generator assumptions against the target. Reuse, configure, adapt, or replace the bundled script as needed.
1. Generate factual baseline routes according to `generation` without violating `overwrite`.
1. Tune generator compatibility and route quality according to `tuning`.
1. Validate according to `validation`. Reuse target-native checks first; adapt the bundled checker or CI example only when useful.
1. Verify authority boundaries and that intentional tuning is preserved.

## Validation

Verify that:

- routing has a clear entrypoint without requiring `ROUTE.md` when another shape is better;
- local `source` values are repository-root-relative and remote `source` values are URLs;
- Skill routing is selective without becoming a duplicate Skill body;
- Rule routing preserves authoritative selector semantics;
- generation and validation match or have been adapted to the target asset layout and metadata contract;
- generated baseline output is deterministic when generation is used;
- validation protects factual invariants without rejecting approved semantic tuning;
- rerunning generation does not silently erase approved tuning;
- no project policy or asset body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
