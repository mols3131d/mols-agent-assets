---
name: rpwr-loop
description: >-
  Improve difficult or high-level work through an adaptive Research → Plan → Work →
  Review main loop supported by Prepare and Finalize workflows. Use when the user asks
  for deep iterative work, repeated improvement or review loops, says to run loops, or
  explicitly asks for RPI, RPWR, an RPI loop, or an RPWR loop instead of a single-pass
  result.
---

# RPWR Loop

Use **RPWR** as one iterative main loop with two supporting workflows. `RPI` is an alias.

```text
Prepare workflow
→ RPWR main loop: Research → Plan → Work → Review × N
→ Finalize workflow
```

Only the RPWR main loop is counted. Prepare and Finalize are workflows, not loops.

# Arguments

All arguments are optional.

```yaml
output_policy: auto       # auto | chat | persist | both
rpwr_loops: {min: 2, max: 10}
acceptance_ledger: auto   # auto | on | off
live_progress: auto       # auto | compact | quiet
research_policy: auto     # auto | internal | external | mixed
```

Explicit user overrides take precedence unless they conflict with higher authority.
Workflow order, genuine-loop counting, evidence-based completion, and authority checks
are invariants rather than configurable options.

`rpwr_loops` applies only to the RPWR main loop. Do not reset its budget by silently
starting another run. Another run requires explicit user continuation or an
already-established higher-level campaign/iteration budget that clearly authorizes it.

## Execution Policies

- `acceptance_ledger: auto` — create a ledger only for consequential multi-gate work.
  `on` forces an explicit ledger; `off` suppresses the explicit ledger but never removes
  required acceptance conditions.
- `live_progress: auto` — surface useful loop/stage updates without narrating mechanics.
  `compact` reports each counted loop plus material gate changes. `quiet` reports only
  major transitions, blockers, and completion.
- `research_policy: auto` — allocate internal/external evidence by uncertainty and
  expected information gain. `internal` or `external` constrains the primary evidence
  surface when the task permits it. `mixed` deliberately uses both where material.
  Higher-authority freshness or verification requirements still apply.

## Output Policy

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

## Main-Loop Integrity

A counted loop is one complete, substantive `Research → Plan → Work → Review` cycle,
not an edit, finding, file, subtask, tool call, or label around mechanical work.

Count it only when the cycle materially changes understanding, a decision, work,
validation, risk, or confidence. A no-change loop may count when distinct substantive
investigation or validation closes important uncertainty.

Name loops by the material question, risk, or uncertainty resolved, not by file groups
or mechanical work units.

Do not count isolated edits, repeated evidence, mechanical execution, cosmetic churn,
or artificial splitting. Never invent findings or simulate reasoning. If genuine minima
cannot be satisfied, report the shortfall instead of manufacturing loops.

Prepare and Finalize never contribute to the loop count.

Do not expose private chain-of-thought. Report observable evidence, decisions, work,
validation, and outcomes only.

## Stage Discipline

Progression is monotonic:

`Prepare workflow → RPWR main loop → Finalize workflow`

Prepare establishes execution readiness. Finalize closes the shaped result. Neither is a
second improvement loop in disguise.

Once Finalize begins, bounded finishing work stays in `Resolve`. If Finalize discovers a
core-assumption failure requiring broad Research, replanning, or substantial reshaping,
return `BLOCKED`; do not reopen the main loop inside the same run. Another run requires
the run-start authority defined above.

## Acceptance Ledger

For multiple consequential completion conditions, explicit gates, or costly false
completion, use a compact ledger:

```text
Gate | Evidence needed | Status
```

Use `pending`, `pass`, `fail`, `accepted-limit`, or `not-applicable`.

- Prepare establishes material gates and evidence.
- The RPWR loop updates a gate in the same loop when evidence changes it.
- Finalize checks every material gate before `PASS`.

The ledger is working state, not a deliverable or loop. Add newly discovered material
gates explicitly. Never infer `pass` from intended work. `accepted-limit` cannot relax a
user, policy, or contract requirement unless the same authority permits it.

# Prepare Workflow

Run once before the main loop:

`Discover → Assess → Configure → Verify`

The workflow may revisit its own steps while establishing readiness, but those passes
are not counted loops.

## Discover

Build an evidence-based view of the **task** (objective, scope, constraints, stakes,
acceptance conditions, evidence, failure modes) and **environment** (capabilities, tools,
permissions, governing instructions, write authority, validation/persistence surfaces,
limitations).

## Assess

Match requirements to the environment and identify material gaps, dependencies,
evidence/tools, risks, and authority boundaries. Distinguish **available** (technically
possible) from **authorized** (permitted), and unavailable from merely unchecked.

## Configure

Choose the smallest viable strategy for the main loop and Finalize: evidence surfaces,
Research scope, assumptions, acceptance gates, Review emphasis, validation, transition
signals, and persistence. Apply the optional execution policies. Keep the strategy
adaptive rather than scripting every future loop.

## Verify

Verify the strategy is executable, proportionate, authorized, and free of material
unchecked dependencies. For a ledger, every known material gate needs an evidence path
or explicit non-blocking limitation.

Return one readiness state:

- **READY**
- **READY WITH LIMITS**
- **BLOCKED**

Enter the main loop only from `READY` or `READY WITH LIMITS`.

# RPWR Main Loop

Run `Research → Plan → Work → Review` within `rpwr_loops`.

## Research

Gather evidence for the current objective and unresolved findings. Orient broadly,
narrow as findings localize, and broaden again when boundaries are unclear, evidence
conflicts, or a core assumption fails. Change method or perspective when investigation
saturates. Research is not synonymous with web search.

Under `research_policy: auto`, allocate internal vs external research by uncertainty and
expected information gain, not a fixed ratio. Favor internal evidence for
artifact/repository/data truth; favor external evidence for freshness, standards,
vendor behavior, alternatives, or independent challenge.

## Plan

Turn evidence into the smallest plan that can materially improve the result: needed
scope, constraints, approach, trade-offs, gates, and validation.

## Work

Perform a meaningful batch against the plan. Preserve confirmed constraints unless
evidence justifies change. Never claim unperformed work or validation. Update changed
acceptance gates in the same loop.

## Review

Default cadence by counted loop number:

- **odd — Quality Review** — correctness, completeness, coherence, clarity, usability,
  evidence quality, objective fit.
- **even — Pessimistic Review** — consequential failure modes, edge cases, hidden
  assumptions, regressions, misuse, operational/security/safety risk when relevant.

Override the cadence when current risk clearly needs another perspective.

Treat concrete failure/correction as evidence for the next unresolved question. If the
same failure recurs, change the plan, evidence, or approach rather than repeating it.

After the minimum genuine loops, move to Finalize when the result is substantially
shaped, no known issue requires broad reshaping, and remaining work is mainly completion
or validation. Otherwise continue while material deltas remain, up to the configured
maximum. Carry unresolved findings into Finalize honestly.

# Finalize Workflow

Run once after the main loop:

`Inspect → Resolve → Validate → Gate`

Finalize is a completion workflow, not a counted loop. It may perform bounded finishing
corrections in `Resolve` and validate them before `Gate`; do not turn those corrections
into hidden RPWR loops.

## Inspect

Inspect acceptance gates, unresolved findings, recent changes, validation gaps,
regressions, residual risk, and main-loop integrity. Look only where completion could
still materially change.

## Resolve

Correct, complete, revert, or explicitly accept what blocks trustworthy completion.
Keep remediation bounded to the shaped result and reject new scope. If broad new
Research/replanning/reshaping is required, the Gate must become `BLOCKED`.

## Validate

Run the smallest checks that can materially change completion confidence. Validate
requirements, regressions, residual risk, and checks claimed by the work. Validate
ledger gates against named evidence; `pending` or `fail` cannot silently pass.

## Gate

Return one result:

- **PASS** — genuine main-loop minima are satisfied; material gates pass or are validly
  accepted as non-blocking; limitations are documented.
- **INCOMPLETE** — a best-effort result exists, but required loop depth or completion
  evidence remains unsatisfied after bounded finishing work.
- **BLOCKED** — trustworthy completion requires unavailable
  budget/evidence/capability/authority or broad reshaping.

A main-loop budget shortfall prevents `PASS` unless the user explicitly overrode that
budget. Finalize cannot retroactively legitimize fake or missing loops.

# Output

## Live Progress

Follow explicit user cadence/format overrides first.

For a counted main loop:

```markdown
**RPWR 3/10 — <material question or outcome>**
- **Research** — <new evidence>
- **Plan** — <decision or next approach>
- **Work** — <meaningful work completed>
- **Review** — <finding, risk, or confidence change>
```

Prepare/Finalize updates are unnumbered:

```markdown
**Prepare — READY**
- **Discover** — <task/environment delta>
- **Assess** — <risk or constraint>
- **Configure** — <execution strategy>
- **Verify** — <readiness>
```

```markdown
**Finalize — PASS**
- **Inspect** — <material final finding>
- **Resolve** — <bounded completion work>
- **Validate** — <evidence>
- **Gate** — <result>
```

For a material gate/status change outside a completed main-loop cycle:

```markdown
**Gate update — <gate>**
- **Status** — <new status>
- **Impact** — <what this changes>
```

Gate-only updates and Prepare/Finalize workflow updates are not counted loops. Do not
assign them loop numbers. Keep fields short, avoid repeated unchanged evidence, and do
not dump the full ledger on every update.

## Final Reporting

Keep the final/persisted record compact and audit-oriented:

```text
Prepare — D: <discovery> | A: <assessment> | C: <configuration> | V: <readiness>
RPWR N — Research: <research> | Plan: <decision> | Work: <work> | Review: <review>
Finalize — I: <inspection> | R: <resolution> | V: <validation> | G: <gate>
```

Only RPWR main-loop records are numbered and repeated. Prepare and Finalize appear once.
Live and final formats describe the same observable work without exposing private
reasoning.

Add concise stage summaries when useful. End with one workflow status:

- **COMPLETE** — required main-loop budget was genuinely satisfied and Finalize passed.
- **INCOMPLETE** — a best-effort result exists but required depth/validation did not.
- **BLOCKED** — a material capability, evidence, authority, or completion blocker
  prevented trustworthy completion.

Include unresolved limitations/checks and final material gate state when a ledger was
used. Deliver/persist according to `output_policy`. Reporting never counts as a loop.
