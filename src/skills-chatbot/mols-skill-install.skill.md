---
name: mols-skill-install
description: >-
  Install, update, migrate, sync, or explicitly load a selected Skill into the active
  agent/chatbot target using the most direct supported target surface. Preserve persistent
  installation intent for install/update/sync/migrate; use non-persistent loading only when
  explicitly requested or as a temporary execution aid, never as a silent substitute for
  installation. Use after Skill discovery or when a specific Skill source is already known.
  Do not perform broad Skill discovery itself.
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

- `selection` — one or more resolved Skill candidates, preferably the handoff from `mols-skill-find`. `<auto>` uses an unambiguous candidate already established by the caller/context.
- `source` — direct Skill path, package, URL, or repository source when no selection record is supplied. `<auto>` uses the resolved source already associated with the task.
- `target` — installation destination or active harness. `<auto>` uses the current agent/chatbot target and its actual Skill capabilities.
- `action` — `install`, `update`, `sync`, `migrate`, `load`, or `<auto>`. `install`, `update`, `sync`, and `migrate` require a persistent target result; `load` explicitly requests a non-persistent usable state. `<auto>` preserves the caller's intent instead of downgrading persistence silently.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` never authorizes a destructive resolution; it reports the conflict for user choice.

`<auto>` is an inference sentinel. Resolve it from explicit user input, the caller's selection, live installed state, repository evidence, and target capabilities. Do not turn `<auto>` into a fixed repository path or platform assumption.

## Contract

This Skill owns **target delivery and installation-state mutation** for already selected Skills.

Use `mols-skill-find` first when the source is broad, the candidate is ambiguous, target-specific siblings must be selected, or a repository inventory is needed.

Preserve the requested end state:

- `install`, `update`, `sync`, `migrate` → persistent Skill state;
- `load` → non-persistent usable state.

A temporary load may help complete the current workflow while a persistent operation is unavailable or awaiting approval, but it does **not** satisfy a persistent action.

Do not:

- crawl unrelated Skill sources to find alternatives;
- install multiple sibling projections of one capability;
- overwrite, rename, delete, or merge an installed Skill when identity is uncertain;
- export a file or package when the target can directly install, create, import, update, or stage the Skill through a native surface;
- report a persistent action as complete when the Skill is only loaded in chat/project/workspace context;
- claim any install/update/migration/load occurred unless the target state actually reflects it.

## Resolve the candidate

Prefer a `mols-skill-find` selection record. If only `source` is given, inspect the smallest sufficient Skill material to establish its identity and package requirements.

A candidate must identify a concrete target-compatible projection. If multiple sibling variants remain unresolved, return to `mols-skill-find` rather than choosing by filename, package size, or directory name.

## Choose the target path

Inspect the active target's actual Skill or equivalent capability before deciding how to deliver the candidate. Do not assume every chatbot uses files, ZIP packages, an install API, or the same UI.

### Persistent actions

For `install`, `update`, `sync`, or `migrate`, use the highest available path that can produce persistent target state:

1. **Direct persistent mutation** — install, update, migrate, create, or import through an available target tool, API, connector, Skill manager, or equivalent native capability.
1. **Native interactive install flow** — prepare the Skill in the target's native creation/import/install surface and surface the shortest required review or confirmation action. Pre-fill everything the target allows.
1. **Assisted persistent import** — when the target cannot perform or stage the operation itself but supports persistent manual import/upload/editor installation, prepare the exact accepted payload and lead the user to the shortest native interface.
1. **Package handoff** — return a file, directory, archive, or pasted body only when the target genuinely requires that payload for persistent installation or the user explicitly requests export/manual installation.

If none of these paths can persist the Skill, do not silently convert the requested action to `load`. You may load the capability temporarily when it helps the current workflow, but report the persistent operation as `Pending User Action`, `Unsupported`, or `Limitations` as appropriate.

### Load action

For explicit `action: load`, use the most direct supported scoped loading mechanism. Report the scope and whether it survives the current chat, project, workspace, or session.

Do not stop at generic instructions such as “download this and upload it” when a more direct target-specific surface is available. Do not invent a target UI or capability that cannot be established from the active environment or reliable target evidence.

## Inspect installed state

Before persistent mutation, inspect the target's installed Skills when the harness supports it. Compare candidate and installed state using:

- stable identity, provenance, or previous-name metadata;
- responsibility and intended outcome;
- activation intent and negative boundary;
- behavioral contract and invariants;
- package/runtime relationships;
- repository history when available;
- name and description as supporting signals.

If the target cannot inspect installed Skills, state that limitation. For `sync` or migration-sensitive work, do not pretend reconciliation is complete. A direct install may proceed only when the user's intent is explicit and the target can safely reject or surface collisions.

## Reconcile identity

### Same name, same identity

Update the existing Skill instead of creating a duplicate.

- Preserve installation identity and target-managed settings when possible.
- Replace stale repository content with the selected canonical version.
- Preserve user customization that is not stale repository content; if it conflicts with the canonical contract, surface a conflict rather than silently deleting it.

If already current, make no mutation.

### Same name, different identity

Treat this as a **name collision**. Do not auto-overwrite.

- `on_conflict: override` — replace the installed Skill only when the user explicitly selected this policy.
- `on_conflict: separate` — install the candidate under a distinct user-approved name.
- `on_conflict: skip` — keep the existing Skill and do not install the candidate.
- `on_conflict: <auto>` — stop this item and present the three choices through the most convenient target-supported interaction available.

Explain only the material identity differences: activation, responsibility, outcome, or core contract.

### Different name, same identity

When rename continuity is **confirmed**, migrate instead of duplicating:

```text
old-name → new-canonical-name
```

Update content/resources and keep only one active Skill when the target supports rename/migration.

Strong rename evidence includes explicit metadata/provenance, repository history, or clear continuity of activation, responsibility, outcome, and core contract. Similar wording or domain alone is insufficient.

If rename is only probable, treat it as a conflict. Do not leave old/new duplicates merely because migration is uncertain.

### No installed match

For a persistent action, install or stage the selected candidate through the best persistent target path once compatibility and package requirements are satisfied. For `load`, load it into the requested supported scope.

## Sync behavior

For `action: sync`, require a complete capability selection set from `mols-skill-find` or equivalent caller evidence.

- Reconcile each selected repository capability against installed state.
- Converge each selected capability toward a **persistent installed target state**.
- Install/update/migrate only the preferred projection for each capability.
- A transient load may keep the current run usable, but it does not mark that capability synchronized.
- Process any Skill actively controlling the current discovery/install run after other selected capabilities. Do not restart or reinterpret the current run against a just-updated control Skill; use the new version on the next invocation.
- Report installed Skills with no corresponding source capability as orphan candidates; do not delete them automatically.
- Do not expand sync scope beyond the supplied source/selection.

When a target requires separate user confirmations, stage as much of the persistent sync as the native surface safely allows and present the minimum remaining actions. Do not degrade the sync into a load-only result merely because confirmation is required.

## Package handling

Prepare the package shape required by the chosen target path.

- For self-contained flat Skills, use the single Skill content without inventing bundled dependencies.
- For bundled/runtime Skills, preserve runtime-required references, scripts, assets, and dependency relationships.
- Exclude maintainer-only material when the source distinguishes it from runtime payload.
- If the target cannot support a required dependency, do not silently install a degraded capability. Return the candidate as unsupported or request a different projection from `mols-skill-find`.
- Create an archive only when the persistent target path specifically requires one or the user explicitly asks for it.

## Safety Boundary

Without sufficient identity evidence, do not:

- overwrite an installed Skill;
- rename or delete an installed Skill;
- merge two installed Skills;
- discard user customization;
- resolve a same-name collision automatically.

`<auto>` may automate safe install/update/migration/load decisions supported by evidence. It is never implicit permission for a destructive conflict choice or for downgrading a persistent action to a transient load.

## Output

Report the actual target state and only the remaining user action, if any:

- `Installed`
- `Updated`
- `Renamed / Migrated`
- `Loaded` — include scope and persistence; for persistent actions this is informational only and never completion
- `Pending User Action` — include the shortest native confirmation/import action required to reach the requested persistent state
- `Skipped`
- `Conflicts`
- `Orphan Candidates` for sync
- `Unsupported`
- `Limitations` when target capabilities prevented inspection or mutation

Do not report staged, generated, exported, approval-pending, or transiently loaded content as installed or synchronized. For conflicts or pending actions, include only the minimum information the user needs to continue.