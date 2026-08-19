---
name: mols-ci-design
description: >-
  Design efficient CI for chatbot and agent repositories and produce an implementation-ready
  handoff. Use for CI planning, review, or redesign involving tests, evals, change-impact
  routing, evidence boundaries, and maintenance automation. Do not implement workflows unless
  explicitly requested.
---

# Mols CI Design

Design the smallest CI system that provides enough evidence for the target, then hand the design to an implementation agent or maintainer.

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

- `target` — repository or workspace to inspect. `<auto>` uses the active target.
- `mode` — `design`, `review`, `refresh`, or `<auto>`. `<auto>` uses `review` for assessment-only intent, `refresh` for an existing design being updated, otherwise `design`.
- `scope` — asset, subsystem, or repository scope, or `<auto>`. `<auto>` includes only surfaces that can materially affect the requested design.
- `provider` — established CI provider, `<none>`, or `<auto>`. `<auto>` reuses the target provider when one exists and does not introduce one only to make the design concrete.
- `evals` — `none`, `deterministic`, `smoke`, `full`, or `<auto>`. `<auto>` selects the cheapest evaluation depth that covers the evidenced behavior risk.
- `maintenance` — `include`, `exclude`, or `<auto>`. `<auto>` includes write-back automation only when the target has a real maintenance need and keeps it separate from merge gates.
- `constraints` — explicit cost, latency, security, runner, secret, branch, or platform constraints, or `<auto>`. `<auto>` derives only evidenced constraints.
- `output` — handoff destination, `inline`, or `<auto>`. `<auto>` follows established artifact policy when one exists; otherwise return the handoff inline.

Explicit values win. `<auto>` means inspect first and resolve from evidence, not apply a fixed CI profile.

## Contract

Design and hand off by default.

- Inspect repository guidance, CI, tests, evals, scripts, generators, asset roots, and existing validation before proposing changes.
- Map each important failure class to the cheapest evidence that can detect it.
- Separate merge gates, broader regression, semantic/runtime evaluation, and write-capable maintenance when those responsibilities exist.
- Reuse repository-native checks, validators, providers, and conventions before adding machinery.
- Treat static, deterministic, projection, semantic, and live-runtime evidence as distinct claims.
- Define provider-specific syntax only after the CI architecture is clear.
- Do not create workflows, scripts, tests, eval fixtures, secrets, or branch rules unless implementation is explicitly requested.

## Resources

Read only what the current design needs.

- [Principles](references/principles.md) — evidence tiers, selection rules, safety, and authority boundaries.
- [Patterns](references/patterns.md) — reusable CI architectures and impact-routing patterns.
- [Handoff](references/handoff.md) — implementation-ready output contract.

## Workflow

1. Resolve arguments and inspect the target.
2. Inventory relevant change surfaces and existing verification; record what each check actually proves.
3. Map likely failures to evidence tiers and design the smallest maintainable change-to-check routing.
4. Select only the CI patterns needed for those failures and separate PR, broader regression, expensive eval, and maintenance responsibilities as applicable.
5. Define triggers, permissions, secrets, concurrency, caching, matrices, and timeouts only where they materially affect the design.
6. Produce one repository-specific handoff using `references/handoff.md`.
7. Review against `references/principles.md`; remove duplicated checks, speculative machinery, stale path coupling, and claims stronger than the evidence.

## Validation

Before finalizing, verify that:

- every proposed check owns a real failure class;
- expensive or stochastic checks have a reason cheaper evidence is insufficient;
- impact routing is understandable and maintainable for the target;
- merge gates use the least privilege practical;
- runtime claims require runtime evidence;
- the plan can be implemented incrementally without an unrelated framework migration.

Stop at the handoff unless implementation is explicitly requested.
