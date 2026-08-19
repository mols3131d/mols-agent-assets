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

## Contract

Inspect the repository first. Reuse existing instructions, routes, scripts, and CI.
Create only what is actually needed.

- Keep root `CHATBOT.md` minimal and root-only.
- Recover only harness behavior the runtime does not already provide.
- Prefer `.agents/routes/ROUTE.md` as the default single routing entrypoint when useful, but do not require it.
- Keep `AGENTS.md`, Skills, and Rules authoritative; route assets are discovery metadata only.
- Use generation for mechanical baseline metadata and model review for routing quality.

## Resources

Read only the reference needed for the current work.

- [Route convention](references/routes.md) — route files, `_meta`, `source`, `ROUTE.md`, Skill and Rule entry shapes.
- [Generation and tuning](references/tuning.md) — baseline generation, semantic tuning, overwrite safety, and drift validation.
- `scripts/generate_routes.py` — deterministic baseline generator for local `.agents/skills/` and glob/path `.agents/rules/` assets.

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

1. Inspect repository instructions, asset roots, current routing surfaces, scripts, and CI.
2. Determine which compatibility responsibilities are actually missing.
3. Create or update minimal root `CHATBOT.md` only when needed.
4. Create or update the smallest useful route surface; use `ROUTE.md` by default when a single entrypoint helps.
5. Generate factual baseline routes when useful.
6. Review the route set together and tune only where routing quality improves.
7. Add drift validation only when stale routes are a real risk.
8. Verify authority boundaries and that intentional tuning is preserved.

## Validation

Verify that:

- routing has a clear entrypoint without requiring `ROUTE.md` when another shape is better;
- local `source` values are repository-root-relative and remote `source` values are URLs;
- Skill routing is selective without becoming a duplicate Skill body;
- Rule routing preserves authoritative selector semantics;
- generated baseline output is deterministic;
- rerunning generation does not silently erase approved tuning;
- no project policy or asset body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
