---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through adaptive Research → Plan → Work → Review
  loops. Use when the user asks for deep or high-quality iterative work, repeated
  improvement or review loops, says to run loops, or explicitly asks for RPI, RPWR,
  an RPI loop, or an RPWR loop rather than a single-pass result.
---

# RPWR Loop

Use **Research → Plan → Work → Review (RPWR)** to improve a task through repeated,
finding-driven loops. `RPI` is an alias for this workflow.

RPWR has three phases:

1. **Calibrate** — decide how Research and Review should behave.
2. **Iterate** — perform the main work through repeated RPWR loops.
3. **Converge** — finish with narrower, material-only RPWR loops.

Keep **Plan** and **Work** simple. Adapt **Research** and **Review** as understanding,
risk, and confidence change.

## Defaults

```yaml
min_iteration_loops: 4
min_convergence_loops: 2
max_loops: 10
stop_condition: minimums_met_and_no_material_findings
```

The phase minimums are mandatory unless the user explicitly overrides RPWR itself.
Treat a user-specified loop count as a maximum when it is above the minimums unless
they explicitly require exactly that many completed loops.

Reserve at least the final two counted loops for Convergence. If Iterate still has
material findings when only the Convergence minimum remains within the loop budget,
carry those findings into Convergence instead of extending the main-work phase
indefinitely.

Never invent findings or split one action into multiple passes merely to satisfy a
count.

## What Counts as One Loop

A counted RPWR loop is a **complete reasoning cycle**, not a unit of edits or tasks.
It must substantively perform all four phases:

1. **Research** changes or confirms the task understanding using relevant evidence,
   context, assumptions, alternatives, or prior findings.
2. **Plan** makes a task-specific decision about what should be done next and why.
3. **Work** performs a meaningful batch of task-appropriate work against that plan.
4. **Review** evaluates the resulting state and determines what materially remains.

A loop does **not** count when it is only:

- one edit, one fix, one file change, one finding, or one subtask;
- mechanical execution without task-specific judgment;
- rereading or restating the same evidence;
- repeating the same review from the same perspective;
- cosmetic churn created to increase the loop number;
- a phase label wrapped around work that would have happened identically without the
  loop.

Several edits or findings may belong to one loop, and one complex objective may span
several loops. Count the completed reasoning cycle, not the number of actions inside
it.

Do not expose private chain-of-thought to prove a loop happened. Report only the loop
count and material deltas.

## Phase 1 — Calibrate

Before Loop 1, choose a provisional strategy for Research and Review. Calibration is
preparation and does not count as an RPWR loop.

Consider the task's uncertainty, breadth, stakes, evidence quality, likely failure
modes, and acceptance conditions. Decide only what materially guides the workflow:

- how broad and deep Research should begin;
- what evidence or context is worth investigating;
- which Review perspectives matter most;
- what signals should narrow Research;
- what signals should move the workflow from Iterate to Converge.

Treat this strategy as provisional. Change it when findings, evidence, or risk change.
Do not expose this internal calibration unless useful to the user.

## Phase 2 — Iterate

This is the primary work phase. Complete **at least four counted RPWR loops** before
moving to Converge.

Each loop follows the same spine:

### Research

Gather enough evidence to understand the current objective and unresolved findings.
Research may inspect existing context, artifacts, repositories, data, prior results,
domain knowledge, or external sources. It is not synonymous with web search.

Use a relatively broad scope in early loops to understand the problem boundary,
important assumptions, plausible alternatives, and missing evidence. Be broad enough
to orient the work, not exhaustive by default. As understanding improves, narrow
toward unresolved findings and weak assumptions.

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

During Iterate, use this default cadence:

- **odd-numbered loops — Quality Review:** improve correctness, completeness,
  coherence, clarity, usability, evidence quality, and fit to the objective;
- **even-numbered loops — Pessimistic Review:** look for serious failure modes,
  edge cases, hidden assumptions, regressions, security or safety concerns,
  operational risks, misuse, contradictions, and consequential side effects.

This cadence is a default, not a ritual. Override it when current findings or risk
clearly require the other perspective. Apply only review dimensions that materially
fit the task; do not force security, safety, or other categories where they do not
matter.

The Review must identify the next meaningful delta or establish that the result is
ready to move toward convergence. A finding is useful only when it can materially
change the result, validation, or confidence.

## Phase 3 — Converge

After the main work is substantially shaped, switch from broad improvement to
finishing. Complete **at least two counted RPWR loops** in this phase.

Convergence loops still use **Research → Plan → Work → Review**, but each phase is
narrower:

- **Research:** investigate only evidence or uncertainty that can still change the
  outcome.
- **Plan:** target unresolved material findings, validation gaps, or regression risk.
- **Work:** make only changes needed to finish or validate the result.
- **Review:** inspect only issues that can still materially undermine the task's core
  purpose.

Convergence Review is limited to:

- unresolved material findings;
- violated objectives or acceptance conditions;
- regressions introduced by recent Work;
- residual risks that materially weaken the result;
- final validation that can change confidence in completion.

`No material finding` is a valid Review result. Do not manufacture another criticism
merely because another pass exists.

The two minimum Convergence loops must still be genuine counted loops. Use a distinct
material validation question, evidence surface, or review perspective when needed;
do not duplicate the same validation to satisfy the minimum.

## Phase Transition

Move from Iterate to Converge only after at least four counted Iterate loops and when
several of these signals appear:

- major requirements are substantially satisfied;
- findings are fewer, smaller, or localized;
- Research produces little new material evidence;
- recent Work changes only narrow surfaces;
- Review increasingly repeats known issues or cosmetic preferences;
- remaining work is mainly validation, regression control, or finishing.

If new conflicting evidence, a failed core assumption, or a changed problem boundary
appears before the loop budget is exhausted, broaden Research and strengthen Review
again. Do not reset the loop count.

## Repeat Gate

After the phase minimums are satisfied, continue only when another loop has a concrete
expected delta, such as:

- an unresolved material finding;
- new or conflicting evidence;
- a changed assumption or problem boundary;
- a useful counterexample or unexplored perspective;
- a materially different validation method;
- Work that can meaningfully improve the result.

Repeating the same search, review perspective, argument, or cosmetic preference does
not justify another loop. If the same finding repeatedly survives Work, reconsider
the Plan or underlying assumption instead of reviewing it again.

At `max_loops`, stop and report material unresolved findings rather than simulating
additional loops.

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
- counted RPWR loops, separated into Iterate and Converge;
- material changes or conclusions;
- unresolved findings or checks that could not be performed.

Show detailed phase work only when the user asks for it or it is necessary to
understand the result.
