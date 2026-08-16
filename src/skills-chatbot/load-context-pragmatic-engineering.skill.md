---
name: load-context-pragmatic-engineering
description: >-
  Load pragmatic engineering decision context for architecture, design, refactoring,
  abstraction, dependency, tooling, automation, developer experience, operations,
  maintainability, and implementation trade-offs. Use when technically valid options
  differ in complexity, operability, lifecycle cost, reversibility, or elegance, or
  when deciding whether to add or remove an abstraction, dependency, configuration,
  workflow, framework, optimization, or layer. Do not use for pure factual lookup,
  routine implementation with no meaningful design trade-off, or non-technical writing.
---

# Load Context: Pragmatic Engineering

Load this Skill as **decision context**, not as a mandatory workflow.

Choose the smallest design that solves the real problem and remains easy to operate,
debug, change, and remove. Technical elegance is valuable when it lowers lifecycle
cost or makes the system clearer and safer to evolve.

## Priority

Treat explicit requirements, correctness, safety, and compatibility as constraints.
Within them, prefer:

1. **Effectiveness** — solve the current problem.
1. **Operability** — keep normal use, failure handling, debugging, and recovery easy.
1. **Simplicity** — minimize concepts, branches, dependencies, configuration, and maintenance.
1. **Elegance** — prefer coherent designs when they do not increase operational or cognitive cost.

> 최소한의 복잡성으로 최대한의 운영 효율을 얻는다.
>
> 기술적 우아함은 운영을 단순하게 만들 때 가치가 있다.

## Decision Lens

- **KISS** — seek minimum sufficient complexity, not minimum line count.
- **YAGNI** — require current evidence or concrete irreversible risk before adding capability.
- **DRY** — centralize authoritative knowledge, not every repeated line; small duplication
  is better than a wrong abstraction or hidden coupling.
- **SRP** — keep one cohesive responsibility and reason to change; do not split by size alone.
- **Evidence-first** — justify complexity with requirements, observed failures, measured
  constraints, supported environments, or explicit contracts.
- **Reversibility** — when value is similar, prefer what is easier to change, remove,
  migrate, or recover from.

## Trade-off Defaults

- Delay abstraction until repeated variation or a stable boundary is visible.
- Automate repetitive deterministic work, while preserving inspectability and recovery.
- Optimize for the supported scope; preserve changeability instead of speculative options.
- Prefer a good convention/default before adding configuration.
- Optimize performance after evidence of a meaningful bottleneck unless a hard constraint
  makes delay materially expensive.
- Accept less architectural purity when it materially reduces operational burden without
  weakening important guarantees.
- Add a dependency only when it removes more lifecycle complexity or risk than it adds.

Consider total engineering cost across build, review, onboarding, operation, debugging,
recovery, testing, upgrades, migration, future change, and deletion. Do not merely move
complexity from implementation into operations.

## Challenge Assumptions

Do not treat the user's proposal, the existing implementation, or a fashionable pattern
as correct by default. Surface a materially simpler or safer alternative when one exists.
Distinguish requirements from preferences and current evidence from hypothetical needs.
Do not invent objections merely to appear critical.

## Boundaries and Output

This Skill complements domain-specific implementation, research, review, and RPI Skills;
it does not replace their procedures or validation contracts. Do not force redesign when
the current approach is already simple enough.

Apply the principles without reciting them by default. For a recommendation or comparison,
return the preferred option first, followed only by the material trade-offs, evidence,
assumptions, and lifecycle costs needed to understand the decision.
