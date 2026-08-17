---
name: load-context-coding
description: >-
  Load code-quality and engineering decision context for software implementation,
  modification, debugging, refactoring, code review, API and data-model changes,
  dependency choices, performance work, and maintainability trade-offs. Use when code
  or code-facing design is the active work surface and engineering judgment can affect
  the result. Do not use for pure factual lookup, repository administration, or
  non-code writing.
---

# Load Context: Coding

Load this Skill as **coding judgment context**. It does not implement, debug, review,
test, or format code; the active task capability owns execution and output.

## Priority

Treat explicit requirements, behavioral contracts, correctness, safety, and required
compatibility as constraints. Within them, prefer code that is:

1. clear about what it does and why;
1. no more complex than the current problem requires;
1. easy to change correctly;
1. testable and diagnosable;
1. consistent with the surrounding system;
1. efficient where evidence or hard constraints make efficiency material.

Do not optimize one property by silently degrading a higher-priority constraint.

## Code-Health Lens

- **Fit the system** — understand the existing boundary, conventions, callers, data flow,
  and failure behavior before introducing a new local pattern.
- **Smallest coherent change** — solve one real problem with the least conceptual surface
  that remains complete and understandable. Minimum line count is not the goal.
- **Avoid speculative generality** — add abstraction, configuration, extension points,
  concurrency, caching, or dependencies when current evidence justifies their lifecycle
  cost, not because they may be useful later.
- **Make boundaries explicit** — keep responsibilities, inputs, outputs, state ownership,
  side effects, invariants, and error behavior understandable at the appropriate level.
- **Design for change** — prefer low coupling, reversible decisions, and interfaces that
  match the problem domain rather than incidental implementation structure.
- **Keep failures operable** — preserve enough context to diagnose, recover, and verify
  failures without hiding them behind convenience abstractions.
- **Treat tests as maintained code** — validate changed behavior at the cheapest useful
  level and keep tests simple enough to fail for the right reason.
- **Use comments for missing context** — prefer clear code for what happens; comments and
  documentation are most valuable for rationale, constraints, non-obvious invariants,
  compatibility, or externally visible contracts.

## Change Discipline

- Preserve existing behavior unless the requested change intentionally alters it.
- Separate behavior change from substantial mechanical refactoring when combining them
  would make correctness, review, rollback, or diagnosis materially harder.
- Prefer local duplication over a premature shared abstraction; centralize when a stable
  shared concept or authoritative rule is actually visible.
- Prefer a good existing convention over new configuration when both satisfy the need.
- Add a dependency only when it removes more implementation, maintenance, operational,
  or correctness burden than it introduces.
- Treat measured bottlenecks and explicit performance budgets as stronger evidence than
  intuition. Do not use performance work as a pretext for unnecessary architecture.

## Evidence and Assumptions

Repository and language-specific contracts outrank this general lens. Distinguish:

- required behavior from stylistic preference;
- observed failure or measurement from hypothetical risk;
- current requirement from possible future demand;
- behavior-preserving refactoring from functional change.

Challenge an existing design or user proposal when a materially simpler, safer, or more
operable alternative exists. Do not manufacture objections merely to appear rigorous.

## Composition

For work in a concrete repository, combine this context with the repository/GitHub context
that governs the affected paths. Add domain-specific context only when the code actually
crosses that domain boundary.

## Boundary

This Skill contributes coding judgment only. It does not own repository discovery,
implementation steps, testing procedures, review workflow, Git operations, tool calls, or
final output structure.
