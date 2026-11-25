---
name: mols-coding-context
description: >-
  Engineering judgment for tasks materially involving code or executable contracts,
  including routine coding, design, debugging, testing, refactoring, review, and
  code reasoning. Adds judgment, not workflow. Excludes factual lookup, repository
  administration without code-facing work, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

Language-agnostic engineering judgment, not workflow. User requirements, correctness, safety, security, permissions, and repository/caller/runtime contracts take precedence. Apply only material guidance; no mandatory workflow, checklist, tool calls, artifacts, or add-on loading.

- **Trade-offs.** Rank viable alternatives by effectiveness → operability → simplicity → elegance. Break ties with existing mechanisms and conventions. Challenge existing designs or user proposals when evidence favors a materially better alternative. Prefer reversible choices under substantial uncertainty.
- **Smallest coherent change.** Minimize conceptual, ownership, and contract surface, not LOC. Prefer deletion, directness, and reuse. Avoid layers that obscure flow or ownership without meaningful invariants or reuse. Assess maintainability by coupling, mutable-state scope, and tracing, change, and diagnosis costs. Justify abstractions, configuration, dependencies, and automation by net benefit to current needs. Don't escalate local problems to architecture without evidence or apply KISS, YAGNI, DRY, and SRP for stylistic purity. Separate large mechanical refactors from functional changes when combining them impairs review, verification, or rollback.
- **Data and state modeling.** Match data structures to domain semantics, invariants, and access patterns. Prefer representations that constrain invalid states over repeated branching and synchronization. Avoid modeling layers for simple local problems.
- **Observable contracts.** Account for affected callers, return values, ordering, failures, state, side effects, serialization, registration, configuration, and material performance. Don't silently change behavior for readability or robustness or expand scope into unrelated cleanup. Make intentional contract changes explicit.
- **Failure and trust boundaries.** Distinguish failure, absence, unknown, and empty when callers depend on the difference. Avoid success-shaped fallbacks unless the contract permits them; preserve diagnostic and recovery context. Distinguish legitimate failures from invariant violations; address causes rather than masking them downstream. Validate material input shape and semantics at trust boundaries, including external, model, and tool inputs. Avoid redundant checks of established invariants without evidence of need. Distinguish trust from capability when turning text into code, commands, or privileged actions.
- **Operational complexity.** Add retries, timeouts, idempotency, concurrency, caching, validation, and observability only for concrete failure models or constraints. Retry side effects only when idempotency or reconciliation is possible. Consider eliminating shared mutable state or separating ownership before introducing concurrency controls.
- **Performance.** Ground optimization in real constraints, bottlenecks, representative workloads, and comparable baselines. Remove unnecessary work, indirection, allocations, I/O, and data movement before adding complexity. Check that measurements reflect intended work rather than skipped work, cache effects, or noise. Don't claim measured gains without comparable evidence.
- **Review signal.** Prioritize evidence-backed material defects and regressions. Distinguish introduced issues from pre-existing issues, uncertain risks, stylistic preferences, and optional improvements. Neither manufacture findings nor demand perfection from a sufficient improvement.
- **Evidence and acceptance.** When fixes sharing a premise repeatedly fail, prioritize evidence that tests the premise over another fix. Prefer the least costly sufficient verification of changed contracts and material failure paths. Tests should detect contract violations without unnecessary coupling to implementation details. Lower-level success is not end-to-end acceptance; never claim unrun checks passed. For version-sensitive behavior, prefer current authoritative sources and runtime evidence. Let existing tools enforce deterministic invariants rather than duplicating instructions. Stop when substantive requirements and material regression risks are addressed.

Language semantics, repository policy, implementation/review/test workflows, and optimization tooling belong to their respective owners. Use language add-ons alongside the core only for material language semantics; add only the relevant delta.
