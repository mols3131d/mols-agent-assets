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
finding-driven reasoning cycles. `RPI` is an alias for this workflow.

RPWR has three phases. Every phase uses the same RPWR spine, but for a different
purpose:

1. **Prepare** — understand the task and execution environment, then set the strategy.
2. **Improve** — perform the main work and substantive improvement.
3. **Finalize** — finish, validate, and stop without manufacturing findings.

Keep **Plan** and **Work** simple. Adapt **Research** and **Review** as understanding,
risk, and confidence change.

## Arguments

```yaml
output_policy: auto  # auto | chat | document | both
```

`output_policy` controls delivery after all counted loops finish:

- `auto` — default. Use chat in a normal chatbot context. When the work is performed
  in a durable writable workspace such as a repository or Notion, save the report in
  the appropriate existing location and return only a concise chat summary and link
  or location.
- `chat` — return the full work report in chat.
- `document` — persist the work report when a suitable target and write authority are
  available; otherwise fall back to chat and state the limitation.
- `both` — persist the report and also return the full report in chat.

Honor an explicit user choice. Under `auto`, choose the report location from the
workspace conventions and authority discovered in Prepare; do not invent a new
storage convention or assume write access.

## Phase Budgets

```yaml
phase_1_prepare:
  min_loops: 1
  max_loops: 2
phase_2_improve:
  min_loops: 4
  max_loops: 8
phase_3_finalize:
  min_loops: 2
  max_loops: 4
```

Each phase owns its own loop budget. There is no separate global loop cap.

- Do not leave a phase before its minimum is satisfied.
- After the minimum, advance when that phase's purpose is materially satisfied.
- At the maximum, advance or stop even if findings remain; carry unresolved material
  findings forward or report them at the end.
- A user who explicitly changes a phase budget overrides these defaults.

The default workflow therefore contains **7–14 counted loops**, but the count is a
reasoning budget, not a target to inflate.

## What Counts as One Loop

A counted loop is a **complete, substantive RPWR reasoning cycle**, not a unit of
edits, findings, files, or subtasks.

1. **Research** changes or materially confirms the understanding relevant to the
   current phase.
2. **Plan** makes a task-specific decision about what should happen next and why.
3. **Work** performs a meaningful batch of phase-appropriate work against that plan.
4. **Review** evaluates the resulting state and determines the next material delta or
   establishes that the current concern is resolved.

A loop does **not** count when it is only:

- one edit, one fix, one file change, one finding, or one subtask;
- mechanical execution without task-specific judgment;
- rereading or restating the same evidence;
- repeating the same review from the same perspective;
- cosmetic churn created to increase the loop number;
- phase labels wrapped around work that would have happened identically without the
  loop.

Several changes may belong to one loop, and one difficult objective may span several
loops. A no-change result may count only when substantive investigation or validation
materially increases confidence or closes an important uncertainty.

Never invent findings, split one action into artificial passes, or simulate reasoning
to satisfy a minimum. Do not expose private chain-of-thought to prove a loop happened;
report observable evidence, decisions, validation, and material deltas instead.

## Phase 1 — Prepare

Complete **1–2 RPWR loops** focused on understanding both the task and the execution
environment before the main work begins.

### Research

Orient on two surfaces:

- **Task:** objective, boundaries, context, uncertainty, evidence quality, stakes,
  constraints, likely failure modes, and acceptance conditions.
- **Execution environment:** available agent capabilities, tools, connected resources,
  permissions, write authority, validation surfaces, and material limitations.

Use available evidence to confirm capabilities and authority when they affect the
workflow. Do not assume a tool, permission, connection, or write capability exists.

### Plan

Decide what preparation must resolve, especially:

- what the task actually requires;
- what the agent can and cannot do in the current environment;
- which tools, capabilities, permissions, and evidence surfaces should be used;
- the initial breadth and depth of Research;
- which Review perspectives and risks deserve attention;
- what signals should narrow Research or trigger Finalize.

Design the strategy around real capabilities and authority. Do not plan execution that
requires unavailable tools or permissions without making that limitation explicit.

### Work

Establish the smallest viable execution strategy for Improve and Finalize. Select the
useful capabilities, tools, evidence surfaces, Research posture, Review posture, and
validation approach. Keep it adaptive rather than scripting every future loop.

### Review

Challenge whether the strategy:

- understands the user's actual objective and important constraints;
- uses the available agent capabilities and tools effectively;
- respects permission and authority boundaries;
- depends on any unverified capability, resource, or access;
- misses a material uncertainty, risk, evidence surface, or review perspective.

The first Prepare loop is mandatory. Use the second only when the first leaves a
material task, capability, tool, permission, or strategy uncertainty worth resolving.
At two loops, proceed to Improve with any remaining limitation or uncertainty explicit.

## Phase 2 — Improve

Complete **4–8 RPWR loops**. This is the primary work phase where most substantive
changes should happen.

### Research

Use a relatively broad scope in early Improve loops to understand the problem
boundary, important assumptions, plausible alternatives, and missing evidence. Be
broad enough to orient the work, not exhaustive by default.

As understanding improves, narrow toward unresolved findings and weak assumptions.
Adapt instead of repeating:

- broaden when the problem boundary is unclear, evidence conflicts, or a core
  assumption fails;
- deepen when material uncertainty or weak evidence remains;
- narrow when findings become localized;
- change evidence, method, or perspective when the previous investigation saturates.

Research may inspect existing context, artifacts, repositories, data, prior results,
domain knowledge, or external sources. It is not synonymous with web search.

### Plan

Translate current evidence and findings into the smallest plan that can materially
improve the result. Set only the objective, scope, constraints, approach, work units,
trade-offs, acceptance conditions, and validation points needed for the next work.

### Work

Perform the requested work against the current plan and evidence. Work may include
analysis, writing, editing, design, implementation, transformation, decision-making,
or other task-appropriate actions.

Preserve confirmed constraints and conclusions unless new evidence justifies changing
them. Do not claim work or validation that was not performed.

### Review

Use this default cadence based on the **Phase 2 loop number**:

- **odd loops — Quality Review:** improve correctness, completeness, coherence,
  clarity, usability, evidence quality, and fit to the objective;
- **even loops — Pessimistic Review:** look for consequential failure modes, edge
  cases, hidden assumptions, regressions, security or safety concerns, operational
  risks, misuse, contradictions, and side effects.

This cadence is a default, not a ritual. Override it when current findings or risk
clearly require the other perspective. Apply only dimensions that materially fit the
task; do not force security, safety, or other categories where they do not matter.

After four loops, move to Finalize when the main result is substantially shaped and
remaining work is mainly finishing or validation. Otherwise continue only while a
meaningful delta remains, up to eight loops. At eight, carry remaining material
findings into Finalize rather than extending Improve indefinitely.

## Phase 3 — Finalize

Complete **2–4 RPWR loops** focused on finishing and trustworthy completion.

### Research

Investigate only evidence or uncertainty that can still materially change the outcome
or confidence in it.

### Plan

Target unresolved material findings, acceptance gaps, validation gaps, or regression
risk. Avoid new scope unless a core assumption has failed.

### Work

Make only changes needed to finish, correct, or validate the result.

### Review

Limit review to issues that can still materially undermine the task's core purpose:

- unresolved material findings;
- violated objectives or acceptance conditions;
- regressions introduced by recent Work;
- residual risks that materially weaken the result;
- final validation that can change confidence in completion.

`No material finding` is a valid Review result. Do not manufacture another criticism
merely because another pass exists.

The two minimum Finalize loops must still be genuine reasoning cycles. Use distinct,
material validation questions, evidence surfaces, or residual-risk perspectives when
needed; duplicating the same validation does not count.

After two loops, stop when no meaningful completion delta remains. Otherwise continue
up to four loops. At four, stop and report unresolved material findings rather than
simulating additional loops.

## Phase Transition

Use state, not a fixed global loop number, to decide transitions within each phase's
budget.

Signals for moving from Improve to Finalize include:

- major requirements are substantially satisfied;
- findings are fewer, smaller, or localized;
- Research produces little new material evidence;
- recent Work changes only narrow surfaces;
- Review increasingly repeats known issues or cosmetic preferences;
- remaining work is mainly validation, regression control, or finishing.

If conflicting evidence, a failed core assumption, or a changed problem boundary
appears, adapt Research and Review within the current phase. Do not reset completed
loop counts or exceed the phase maximum.

## Context and Validation

Activate specialized context only when it materially improves the current phase. Do
not preload every possibly relevant Skill or carry phase-specific context longer than
needed.

Choose validation that matches the work and current risks. Prefer better evidence,
contradiction tests, counterexamples, alternatives, and task-appropriate validation
over longer narration.

## Reporting

Keep a compact observable record while working. Do not expose private reasoning.

For **every counted loop**, produce one line that summarizes the whole RPWR cycle:

```text
<Phase> <N> — R: <evidence/understanding> | P: <decision> | W: <material work> | R: <review result>
```

Each field should state only the material delta. One action, edit, or finding must not
be expanded into multiple lines to imitate multiple loops.

For **each completed phase**, produce one paragraph summarizing its objective, major
decisions or changes, evidence or validation, and remaining material concerns.

After all phases finish, produce a **work report** containing:

- final result or outcome;
- loop summaries grouped by Prepare, Improve, and Finalize;
- one paragraph summary for each phase;
- material changes, decisions, and validation performed;
- unresolved findings, limitations, or checks not performed.

Deliver or persist this report according to `output_policy`. Report delivery happens
after the RPWR loops and never counts as an additional loop.
