---
name: mols-chatbot-bootstrap
description: >-
  Bootstrap or update a repository for mols CHATBOT.md compatibility. Use when a
  repository should support chat runtimes that may not automatically load applicable
  AGENTS.md guidance, task-relevant Skills, or path-scoped Rules, including requests to
  create CHATBOT.md, route metadata, route generation, or drift validation.
---

# Mols Chatbot Bootstrap

Establish the smallest repository-local compatibility harness for chat runtimes.

## Contract

Inspect the repository first. Reuse existing instructions, scripts, routes, and CI.
Create only what is actually needed.

As needed:

- create or update root `CHATBOT.md`;
- prefer `.agents/routes/ROUTE.md` as the default single route entrypoint when useful;
- maintain `.agents/routes/skills.jsonl` for task-intent Skill routing;
- maintain `.agents/routes/rules.jsonl` for path/glob Rule routing;
- use deterministic generation for factual baseline metadata;
- tune routing metadata when the generated baseline is not selective enough;
- add the smallest useful drift validation.

`ROUTE.md` is a convenience convention, not a requirement. Reuse another route entrypoint
or direct route-file links when that is simpler or already established by the repository.

`AGENTS.md`, Skills, and Rules remain authoritative. Route assets are discovery metadata.

## CHATBOT.md

Keep root `CHATBOT.md` minimal and root-only.

When repository routing is needed, prefer linking to `.agents/routes/ROUTE.md` as one
single entrypoint. If the repository already has an equivalent routing entrypoint, use it.
Direct links to route files are also valid when they are simpler.

Recover only harness behavior the runtime does not already provide:

- applicable `AGENTS.md` hierarchy loading;
- task-relevant Skill discovery/loading;
- target-path Rule discovery/loading.

Do not copy project policy, Skill bodies, Rule bodies, catalogs, or static path tables into
`CHATBOT.md`.

## Route Shape

Each JSONL route file reserves its first line for `_meta`; remaining lines are route entries.
Keep deterministic order.

Use one `source` locator:

- local asset → repository-root-relative path;
- remote asset → URL.

### Skills

Route Skills primarily by `name` and `description`.

```jsonl
{"_meta":{"kind":"skills","instructions":"Select task-relevant Skills by name and description, then load only the selected source."}}
{"name":"example-skill","description":"Do X when Y. Do not use for Z.","source":".agents/skills/example-skill/SKILL.md"}
```

The generator may copy canonical `name` and `description` as a baseline. After generation,
review the route set as a routing system and tune `description` when that improves selection
precision or reduces overlap between Skills.

Tuning must preserve the Skill's actual capability and trigger boundary. Do not invent a
capability, narrow away intended use, or turn the route description into a second Skill body.

Keep `name` and local `source` aligned with the canonical Skill unless migration explicitly
changes identity or location.

### Rules

Route Rules primarily by applicability selectors such as `globs` or `applyTo`.

```jsonl
{"_meta":{"kind":"rules","instructions":"Match known target paths against globs, then load only matching Rule sources."}}
{"source":".agents/rules/python.md","globs":["**/*.py","**/*.pyi"]}
```

Generate selectors from authoritative Rule metadata. Tune only the route representation
needed for reliable matching; do not change selector meaning or copy Rule policy text.

Global or non-path Rules do not need entries unless the repository has a real discovery need.

## Generation

Use `scripts/generate_routes.py` as a baseline generator or as a starting point for a
repository-local generator.

It deterministically extracts:

- local Skills from `.agents/skills/*/SKILL.md` using `name`, `description`, and `source`;
- local glob/path Rules from `.agents/rules/**/*.md` using selectors and `source`;
- the reserved `_meta` headers.

The script is intentionally not the final authority for routing quality. Generation handles
mechanical facts; review and tuning handle semantic routing quality.

When the target repository uses different asset roots or front-matter conventions, adapt the
smallest part of the script rather than adding another framework or manifest layer.

## Tuning

After generation, inspect the route set together rather than reviewing entries in isolation.

Tune only when useful:

- distinguish Skills whose canonical descriptions overlap;
- make positive triggers and important exclusions easier to route;
- remove wording that does not help selection;
- normalize equivalent Rule selector metadata without changing applicability;
- keep `_meta.instructions` concise and specific to how that route file should be consumed.

Prefer canonical metadata unchanged when it already routes well.

## Automation

If generated route files are committed and sources can change, add the smallest practical
validation against stale structural metadata.

Do not require byte-for-byte regeneration when intentional routing tuning is allowed. A drift
check should protect factual invariants such as missing/renamed sources, Skill identity, and
Rule selectors without erasing approved semantic tuning.

Reuse an existing workflow when possible.

## Workflow

1. Inspect repository instructions, asset roots, routes, scripts, and CI.
2. Determine which compatibility responsibilities are missing.
3. Create or update minimal root `CHATBOT.md` with the smallest useful routing entrypoint.
4. Create or update required route assets; use `ROUTE.md` by default when one entrypoint helps.
5. Generate factual baseline metadata where useful.
6. Tune routing metadata only where it improves routing quality.
7. Add drift validation only where stale routes are a real risk.
8. Verify authority boundaries and routing behavior.

## Validation

Verify that:

- `CHATBOT.md` is root-only and minimal;
- routing has a clear entrypoint without requiring `ROUTE.md` when another shape is better;
- route entries use one valid `source` locator;
- Skill routes are useful for intent selection without becoming duplicate Skill bodies;
- Rule routes preserve authoritative selector semantics;
- generated baseline output is deterministic;
- intentional tuning is not overwritten by drift validation;
- no project policy or asset body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
