---
name: mols-ci-design
description: >-
  Design lightweight, risk-proportional CI with strict admission to main and an
  implementation-ready handoff. Use for CI planning, review, or redesign involving tests,
  evals, change-impact routing, evidence boundaries, and maintenance automation. Do not
  implement workflows unless explicitly requested.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols CI Design

Design the lightest CI that preserves strict admission to `main` and provides enough automated evidence for safe delegated development.

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

- Treat `main`, or the target's established equivalent integration branch, as the strict admission boundary.
- Identify failures that would make a change unacceptable on that boundary and require blocking pre-merge evidence for them.
- Optimize verification scope, cost, and latency without lowering the admission standard.
- Use risk-proportional verification: low-risk or non-semantic changes should not pay for unrelated checks.
- Prefer the cheapest evidence that can prove each required claim, and keep different evidence tiers distinct.
- Make impact routing fail-safe: when affected scope is uncertain, broaden validation rather than silently skip relevant checks.
- Keep pure style or formatting out of merge evidence unless representation affects parseability, correctness, or an explicit contract.
- Reuse repository-native checks, validators, providers, and conventions before adding machinery.
- Do not create workflows, scripts, tests, eval fixtures, secrets, or branch rules unless implementation is explicitly requested.

## Resources

Read only what the current design needs.

- [Principles](references/principles.md) — admission boundary, evidence tiers, selection rules, safety, and authority boundaries.
- [Patterns](references/patterns.md) — reusable CI architectures and impact-routing patterns.
- [Handoff](references/handoff.md) — implementation-ready output contract.

## Workflow

1. Resolve arguments and inspect the target.
1. Inventory relevant change surfaces and existing verification; record what each check actually proves.
1. Classify failures by whether they would make a change unacceptable on `main` or its equivalent integration branch.
1. Map merge-critical failures to blocking evidence, then choose the cheapest sufficient check and smallest maintainable impact routing.
1. Place broader, expensive, stochastic, or maintenance work outside the merge gate when it does not affect admission.
1. Define triggers, permissions, secrets, concurrency, caching, matrices, and timeouts only where they materially affect the design.
1. Produce one repository-specific handoff using `references/handoff.md`.
1. Review against `references/principles.md`; remove duplicated checks, speculative machinery, stale path coupling, and claims stronger than the evidence.

## Validation

Before finalizing, verify that:

- every known failure that would make the change unacceptable on `main` has blocking pre-merge evidence;
- optimization reduces execution cost or scope, not the admission standard;
- low-risk changes do not trigger unrelated expensive checks;
- uncertain impact broadens validation instead of creating a silent coverage gap;
- merge gates use the least privilege practical;
- runtime claims require runtime evidence;
- known merge-critical verification cannot be silently omitted from delegated changes by impact routing;
- the plan can be implemented incrementally without an unrelated framework migration.

Stop at the handoff unless implementation is explicitly requested.
