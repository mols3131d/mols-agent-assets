# Execution Adaptation for Chatbot Harnesses

Load this reference **only when designing or repairing a chatbot harness whose applicable
agent instructions require execution, delegation, or tool behavior the active chat runtime
cannot natively provide**. It guides authors of chatbot-facing instructions; it does not
itself perform the target task, authorize tool use, or establish a universal fallback.

## Diagnose a real gap

1. Identify the specific source contract and task scope: required behavior, inputs and
   outputs, source/ref, order, dependencies, permissions, side effects, evidence, and any
   required independence or isolation. Include commands, scripts, tools, delegation,
   scheduled work, or other execution mechanisms **only when the target uses them**.
2. Check the actual runtime mode, connected and exposed tools, accessible sources,
   execution environment, and current authorization. Reuse native or established
   alternatives first. A product capability description is not evidence of current access.
3. Separate a missing executable capability from a missing first-hop or asset-selection
   path. Repair discovery through the existing entry/router; do not write an execution
   fallback for a routing problem.
4. Do not add persistent guidance for a gap that is absent, wholly optional, or already
   addressed by the target's existing instructions. For a one-off limitation, an in-task
   explanation or handoff may be cheaper than a durable harness change.

## Choose an outcome for each required responsibility

| Outcome | Condition |
| --- | --- |
| Native | Available tool or runtime behavior satisfies the original contract. |
| Adapted execution | An authorized mechanism preserves the contract's **material** input/output, ordering, side-effect, trust, and independence requirements. Document any nonmaterial difference. |
| Partial | A useful, independently valid subset can be performed safely while remaining requirements are explicitly left open. |
| Skip | The step is optional under the authoritative contract and user goal; omission does not invalidate required outcomes. Disclose any material effect. |
| Handoff / blocked | A necessary capability, source, authorization, safety condition, or required isolation cannot be preserved. State the exact remaining action and who can perform it. |

These are decisions, not an ordered fallback ladder. Do not redefine a required step as
optional to obtain a successful outcome. If the user requested complete execution,
partial work and handoff are not complete execution. The user must be able to distinguish
what ran, what was omitted, and what remains.

## Author the smallest applicable instruction

Place durable guidance only in a **target-owned instruction surface the future chat
runtime actually reads**, or in an existing conditional reference reachable from it.
Use `CHATBOT.md` only where it is an established or authorized compatibility entrypoint.
Keep authoritative project policy, source asset behavior, and tool permissions with their
existing owners. Do not copy whole scripts, agent definitions, or catalogs into the entry.

Write a concise conditional rule that supplies:

- **Trigger and scope:** the missing capability and the task/path where it matters; don't
  activate this fallback when native execution is sufficient.
- **Source of truth:** how to reach the actual instruction/command/script/agent definition
  at the correct revision, and which semantics cannot be relaxed.
- **Permitted adaptation:** usable native tool or bounded substitution, required inputs,
  dependencies and expected observable result; preserve the original verification logic.
- **Safety gates:** actual tool permissions, identity, side effects, external writes,
  isolation, independence, and approvals. A tool's availability is not permission.
- **Failure disposition:** when to perform a safe subset, skip an optional step, or stop
  and hand off; specify the *missing* capability/approval and an actionable next step.
- **Evidence and disclosure:** identify what was directly executed and observed versus
  simulated, inferred, not run, or blocked; report any meaningful loss of fidelity to the
  user in the task result.

These are authoring considerations, **not a new file schema or required template**.
Prefer direct, executable wording over an abstract decision matrix in the resulting
runtime instruction. Do not install an adapter or add a new persistent asset merely
because one is available.

When proposing or making a durable change, identify the target file/instruction owner,
the actual trigger, the minimal text or patch, and how a future task will reach it.
Check the applicable scope/ref and whether existing instructions conflict. If the
entry surface cannot be changed, provide that same actionable patch as a user-side
handoff rather than claiming it is installed.

## Representative patterns

**Scripts / CLI.** When shell/CLI is absent but a permitted code executor is available,
retrieve and inspect the exact original program/ref, its dependencies, I/O, working
directory, external commands, and side effects before attempting an equivalent call.
A thin invocation adapter is acceptable only if it preserves the meaningful operation
and safety boundary. If dependencies or runtime semantics cannot be reproduced, perform
only an independently useful subset or hand off. Never label a reimplementation or
partial check as a successful run of the original command.

**Subagents / delegation.** Prefer actual target-supported delegation. When native
subagents are unavailable, sequential role-specific passes may be useful **only if the
original contract permits shared-context sequential work**. Preserve role ownership,
inputs/outputs, handoffs, and final decision authority. A single model's sequential
perspectives are not independent, concurrent, isolated, or separately permissioned
agents; if any of those properties is required, report the gap and hand off rather than
claim parity.

**Commands, integrations, and side effects.** Where a command or service action is
unavailable, first check for an authorized native tool with equivalent scope. Read-only
analysis or a proposed change can be a partial result, not proof that a remote mutation
occurred. Do not invent endpoints, connections, identities, privileges, or approvals.
A user-facing handoff should identify the missing capability or approval and the exact
action required without exposing secret values.

**Long-running or scheduled work.** Do not promise later execution or monitoring when
the active runtime has no approved durable execution mechanism. Use existing authorized
scheduling only when its actual behavior and access are known; otherwise describe the
bounded work completed now and the user's next step.

## Example instruction shapes

The following are **illustrative conditionals**, not text to copy into every
`CHATBOT.md`. Adapt the source path, trigger, approval boundary, and actual tools
to the target's own contract.

**No shell, but a permitted code executor:**

> When a task requires the repository's original validation script but shell execution
> is unavailable, inspect that script at the task's ref, its dependencies and side
> effects. Use the available code executor only if the same verification and required
> environment can be preserved without new permissions. Otherwise run only a
> separately meaningful check and tell the user which original validation remains
> unexecuted, or hand it off with the exact command and prerequisites. Never call
> a partial substitute a passing repository-native validation.

**No native agent delegation:**

> When a selected workflow requires a Subagent and native delegation is unavailable,
> inspect the canonical role and independence requirements. If sequential
> shared-context passes are allowed, preserve role boundaries and distinguish them
> from independent agents in the result. If independence, separate permissions,
> isolation, or concurrency is essential, do not claim a substitute ran; report
> the blocked role and the required delegation environment to the user.

For these and other gaps, the fallback must apply **only** when the canonical behavior
is needed for the current task. Keep the user's final outcome and missing-work
disclosure in the normal task flow; do not bury it solely in maintainer documentation.

## Review and maintenance

- Check native-sufficient, reproducible-adaptation, partial-only, optional-skip, and
  required-block scenarios; focus on preserving the intended outcome and safety, not
  matching an arbitrary tool sequence.
- Ensure target changes are scoped to the actual consumer and are discoverable in a
  normal task. Re-evaluate source selection and fallback applicability on material
  task/path/ref, runtime mode, or exposed capability changes, without requiring this
  provisioning Skill to remain in normal-task context.
- Prefer a small edit to the existing instruction owner. Remove obsolete fallback
  guidance when native support becomes sufficient; do not keep a catalog of speculative
  platform exceptions.
- A source review can establish instruction quality but cannot prove runtime parity or
  successful execution. Record observed behavior only when the target runtime runs it.
