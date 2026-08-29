---
description: >-
  Reusable OpenSpec customization design guidance. Use when choosing the smallest
  customization surface, deciding config versus schema, keeping project context
  delta-only, maintaining custom schemas, dogfooding, tuning, or verifying a
  customization. This reference provides design heuristics, not exact OpenSpec
  commands, fields, paths, or version-specific behavior.
---

# OpenSpec Customization Patterns

Use this reference for **how to design and maintain OpenSpec customization** across
projects. It contains reusable heuristics, not vendor requirements or
project-specific policy.

When a decision depends on exact commands, fields, paths, precedence, or supported
behavior, consult [Official customization](official-customization.md).

## Prefer config before a custom schema

Use project configuration when the existing workflow can stay intact and the change
only adds context, artifact guidance, operation guidance, or another project-level
option that OpenSpec already supports.

Use a custom schema only when the artifact set, dependency flow, templates, or
schema-level instructions must materially differ. A schema fork creates another
snapshot to maintain, so do not fork when additive configuration can express the
change.

## Choose the narrowest surface

Put each customization on the smallest supported surface that needs it.

| Needed effect | First surface to consider |
| --- | --- |
| Choose installed workflows or delivery form | Profile |
| Add broad project planning context | Project configuration |
| Add guidance for one artifact | Artifact-scoped project rule |
| Add apply or archive guidance | Operation guidance |
| Select a project schema | Project configuration |
| Change artifacts, dependencies, templates, or schema instructions | Custom schema |
| Preserve policy OpenSpec does not need to inject | Existing repository owner |

This table is a selection heuristic. Confirm exact support through the official
OpenSpec contract when it matters.

## Keep OpenSpec context delta-only

Do not turn OpenSpec configuration into a second project handbook. Keep only context
that should materially shape OpenSpec output, and put narrow rules on narrow
surfaces.

When the active agent can reliably load existing repository guidance, keep that
guidance in its canonical owner and inject only the delta OpenSpec actually needs.

## Keep custom schemas maintainable

Treat a non-trivial project schema as a small maintained package. Keep OpenSpec
runtime inputs separate from optional maintenance material.

Start with only what the schema needs. Add companion surfaces only when they reduce
real user or maintainer cost:

```text
openspec/schemas/<name>/
├── schema.yaml
├── templates/
├── README.md       # optional
└── docs/           # optional
```

`README.md` and `docs/` are project-owned aids, not a required OpenSpec schema
layout. Runtime semantics belong to the OpenSpec-owned schema inputs for the target
version.

### `README.md`: optional schema entrypoint

Add a `README.md` when `schema.yaml` alone is not enough for users or maintainers to
understand the schema.

A useful README answers four questions quickly:

1. What is this schema for?
1. When should I use or avoid it?
1. What is intentionally different about its workflow or artifact flow?
1. Where should I go next for deeper detail or the governing project authority?

It may also show how to begin inspecting, validating, or dogfooding the schema, but
do not duplicate fast-changing CLI reference material.

Treat the README as a human-readable entrypoint, not as an agent-runtime contract.
An agent may read it when already inspecting the package, but automatic discovery
and instruction precedence belong to the active repository and harness.

### `docs/`: optional supporting detail

Add `docs/` only when durable supporting knowledge is useful near the schema but
would make the README harder to read or maintain.

Do not prescribe a standard document set, filenames, or taxonomy. Let the concrete
schema, project needs, and repository documentation conventions determine what goes
there.

If `docs/` exists:

- keep only information with a concrete maintenance or comprehension benefit;
- give each concern one authoritative home;
- link useful detail from the README;
- keep transient logs, disposable experiments, and regenerable state elsewhere.

If no durable detail justifies another document, omit `docs/` entirely.

### One concern, one owner

| Concern | Preferred owner |
| --- | --- |
| What the schema is, who it is for, when to use it, and package navigation | `README.md` |
| Durable detail that would overload the entrypoint | `docs/` |
| Actual OpenSpec schema behavior | OpenSpec schema inputs for the target version |
| Repository-wide or harness-specific agent policy | Existing repository authority |

Prefer links over copies. If a fact must affect runtime behavior, put it in the
runtime owner even when it is also explained for humans elsewhere.

Omit any companion surface that does not earn its maintenance cost. A simple schema
may correctly contain only `schema.yaml` and `templates/`.

## Preserve project authority

OpenSpec customization should adapt to repository policy, not become a competing
owner of testing, architecture, security, documentation, language, contribution,
or other project rules.

If the same rule appears in project instructions, OpenSpec configuration, and a
schema template, identify the real owner. Remove accidental copies unless OpenSpec
needs a deliberate operational copy.

## Treat schema forks as owned snapshots

A project-local custom schema is an intentionally owned copy. Do not assume routine
OpenSpec updates will merge later built-in improvements into it.

Keep shared schemas versioned with the project. Compare upstream deliberately and
port only changes that still fit. Record fork provenance only when it materially
reduces future maintenance cost.

## Dogfood before stabilizing

Tune against real project work before treating a customization as settled. Choose a
small representative set for information value, for example:

- ordinary work;
- a case that stresses the intended customization;
- a near-miss or edge case when overfitting is plausible.

For each material friction point:

1. capture the observed behavior or maintainer difficulty;
1. state the expected behavior and why it matters;
1. identify the narrowest owner: project config, schema graph, template, schema
   instruction, repository policy, or something outside OpenSpec;
1. make the smallest change at that owner;
1. rerun the relevant case and check likely regressions.

Do not compensate for a template problem with global context, or for a repository
policy problem with duplicated schema instructions.

## Tune from evidence, not taste

Prefer observable failure modes over vague goals such as "make the model smarter"
or "improve the prompt." Useful signals include repeated omissions, irrelevant
boilerplate, bad dependency timing, template friction, recurring manual correction,
or an improvement in one case that harms another.

Change one meaningful owner at a time when practical so effects stay attributable.
Preserve a baseline for material workflow comparisons. Stop adding guidance when the
remaining failure belongs outside OpenSpec or further tuning has no credible benefit.

## Verify resolved behavior

Match the evidence to the claim. Static YAML review alone does not prove resolved
workflow behavior.

1. Validate schema or config structure when machine-checkable validation exists.
1. Inspect resolved schema, templates, or instructions when selection and precedence
   matter.
1. Run representative dogfood cases for artifact quality and project fit.
1. Review whether the customization remains understandable and maintainable.

Use current official CLI syntax when commands are needed rather than freezing
experimental behavior into this pattern.
