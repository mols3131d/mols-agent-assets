---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through adaptive multi-phase loops. Use when the
  user asks for deep iterative work, repeated improvement or review loops, says to run
  loops, or explicitly asks for RPI, RPWR, an RPI loop, or an RPWR loop instead of a
  single-pass result.
---

# RPWR Loop

Use **RPWR** as a three-phase workflow for difficult or high-level work. `RPI` is an
alias for this workflow.

Each phase has its own loop:

1. **Prepare** — `Discover → Assess → Configure → Verify`
2. **Improve** — `Research → Plan → Work → Review`
3. **Finalize** — `Inspect → Resolve → Validate → Gate`

Do not force phases into the same reasoning shape. Count only genuine phase cycles.

## Arguments

```yaml
output_policy: auto  # auto | chat | persist | both
phase_1_prepare: {min_loops: 1, max_loops: 2}
phase_2_improve: {min_loops: 4, max_loops: 8}
phase_3_finalize: {min_loops: 2, max_loops: 4}
```

An explicit user override takes precedence over these defaults.

### Output Policy

- `auto` — default. Return the report in chat unless Prepare identifies a clearly
  appropriate durable, writable destination that already belongs to the work context.
  If so, persist it there and return a concise chat summary with its location.
- `chat` — return the full report in chat.
- `persist` — persist to the most appropriate confirmed destination; if none is clear
  or writable, fall back to chat and state the limitation.
- `both` — persist the report and also return it in chat.

A destination may be a repository, Drive, workspace document system, chatbot library,
knowledge base, or another persistent surface. Availability alone does not make a
surface appropriate. Prefer where the work already belongs; if ambiguous, use chat.
Never invent a storage convention or assume write access.

## Loop Integrity

A counted loop is one complete, substantive cycle of the **current phase's loop**. It
is not an edit, finding, file, subtask, tool call, or label around mechanical work.

Count a loop only when its cycle produces a material understanding, decision, work,
validation, risk, or confidence delta. A no-change loop may count when a distinct,
substantive investigation or validation closes important uncertainty.

Do not count:

- one isolated edit, fix, finding, file change, or subtask;
- rereading or restating the same evidence;
- repeated review or validation from the same perspective;
- mechanical execution without task-specific judgment;
- cosmetic churn or artificial splitting used to satisfy a loop count.

Never invent findings or simulate reasoning. If a phase minimum cannot be satisfied
with genuine cycles, do not claim that it was; return the best result and report the
budget shortfall.

A confirmed blocker may end a phase or the workflow before its minimum. Do not perform
fake loops after further execution has become impossible or unauthorized.

Do not expose private chain-of-thought. Report observable evidence, decisions, work,
validation, and outcomes only.

## Phase 1 — Prepare

Complete **1–2 Prepare loops** to establish a trustworthy execution strategy.

### Discover

Build an evidence-based picture of:

- **Task:** objective, scope, context, constraints, uncertainty, stakes, acceptance
  conditions, relevant evidence, likely failure modes, and natural work context.
- **Environment:** agent capabilities, tools, connected resources, permissions,
  governing instructions, write authority, validation surfaces, durable storage
  surfaces, and material limitations.

Confirm capabilities and authority when they affect execution. Do not assume a tool,
connection, permission, storage target, or write capability exists.

### Assess

Match task requirements against the actual environment. Identify material gaps,
uncertainties, dependencies, useful evidence and tools, major risks, persistence
context, and authority boundaries.

Distinguish:

- **available** — the environment can technically perform an action;
- **authorized** — applicable system, user, workspace, and repository instructions
  permit that action.

Do not treat technical access as authorization. Also distinguish an unavailable
capability from one that has merely not been checked yet.

### Configure

Set the smallest viable strategy for Improve and Finalize. Configure only what changes
execution: useful tools and evidence surfaces, initial Research scope, assumptions,
acceptance conditions, Review emphasis, validation approach, transition signals, and
report delivery or persistence when context justifies it.

Keep the strategy adaptive. Do not script every future loop or route around governing
instructions merely because a tool makes it possible.

### Verify

Verify that the strategy is executable, proportionate, authorized, and free of material
unverified dependencies.

End each Prepare loop with a readiness result:

- **READY** — execution can proceed.
- **READY WITH LIMITS** — execution can proceed with explicit non-blocking limits.
- **BLOCKED** — a critical dependency, capability, authority, or evidence gap prevents
  trustworthy execution.

The first loop is mandatory. Use the second when material preparation uncertainty
remains. Enter Improve only if readiness is `READY` or `READY WITH LIMITS`; otherwise
stop and report the blocker.

## Phase 2 — Improve

Complete **4–8 Improve loops**. This is the primary work phase.

### Research

Gather evidence needed for the current objective and unresolved findings. Start broad
enough to orient the work, then narrow as findings localize. Broaden again when the
problem boundary is unclear, evidence conflicts, or a core assumption fails. Change
evidence, method, or perspective when the previous investigation saturates.

Research may use current context, artifacts, repositories, data, prior results, domain
knowledge, or external sources. It is not synonymous with web search.

### Plan

Turn current evidence and findings into the smallest plan that can materially improve
the result. Set only the needed objective, scope, constraints, approach, work units,
trade-offs, acceptance conditions, and validation points.

### Work

Perform a meaningful batch of task-appropriate work against the plan and evidence.
Preserve confirmed constraints unless new evidence justifies changing them. Do not
claim work or validation that was not performed.

### Review

Use this default cadence by **Improve loop number**:

- **odd — Quality Review:** correctness, completeness, coherence, clarity, usability,
  evidence quality, and objective fit.
- **even — Pessimistic Review:** consequential failure modes, edge cases, hidden
  assumptions, regressions, misuse, operational risk, and security or safety when
  relevant.

The cadence is a default, not a ritual. Override it when current risk clearly requires
a different perspective; do not force irrelevant review dimensions.

After four genuine loops, move to Finalize when the result is substantially shaped and
remaining work is mainly finishing or validation. Otherwise continue while a material
delta remains, up to eight loops. At eight, carry unresolved material findings into
Finalize.

## Phase 3 — Finalize

Complete **2–4 Finalize loops**. Finalize is the completion gate for the work.

Finalize loop:

**Inspect → Resolve → Validate → Gate**

### Inspect

Inspect acceptance conditions, unresolved material findings, recent changes,
validation gaps, regressions, residual risks, and required phase-loop integrity. Look
only where an issue could still materially affect completion.

### Resolve

Correct, complete, revert, or explicitly accept what materially blocks trustworthy
completion. Reject new scope unless a core assumption failed or completion would
otherwise be misleading.

### Validate

Perform the smallest task-appropriate checks that can materially change confidence in
completion. Validate the result and final changes against important requirements,
evidence, regression risk, residual risk, and checks claimed by the work.

### Gate

Return one gate result:

- **PASS** — completion is trustworthy, required genuine-loop minima were satisfied,
  and any remaining limitations are non-blocking and documented.
- **RETRY** — an actionable material issue remains and another Finalize loop can
  meaningfully address it.
- **BLOCKED** — trustworthy completion cannot be reached with the remaining loop
  budget, evidence, capability, or authority.

Do not pass the gate before the Finalize minimum is satisfied. After two genuine loops,
stop on `PASS`; continue on `RETRY` while a material delta remains, up to four loops.
At four loops, unresolved completion-blocking issues produce `BLOCKED`, not a false
success.

A prior phase budget shortfall prevents `PASS` unless the user explicitly overrode that
budget. Do not use Finalize to retroactively legitimize fake or missing loops.

## Reporting

Keep a compact observable record while working.

For every counted loop, write one line using the phase's actual cycle:

```text
Prepare N — D: <discovery> | A: <assessment> | C: <configuration> | V: <readiness>
Improve N — R: <research> | P: <decision> | W: <work> | R: <review>
Finalize N — I: <inspection> | R: <resolution> | V: <validation> | G: <gate>
```

Each field states only the material delta. Do not expand one action into multiple loop
lines.

For each phase reached, write **one paragraph** summarizing its objective, major
decisions or changes, evidence or validation, and remaining material concerns.

When the workflow ends for any reason, produce a work report with one final status:

- **COMPLETE** — required phase budgets were genuinely satisfied and Finalize passed.
- **INCOMPLETE** — a best-effort result exists, but required loop depth or validation
  was not genuinely satisfied.
- **BLOCKED** — a material capability, evidence, authority, or completion blocker
  prevented trustworthy completion.

Include the final result, loop summaries grouped by phase, one paragraph per phase
reached, material decisions and validation, and unresolved findings, limitations,
blockers, or checks not performed.

Deliver or persist the report according to `output_policy`. Reporting happens after
execution ends and never counts as another loop.
