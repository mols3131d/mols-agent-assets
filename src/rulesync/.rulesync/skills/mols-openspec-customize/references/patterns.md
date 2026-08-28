# OpenSpec Customization Patterns

Use these as reusable design heuristics, not OpenSpec requirements. Confirm exact
fields, commands, paths, and supported behavior through [Official](official.md).

## Config before schema

Prefer project configuration when the existing workflow can stay intact and the
change only adds context, artifact guidance, operation guidance, or another
project-level option supported by OpenSpec.

Use a custom schema when the artifact set, dependency flow, templates, or
schema-level instructions must materially differ. A schema fork creates another
snapshot to own, so do not fork for a change additive configuration can express.

## Narrowest surface

Put a customization on the smallest supported surface that needs it.

| Needed effect | First surface to consider |
| --- | --- |
| Choose installed workflows or delivery form | Profile |
| Add broad project planning context | Project configuration |
| Add guidance for one artifact | Artifact-scoped project rule |
| Add apply or archive guidance | Operation guidance |
| Select a project schema | Project configuration |
| Change artifacts, dependencies, templates, or schema instructions | Custom schema |
| Preserve policy OpenSpec does not need to inject | Existing repository owner |

This is a selection heuristic, not a replacement for OpenSpec's current contract.

## Delta-only context

Do not turn OpenSpec configuration into a second project handbook. Keep only
context that should materially shape OpenSpec output, and put narrow rules on
narrow surfaces.

When the active agent can reliably load existing repository guidance, prefer that
canonical owner and inject only the delta OpenSpec actually needs.

## Maintainable schema package

Treat a non-trivial project schema as a small maintained package while keeping
OpenSpec runtime inputs distinct from maintainer material.

A useful team-owned shape can be:

```text
openspec/schemas/<name>/
├── schema.yaml
├── templates/
├── README.md
└── docs/
    ├── scenarios.md
    ├── tuning.md
    └── upstream.md
```

The extra files are optional examples, not a required layout. Under the current
contract, only `schema.yaml` and referenced templates are schema semantics;
`README.md` and `docs/` are project-owned companion surfaces.

Use `README.md` when the schema is shared, substantially customized, or difficult
to understand from `schema.yaml` alone. Keep it focused on maintainer needs:

- purpose and when to use or avoid the schema;
- artifact flow and intentional differences;
- source or fork baseline when useful for future upgrades;
- project-specific invariants not obvious from the runtime files;
- how maintainers verify and dogfood changes with the current OpenSpec tooling.

Use `docs/` only when durable material outgrows the README. Typical roles are:

- `scenarios.md` — a small representative dogfood set and what each case is meant
  to exercise;
- `tuning.md` — accepted findings, decisions, and rejected alternatives worth
  remembering, not every experiment log;
- `upstream.md` — fork provenance and porting notes when upstream drift is a real
  maintenance concern.

Omit files that do not earn their maintenance cost. Do not assume OpenSpec loads
companion documentation. If information must affect runtime behavior, put it in the
OpenSpec surface that actually owns that behavior.

## Preserve project authority

OpenSpec customization should adapt to repository policy, not become a competing
owner of testing, architecture, security, documentation, language, contribution,
or other project rules.

If the same rule appears in project instructions, OpenSpec configuration, and a
schema template, identify the actual owner and remove accidental copies unless
OpenSpec needs a deliberate operational copy.

## Treat schema forks as owned snapshots

A project-local custom schema is an intentionally owned copy. Do not assume normal
OpenSpec updates will merge later built-in improvements into it.

Keep shared schemas versioned with the project. Compare upstream deliberately and
port only changes that still fit. Record fork provenance only when it materially
reduces future maintenance cost.

## Dogfood before stabilizing

Tune against real project work before treating a customization as settled. Use a
small representative set chosen for information value: ordinary work, a case that
stresses the intended customization, and a near-miss or edge case when overfitting
is plausible.

For each material friction point:

1. capture the observed instruction, artifact, workflow behavior, or maintainer
   difficulty;
1. state the expected behavior and why the project needs it;
1. classify the narrowest owner: project config, schema graph, template, schema
   instruction, repository policy, or something outside OpenSpec;
1. make the smallest change at that owner;
1. rerun the relevant case and check likely regressions in the representative set.

Do not compensate for a template problem with global context, or for a repository
policy problem with duplicated schema instructions.

## Tune from evidence, not taste

Prefer observable failure modes over vague goals such as "make the model smarter"
or "improve the prompt." Useful signals include repeated omissions, irrelevant
boilerplate, bad dependency timing, template editing friction, recurring manual
correction, or an improvement in one case that harms another.

Change one meaningful owner at a time when practical so effects stay attributable.
Preserve a baseline for material workflow comparisons. Stop adding guidance when
remaining failures belong outside OpenSpec or further tuning has no credible
benefit.

## Verify resolved behavior

Static YAML review proves less than resolved workflow behavior. Use evidence
appropriate to the claim:

1. schema/config validation for machine-checkable structure;
1. schema, template, or instruction resolution for what OpenSpec actually selects;
1. representative dogfood runs for artifact quality and project fit;
1. maintainer review for whether the customization remains understandable and
   upgradeable.

Use current official CLI syntax rather than freezing experimental command behavior
into this pattern.
