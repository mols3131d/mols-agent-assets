# ChatGPT Work Chatbot Skill Sync

## Intent

**Synchronize canonical repository chatbot Skills into reusable ChatGPT Personal Skills through ChatGPT Work.**

Do not interpret this as “read the Skill files into this chat.” The task is to create or update actual reusable ChatGPT Skills from the selected canonical repository Skills and complete the native Skill installation flow.

This is a ChatGPT-specific orchestration Prompt. It owns the ChatGPT Work surface, Skill Creator invocation, draft fidelity review, and native Install/update flow. `mols-skill-find` and `mols-skill-install` remain chatbot-service-agnostic control Skills for discovery, identity, reconciliation, and generic policy.

A changed set of **N Skills may legitimately require N native Install/update confirmations**. That is an expected success path, not a reason to fall back to package export or temporary loading.

## Arguments

```yaml
source: <auto>
ref: <auto>
target: ChatGPT
surface: Work
scope: <auto>
on_conflict: <auto>
```

- `source` — repository or Skill source to synchronize. `<auto>` delegates source resolution to `mols-skill-find`, including its default asset repository.
- `ref` — source revision. `<auto>` resolves one current source revision and pins the whole run to it when possible.
- `target` — ChatGPT Personal Skills.
- `surface` — execution surface. Default to ChatGPT Work. Outside Work, continue only if the active ChatGPT surface actually exposes equivalent Personal Skill create/modify and native Install/update capability.
- `scope` — capabilities to synchronize. `<auto>` discovers the complete repository-declared chatbot Skill set with a ChatGPT-compatible projection.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` never authorizes a destructive conflict resolution.

`<auto>` is an inference sentinel. Do not duplicate generic discovery, identity, collision, rename, or target-selection policy owned by the control Skills.

## Pin the Canonical Run

Resolve one `source + ref` for the run before discovery and keep all repository reads pinned to that revision when the source supports revisions.

From the same revision, read:

- `src/skills-chatbot/mols-skill-find.skill.md`
- `src/skills-chatbot/mols-skill-install.skill.md`

Apply them as task-local control instructions for this run. Installed copies, if any, are target state to reconcile, not authority for the current run. Task-local loading is not installation.

The two control Skills are ordinary synchronization targets too. Synchronize them last so a just-updated controller cannot reinterpret the current run.

Report **Bootstrap Required** only when either canonical control source cannot be obtained or safely applied.

## Preflight the ChatGPT Skill Surface

Before inventory or mutation, establish the smallest facts required to execute the native Skill flow:

1. The active ChatGPT surface can create or modify reusable Personal Skills.
1. A Skill creation/modification request can reach the product's Skill Creator flow.
1. ChatGPT can surface the native Install/update confirmation required to persist the Skill.
1. The resolved canonical repository source is readable.

`skill-creator` is a host-provided ChatGPT capability, not a repository dependency. Do not search the source repository for it or try to bootstrap it as one of the repository Skills. Trigger it through an actual Skill create/modify request.

Do not infer that Skill creation is unavailable merely because installed-Skill listing or full target-state inspection is unavailable. Limited inspection may reduce reconciliation confidence without blocking a native create/modify flow that can surface collisions itself.

If reusable Skill creation or native installation is genuinely unavailable on the active surface, stop before discovery-heavy work and report:

**Unsupported Surface — run this Prompt in ChatGPT Work with Personal Skills available.**

Do not silently substitute a generated `SKILL.md`, ZIP, attachment, editor paste, or temporary in-context load. Use a manual/upload fallback only when the user explicitly requests it.

## Discover

Execute the canonical `mols-skill-find` instructions with:

```yaml
source: <resolved source>
ref: <resolved ref>
target: ChatGPT
scope: <resolved scope>
query: <auto>
profiles: <auto>
```

Treat this as a complete inventory/synchronization search.

Require discovery to:

- use repository evidence instead of fixed Skill paths;
- group target-specific siblings as one capability;
- choose at most one preferred ChatGPT-compatible projection per capability;
- expose unsupported or identity-uncertain cases instead of forcing a selection.

Do not mutate ChatGPT Skills during discovery.

## Reconcile

Apply the canonical `mols-skill-install` reconciliation rules with:

```yaml
action: sync
selection: <mols-skill-find result>
target: ChatGPT
on_conflict: <resolved on_conflict>
```

Use it to decide identity, current-vs-stale state, create-vs-update, rename continuity, conflicts, customization boundaries, and orphan candidates when observable.

For this Prompt, **the ChatGPT-specific execution path below owns delivery**. Do not let a generic installer fallback replace an available Work → Skill Creator → native Install/update flow.

If full target-state inspection is unavailable, do not abort the whole synchronization. Reconcile each item using the strongest native evidence available. Let the native Skill flow update a confirmed same-identity Skill or create a missing one when it can do so safely; if it cannot distinguish a collision safely, mark only that item `Conflict` or `Unsupported` and continue with unrelated items.

Never invent reconciliation evidence.

## Synchronize Each Capability

Process one selected capability at a time. Skip `Already Current` items without invoking Skill Creator.

### Choose the operation

- **No existing match** — create a ChatGPT Skill.
- **Same identity, stale content** — modify/update the existing ChatGPT Skill.
- **Confirmed rename or migration** — modify/migrate the existing Skill when the product supports continuity.
- **Conflict or uncertain destructive identity** — stop that item until `on_conflict` or explicit user choice resolves it.

A blocked, unsupported, or conflicting item does not block unrelated selected capabilities.

### Invoke the Skill Creator

For every create or modify item, issue an **actual ChatGPT Skill creation/modification request** through the product Skill flow. Do not merely describe what Skill Creator should do.

Use the equivalent native intent:

- **Create** — create a ChatGPT Skill from the pinned canonical repository Skill.
- **Update** — modify the existing same-identity ChatGPT Skill to match the pinned canonical repository Skill.

Treat the selected repository Skill as canonical. Preserve its:

- name and description;
- activation intent and negative boundary;
- behavioral contract and invariants;
- procedure/workflow semantics;
- output semantics;
- runtime-required relationships that the chosen ChatGPT projection depends on.

Make only transformations required for ChatGPT Skill compatibility. Do not redesign, simplify, expand, “improve,” or reinterpret the capability during synchronization.

### Review the draft

Review the generated draft only for:

1. fidelity to the pinned canonical source;
1. required ChatGPT Skill compatibility;
1. accidental omission, semantic drift, or unsupported dependency.

Do not turn synchronization into an editorial improvement pass. If fidelity cannot be preserved, mark the item `Unsupported` instead of installing a degraded Skill.

### Complete native installation

After the draft or modification is ready, use the native ChatGPT Install/update action.

- If ChatGPT requires user confirmation, surface that native action immediately as `Pending User Action`.
- **One confirmation per changed Skill is acceptable.** Do not optimize those clicks away by changing the requested end state.
- Prefer completing one Skill's native flow before advancing to the next when the surface allows resumption after confirmation.
- After confirmation, resume the same synchronization run and continue with the next selected capability when the surface supports continuation. Do not require the user to restate the sync request.
- Verify the strongest available evidence that the reusable Skill is installed or updated before reporting success.
- If confirmation completion is not observable, keep the item pending rather than claiming installation.

## Ordering

Synchronize ordinary selected capabilities first.

Synchronize `mols-skill-find` and `mols-skill-install` last. Their task-local pinned versions continue governing the current run even if their installed copies are updated during the run.

Do not restart discovery or reinterpret earlier decisions against a newly installed controller.

## Hard Boundaries

The intended path is:

```text
pinned repository Skill
→ actual ChatGPT create/modify request
→ Skill Creator
→ fidelity review
→ native Install/update confirmation
→ reusable ChatGPT Skill
```

- In-context loading is not synchronization.
- A generated file, package, archive, attachment, or download link is not synchronization.
- A Work artifact is not a substitute for a ChatGPT Skill.
- Do not claim a Skill Creator invocation, UI state, installation, update, migration, persistence, or confirmation that the product did not actually provide.
- Do not require bulk installation. Sequential native confirmations are valid.
- Do not broaden the synchronization scope to unrelated repository assets or external Skill sources.

## Report

Keep the final report compact and factual.

Report the pinned `source + ref`, the active ChatGPT surface, and whether both canonical control Skills governed the run.

Then report one row per selected capability:

| Skill | Result | Remaining action |
| --- | --- | --- |
| `<name>` | `Installed / Updated / Renamed / Already Current / Pending User Action / Skipped / Conflict / Unsupported` | `<only the shortest action still required>` |

Add `Orphan Candidates` and `Limitations` only when observable and material.

For `Pending User Action`, state only the native confirmation still needed, such as **Install** or **Update**. Do not use `Loaded`, `Generated`, or `Packaged` as successful synchronization states, and do not include internal reasoning or file-by-file discovery logs.