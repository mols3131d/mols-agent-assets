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
OpenSpec runtime inputs distinct from optional maintenance material.

Start with only the files the schema actually needs. Add companion surfaces only
when they reduce real user or maintainer cost:

```text
openspec/schemas/<name>/
├── schema.yaml
├── templates/
├── README.md       # optional
├── AGENTS.md       # optional
└── docs/           # optional
    ├── scenarios.md
    ├── tuning.md
    └── upstream.md
```

`README.md`, `AGENTS.md`, `docs/`, and the example files under `docs/` are not a
required schema layout. Under the current OpenSpec contract, schema runtime
semantics belong to `schema.yaml` and referenced templates. Companion surfaces are
project-owned aids and should exist only when they materially improve schema use or
maintenance.

### `README.md`: user-facing entrypoint

Use `README.md` when users or maintainers benefit from an introduction that
`schema.yaml` alone does not provide. It is the default human-facing entry document
for the schema package.

It can explain:

- what the schema is for and the kinds of work it supports;
- when a user should choose it, and important cases where they should not;
- the artifact flow and the schema's intentional differences at a useful overview
  level;
- how to start using, inspecting, validating, or dogfooding it without duplicating
  fast-changing CLI reference material;
- where deeper material lives in `docs/`;
- maintenance or fork provenance only when it is useful to readers of the entry
  document.

Keep README readable as an introduction. Move detailed tuning history, scenario
catalogs, upgrade notes, or long rationale into `docs/` rather than turning the
entrypoint into a maintainer dump.

### `AGENTS.md`: agent-only scoped guidance

Use `AGENTS.md` only when agents working inside the schema directory need local
instructions that are not already determined by repository-wide guidance or the
schema files themselves. Its scope and discovery semantics belong to the active
agent harness and repository policy; do not assume the OpenSpec CLI reads it.

Good candidates are agent-only working rules such as:

- which schema surfaces an agent may edit for different kinds of failures;
- local validation or dogfood expectations before accepting a change;
- invariants that matter specifically while modifying or tuning this schema;
- local editing boundaries that would be noise in a user-facing README.

Do not copy user documentation, durable rationale, or general repository policy
into `AGENTS.md`. If humans and agents both need the information, put it in
`README.md`, `docs/`, or another canonical project owner and let `AGENTS.md` point
to that source when necessary.

### `docs/`: durable detail

Use `docs/` when durable schema knowledge is useful but too detailed for the
README. It is a supporting documentation surface, not an automatic schema contract
or a dumping ground for every experiment.

Possible documents include:

- `scenarios.md` — representative dogfood or regression scenarios worth preserving;
- `tuning.md` — accepted tuning decisions and rationale that future maintainers may
  need to reproduce or reconsider;
- `upstream.md` — fork provenance, upstream comparison, and deliberate porting notes.

These filenames are examples. Create only the documents with durable value. Keep
transient run logs and disposable experiments in the project's existing working
artifact surface instead.

### Keep companion surfaces DRY

Give each concern one owner:

| Concern | Preferred owner |
| --- | --- |
| What the schema is, who it is for, how to enter and navigate it | `README.md` |
| Agent-only local editing or tuning behavior | `AGENTS.md` |
| Detailed durable scenarios, rationale, maintenance, or upgrade knowledge | `docs/` |
| Actual OpenSpec schema behavior | `schema.yaml` and `templates/` |
| Repository-wide policy | Existing repository authority |

Prefer links over copies across these surfaces. A fact that must affect OpenSpec
runtime behavior belongs in the runtime surface even if it is also explained to
humans elsewhere. A maintenance explanation does not become runtime behavior merely
because it is colocated with the schema.

Omit any companion surface that does not earn its maintenance cost. A simple schema
may correctly contain only `schema.yaml` and `templates/`.

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
