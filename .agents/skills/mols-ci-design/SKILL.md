---
name: mols-ci-design
description: >-
  Design efficient CI for chatbot and agent development and produce an implementation-ready
  handoff. Use when a repository needs a CI plan, review, or redesign covering tests, evals,
  change-impact routing, runtime evidence, and maintenance automation without implementing
  workflows by default.
---

# Mols CI Design

Design the smallest CI system that gives enough evidence for the target repository, then hand the design to an implementation agent or maintainer.

## Arguments

```yaml
target: <auto>
mode: <auto>
scope: <auto>
provider: <auto>
evals: <auto>
maintenance: <auto>
constraints: <auto>
output: <auto>
```

- `target` — repository or workspace to inspect. `<auto>` uses the active target established by the caller or runtime.
- `mode` — `design`, `review`, `refresh`, or `<auto>`. `<auto>` uses `review` for assessment-only intent, `refresh` when an existing CI design is being updated, otherwise `design`.
- `scope` — explicit asset, subsystem, or repository scope, or `<auto>`. `<auto>` includes only development surfaces that can materially affect the requested CI design.
- `provider` — CI provider such as GitHub Actions, another established provider, `<none>`, or `<auto>`. `<auto>` reuses the target's existing provider when one exists and does not introduce a provider merely to make the design concrete.
- `evals` — `none`, `deterministic`, `smoke`, `full`, or `<auto>`. `<auto>` proposes the cheapest evaluation tier that can cover the behavior risk; model/runtime evaluation is not assumed.
- `maintenance` — `include`, `exclude`, or `<auto>`. `<auto>` includes post-merge generation, formatting, synchronization, or self-writing automation only when the target has a real maintenance need, and keeps it separate from merge gates.
- `constraints` — explicit cost, latency, security, runner, secret, branch, or platform constraints, or `<auto>`. `<auto>` derives only constraints evidenced by the target or caller.
- `output` — handoff destination or `inline`, or `<auto>`. `<auto>` follows the target's established artifact policy when one exists; otherwise return the handoff inline.

Explicit values always win. `<auto>` means inspect first and resolve from evidence, not apply a fixed CI profile.

## Contract

Design and hand off by default. Do not implement CI merely because the design is actionable.

- Inspect repository guidance, CI, tests, evals, scripts, generators, asset roots, and existing validation before proposing replacements.
- Distinguish deterministic correctness, projection/harness compatibility, semantic behavior, and live runtime evidence.
- Prefer deterministic evidence before probabilistic/model-graded evidence.
- Prefer affected checks before exhaustive suites.
- Keep PR feedback smaller than scheduled/manual exhaustive evaluation unless the target requires otherwise.
- Keep validation gates read-only when practical; separate self-writing maintenance automation from merge gates.
- Reuse repository-native tests, validators, and providers before adding new machinery.
- Do not claim runtime behavior from static, structural, or projection-only validation.
- Do not invent exact cost or latency claims without evidence.
- Do not create workflow files, scripts, tests, eval fixtures, secrets, or branch rules unless the caller explicitly expands the task to implementation.

## Resources

Read only the reference needed for the current design.

- [Principles](references/principles.md) — evidence tiers, cost ordering, safety, and design boundaries.
- [Patterns](references/patterns.md) — reusable CI patterns for chatbot and agent repositories.
- [Handoff](references/handoff.md) — implementation-ready output contract and template.

## Workflow

1. Resolve arguments and inspect the target repository before choosing a CI shape.
2. Inventory relevant change surfaces: prompts/instructions, Skills, Rules, Agents, scripts, tests, evals, generated projections, indexes, documentation, and runtime integrations as applicable.
3. Inventory existing verification surfaces and identify what each one actually proves.
4. Classify likely failures by the cheapest evidence capable of detecting them.
5. Design change-impact routing so each change triggers the smallest sufficient checks.
6. Separate PR gates, broader main-branch checks, scheduled/manual evaluation, and maintenance automation when those responsibilities exist.
7. Add semantic or runtime eval only where deterministic evidence cannot cover the important risk.
8. Define provider-specific triggers, permissions, concurrency, secrets, caches, matrices, and timeouts only after the architecture is clear.
9. Produce an implementation-ready handoff using `references/handoff.md`.
10. Review the design for stale path coupling, duplicated checks, unnecessary matrices, write permissions, hidden model cost, and claims stronger than the evidence.

## Decision Rules

Use these defaults unless target evidence justifies a different choice:

- deterministic before probabilistic;
- affected before exhaustive;
- PR smoke before full matrix;
- validation before self-writing automation;
- convention-based impact mapping before a new dependency manifest;
- existing provider/tooling before a new CI stack;
- no cache until repeated setup cost is material;
- no model grader when deterministic assertions are sufficient.

These are design defaults, not universal requirements. Preserve stronger target-specific constraints.

## Output

Produce one handoff that is specific enough to implement without repeating repository discovery.

The handoff should include:

- current-state evidence and relevant repository paths;
- goals and explicit non-goals;
- failure/evidence model;
- proposed CI architecture and responsibility boundaries;
- change-to-check impact mapping;
- workflow/job designs with triggers, permissions, dependencies, and failure semantics;
- eval strategy and evidence boundaries;
- maintenance automation separated from merge gates;
- implementation order;
- acceptance criteria;
- unresolved decisions, assumptions, and risks.

Prefer concrete repository-specific references over generic CI advice. Keep implementation syntax illustrative unless exact syntax is necessary to remove ambiguity.

## Validation

Before finalizing the handoff, verify that:

- every proposed check has a failure class it is meant to detect;
- expensive checks have a reason they cannot be replaced by cheaper evidence;
- changed assets can be mapped to checks without fragile unexplained coupling;
- semantic tuning is not rejected by byte-for-byte baseline checks unless byte identity is the real contract;
- runtime claims require runtime evidence;
- merge gates do not need write permission unless there is a demonstrated exception;
- maintenance automation cannot silently redefine canonical source authority;
- the design can be implemented incrementally rather than requiring a framework migration first.

Stop at the handoff unless implementation is explicitly requested.
