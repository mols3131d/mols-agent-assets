---
name: mols-chatbot-bootstrap
description: >-
  Bootstrap or update a repository for mols CHATBOT.md compatibility. Use when a
  repository should support chat runtimes that may not automatically load applicable
  AGENTS.md guidance, task-relevant Skills, or path-scoped Rules, including requests to
  create CHATBOT.md, discovery routes, route generators, or drift-check CI.
---

# Mols Chatbot Bootstrap

Establish the smallest repository-local compatibility harness for chat runtimes.

## Contract

Inspect the repository before changing it. Reuse existing conventions, scripts, routes,
and CI before creating new ones.

As needed:

- create or update root `CHATBOT.md`;
- expose Skills through `.agents/routes/skills.jsonl` for task-intent discovery;
- expose path/glob-scoped Rules through `.agents/routes/rules.jsonl` for selector-based discovery;
- generate route files from canonical sources when they can drift;
- add CI validation when committed generated routes can become stale.

Do not add machinery merely because this Skill lists it. Create only what the repository
actually needs.

`AGENTS.md`, Skills, and Rules remain authoritative. `CHATBOT.md` and route files are
routing and compatibility surfaces only.

## CHATBOT.md

Keep root `CHATBOT.md` minimal and root-only.

It should recover only harness behavior the active runtime does not already provide:

- load the applicable `AGENTS.md` hierarchy for known target paths;
- discover/load task-relevant Skills through `.agents/routes/skills.jsonl`;
- discover/load Rules whose selectors match known target paths through `.agents/routes/rules.jsonl`.

Do not copy project policy, Skill bodies, Rule bodies, full catalogs, or static path tables
into `CHATBOT.md`. Do not invent a `CHATBOT.md → AGENTS.md → README.md` fallback chain.

Treat the responsibilities independently. If the runtime already provides one, recover
only the missing ones.

## Route Files

Each route file is JSONL discovery metadata, not a second source of truth. Keep one JSON
object per line and preserve deterministic order.

Reserve the first line for a header object with `_meta`. It may carry concise metadata and
instructions for consuming that route file. Consumers must not treat the header as an
asset entry.

Example:

```json
{"_meta":{"kind":"skills","instructions":"Select task-relevant Skills by name and description, then load only the selected source."}}
```

Keep the header small. Do not move project policy or asset content into it.

Every asset entry uses one `source` field as its locator:

- local asset → repository-root-relative path;
- remote asset → URL.

Do not add separate local/remote locator fields for the same purpose.

### Skills

Index Skills for task-intent selection. Derive local entries from each canonical
`SKILL.md` front matter.

Use `name`, `description`, and `source`:

```json
{"_meta":{"kind":"skills","instructions":"Select task-relevant Skills by name and description, then load only the selected source."}}
{"name":"example-skill","description":"Do X when Y. Do not use for Z.","source":".agents/skills/example-skill/SKILL.md"}
```

A remote Skill uses the same shape with a URL in `source`.

Do not summarize the full Skill body into the route file. `description` should remain the
Skill's own discovery description rather than a separately maintained synopsis.

### Rules

Index Rules primarily when applicability depends on a path/glob selector. The route file
should let a runtime decide whether a Rule applies without loading every Rule body first.

For glob-scoped Rules, preserve `source` and normalized glob selectors:

```json
{"_meta":{"kind":"rules","instructions":"Match known target paths against globs, then load only matching Rule sources."}}
{"source":".agents/rules/python.md","globs":["**/*.py","**/*.pyi"]}
```

Read selectors from authoritative Rule metadata such as `globs`, `applyTo`, or an
equivalent repository convention. Normalize only the route representation; do not change
the Rule's own selector semantics.

Do not add global or non-path Rules merely to make the route file a complete catalog
unless the repository actually needs them for discovery. Do not copy Rule policy text
into the route file.

## Automation

When source assets can change and generated route files are committed, prefer
deterministic generation over manual maintenance.

The generator should derive:

- Skill entries from canonical `name`, `description`, and `source`;
- Rule entries primarily from canonical path/glob selectors and `source`;
- the reserved `_meta` header deterministically.

Use the repository's existing language and automation surface when practical. Keep the
generator small and idempotent. Prefer one generator when Skill and Rule routes share the
same source-discovery logic.

Add the smallest CI drift check that can prove committed route files match canonical
sources. Reuse an existing workflow when possible instead of creating another workflow.

Do not require generation or CI for static routes intentionally maintained by another
authoritative mechanism.

## Workflow

1. Inspect repository instructions, asset roots, existing routes, scripts, and CI.
2. Determine which compatibility responsibilities are actually missing.
3. Create or update the minimal root `CHATBOT.md` router.
4. Add or repair only the route files required by the repository.
5. Add generation and drift validation only where route drift is a real possibility.
6. Validate idempotence, routing metadata, and authority boundaries.

## Validation

Verify that:

- `CHATBOT.md` is root-only and minimal;
- native harness behavior is not duplicated;
- `.agents/routes/skills.jsonl` reflects canonical Skill `name` and `description` metadata;
- `.agents/routes/rules.jsonl` reflects canonical path/glob selectors;
- the first line is a reserved `_meta` header, not an asset entry;
- each asset entry has one valid `source` locator;
- route files contain only routing metadata and concise routing instructions;
- generated routes are deterministic when generation is used;
- CI detects stale committed routes when CI validation is used;
- no project policy, Skill body, or Rule body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
