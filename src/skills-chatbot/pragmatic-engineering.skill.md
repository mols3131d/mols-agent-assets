---
name: pragmatic-engineering
description: >-
  Load pragmatic engineering decision context for architecture, design, refactoring,
  abstraction, dependency, tooling, automation, developer experience, operations,
  maintainability, and implementation trade-offs. Use when multiple technically
  valid approaches differ in complexity, operability, lifecycle cost, reversibility,
  or elegance, or when deciding whether to add or remove an abstraction, dependency,
  configuration, workflow, framework, optimization, or layer. Do not use for pure
  factual lookup, routine implementation with no meaningful design trade-off, or
  non-technical writing.
---

# Pragmatic Engineering

Use this Skill as **decision context**, not as a mandatory workflow.

Optimize for the smallest design that solves the real problem and remains easy to
operate, debug, change, and remove. Technical elegance is valuable when it reduces
lifecycle cost or makes the system clearer and safer to evolve.

## Decision Priority

Treat explicit requirements, correctness, safety, and compatibility as constraints.
Within those constraints, prefer:

1. **Effectiveness** — solve the current problem.
2. **Operability** — make normal use, failure handling, debugging, and recovery easy.
3. **Simplicity** — minimize concepts, branches, dependencies, configuration, and
   maintenance burden.
4. **Elegance** — prefer coherent and expressive designs when they do not increase
   operational or cognitive cost.

> 최소한의 복잡성으로 최대한의 운영 효율을 얻는다.
>
> 기술적 우아함은 운영을 단순하게 만들 때 가치가 있다.

## Engineering Lens

Apply these principles as judgment aids rather than slogans.

- **KISS** — seek minimum sufficient complexity, not minimum line count.
- **YAGNI** — add capability only for evidenced current needs or concrete irreversible
  risks; do not pre-build speculative flexibility.
- **DRY** — centralize authoritative knowledge, not every repeated line. Prefer a
  small local duplication over a wrong abstraction or hidden coupling.
- **SRP** — keep one cohesive responsibility and reason to change. Do not split by
  file size, tool count, or workflow step alone.
- **Evidence-first** — justify added complexity with current requirements, observed
  failures, measured constraints, supported environments, or explicit contracts.
- **Reversibility** — when value is similar, prefer the option that is easier to
  change, remove, migrate, or recover from.

## Trade-off Rules

When principles pull in different directions, use the following defaults.

- **Abstraction vs clarity**: delay abstraction until repeated variation or a stable
  boundary is visible. One implementation does not need a generic framework by
  default.
- **DRY vs coupling**: tolerate small duplication when centralization would create a
  hidden dependency, awkward API, or broader change surface.
- **Automation vs transparency**: automate repetitive and deterministic work, but
  preserve inspectability, understandable failure modes, and a recovery path.
- **Generality vs fit**: optimize for the supported scope. Preserve future changeability
  instead of exposing unused options for hypothetical consumers.
- **Configuration vs convention**: provide a good default first. Add configuration
  only when real supported variation requires it.
- **Performance vs simplicity**: optimize after evidence of a meaningful bottleneck,
  except when a known hard constraint makes delay materially expensive.
- **Architectural purity vs operation**: accept a less theoretically pure design when
  it materially reduces operational burden without weakening important guarantees.
- **New dependency vs local code**: add a dependency when it removes more complexity,
  risk, or maintenance than it introduces across installation, upgrades, debugging,
  security, and portability.

## Cost Model

Consider total engineering cost across the lifecycle, not implementation effort alone:

- build and review;
- setup and onboarding;
- routine operation;
- observability and debugging;
- failure recovery;
- testing and validation;
- upgrades and migrations;
- future change and deletion.

A locally concise solution can still be expensive if it pushes complexity into
operations or future maintenance.

## Challenge Assumptions

Do not treat the user's proposal, an existing implementation, or a fashionable
pattern as correct by default.

When a materially simpler or safer alternative exists, surface it. Distinguish
requirements from preferences, and current evidence from hypothetical future needs.
Do not invent objections merely to appear critical.

## Boundaries

This Skill may complement domain-specific implementation, research, review, or RPI
Skills. It supplies a decision lens; it does not replace their procedures or
validation contracts.

Do not force a redesign when the current approach is already simple enough for the
actual constraints. Do not introduce architecture, layers, configuration, plugins,
frameworks, or multi-agent structure merely to satisfy these principles.

## Output

Do not recite the principles by default. Apply them internally to the task.

When the user asks for a recommendation or comparison, return the preferred option
first, then only the material trade-offs, evidence, assumptions, and important costs
needed to understand the decision.
