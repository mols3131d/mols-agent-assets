---
name: mols-chatbot-bootstrap
description: >-
  Bootstrap or update a repository for mols CHATBOT.md compatibility. Use when a
  repository should support chat runtimes that may not automatically load applicable
  AGENTS.md guidance, task-relevant Skills, or path-scoped Rules, including requests to
  create CHATBOT.md, discovery indexes, index generators, or drift-check CI.
---

# Mols Chatbot Bootstrap

Establish the smallest repository-local compatibility harness for chat runtimes.

## Contract

Inspect the repository before changing it. Reuse existing conventions, scripts, indexes,
and CI before creating new ones.

As needed:

- create or update root `CHATBOT.md`;
- expose Skills through a lightweight `INDEX.jsonl` for task-intent discovery;
- expose path/glob-scoped Rules through a lightweight `INDEX.jsonl` for selector-based discovery;
- generate indexes from canonical sources when they can drift;
- add CI validation when committed generated indexes can become stale.

Do not add machinery merely because this Skill lists it. Create only what the repository
actually needs.

`AGENTS.md`, Skills, and Rules remain authoritative. `CHATBOT.md` and indexes are routing
and compatibility surfaces only.

## CHATBOT.md

Keep root `CHATBOT.md` minimal and root-only.

It should recover only harness behavior the active runtime does not already provide:

- load the applicable `AGENTS.md` hierarchy for known target paths;
- discover/load task-relevant Skills;
- discover/load Rules whose selectors match known target paths.

Do not copy project policy, Skill bodies, Rule bodies, full catalogs, or static path tables
into `CHATBOT.md`. Do not invent a `CHATBOT.md → AGENTS.md → README.md` fallback chain.

Treat the responsibilities independently. If the runtime already provides one, recover
only the missing ones.

## Discovery Indexes

An `INDEX.jsonl` is discovery metadata, not a second source of truth. Keep one JSON object
per line and preserve a deterministic order.

Include the source path so the selected asset can be loaded on demand. Do not copy asset
bodies or invent metadata that is not needed for routing.

### Skills

Index Skills for task-intent selection. Derive entries from each Skill's canonical
`SKILL.md` front matter.

Use `name` and `description` as the primary discovery fields, plus the source path:

```json
{"name":"example-skill","description":"Do X when Y. Do not use for Z.","path":".agents/skills/example-skill/SKILL.md"}
```

Do not summarize the full Skill body into the index. The `description` should remain the
Skill's own discovery description rather than a separately maintained synopsis.

### Rules

Index Rules primarily when applicability depends on a path/glob selector. The index should
let a runtime decide whether a Rule applies without loading every Rule body first.

For glob-scoped Rules, preserve the source path and normalized glob selectors:

```json
{"path":".agents/rules/python.md","globs":["**/*.py","**/*.pyi"]}
```

Read the selectors from the Rule's authoritative metadata such as `globs`, `applyTo`, or
an equivalent repository convention. Normalize only the index representation; do not
change the Rule's own selector semantics.

Do not add global or non-path Rules merely to make the index a complete catalog unless the
repository actually needs them for discovery. Do not copy Rule policy text into the index.

## Automation

When source assets can change and generated indexes are committed, prefer deterministic
generation over manual maintenance.

The generator should derive:

- Skill index entries from canonical Skill `name`, `description`, and source path;
- Rule index entries primarily from canonical path/glob selectors and source path.

Use the repository's existing language and automation surface when practical. Keep the
generator small and idempotent. Prefer one generator when Skill and Rule indexes share the
same source-discovery logic.

Add the smallest CI drift check that can prove committed indexes match canonical sources.
Reuse an existing workflow when possible instead of creating another workflow.

Do not require generation or CI for static indexes that are intentionally maintained by
another authoritative mechanism.

## Workflow

1. Inspect repository instructions, asset roots, existing indexes, scripts, and CI.
2. Determine which compatibility responsibilities are actually missing.
3. Create or update the minimal root `CHATBOT.md` router.
4. Add or repair only the discovery indexes required by the repository.
5. Add generation and drift validation only where index drift is a real possibility.
6. Validate idempotence, routing metadata, and authority boundaries.

## Validation

Verify that:

- `CHATBOT.md` is root-only and minimal;
- native harness behavior is not duplicated;
- Skill indexes reflect canonical `name` and `description` metadata;
- Rule indexes reflect canonical path/glob selectors;
- indexes point to canonical sources and contain only routing metadata;
- generated indexes are deterministic when generation is used;
- CI detects stale committed indexes when CI validation is used;
- no project policy, Skill body, or Rule body was duplicated.

Prefer the smallest valid result over a uniform repository layout.
