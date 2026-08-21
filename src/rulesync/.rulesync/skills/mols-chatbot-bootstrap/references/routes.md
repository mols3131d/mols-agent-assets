# Fallback Route Convention

Use this reference only when a separate routing surface is justified and the target has no
stronger native or established representation.

This is one **mols fallback convention** for deciding which canonical asset to load without
loading every asset body first. It is not a portable chatbot, Skill, Rule, or repository
standard. Reuse a target-native or already-established route/index surface when it can
preserve the same behavior with less local machinery.

## Layout

Fallback target layout:

```text
.agents/routes/
├── ROUTE.md
├── skills.jsonl
└── rules.jsonl
```

`ROUTE.md` is optional. Reuse another established entrypoint or link route files directly
when that is simpler.

Do not create this layout merely for uniformity. A small repository may need only an inline
router, one index, or no separate route asset at all.

## ROUTE.md

When a single entrypoint is useful, keep it small but **actionable**. Reading the entrypoint
must lead to loading the route metadata needed for routing; a passive link list is
insufficient.

Example:

```md
# Routes

When this entrypoint is loaded, immediately read the complete linked route metadata before continuing. Do not stop at this file.

- [Skills](skills.jsonl)
- [Rules](rules.jsonl)

After loading each route file, follow its `_meta.instructions`.
```

Link only route files that actually exist. Do not copy route entries, project policy, or
asset bodies into `ROUTE.md`.

Use a locator the active harness can actually load. Repository-local consumers may use
relative paths; remote chat consumers may need a directly fetchable URL.

## JSONL Header

In this fallback representation, each route file reserves the first line for a `_meta`
object. Remaining lines are route entries.

```jsonl
{"_meta":{"kind":"skills","instructions":"Select task-relevant Skills by name and description, then load only the selected source."}}
```

`ROUTE.md` owns only the bootstrap transition. `_meta.instructions` owns routing behavior
for this route file. The referenced canonical asset owns its own behavior.

Keep `_meta` concise and routing-specific.

## Source Locator

Each fallback route entry uses one `source` field.

- local asset → repository-root-relative path;
- remote asset → URL.

Do not split this into separate `path` and `url` fields unless the target representation
already requires another shape.

## Skills

Route Skills primarily by `name` and `description`.

```jsonl
{"name":"example-skill","description":"Use for X when Y. Do not use for Z.","source":".agents/skills/example-skill/SKILL.md"}
```

For remote assets, keep the same shape and place the URL in `source`.

`description` exists for routing quality. It may be tuned from the canonical Skill
description when needed, but must preserve the Skill's real capability and trigger
boundary. Do not copy the Skill body into the route file.

## Rules

The fallback Rule route shape covers applicability driven by path/glob selectors.

```jsonl
{"source":".agents/rules/python.md","globs":["**/*.py","**/*.pyi"]}
```

Derive selectors from the target repository's authoritative Rule metadata. `globs` and
`applyTo` are common examples, not universal requirements.

Normalize representation only. Do not change applicability semantics or copy Rule policy
text into the route.

Do not force global or non-path Rules into this selector shape. If a target has a real need
to route them, use the target's established representation or define the smallest explicit
local extension instead of inventing fake globs.

## Ordering

Keep generated entries deterministic. Prefer stable source ordering unless the repository
has a stronger routing reason to use another order.
