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
1. **Improve** — `Research → Plan → Work → Review`
1. **Finalize** — `Inspect → Resolve → Validate → Gate`

Count only genuine phase cycles. Do not force phases into the same reasoning shape.

## Arguments

```yaml
output_policy: auto  # auto | chat | persist | both
phase_1_prepare: {min_loops: 1, max_loops: 2}
phase_2_improve: {min_loops: 4, max_loops: 8}
phase_3_finalize: {min_loops: 1, max_loops: 2}
```

An explicit user override takes precedence over these defaults.

These phase budgets belong to one RPWR run. Do not reset or bypass them by
silently starting another run. A new run requires either explicit user continuation or
an already-established higher-level campaign/iteration budget that clearly authorizes
another run.

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

Name or summarize loops by the material question, risk, or uncertainty they resolve,
not by the file group or mechanical work unit they happened to touch.

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

## Phase Discipline

Phase progression is monotonic:

`Prepare → Improve → Finalize`

Do not return to an earlier phase for ordinary remediation. Once Finalize begins, a
material issue is handled by the current Finalize loop's `Resolve`, or by the second
Finalize loop after `RETRY`.

If Finalize discovers that a core assumption failed so materially that broad Research,
replanning, or substantial reshaping is required, return `BLOCKED` rather than
silently reopening Improve. `BLOCKED` ends the current run. Its result may become input
to another run only when the user or an already-established higher-level budget
actually authorizes that run.

This rule keeps phase counts auditable and prevents finishing work from being relabeled
as extra Improve loops.

## Acceptance Ledger

When the task has multiple consequential completion conditions, explicit gates, or a
high cost of false completion, Prepare creates a compact **acceptance ledger**. Do not
create one for a simple task with one obvious success condition.

Track only material gates:

```text
Gate | Evidence needed | Status
```

Use statuses such as `pending`, `pass`, `fail`, `accepted-limit`, or `not-applicable`.
The ledger is working state, not another deliverable or loop.

- **Prepare** establishes the initial gates and evidence requirements.
- **Improve** updates the ledger when work or new evidence changes a gate.
- **Finalize** checks every material gate before `PASS`.

If a new material gate emerges after Prepare, add it explicitly instead of relying on
memory. Never mark a gate passed from intended work or inferred success; require the
evidence named by that gate. Do not use `accepted-limit` to relax an explicit user,
policy, or contract requirement unless the same authority permits that limitation.

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

If the task warrants an acceptance ledger, materialize it here with the evidence needed
for each gate. Prefer observable checks over vague success language.

Keep the strategy adaptive. Do not script every future loop or route around governing
instructions merely because a tool makes it possible.

### Verify

Verify that the strategy is executable, proportionate, authorized, and free of material
unverified dependencies. When an acceptance ledger exists, verify that every known
material gate has an evidence path or an explicit non-blocking limitation.

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

Allocate research effort adaptively across internal and external evidence according to
current uncertainty, evidence gaps, task risk, and which source is most likely to
materially change understanding or confidence. Favor internal evidence when correctness
depends on the actual artifact, repository, data, or established work context; favor
external evidence when freshness, standards, vendor behavior, alternatives, or
independent validation matter. Use both when local conclusions need external grounding
or challenge. Do not target a fixed ratio.

### Plan

Turn current evidence and findings into the smallest plan that can materially improve
the result. Set only the needed objective, scope, constraints, approach, work units,
trade-offs, acceptance conditions, and validation points.

### Work

Perform a meaningful batch of task-appropriate work against the plan and evidence.
Preserve confirmed constraints unless new evidence justifies changing them. Do not
claim work or validation that was not performed.

When work or evidence changes a material acceptance gate, update the ledger in the same
loop. Do not postpone known gate state until Finalize.

### Review

Use this default cadence by **Improve loop number**:

- **odd — Quality Review:** correctness, completeness, coherence, clarity, usability,
  evidence quality, and objective fit.
- **even — Pessimistic Review:** consequential failure modes, edge cases, hidden
  assumptions, regressions, misuse, operational risk, and security or safety when
  relevant.

The cadence is a default, not a ritual. Override it when current risk clearly requires
a different perspective; do not force irrelevant review dimensions.

A concrete failure or correction becomes evidence for the next unresolved question.
Do not merely repeat the failed method; change the plan, evidence, or execution approach
when the same failure recurs.

After four genuine loops, move to Finalize when the result is substantially shaped,
no known issue still requires broad Improve-phase reshaping, and remaining work is
mainly completion or validation. Otherwise continue while a material delta remains, up
to eight loops. At eight, carry unresolved material findings into Finalize without
pretending they disappeared.

## Phase 3 — Finalize

Complete **1–2 Finalize loops**. Finalize is the completion gate for the work.

Finalize loop:

`Inspect → Resolve → Validate → Gate`

### Inspect

Inspect acceptance conditions, the acceptance ledger when present, unresolved material
findings, recent changes, validation gaps, regressions, residual risks, and required
phase-loop integrity. Look only where an issue could still materially affect completion.

### Resolve

Correct, complete, revert, or explicitly accept what materially blocks trustworthy
completion. Keep remediation bounded to finishing the shaped result. Reject new scope.

If the issue requires broad new Research, replanning, or substantial reshaping rather
than bounded completion work, do not return to Improve; the Gate must become `BLOCKED`.

### Validate

Perform the smallest task-appropriate checks that can materially change confidence in
completion. Validate the result and final changes against important requirements,
evidence, regression risk, residual risk, and checks claimed by the work.

When an acceptance ledger exists, validate its material gates against their named
evidence. A `pending` or `fail` gate cannot be silently treated as passed.

### Gate

Return one gate result:

- **PASS** — completion is trustworthy, required genuine-loop minima were satisfied,
  all material acceptance gates are passed or explicitly accepted as non-blocking, and
  remaining limitations are documented.
- **RETRY** — an actionable material issue remains and one more bounded Finalize loop
  can meaningfully resolve and validate it without reopening Improve.
- **BLOCKED** — trustworthy completion cannot be reached with the remaining Finalize
  budget, evidence, capability, authority, or without broad reshaping.

The first genuine Finalize loop is the normal completion gate. Stop on `PASS`. On
`RETRY`, run one additional genuine Finalize loop using the same
`Inspect → Resolve → Validate → Gate` cycle. Do not relabel its remediation as another
Improve loop. At the second Finalize loop, unresolved completion-blocking issues produce
`BLOCKED`, not a false success.

A prior phase budget shortfall prevents `PASS` unless the user explicitly overrode that
budget. Do not use Finalize to retroactively legitimize fake or missing loops.

## Live Progress

When the user can see work while it is running, prefer **scan-friendly loop updates**
over the dense audit line used in the final report. Follow an explicit user cadence or
format override when provided.

Emit a live update after a counted loop or another material gate/status change, not for
every tool call or mechanical action. Do not repeat unchanged evidence from the previous
update.

Use this default shape for a completed counted loop:

```markdown
**Improve 3/8 — <material question or outcome>**
- **Research** — <new evidence>
- **Plan** — <decision or next approach>
- **Work** — <meaningful work completed>
- **Review** — <finding, risk, or confidence change>
```

Use the current phase's actual field names:

- Prepare — **Discover / Assess / Configure / Verify**
- Improve — **Research / Plan / Work / Review**
- Finalize — **Inspect / Resolve / Validate / Gate**

A material gate/status change that occurs outside a completed phase cycle may be shown
as an unnumbered gate update, for example:

```markdown
**Gate update — <gate>**
- **Status** — <new status>
- **Impact** — <what this changes>
```

A gate-only update is **not a counted loop**. Do not assign it a new loop number or
include it as a loop record in Final Reporting.

Keep each field to one short sentence or fragment unless the material finding needs more
context. Put the most important delta in the title so the update is useful when skimmed.
Status symbols such as `✅`, `⚠️`, `❌`, or `⏳` may be used sparingly when they encode
real state; do not use decoration as structure.

When a phase completes, optionally add one compact transition line when it helps the
user orient:

```text
Improve complete — 4 genuine loops | gates: 5 pass, 1 pending
```

Do not dump the full acceptance ledger on every update. Surface only gates whose state
changed or that currently block progress.

## Final Reporting

Keep a compact audit-oriented record for the final or persisted work report.

For every counted loop, record one line using the phase's actual cycle:

```text
Prepare N — D: <discovery> | A: <assessment> | C: <configuration> | V: <readiness>
Improve N — Research: <research> | Plan: <decision> | Work: <work> | Review: <review>
Finalize N — I: <inspection> | R: <resolution> | V: <validation> | G: <gate>
```

Each field states only the material delta. Do not expand one action into multiple loop
lines. Preserve these phase fields in a persisted report instead of collapsing them into
ambiguous `I1`, `I2`, or workstream-only summaries when auditability matters.

Numbered live loop updates and final reporting are two presentations of the same
observable loop record. Unnumbered gate-only updates are working-state notifications,
not loop records. Do not duplicate live and audit formats in the same update.

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
blockers, or checks not performed. When an acceptance ledger was used, include its final
material gate state or an equivalent concise gate summary.

Deliver or persist the report according to `output_policy`. Reporting happens after
execution ends and never counts as another loop.
