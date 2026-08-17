---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through adaptive multi-phase loops. Use when the
  user asks for deep or high-quality iterative work, repeated improvement or review
  loops, says to run loops, or explicitly asks for RPI, RPWR, an RPI loop, or an RPWR
  loop rather than a single-pass result.
---

# RPWR Loop

Use **RPWR** as a three-phase workflow for difficult or high-level work. `RPI` is an
alias for this workflow.

Each phase has a loop designed for its own purpose:

1. **Prepare** — `Discover → Assess → Configure → Verify`
2. **Improve** — `Research → Plan → Work → Review`
3. **Finalize** — `Inspect → Resolve → Validate → Close`

Do not force every phase into the same reasoning shape. Preserve the phase purpose,
adapt depth to the task, and count only genuine cycles.

## Arguments

```yaml
output_policy: auto  # auto | chat | persist | both
```

`output_policy` controls delivery after all counted loops finish:

- `auto` — default. Deliver in chat unless Prepare identifies a clearly appropriate,
  durable, writable destination that belongs to the current work context. When such a
  destination exists, persist the report there and return a concise chat summary with
  its location.
- `chat` — return the full work report in chat.
- `persist` — persist the work report to the most appropriate confirmed destination;
  if no suitable destination or write authority exists, fall back to chat and state
  the limitation.
- `both` — persist the report and also return the full report in chat.

A durable destination may be a repository, user Drive, Notion or another workspace,
a chatbot service library, knowledge base, document store, or another persistent
surface available to the agent. These are examples, not a priority order.

Choose the destination from the task context, existing workspace conventions, user
intent, persistence needs, and confirmed write authority. Prefer the surface the work
already belongs to. Do not move a report to another service merely because it is
available.

Do not invent a storage convention, create an unrelated destination, or assume write
access. If multiple destinations are plausible and context does not establish one,
fall back to chat rather than guessing.

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

The default workflow therefore contains **7–14 counted phase loops**, but the count is
a reasoning budget, not a target to inflate.

## What Counts as One Loop

A counted loop is one complete, substantive cycle of the **current phase's dedicated
loop**. It is not a unit of edits, findings, files, subtasks, or tool calls.

A loop counts only when its steps materially change or confirm the state needed for
that phase and produce a meaningful decision, action, validation, or confidence delta.

A loop does **not** count when it is only:

- one edit, one fix, one file change, one finding, or one subtask;
- mechanical execution without task-specific judgment;
- rereading or restating the same evidence;
- repeating the same review or validation from the same perspective;
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

Complete **1–2 Prepare loops** before the main work.

Prepare loop:

**Discover → Assess → Configure → Verify**

### Discover

Build an evidence-based picture of both the task and the execution environment.

Understand the task's objective, boundaries, context, uncertainty, stakes, constraints,
acceptance conditions, likely failure modes, relevant evidence, and where the work
naturally belongs.

Inspect the execution environment for available agent capabilities, tools, connected
resources, durable storage surfaces, permissions, write authority, validation
surfaces, and material limitations. Confirm capabilities and authority when they
matter; do not assume they exist.

### Assess

Match what the task requires against what the agent can actually do.

Identify material gaps, uncertainties, dependencies, authority boundaries, useful
tools and evidence surfaces, major risks, and the work's natural persistence context.
Distinguish a real capability gap from a capability that simply has not been checked
yet.

### Configure

Set the smallest viable strategy for Improve and Finalize.

Configure only what materially guides execution:

- tools, capabilities, and evidence surfaces to use;
- initial Research breadth and depth;
- important assumptions and acceptance conditions;
- Review perspectives and risk emphasis;
- validation approach;
- signals for narrowing Research or moving to Finalize;
- report delivery and persistence target when context clearly justifies one.

Keep the strategy adaptive. Do not script every future loop or plan around unavailable
capabilities, storage, or permissions.

### Verify

Challenge whether the prepared strategy is executable and proportionate.

Check that it reflects the user's actual objective, uses available capabilities well,
respects authority boundaries, avoids unverified dependencies, covers material risks,
and chooses a persistence surface only when context and write authority support it.

The first Prepare loop is mandatory. Use the second only when material task,
capability, tool, permission, storage, or strategy uncertainty remains. At two loops,
proceed to Improve with remaining limitations explicit.

## Phase 2 — Improve

Complete **4–8 Improve loops**. This is the primary work phase where most substantive
changes should happen.

Improve loop:

**Research → Plan → Work → Review**

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

Perform a meaningful batch of requested work against the current plan and evidence.
Work may include analysis, writing, editing, design, implementation, transformation,
decision-making, or other task-appropriate actions.

Preserve confirmed constraints and conclusions unless new evidence justifies changing
them. Do not claim work or validation that was not performed.

### Review

Use this default cadence based on the **Improve loop number**:

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

Complete **2–4 Finalize loops** focused on trustworthy completion.

Finalize loop:

**Inspect → Resolve → Validate → Close**

### Inspect

Inspect the current result, unresolved material findings, acceptance conditions,
recent changes, validation gaps, regression risk, and residual risk. Look only where a
problem could still materially affect completion.

### Resolve

Decide what must still be corrected, completed, reverted, or explicitly accepted.
Reject new scope unless a core assumption has failed or completion would otherwise be
misleading.

### Validate

Perform the smallest set of task-appropriate checks that can materially change
confidence in completion. Validate the result and any final changes against the
important requirements, evidence, regressions, and residual risks.

### Close

Decide whether the work can end. Record unresolved material findings, limitations, or
checks not performed. `No material finding` is a valid close result.

Do not manufacture criticism merely because another pass exists. Distinct Finalize
loops must address a materially different completion question, validation surface, or
residual risk; duplicating the same validation does not count.

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
appears, adapt within the current phase. Do not reset completed loop counts or exceed
the phase maximum.

## Context and Validation

Activate specialized context only when it materially improves the current phase. Do
not preload every possibly relevant Skill or carry phase-specific context longer than
needed.

Prefer better evidence, contradiction tests, counterexamples, alternatives, and
phase-appropriate validation over longer narration.

## Reporting

Keep a compact observable record while working. Do not expose private reasoning.

For **every counted loop**, produce one line using that phase's actual cycle:

```text
Prepare N — D: <discovered> | A: <assessment> | C: <configuration> | V: <verification>
Improve N — R: <research delta> | P: <decision> | W: <material work> | R: <review result>
Finalize N — I: <inspection> | R: <resolution> | V: <validation> | C: <close result>
```

Each field states only the observable material delta. One action, edit, or finding
must not be expanded into multiple lines to imitate multiple loops.

For **each completed phase**, produce one paragraph summarizing its objective, major
decisions or changes, evidence or validation, and remaining material concerns.

After all phases finish, produce a **work report** containing:

- final result or outcome;
- loop summaries grouped by Prepare, Improve, and Finalize;
- one paragraph summary for each phase;
- material changes, decisions, and validation performed;
- unresolved findings, limitations, or checks not performed.

Deliver or persist this report according to `output_policy`. Report delivery happens
after the phase loops and never counts as an additional loop.
