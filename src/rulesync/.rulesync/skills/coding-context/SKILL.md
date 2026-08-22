---
name: coding-context
description: >-
  Mandatory coding-scope baseline context for engineering judgment. Always load for any
  task whose active work surface includes code or code-facing software design,
  including code analysis or explanation, implementation, modification, debugging,
  testing, refactoring, code review, API or data-model changes, dependency decisions,
  performance work, and maintainability work. Do not skip for simple or routine coding
  tasks. Do not use for pure factual lookup, repository administration with no
  code-facing work, or non-code writing where code is only incidental.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Contract

This Skill contributes **baseline coding and engineering judgment**. Explicit user requirements, repository and language contracts, behavioral compatibility, correctness, safety, and target-platform constraints outrank this general lens. The active task owns repository discovery, implementation, testing workflow, review workflow, Git operations, tool calls, and final output.

When valid approaches remain after those constraints, use **effectiveness → operability → simplicity → elegance** as a default tie-breaker. Prefer reversible choices when uncertainty is material. When materially equivalent approaches remain, choose the established local/default option instead of creating an option menu; add escape conditions only for real differences.

# Engineering Defaults

- **KISS** — choose the minimum sufficient complexity that reliably solves the current problem. Shorter code is not automatically simpler.
- **YAGNI** — do not add capability, abstraction, configuration, extension points, caching, concurrency, or infrastructure for hypothetical future demand. Complexity carries the burden of proof.
- **DRY** — duplication alone is not sufficient reason to abstract. Centralize when repeated code or knowledge represents one stable concept or rule that should change together.
- **SRP** — split by responsibility, reason to change, ownership, or lifecycle; do not split merely to make functions, classes, or files smaller.
- **Fit the system** — inspect existing boundaries, callers, data flow, failure behavior, tests, and local conventions before adding a new pattern. Prefer a good existing pattern over an equally good new one.
- **Treat maintainability as cost** — judge avoidable coupling, duplicated knowledge, hidden behavior, and the effort to understand, modify, diagnose, and verify the code; do not use pattern count or stylistic purity as proxies.
- **Prefer explicitness over hidden magic** when it materially improves comprehension, modification, or verification. Avoid indirection that hides control flow, data flow, state, or ownership without paying for itself.
- **Prefer operational simplicity over technical purity** when both satisfy the required behavior and constraints.

Do not turn a local code problem into an architecture problem unless evidence shows that architecture is the constraint.

# Change Discipline

- Make the **smallest coherent change**: minimize conceptual surface, not line count.
- Preserve behavior outside the requested change unless an adjacent change is necessary for correctness, safety, compatibility, or a clearly demonstrated simplification.
- Avoid unrelated cleanup and speculative future-proofing while solving the active task.
- Separate substantial mechanical refactoring from functional change when combining them would materially hinder review, rollback, diagnosis, or verification. Small local cleanup may stay with the change when it improves clarity without obscuring behavior.
- Prefer local duplication over premature shared abstraction. Introduce shared abstractions only when the shared concept and ownership are stable enough to justify them.
- Add configuration only for real variability with a current consumer or contract; do not replace a good default with unnecessary options.
- Add a dependency only when it removes more implementation, maintenance, operational, security, or correctness burden than it introduces.
- Add automation when it removes repeated error-prone work or enforces a real contract; avoid automation whose lifecycle cost exceeds the burden it removes.
- Prefer naming, structure, and local simplification before adding wrappers, helpers, indirection, or new layers solely for readability.

# Evidence and Verification

Keep these distinctions explicit:

- required behavior vs. stylistic preference;
- observed failure or measurement vs. hypothetical risk;
- current requirement vs. possible future demand;
- behavior-preserving refactor vs. functional change;
- measured bottleneck or explicit budget vs. assumed performance concern;
- changed behavior vs. pre-existing condition.

For version-sensitive APIs, libraries, tools, or platform behavior, prefer current primary documentation, source, or runtime evidence over memory or generic convention.

Validate changed behavior and material failure paths at the cheapest useful level. Tests are maintained code: assertions, fixtures, and test structure should be simple enough to fail for the right reason. Prefer tests that protect observable contracts rather than incidental implementation details.

Do not treat the presence of tests as proof. When execution is available and material, run the relevant checks. Never claim that code, tests, performance, or behavior was verified when it was not actually verified.

# Operability

- Keep inputs, outputs, state ownership, side effects, invariants, error behavior, and important boundaries understandable.
- Preserve enough failure context to diagnose, recover from, and verify material failures.
- Use comments for rationale, constraints, non-obvious invariants, compatibility requirements, and external contracts; prefer clear code for describing what happens.
- Add observability, retries, concurrency controls, idempotency, security hardening, or resource safeguards when the task or evidence makes them material, not as generic ceremony.
- Treat measurements and explicit performance budgets as stronger evidence than intuition before adding performance complexity.

# Review Discipline

When reviewing code or a proposed change, inspect the current question and affected code paths first. Prioritize material correctness, compatibility, regression, maintainability, security, operability, and validation issues over stylistic preference or speculative architecture concerns. Separate required or material findings from optional suggestions and nits.

Distinguish defects introduced by the change from pre-existing conditions. Preserve uncertainty when evidence is incomplete. Do not manufacture findings, objections, or edge cases merely to appear rigorous, and do not demand perfection when a change is already a clear net improvement within the task's constraints.

Challenge an existing design or user proposal when a materially simpler, safer, more maintainable, or more operable alternative exists. Do not blindly preserve an existing pattern because it exists, and do not replace it merely because another valid design is possible.

# Boundary

Add domain-specific context only when the code crosses that domain boundary. This Skill contributes coding and engineering judgment; it does not create a separate coding workflow or take ownership from downstream capabilities.
