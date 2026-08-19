# Route Convention

Use route assets to decide which canonical asset to load without loading every asset first.

## Layout

Default target layout:

```text
.agents/routes/
├── ROUTE.md
├── skills.jsonl
└── rules.jsonl
```

This is a default convention for the **target workspace**, not a requirement for the repository that packages this Skill.

`ROUTE.md` is the default single entrypoint when that is useful. It is not mandatory.
Repositories may reuse another routing entrypoint or link route files directly.

## ROUTE.md

Create or update `ROUTE.md` in the target workspace only when a single route entrypoint is useful.
Do not create it merely because this Skill is installed or packaged.

Keep `ROUTE.md` small. It should identify available route assets and how to consume them.

Example:

```md
# Routes

- [Skills](skills.jsonl) — select task-relevant Skills, then load the selected `source`.
- [Rules](rules.jsonl) — match target paths against selectors, then load matching `source` entries.
```

Link only route assets that actually exist or are being created as part of the same bootstrap operation.
Do not move project policy or asset bodies into `ROUTE.md`.

## JSONL Header

Each route file reserves the first line for a `_meta` object. Remaining lines are route entries.

```jsonl
{"_meta":{"kind":"skills","instructions":"Select task-relevant Skills by name and description, then load only the selected source."}}
```

Keep `_meta` concise and routing-specific.

## Source Locator

Every route entry uses one `source` field.

- local asset → repository-root-relative path;
- remote asset → URL.

Do not split this into separate `path` and `url` fields.

## Skills

Route Skills primarily by `name` and `description`.

```jsonl
{"name":"example-skill","description":"Use for X when Y. Do not use for Z.","source":".agents/skills/example-skill/SKILL.md"}
```

For remote assets, keep the same shape and place the URL in `source`.

`description` exists for routing quality. It may be tuned from the canonical Skill description when needed, but must preserve the Skill's real capability and trigger boundary.

Do not copy the Skill body into the route file.

## Rules

Route Rules primarily when applicability depends on path/glob selectors.

```jsonl
{"source":".agents/rules/python.md","globs":["**/*.py","**/*.pyi"]}
```

Derive selectors from the target repository's authoritative Rule metadata. `globs` and `applyTo` are common examples, not universal requirements.

Normalize representation only. Do not change applicability semantics or copy Rule policy text into the route.

Global or non-path Rules do not need entries unless they have a real discovery need.

## Ordering

Keep generated entries deterministic. Prefer stable source ordering unless the repository has a stronger routing reason to use another order.
