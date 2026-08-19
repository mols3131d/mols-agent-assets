---
name: mols-skill-install
description: >-
  Install, update, sync, migrate, or load a selected or otherwise unambiguous Skill into
  an active target, including the current runtime when it exposes an observable Skill
  management surface. Use when the requested end state is target delivery or Skill-state
  mutation and the candidate is resolved enough to act on safely. Do not use for broad
  Skill discovery, capability matching, or unresolved candidate selection.
---

# Mols Skill Install

## Arguments

```yaml
selection: <auto>
source: <auto>
target: <auto>
action: <auto>
on_conflict: <auto>
```

- `selection` — one or more resolved Skill records, preferably the handoff from `mols-skill-find`. `<auto>` uses an unambiguous candidate already established by the caller or context.
- `source` — direct Skill path, package, URL, repository, or other source when no selection record is supplied. `<auto>` uses the source already associated with the resolved candidate.
- `target` — installation destination or active Skill consumer. `<auto>` resolves from user intent, live context, and observable target capabilities; the current runtime is eligible when it exposes a suitable Skill management surface.
- `action` — `install`, `update`, `sync`, `migrate`, `load`, or `<auto>`. `<auto>` infers the requested end state from caller intent and target semantics; it does not silently substitute a materially different state.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` never authorizes a destructive resolution; it reports the conflict for user choice.

`<auto>` is an inference sentinel. Resolve it from explicit user input, the caller's selection, live target state, source evidence, and target capabilities. Do not turn `<auto>` into a fixed repository path, product, actor category, or platform assumption.

## Contract

This Skill owns **target delivery and Skill-state mutation** for already selected Skills.

Use `mols-skill-find` first when the source is broad, the candidate is ambiguous, target compatibility must be resolved, or an inventory/sync selection set is needed.

Resolve delivery by **requested end state and observable capability**, not by classifying the current actor as a chatbot, coding agent, or another runtime category. The runtime executing this Skill may itself be the target when it provides a suitable native or equivalent Skill-management surface.

Preserve the requested end state. If a target distinguishes a reusable or registered Skill from a temporary in-context load, do not report the temporary state as equivalent to the requested reusable state. If a target does not make that distinction, follow its native model instead of inventing one.

Do not:

- crawl unrelated Skill sources to find alternatives;
- install multiple representations of one capability when one selected candidate is sufficient;
- overwrite, rename, delete, or merge an existing Skill when identity is uncertain;
- export a file or package when the target can complete or stage the requested state through a more direct native surface;
- claim a target state that the target did not actually reach.

## Resolve the candidate

Prefer a `mols-skill-find` selection record with at least `selected`, `source`, compatibility, and identity evidence. If only `source` is given, inspect the smallest sufficient Skill material to establish identity, target compatibility, and package requirements.

A candidate must resolve to one concrete Skill package or target-native equivalent. If alternatives remain materially unresolved, return to `mols-skill-find` rather than choosing by filename, package size, vendor name, or directory shape.

## Resolve the target

Honor an explicit target first. For `target: <auto>`, infer the destination from the requested end state, established conversation/task context, and live observable capabilities.

Treat the **current runtime itself as a target candidate** when it exposes a Skill or equivalent management surface that can satisfy the requested state, such as install, create, import, register, update, sync, or persistent reusable storage. This is capability-based self-targeting, not a chatbot-specific rule.

Do not infer target capability merely because the runtime can read a Skill, execute its instructions, access its source, or temporarily place it in context. Those abilities may support `load`, inspection, or staging without supporting persistent installation.

When user wording such as “install here”, “sync these Skills here”, or an equivalent request clearly refers to the active environment, prefer the current runtime if it can satisfy that state. When the requested destination remains materially ambiguous, do not silently choose among unrelated targets.

Action intent and target resolution are separate:

- `install`, `update`, `sync`, and `migrate` require the corresponding reusable target-state capability or an honest staged/pending transition;
- `load` may be temporary when that is the requested end state;
- requests to inspect, read, use as context, or run a Skill do not by themselves authorize persistent target-state mutation.

## Choose the target path

Inspect the resolved target's actual Skill or equivalent capabilities before deciding how to deliver the candidate. Do not assume every target uses files, archives, install APIs, editors, persistent registries, or the same UI.

Use the highest available path that satisfies the requested end state:

1. **Direct target action** — install, update, sync, migrate, create, import, or load through an available target tool, API, connector, Skill manager, or equivalent native capability.
1. **Native interactive flow** — prepare or stage the candidate in the target's native creation/import/install/editor surface and surface the shortest unavoidable review or confirmation action. Pre-fill everything the target allows.
1. **Assisted manual flow** — when the target cannot perform or stage the operation itself, prepare the exact accepted payload and lead the user to the shortest supported import/upload/editor path. Minimize clicks, retyping, conversion, and context switching.
1. **Package handoff** — return a file, directory, archive, or pasted body only when the target genuinely requires that form or the user explicitly requests export/manual installation.

A temporary load may be used as an execution aid when useful, but it does not satisfy a caller that requested a different reusable or installed state. Report the remaining state transition instead of silently downgrading the request.

Do not stop at generic instructions such as “download this and upload it” when a more direct target-specific surface is available. Do not invent a target capability or UI that cannot be established from the active environment or reliable target evidence.

## Inspect target state

Before mutation, inspect the target's existing Skills or equivalent state when supported. Compare candidate and target state using:

- stable identity, provenance, or previous-name metadata;
- responsibility and intended outcome;
- activation intent and negative boundary;
- behavioral contract and invariants;
- runtime-required files, tools, and resources;
- source history when available;
- name and description as supporting signals.

If the target cannot inspect existing Skill state, state that limitation. For synchronization or migration-sensitive work, do not pretend reconciliation is complete. Proceed only when the requested operation can safely surface or reject collisions.

## Reconcile identity

### Same name, same identity

Update the existing Skill instead of creating a duplicate when the target supports an update-equivalent operation.

- Preserve target identity and target-managed settings when possible.
- Replace stale source-controlled content with the selected canonical version.
- Preserve user customization that is not stale source content; if it conflicts with the canonical contract, surface a conflict instead of silently deleting it.

If already current, make no mutation.

### Same name, different identity

Treat this as a **name collision**. Do not auto-overwrite.

- `on_conflict: override` — replace the existing Skill only when the user explicitly selected this policy.
- `on_conflict: separate` — create the candidate under a distinct user-approved identity or name when supported.
- `on_conflict: skip` — keep the existing Skill and do not apply the candidate.
- `on_conflict: <auto>` — stop this item and present the valid choices through the most convenient target-supported interaction available.

Explain only material identity differences: activation, responsibility, outcome, or core contract.

### Different name, same identity

When rename continuity is **confirmed**, migrate instead of duplicating when the target supports an equivalent operation.

Strong evidence includes explicit provenance or previous-name metadata, source history, or clear continuity of activation, responsibility, outcome, and core contract. Similar wording or domain alone is insufficient.

If continuity is only probable, treat it as a conflict.

### No existing match

Apply the candidate once target compatibility and package requirements are satisfied, using the best path for the requested end state.

## Sync behavior

For `action: sync`, require a complete `sync-prep` selection set from `mols-skill-find` or equivalent caller evidence.

- Reconcile each selected source capability against target state.
- Apply only the selected candidate for each capability.
- Preserve the sync end state defined by the caller and target; do not replace it with an easier but materially different state.
- Process any Skill actively controlling the current discovery/install run after other selected capabilities. Do not restart or reinterpret the current run against a just-updated control Skill; use the new version on the next invocation.
- Report target-only Skills as orphan candidates when that concept is observable; do not delete them automatically.
- Do not expand sync scope beyond the supplied source or selection set.

When a target requires separate user confirmations, stage as much as it safely allows and present the minimum remaining actions rather than degrading the entire sync into manual package export.

## Package handling

Prepare only the payload required by the chosen target path.

- For a single-file Skill, use `SKILL.md` without inventing supporting files.
- For a Skill with runtime-required supporting resources, preserve only the files and dependency relationships the capability actually needs.
- Exclude maintainer-only material when the source distinguishes it from runtime payload.
- If the target cannot support a required dependency, do not silently apply a degraded capability. Return it as unsupported or request another candidate from `mols-skill-find`.
- Create an archive only when the chosen target path requires one or the user explicitly requests it.

## Safety Boundary

Without sufficient identity evidence, do not:

- overwrite an existing Skill;
- rename or delete an existing Skill;
- merge two existing Skills;
- discard user customization;
- resolve a same-name collision automatically.

`<auto>` may automate safe decisions supported by evidence. It is never implicit permission for a destructive conflict choice or for replacing the requested end state with a materially different one.

## Output

Report actual target states and only the remaining user action, if any:

- `Installed / Applied`
- `Updated`
- `Renamed / Migrated`
- `Loaded` — include scope and persistence or activation boundary when meaningful
- `Already Current`
- `Pending User Action` — include the shortest target-native confirmation/import action
- `Skipped`
- `Conflicts`
- `Orphan Candidates` for sync when observable
- `Unsupported`
- `Limitations`

Do not report staged, generated, exported, approval-pending, or temporary content as a stronger target state than it actually reached. For conflicts or pending actions, include only the minimum information the user needs to continue.
