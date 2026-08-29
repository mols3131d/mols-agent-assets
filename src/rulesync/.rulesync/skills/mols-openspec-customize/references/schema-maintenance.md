---
description: >-
  Reusable maintenance guidance for an OpenSpec custom schema that already exists
  or has been chosen as a durable project surface. Load when deciding whether the
  schema package needs a README or nearby docs, separating runtime inputs from
  maintainer material, assigning one owner per concern, or maintaining a forked
  schema over time. Do not use to decide whether a custom schema is needed, for
  exact schema fields or CLI behavior, or for dogfood and tuning methodology.
---

# OpenSpec Schema Maintenance

Use this reference after a custom schema is already the right owner and its
**maintainability as a project-owned package** matters.

It does not define OpenSpec schema semantics. Exact runtime inputs, resolution,
commands, and version-specific behavior belong to
[Official customization](official-customization.md).

## Start with only the schema runtime needs

A simple custom schema may correctly contain only its OpenSpec runtime inputs.
Do not add documentation or maintenance files merely because the schema is custom.

When optional companion material reduces real user or maintainer cost, a project may
use a shape such as:

```text
openspec/schemas/<name>/
├── schema.yaml
├── templates/
├── README.md       # optional
└── docs/           # optional
```

`README.md` and `docs/` are project-owned maintenance surfaces, not required OpenSpec
schema inputs. Do not rely on them for runtime behavior unless the relevant OpenSpec
version explicitly defines such behavior.

## Add a README only when it earns the entrypoint role

Add `README.md` when the schema cannot be understood efficiently from its runtime
files alone and users or maintainers benefit from a human-readable entrypoint.

A useful README should answer only the high-value questions:

1. What is this schema for?
1. When should it be used or avoided?
1. What is intentionally different about its workflow or artifact flow?
1. Where should a maintainer go for deeper detail or governing project authority?

It may briefly point to how the schema is inspected, validated, or dogfooded, but do
not copy fast-changing CLI documentation into it.

Treat the README as a human-readable entrypoint. An agent may read it while already
inspecting the package, but agent discovery and instruction precedence remain owned
by the active repository and harness.

## Add nearby docs only for durable detail

Use `docs/` only when durable supporting knowledge belongs near the schema but would
make the README harder to read or maintain.

Do not prescribe a standard document set, filenames, or taxonomy. Let the concrete
schema, project needs, and repository documentation conventions determine whether
another document is justified and what it should be called.

When `docs/` exists:

- keep only information with a concrete maintenance or comprehension benefit;
- give each concern one authoritative home;
- link useful detail from the README when the README exists;
- keep transient logs, disposable experiments, and regenerable state elsewhere.

If no durable detail justifies another document, omit `docs/` entirely.

## Keep runtime and explanation separate

Give each concern one owner.

| Concern | Preferred owner |
| --- | --- |
| What the schema is, who it is for, when to use it, and package navigation | `README.md` when needed |
| Durable supporting detail that would overload the entrypoint | `docs/` when needed |
| Actual OpenSpec schema behavior | OpenSpec schema inputs for the target version |
| Repository-wide or harness-specific agent policy | Existing repository authority |

Prefer links over copies. If a fact must affect OpenSpec runtime behavior, put it in
the runtime owner even when it is also explained to humans elsewhere. Colocation
does not make maintenance prose part of the runtime contract.

## Treat a schema fork as an owned snapshot

A project-local fork is an intentionally owned copy, not a live extension of its
built-in source. Do not assume routine OpenSpec updates will merge future built-in
improvements into it.

Compare upstream deliberately and port only changes that still fit the project.
Record fork provenance only when it materially reduces future maintenance cost; do
not create provenance ceremony for a schema whose origin is obvious and cheap to
recover.

## Boundaries and handoff

- To decide whether configuration or a custom schema should own a behavior, use
  [Customization design](customization-design.md).
- To evaluate the schema against real work, tune it, or verify regressions, use
  [Dogfood and tuning](dogfood-and-tuning.md).
- For exact schema commands, fields, resolution, or version-specific behavior, use
  [Official customization](official-customization.md).

Do not turn schema maintenance into a second project documentation framework. Add
only surfaces that make this particular schema materially easier to understand or
maintain.
