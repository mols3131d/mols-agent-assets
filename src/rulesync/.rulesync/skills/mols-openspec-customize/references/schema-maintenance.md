---
description: >-
  Maintenance guidance for an OpenSpec custom schema that already exists or has
  been chosen as a durable project surface. Load when deciding whether the package
  needs a README or nearby docs, separating runtime inputs from maintainer material,
  or maintaining the owned schema over time. Do not use to decide whether a custom
  schema is needed, for exact schema or CLI behavior, or for dogfood methodology.
---

# OpenSpec Schema Maintenance

Use this reference after a custom schema is already the right owner and its
**maintainability as a project-owned package** matters. Exact schema semantics and
version-specific behavior belong to [Official contract](official-contract.md).

## Start with runtime inputs only

A simple custom schema may need only its OpenSpec runtime inputs. Do not add
maintenance files merely because the schema is custom.

When companion material reduces real user or maintainer cost, a project may use:

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

## Add a README only when it helps readers enter the package

Use `README.md` when the runtime files alone do not let users or maintainers quickly
answer:

1. What is this schema for?
1. When should it be used or avoided?
1. What is intentionally different about its workflow or artifact flow?
1. Where is deeper detail or the governing project authority?

Keep the README focused on orientation and navigation. It may point to inspection,
validation, or dogfooding, but should not duplicate fast-changing CLI reference
material.

Treat it as a human-readable entrypoint, not an agent-runtime contract. Agent
discovery and instruction precedence remain owned by the active repository and
harness.

## Add nearby docs only when the README would otherwise become worse

Use `docs/` only for durable supporting detail that belongs near the schema but would
make the README harder to read or maintain. Do not prescribe filenames or a standard
document taxonomy; follow the concrete project's documentation conventions.

Keep transient logs, disposable experiments, and regenerable state outside this
durable documentation surface.

## Keep one owner per concern

| Concern | Preferred owner |
| --- | --- |
| What the schema is, when to use it, and package navigation | `README.md` when needed |
| Durable supporting detail that would overload the entrypoint | `docs/` when needed |
| Actual OpenSpec schema behavior | OpenSpec schema inputs for the target version |
| Repository-wide or harness-specific agent policy | Existing repository authority |

Prefer links over copies. If a fact must affect runtime behavior, put it in the
runtime owner even when it is also explained for humans elsewhere.

## Maintain the owned schema deliberately

Treat future changes to an owned custom schema as explicit maintenance decisions.
When update, fork, shadowing, or resolution semantics affect a decision, verify the
target OpenSpec version through [Official contract](official-contract.md).

Record provenance only when it materially reduces future maintenance cost; do not
create provenance ceremony when the origin is obvious and cheap to recover.

## Related references

- Need to decide whether configuration or a schema should own a behavior →
  [Customization design](customization-design.md)
- Need to evaluate or tune the schema against real work →
  [Dogfood and tuning](dogfood-and-tuning.md)
- Need exact schema commands, fields, resolution, or version behavior →
  [Official contract](official-contract.md)
