---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through adaptive multi-phase loops. Use when the
  user asks for deep iterative work, repeated improvement or review loops, says to run
  loops, or explicitly asks for RPI, RPWR, an RPI loop, or an RPWR loop instead of a
  single-pass result.
---

# RPWR Loop

Use **RPWR** for difficult or high-level work. `RPI` is an alias.

1. **Prepare** — `Discover → Assess → Configure → Verify`
1. **Improve** — `Research → Plan → Work → Review`
1. **Finalize** — `Inspect → Resolve → Validate → Gate`

Count only genuine cycles of the current phase.

## Arguments

```yaml
output_policy: auto  # auto | chat | persist | both
phase_1_prepare: {min_loops: 1, max_loops: 2}
phase_2_improve: {min_loops: 4, max_loops: 8}
phase_3_finalize: {min_loops: 1, max_loops: 2}
```

Explicit user overrides take precedence.

Phase budgets belong to one RPWR run. Do not reset them by silently starting another
run. Another run requires explicit user continuation or an already-established
higher-level campaign/iteration budget that clearly authorizes it.

### Output Policy

- `auto` — use chat unless Prepare finds an appropriate writable destination already
  belonging to the work; then persist there and return a concise chat summary.
- `chat` — return the full report in chat.
- `persist` — persist to the confirmed destination; if none is appropriate/writable,
  fall back to chat and state the limitation.
- `both` — persist and return the report in chat.

Availability alone does not make a destination appropriate. Prefer where the work
already belongs; if ambiguous, use chat. Never invent storage conventions or write
access.

# Integrity

## Loop Integrity

A counted loop is one complete, substantive cycle of the current phase, not an edit,
finding, file, subtask, tool call, or label around mechanical work.

Count it only when the cycle materially changes understanding, a decision, work,
validation, risk, or confidence. A no-change loop may count when distinct substantive
investigation or validation closes important uncertainty.

Name loops by the material question, risk, or uncertainty resolved, not by file groups
or mechanical work units.

Do not count:

- isolated edits, fixes, findings, files, or subtasks;
- rereading/restating the same evidence;
- repeated review from the same perspective;
- mechanical execution without task-specific judgment;
- cosmetic churn or artificial splitting.

Never invent findings or simulate reasoning. If genuine minima cannot be satisfied,
report the shortfall. A confirmed blocker may stop execution before its minimum; never
manufacture loops after work is blocked or unauthorized.

Do not expose private chain-of-thought. Report observable evidence, decisions, work,
validation, and outcomes only.

## Phase Discipline

Progression is monotonic: `Prepare → Improve → Finalize`.

Do not return to an earlier phase for ordinary remediation. Once Finalize begins, handle
bounded issues in its `Resolve`, using the second Finalize loop after `RETRY` when needed.

If Finalize discovers a core-assumption failure requiring broad Research, replanning, or
substantial reshaping, return `BLOCKED`; do not reopen Improve. `BLOCKED` ends the
current run. Another run requires the run-start authority defined above.

## Acceptance Ledger

For multiple consequential completion conditions, explicit gates, or costly false
completion, Prepare creates a compact acceptance ledger. Skip it for a simple task with
one obvious success condition.

```text
Gate | Evidence needed | Status
```

Use `pending`, `pass`, `fail`, `accepted-limit`, or `not-applicable`.

- Prepare establishes material gates and evidence.
- Improve updates a gate in the same loop when evidence changes it.
- Finalize checks every material gate before `PASS`.

The ledger is working state, not a deliverable or loop. Add newly discovered material
gates explicitly. Never infer `pass` from intended work. `accepted-limit` cannot relax a
user, policy, or contract requirement unless the same authority permits it.

# Phase 1 — Prepare

Complete **1–2 Prepare loops**.

## Discover

Build an evidence-based view of the **task** (objective, scope, constraints, stakes,
acceptance conditions, evidence, failure modes) and **environment** (capabilities, tools,
permissions, governing instructions, write authority, validation/persistence surfaces,
limitations). Confirm capabilities and authority when they affect execution.

## Assess

Match requirements to the environment and identify material gaps, dependencies,
evidence/tools, risk, and authority boundaries. Distinguish **available** (technically
possible) from **authorized** (permitted), and unavailable from merely unchecked.

## Configure

Choose the smallest viable Improve/Finalize strategy: evidence, Research scope,
assumptions, gates, Review emphasis, validation, transitions, and persistence. If
warranted, materialize the ledger with observable evidence. Keep the strategy adaptive.

## Verify

Verify the strategy is executable, proportionate, authorized, and free of material
unchecked dependencies. For a ledger, every known material gate needs an evidence path
or explicit non-blocking limitation.

Return:

- **READY**
- **READY WITH LIMITS**
- **BLOCKED**

The first Prepare loop is mandatory. Use a second only while material preparation
uncertainty remains. Enter Improve only from `READY` or `READY WITH LIMITS`.

# Phase 2 — Improve

Complete **4–8 Improve loops**.

## Research

Gather evidence for the current objective and unresolved findings. Orient broadly,
narrow as findings localize, and broaden again when boundaries are unclear, evidence
conflicts, or a core assumption fails. Change method or perspective when investigation
saturates. Research is not synonymous with web search.

Allocate internal vs external research by uncertainty and expected information gain, not
a fixed ratio. Favor internal evidence for artifact/repository/data truth; favor external
evidence for freshness, standards, vendor behavior, alternatives, or independent
challenge. Use both when local conclusions need grounding.

## Plan

Turn evidence into the smallest plan that can materially improve the result: needed
scope, constraints, approach, trade-offs, gates, and validation.

## Work

Perform a meaningful batch against the plan. Preserve confirmed constraints unless
evidence justifies change. Never claim unperformed work/validation. Update changed gates
in the same loop.

## Review

Default cadence by Improve loop number:

- **odd — Quality Review** — correctness, completeness, coherence, clarity, usability,
  evidence quality, objective fit.
- **even — Pessimistic Review** — consequential failure modes, edge cases, hidden
  assumptions, regressions, misuse, operational/security/safety risk when relevant.

Override the cadence when risk clearly needs another perspective.

Treat concrete failure/correction as evidence for the next unresolved question. If the
same failure recurs, change the plan, evidence, or approach rather than repeating it.

After four genuine loops, move to Finalize when the result is substantially shaped, no
known issue requires broad reshaping, and remaining work is mainly completion or
validation. Otherwise continue while material deltas remain, up to eight loops. Carry
unresolved findings into Finalize honestly.

# Phase 3 — Finalize

Complete **1–2 Finalize loops** using:

`Inspect → Resolve → Validate → Gate`

## Inspect

Inspect gates, unresolved findings, recent changes, validation gaps, regressions,
residual risk, and loop integrity. Look only where completion could still change.

## Resolve

Correct, complete, revert, or explicitly accept what blocks trustworthy completion.
Keep remediation bounded to the shaped result and reject new scope. If broad new
Research/replanning/reshaping is required, Gate must become `BLOCKED`.

## Validate

Run the smallest checks that can change completion confidence. Validate requirements,
regressions, residual risk, and claimed checks. Validate ledger gates against named
evidence; `pending` or `fail` cannot silently pass.

## Gate

Return:

- **PASS** — genuine loop minima are satisfied; material gates pass or are validly
  accepted as non-blocking; limitations are documented.
- **RETRY** — one more bounded Finalize loop can resolve and validate an actionable
  material issue without reopening Improve.
- **BLOCKED** — trustworthy completion requires unavailable budget/evidence/capability/
  authority or broad reshaping.

Stop on first `PASS`. On first `RETRY`, run one additional
`Inspect → Resolve → Validate → Gate` cycle. Do not relabel its remediation as Improve.
A blocking issue after Finalize 2 yields `BLOCKED`.

A prior phase-budget shortfall prevents `PASS` unless the user explicitly overrode that
budget. Finalize cannot retroactively legitimize fake or missing loops.

# Output

## Live Progress

When the user can see execution, prefer scan-friendly updates. Follow explicit user
cadence/format overrides.

Emit after a counted loop or material gate/status change, not every tool call. Do not
repeat unchanged evidence.

For a completed counted loop:

```markdown
**Improve 3/8 — <material question or outcome>**
- **Research** — <new evidence>
- **Plan** — <decision or next approach>
- **Work** — <meaningful work completed>
- **Review** — <finding, risk, or confidence change>
```

Use the actual phase fields:

- Prepare — **Discover / Assess / Configure / Verify**
- Improve — **Research / Plan / Work / Review**
- Finalize — **Inspect / Resolve / Validate / Gate**

For a material gate/status change outside a completed cycle:

```markdown
**Gate update — <gate>**
- **Status** — <new status>
- **Impact** — <what this changes>
```

A gate-only update is **not a counted loop**. Give it no loop number and exclude it from
Final Reporting.

Keep fields short. Put the main delta in the title. Use status symbols only when they
encode real state. Do not dump the full ledger; surface changed/blocking gates.

An optional phase transition line may help orientation:

```text
Improve complete — 4 genuine loops | gates: 5 pass, 1 pending
```

## Final Reporting

Keep the final/persisted record compact and audit-oriented. For every counted loop:

```text
Prepare N — D: <discovery> | A: <assessment> | C: <configuration> | V: <readiness>
Improve N — Research: <research> | Plan: <decision> | Work: <work> | Review: <review>
Finalize N — I: <inspection> | R: <resolution> | V: <validation> | G: <gate>
```

Each field states only the material delta. Preserve phase fields rather than collapsing
them into ambiguous workstream-only labels.

Numbered live updates and Final Reporting describe the same loop record. Unnumbered gate
updates are working-state notifications, not loops. Do not duplicate live and audit
formats in the same update.

For each reached phase, add one paragraph on objective, material changes,
evidence/validation, and remaining concerns.

End with one workflow status:

- **COMPLETE** — required phase budgets were genuinely satisfied and Finalize passed.
- **INCOMPLETE** — a best-effort result exists but required depth/validation did not.
- **BLOCKED** — a material capability, evidence, authority, or completion blocker
  prevented trustworthy completion.

Include the result, loop summaries, phase paragraphs, validation, and unresolved
limitations/checks. If a ledger was used, include its final material gate state.

Deliver/persist according to `output_policy`. Reporting happens after execution and
never counts as another loop.
