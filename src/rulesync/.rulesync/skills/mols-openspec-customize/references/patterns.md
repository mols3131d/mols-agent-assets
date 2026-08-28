# OpenSpec Customization Patterns

Use these as reusable design heuristics, not OpenSpec requirements. Confirm exact
fields, commands, paths, and supported behavior through [Official](official.md).

## Config before schema

Prefer project configuration when the existing workflow structure can stay intact
and the change only adds context, artifact guidance, operation guidance, or another
project-level option supported by OpenSpec.

Use a custom schema when the planning artifact set, dependency flow, templates, or
schema-level workflow instructions must materially differ.

A schema fork creates another schema snapshot to own, so do not use it for a change
that additive configuration can express.

## Narrowest surface

Put a customization on the smallest supported surface that needs it.

| Needed effect | First surface to consider |
| --- | --- |
| Choose installed workflows or delivery form | Profile |
| Add broadly applicable project planning context | Project configuration |
| Add guidance for one planning artifact | Artifact-scoped project rule |
| Add apply or archive guidance | Operation guidance |
| Select a project schema | Project configuration |
| Change artifacts, dependencies, templates, or schema instructions | Custom schema |
| Preserve repository policy OpenSpec does not need to inject | Existing repository owner |

The table is a selection heuristic, not a replacement for OpenSpec's current
contract.

## Delta-only context

Do not turn OpenSpec configuration into a second project handbook.

Keep only context that should materially shape OpenSpec workflow output. Put narrow
rules on narrow surfaces. When the active agent can reliably load existing
repository guidance, prefer that canonical owner and inject only the delta OpenSpec
actually needs.

## Maintainable schema package

Treat a non-trivial project schema as a small maintained package, while keeping
OpenSpec runtime inputs distinct from maintainer material.

A typical team-owned layout can be:

```text
openspec/schemas/<name>/
├── schema.yaml
├── templates/
├── README.md
└── docs/
    └── ...
```

Only `schema.yaml` and referenced templates are OpenSpec schema semantics unless the
current official contract says otherwise. `README.md` and `docs/` are optional
project-owned companion surfaces.

Use a nearby `README.md` when the schema is shared, substantially different from its
source, or hard to understand from `schema.yaml` alone. Keep it small and useful to
a maintainer, for example:

- purpose and when to use or avoid the schema;
- artifact flow and important intentional differences;
- source or fork baseline when that matters for future upgrades;
- project-specific invariants not obvious from the files;
- how maintainers verify and dogfood changes using the current OpenSpec tooling.

Add `docs/` only when durable rationale, representative scenarios, tuning evidence,
or upstream-port notes no longer fit cleanly in the README. Do not create a docs
hierarchy merely because the schema is custom, and do not dump transient run logs
into durable schema documentation.

## Preserve project authority

OpenSpec customization should adapt to repository policy, not become a competing
owner of testing, architecture, security, documentation, language, contribution,
or other project rules.

If the same rule appears in project instructions, OpenSpec configuration, and a
schema template, identify the actual owner and remove accidental copies unless
OpenSpec needs a deliberate operational copy.

## Treat schema forks as owned snapshots

A project-local custom schema is an intentionally owned copy. Do not assume normal
OpenSpec updates will merge future built-in schema improvements into it.

Keep shared project schemas versioned with the project. When future upstream
improvements matter, compare deliberately and port only changes that still fit the
project. Record a useful fork baseline or provenance when it materially lowers that
future maintenance cost.

## Dogfood before stabilizing

Tune a customization against real project work before treating it as settled.

Use a small representative set of changes that exercises the behavior the
customization is meant to improve. Include ordinary work and, when relevant, a
near-miss or edge case that could reveal over-broad instructions.

For each meaningful friction point:

1. capture the observed instruction, artifact, workflow behavior, or maintainer
   difficulty;
1. state the expected behavior and why the project needs it;
1. classify the actual owner: project config, schema graph, template, schema
   instruction, repository policy, or a problem outside OpenSpec;
1. make the smallest change at that owner;
1. rerun the relevant case and check for regressions in the other representative
   cases.

Do not compensate for a template problem with global context, or for a repository
policy problem with duplicated schema instructions.

## Tune from evidence, not taste

Prefer observable failure modes over vague goals such as "make the model smarter"
or "improve the prompt."

Useful tuning evidence includes:

- an artifact repeatedly omits required project information;
- an instruction causes irrelevant sections or boilerplate;
- a dependency is requested too early or too late;
- a template shape consistently creates editing friction;
- the same project rule must be restated manually during normal use;
- a customization helps one case but harms another representative case.

Change one meaningful owner at a time when practical so the effect stays
attributable. Preserve a baseline when comparing material workflow changes. Stop
adding guidance when remaining failures belong outside OpenSpec or further tuning
has no credible benefit.

## Verify resolved behavior

Static YAML review proves less than resolved workflow behavior.

Use layered evidence appropriate to the claim:

1. schema/config validation for machine-checkable structure;
1. schema, template, or instruction resolution for what OpenSpec actually selects;
1. representative dogfood runs for artifact quality and project fit;
1. maintainer review for whether the customization remains understandable and
   upgradeable.

Use the current official CLI syntax rather than freezing experimental command
behavior into this pattern.
