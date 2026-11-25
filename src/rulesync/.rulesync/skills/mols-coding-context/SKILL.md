---
name: mols-coding-context
description: >-
  Baseline engineering judgment for any task requiring reasoning about code or
  executable behavior, including routine implementation, design, debugging,
  testing, refactoring, and review. Load once at task entry unless already in
  context; reuse while available. Not a workflow. Excludes factual lookup,
  non-code repository administration, and prose-only work.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

Apply only material guidance. User requirements, correctness, safety, security, permissions, and repository/caller/runtime contracts take precedence.

- **Trade-offs.** Rank viable alternatives by effectiveness → operability → simplicity → elegance. Prefer established conventions and mechanisms when equivalent, and reversible choices under substantial uncertainty. Challenge existing designs or user proposals when evidence favors a materially better alternative.
- **Smallest coherent change.** Minimize changed concepts, owners, and contract surface, not LOC. Prefer deletion, directness, and reuse; avoid layers that obscure flow or ownership without meaningful invariants or reuse. Judge maintainability by coupling, mutable-state scope, and the cost of tracing, changing, and diagnosing code. Justify abstractions, configuration, dependencies, and automation by net benefit to current needs. Separate large mechanical refactors from functional changes when mixing them impairs review, verification, or rollback.
- **Data and state modeling.** Match representations to domain semantics, invariants, and access patterns. Prefer structures that constrain invalid states over repeated branching and synchronization.
- **Observable contracts.** Preserve caller contracts and observable behavior, including ordering, failures, state, side effects, serialization, registration, configuration, and material performance. Avoid unrelated cleanup; make intentional contract changes explicit.
- **Failure and trust boundaries.** Distinguish failure, absence, unknown, and empty when callers depend on the distinction. Use success-shaped fallbacks only when permitted by the contract; preserve diagnostic and recovery context. Handle legitimate failures without masking invariant violations; fix their causes. Validate material input shape and semantics at trust boundaries, including model and tool inputs. Avoid redundant checks of established invariants without evidence of need. Separate trust from execution authority when converting text into code, commands, or privileged actions.
- **Operational complexity.** Introduce operational mechanisms only for concrete constraints or failure models. Retry side effects only when safe through idempotency or reconciliation. Consider eliminating shared mutable state or separating ownership before adding concurrency controls.
- **Performance.** Ground optimization in actual constraints and bottlenecks. Remove unnecessary work, indirection, allocations, I/O, and data movement before adding complexity. Compare representative workloads under equivalent conditions; account for skipped work, cache effects, and noise before claiming measured gains.
- **Review signal.** Prioritize evidence-backed material defects and regressions. Distinguish introduced defects, pre-existing issues, uncertain risks, preferences, and optional improvements. Neither manufacture findings nor demand perfection from a sufficient improvement.
- **Evidence and acceptance.** When fixes sharing a premise repeatedly fail, prefer evidence that tests the premise over another fix. Use the least costly sufficient verification of changed contracts and material failure paths. Tests should detect contract violations without unnecessary coupling to implementation. Lower-level success is not end-to-end acceptance. Prefer current authoritative sources and runtime evidence for version-sensitive behavior. Let existing tools enforce deterministic invariants rather than duplicating instructions. Stop when substantive requirements and material regression risks are addressed.

Use language add-ons alongside the core only when language-specific semantics matter.
