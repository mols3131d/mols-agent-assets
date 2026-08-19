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
- `generation` — `script`, `model`, `<none>`, or `<auto>`. `<auto>` reuses existing generation first, uses/adapts the bundled script when repeatability helps, and avoids a generator when a tiny static route is simpler.
- `tuning` — `on`, `off`, or `<auto>`. `<auto>` reviews routing quality but edits semantic routing metadata only when selection materially improves.
- `validation` — `local`, `ci`, `<none>`, or `<auto>`. `<auto>` performs local validation after writes and adds CI only when committed route metadata has a meaningful drift risk.
- `overwrite` — `preserve`, `replace`, or `<auto>`. `<auto>` is `preserve`. Existing approved routing/tuning is never replaced without explicit `replace` intent.

`<auto>` means infer independently from evidence, not use one hidden fixed profile. `<none>` explicitly disables that optional behavior. Explicit arguments always win.

## Auto Resolution

Resolve each `<auto>` independently using this evidence order:

1. explicit caller intent and arguments;
2. active target repository/workspace context;
3. applicable repository instructions and established conventions;
4. existing `CHATBOT.md`, route entrypoints, route files, scripts, and CI;
5. authoritative local asset roots and explicitly declared remote assets;
6. this Skill's defaults and bundled resources.

Default behavior is conservative:

- reuse before creating;
- preserve before replacing;
- local validation before new CI;
- `.agents/routes/ROUTE.md` as the default single entrypoint only when useful, never mandatory;
- script generation only when it reduces real maintenance or drift cost;
- semantic tuning only when routing improves.

`mode: audit` is read-only. Do not infer write behavior from another argument while audit is active.

Do not let one inferred value silently authorize another. If a material value cannot be resolved from evidence, leave that behavior disabled or unresolved rather than inventing repository structure.

## Contract

Inspect the repository first. Reuse existing instructions, routes, scripts, and CI.
Create only what is actually needed.

- Keep root `CHATBOT.md` minimal and root-only.
- Recover only harness behavior the runtime does not already provide.
- Keep `AGENTS.md`, Skills, and Rules authoritative; route assets are discovery metadata only.
- Use generation for mechanical baseline metadata and model review for routing quality.
- Never silently erase approved route tuning.

## Resources

Read only the reference needed for the current work.

- [Route convention](references/routes.md) — route files, `_meta`, `source`, `ROUTE.md`, Skill and Rule entry shapes.
- [Generation and tuning](references/tuning.md) — baseline generation, semantic tuning, overwrite safety, and drift validation.
- `scripts/generate_routes.py` — deterministic baseline generator for local Skills and glob/path Rules; adapt only when `generation` requires it.

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

1. Resolve arguments and inspect the target's current state.
2. Determine which compatibility responsibilities are actually missing or stale.
3. Create, update, or audit root `CHATBOT.md` according to `mode` and `scope`.
4. Establish the smallest useful route surface according to `route_entry` and `sources`.
5. Generate factual baseline routes according to `generation` without violating `overwrite`.
6. Review the route set together and tune according to `tuning`.
7. Validate according to `validation`; add automation only when justified.
8. Verify authority boundaries and that intentional tuning is preserved.

## Validation

Verify that:

- routing has a clear entrypoint without requiring `ROUTE.md` when another shape is better;
- local `source` values are repository-root-relative and remote `source` values are URLs;
- Skill routing is selective without becoming a duplicate Skill body;
- Rule routing preserves authoritative selector semantics;
- generated baseline output is deterministic when generation is used;
- rerunning generation does not silently erase approved tuning;
- no project policy or asset body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
