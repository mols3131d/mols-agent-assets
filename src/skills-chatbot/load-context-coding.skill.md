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

This Skill contributes **coding judgment context**. The active task owns repository discovery, implementation, testing, review workflow, Git operations, tool calls, and final output.

## Decision Order

Treat explicit requirements, behavioral contracts, correctness, safety, and required compatibility as constraints. Within them, prefer code that is:

1. clear about what it does and why;
1. no more complex than the current problem requires;
1. easy to change correctly;
1. testable and diagnosable;
1. consistent with the surrounding system;
1. efficient where evidence or a hard constraint makes efficiency material.

Do not improve a lower-priority property by silently degrading a higher-priority constraint.

## Engineering Lens

- **Fit the system** — inspect existing boundaries, callers, data flow, failure behavior, and local conventions before adding a new pattern.
- **Make the smallest coherent change** — minimize conceptual surface, not line count.
- **Avoid speculative generality** — add abstraction, configuration, extension points, concurrency, caching, or dependencies only when current evidence justifies their lifecycle cost.
- **Make boundaries explicit** — keep responsibility, inputs, outputs, state ownership, side effects, invariants, and error behavior understandable.
- **Design for change** — prefer low coupling, reversible decisions, and interfaces that match the problem domain.
- **Keep failures operable** — preserve enough context to diagnose, recover, and verify failures.
- **Treat tests as maintained code** — validate changed behavior at the cheapest useful level and keep tests simple enough to fail for the right reason.
- **Use comments for missing context** — explain rationale, constraints, non-obvious invariants, compatibility, or external contracts; prefer clear code for what happens.

## Change Discipline

- Preserve existing behavior unless the requested change intentionally alters it.
- Separate functional change from substantial mechanical refactoring when combining them would materially hinder review, rollback, diagnosis, or correctness checks.
- Prefer local duplication over premature shared abstraction. Centralize only when a stable shared concept or authoritative rule is visible.
- Prefer a good existing convention over new configuration when both satisfy the need.
- Add a dependency only when it removes more implementation, maintenance, operational, or correctness burden than it introduces.
- Treat measured bottlenecks and explicit performance budgets as stronger evidence than intuition.

## Evidence Checks

Repository and language-specific contracts outrank this general lens. Keep these distinctions explicit:

- required behavior vs. stylistic preference;
- observed failure or measurement vs. hypothetical risk;
- current requirement vs. possible future demand;
- behavior-preserving refactor vs. functional change.

Challenge an existing design or user proposal when a materially simpler, safer, or more operable alternative exists. Do not manufacture objections merely to appear rigorous.

## Boundary

Add domain-specific context only when the code crosses that domain boundary. This Skill contributes engineering judgment, not a separate coding workflow.
