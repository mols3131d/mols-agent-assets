# v2.1 General Review

## Initial Verdict

`Revise`

## Findings Closed

### G21-001 — High — Legacy consolidation behavior was only implied

Added a first-class `consolidate` mode, decision vocabulary, migration plan,
route test template, and warning-only candidate analyzer.

### G21-002 — High — Behavior-preserving compression lacked enforceable invariants

Added a semantic preservation contract, invariant template, and literal/path/
heading/regex/order checker.

### G21-003 — High — Structural hygiene was not a release gate

Added nested-skill, symlink, cache, empty-directory, zero-byte, orphan, operation
discovery, and test-evidence auditing. Hard structural findings now participate in
runtime skill validation; packaging blocks unresolved structural warnings by
default.

### G21-004 — High — Packaging was not byte reproducible

Added normalized timestamps, permissions, file order, descriptor serialization,
and canonical JSON. Skill and bundle reproducibility have regression tests.

### G21-005 — Medium — Naming, script ROI, rollback, and host validators were implicit

Added project-first fallback naming, determinism guidance, Git-first conditional
rollback, validated argv command plans, and an explicit host runner.

## Closure Verdict

`Pass` after correction and regression validation.
