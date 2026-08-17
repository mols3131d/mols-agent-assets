---
name: install-skills
description: >-
  Install, update, or migrate a selected Skill into the active agent/chatbot target while
  reconciling installed identity, target-specific siblings, renames, name collisions, and
  user customizations. Use after Skill discovery or when a specific Skill source is already
  known. Do not perform broad Skill discovery itself.
---

# Install Skills

## Arguments

```yaml
selection: <auto>
source: <auto>
target: <auto>
action: <auto>
on_conflict: <auto>
```

- `selection` — one or more resolved Skill candidates, preferably the handoff from `find-skills`. `<auto>` uses an unambiguous candidate already established by the caller/context.
- `source` — direct Skill path, package, URL, or repository source when no selection record is supplied. `<auto>` uses the resolved source already associated with the task.
- `target` — installation destination or active harness. `<auto>` uses the current agent/chatbot target and its actual Skill capabilities.
- `action` — `install`, `update`, `sync`, or `migrate`. `<auto>` infers the required mutation from reconciliation rather than forcing a requested verb onto incompatible state.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` never authorizes a destructive resolution; it reports the conflict for user choice.

`<auto>` is an inference sentinel. Resolve it from explicit user input, the caller's selection, live installed state, repository evidence, and target capabilities. Do not turn `<auto>` into a fixed repository path or platform assumption.

## Contract

This Skill owns **installation-state mutation** for already selected Skills.

Use `find-skills` first when the source is broad, the candidate is ambiguous, target-specific siblings must be selected, or a repository inventory is needed.

Do not:

- crawl unrelated Skill sources to find alternatives;
- install multiple sibling projections of one capability;
- overwrite, rename, delete, or merge an installed Skill when identity is uncertain;
- claim an install/update/migration occurred unless the target mutation actually succeeded.

## Resolve the candidate

Prefer a `find-skills` selection record. If only `source` is given, inspect the smallest sufficient Skill material to establish its identity and package requirements.

A candidate must identify a concrete installable projection. If multiple sibling variants remain unresolved, return to `find-skills` rather than choosing by filename, package size, or directory name.

## Inspect installed state

Before mutation, inspect the target's installed Skills when the harness supports it. Compare candidate and installed state using:

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
- `on_conflict: <auto>` — stop this item and present the three choices.

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

Install the selected candidate once target compatibility and package requirements are satisfied.

## Sync behavior

For `action: sync`, require a complete capability selection set from `find-skills` or equivalent caller evidence.

- Reconcile each selected repository capability against installed state.
- Install/update/migrate only the preferred projection for each capability.
- Report installed Skills with no corresponding source capability as orphan candidates; do not delete them automatically.
- Do not expand sync scope beyond the supplied source/selection.

## Package handling

Install the package shape selected for the target.

- For self-contained flat Skills, install the single Skill content without inventing bundled dependencies.
- For bundled/runtime Skills, preserve runtime-required references, scripts, assets, and dependency relationships.
- Exclude maintainer-only material when the source distinguishes it from runtime payload.
- If the target cannot support a required dependency, do not silently install a degraded capability. Return the candidate as unsupported or request a different projection from `find-skills`.

## Safety Boundary

Without sufficient identity evidence, do not:

- overwrite an installed Skill;
- rename or delete an installed Skill;
- merge two installed Skills;
- discard user customization;
- resolve a same-name collision automatically.

`<auto>` may automate safe install/update/migration decisions supported by evidence. It is never implicit permission for a destructive conflict choice.

## Output

Return only states that reflect actual target results:

- `Installed`
- `Updated`
- `Renamed / Migrated`
- `Skipped`
- `Conflicts`
- `Orphan Candidates` for sync
- `Unsupported`
- `Limitations` when target capabilities prevented inspection or mutation

For conflicts, include the minimum information needed for the user to choose `override`, `separate`, or `skip`.
