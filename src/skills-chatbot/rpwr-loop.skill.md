---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through adaptive Research → Plan → Work → Review
  loops. Use when the user asks for deep or high-quality iterative work, repeated
  improvement or review loops, or explicitly asks for RPI, RPWR, an RPI loop, or an
  RPWR loop rather than a single-pass result.
---

# RPWR Loop

Use **Research → Plan → Work → Review (RPWR)** to improve a task through repeated,
finding-driven loops. `RPI` is an alias for this workflow.

Keep **Plan** and **Work** simple. Adapt **Research** and **Review** as understanding,
risk, and confidence change.

## Defaults

```yaml
max_loops: 10
stop_condition: no_material_findings
```

Treat a user-specified loop count as a maximum unless they explicitly require exactly
that many completed loops. Otherwise stop when another loop has no meaningful expected
delta or `max_loops` is reached. When an exact count is required, later loops may be
brief validation passes; never invent findings to justify them.

## Calibrate Before Loop 1

Before the first RPWR loop, choose a provisional strategy for Research and Review.
Calibration is preparation and does not count as an RPWR loop.

Consider the task's uncertainty, breadth, stakes, evidence quality, likely failure
modes, and acceptance conditions. Decide only what materially guides the loop:

- how broad and deep Research should begin;
- what evidence or context is worth investigating;
- which Review perspectives matter most;
- what signals will narrow Research or move Review toward convergence.

Treat this strategy as provisional. Change it when findings, evidence, or risk change.
Do not expose this internal calibration unless useful to the user.

## Loop

Every loop follows the same spine. A phase may be brief when little additional work
is needed.

### Research

Gather enough evidence to understand the current objective and unresolved findings.
Research may inspect existing context, artifacts, repositories, data, prior results,
domain knowledge, or external sources. It is not synonymous with web search.

Use a broader scope in early loops to understand the problem boundary, important
assumptions, plausible alternatives, and missing evidence. Be broad enough to orient
the work, not exhaustive by default. As understanding improves, narrow toward
unresolved findings and weak assumptions.

Adapt instead of repeating:

- broaden when the problem boundary is unclear, evidence conflicts, or a core
  assumption fails;
- deepen when material uncertainty or weak evidence remains;
- narrow when findings become localized and the result is converging;
- change evidence, method, or perspective when the previous investigation saturates.

Stop when the next Plan can be grounded well enough to act.

### Plan

Translate current evidence and findings into the smallest plan that can materially
improve the result.

Set only the objective, scope, constraints, acceptance conditions, approach, work
units, trade-offs, and validation points needed for the task.

### Work

Perform the requested work against the current plan and evidence.

Work may include analysis, writing, editing, design, implementation, transformation,
decision-making, or other task-appropriate actions. Preserve confirmed constraints
and conclusions unless new evidence justifies changing them. Do not claim work or
validation that was not performed.

### Review

Review the result from the perspective most likely to expose material remaining
problems.

During early and middle loops, use this default cadence:

- **odd-numbered loops — Quality Review:** improve correctness, completeness,
  coherence, clarity, usability, evidence quality, and fit to the objective;
- **even-numbered loops — Pessimistic Review:** look for serious failure modes,
  edge cases, hidden assumptions, regressions, security or safety concerns,
  operational risks, misuse, contradictions, and consequential side effects.

This cadence is a default, not a ritual. Override it when current findings or risk
clearly require the other perspective. Apply only review dimensions that are relevant
to the task; do not force security, safety, or other categories where they have no
material bearing.

As the result converges, stop alternating broadly and switch to **Convergence
Review**. Limit review to issues that can still materially change the outcome:

- unresolved material findings;
- violated objectives or acceptance conditions;
- regressions introduced by recent Work;
- residual risks that undermine the task's core purpose.

`No material finding` is a valid Review result.

## Convergence

Treat the task as converging when several of these signals appear:

- major requirements are satisfied;
- findings are fewer, smaller, or localized;
- Research produces little new material evidence;
- recent Work changes only narrow surfaces;
- Review mostly repeats known issues or cosmetic preferences;
- remaining work is verification or polish rather than substantive correction.

Convergence is state-based, not tied to a fixed loop number. If new conflicting
evidence, a failed core assumption, or a changed problem boundary appears, broaden
Research and strengthen Review again.

## Repeat Gate

Continue only when another loop has a concrete expected delta, such as:

- an unresolved material finding;
- new or conflicting evidence;
- a changed assumption or problem boundary;
- a useful counterexample or unexplored perspective;
- a materially different validation method;
- Work that can meaningfully improve the result.

Repeating the same search, review perspective, argument, or cosmetic preference does
not justify another loop. If the same finding repeatedly survives Work, reconsider
the Plan or underlying assumption instead of reviewing it again.

## Context and Validation

Activate specialized context only when it materially improves the current phase. Do
not preload every possibly relevant Skill or carry phase-specific context longer than
needed.

Choose validation that matches the work and current risks. Prefer better evidence,
contradiction tests, counterexamples, alternatives, and task-appropriate validation
over longer narration.

## Output

Do not expose private reasoning or verbose phase-by-phase narration by default.
Return:

- the improved result;
- completed RPWR loop count;
- material changes or conclusions;
- unresolved findings or checks that could not be performed.

Show detailed phase work only when the user asks for it or it is necessary to
understand the result.
