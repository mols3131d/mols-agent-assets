# ChatGPT Chatbot Skill Sync

## Arguments

```yaml
source: <auto>
ref: <auto>
target: <auto>
scope: <auto>
on_conflict: <auto>
```

- `source` — repository or Skill source to synchronize. `<auto>` delegates source resolution to `mols-skill-find`, including its default asset repository.
- `ref` — source revision. `<auto>` uses the live/current ref for the resolved source when explicitly established, otherwise the source default.
- `target` — ChatGPT Skill installation target. `<auto>` uses the current ChatGPT environment.
- `scope` — capabilities to synchronize. `<auto>` discovers repository-declared chatbot/ChatGPT Skill profiles and synchronizes their complete installable capability set.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` leaves destructive conflicts for user choice.

`<auto>` is an inference sentinel. Do not duplicate discovery or installation policy owned by the prerequisite Skills.

## Bootstrap

Before discovery, resolve one prerequisite revision for `mols3131d/mols-agent-assets`. Use an explicitly requested prerequisite revision when supplied; otherwise resolve the repository default branch head and pin its commit when the source allows it.

Read both canonical flat control Skills from that same revision:

- `src/skills-chatbot/mols-skill-find.skill.md`
- `src/skills-chatbot/mols-skill-install.skill.md`

These bootstrap sources are independent of the requested sync `source`.

For this run, apply both canonical sources as task-local in-context instructions and treat them as the execution authority for `mols-skill-find` and `mols-skill-install`, even when installed copies already exist. They remain subordinate to higher-priority host and conversation instructions. Installed copies are target state to reconcile, not execution authority. In-context use is sufficient to run the controller logic, but it is **not** Skill installation.

If the target can establish that either prerequisite is missing, invoke the canonical `mols-skill-install` instructions with persistent `action: install` before discovery. If native review or user confirmation is required, surface the shortest available install action. The current run may continue using the canonical in-context controller while persistence is pending, but do not treat the prerequisite as installed until the target confirms persistent installation.

Do not bootstrap-update an existing prerequisite before the main sync. Let the normal sync reconcile existing `mols-skill-find` and `mols-skill-install` copies under the installer's self-update rules. The current run always remains governed by the canonical in-context sources it started with.

Report **Bootstrap Required** and stop only when either canonical prerequisite source cannot be obtained or cannot be applied safely as instructions for the current run.

## Goal

Synchronize the selected repository Skill source into **persistent ChatGPT Skills**.

For this Prompt, `sync` means converging every selected capability toward a persistent installed, updated, or migrated ChatGPT Skill. In-context loading may support the current execution, but it never satisfies synchronization.

Leave ambiguous or destructive conflicts for explicit user choice.

## Find

Execute the canonical `mols-skill-find` instructions with the resolved `source`, `ref`, `target`, and `scope`.

For default sync intent:

```yaml
query: <auto>
profiles: <auto>
```

Treat the request as an inventory/synchronization search so discovery returns the complete in-scope capability selection set rather than only one match.

Require discovery to:

- use repository evidence instead of fixed Skill paths;
- group target-specific sibling variants as one capability;
- select at most one preferred ChatGPT-compatible projection per capability;
- expose unsupported or identity-uncertain cases instead of forcing a selection.

Do not mutate target Skills during discovery.

## Install

Pass the complete discovery selection set to the canonical `mols-skill-install` instructions:

```yaml
action: sync
selection: <mols-skill-find result>
target: <resolved target>
on_conflict: <resolved on_conflict>
```

`action: sync` is a **persistent intent**. Do not downgrade it to `load` merely because loading is easier or native installation needs user confirmation.

Let `mols-skill-install` own persistent target-path selection, installed-state reconciliation, self-update ordering, conflicts, migrations, unsupported packages, native install UI, assisted import, and package fallback.

For ChatGPT:

- use direct persistent install/update when available;
- otherwise prepare and surface the native Skill creation/import/review/Install flow;
- if persistent installation requires user confirmation, report `Pending User Action` and present the shortest native action;
- use transient in-context loading only as an execution aid, never as the final sync result;
- use manual import/package handoff only when the persistent target path genuinely requires it or the user explicitly asks for manual installation.

A capability is synchronized only after its persistent target state is confirmed as installed, updated, migrated, or already current.

## Sync Boundary

- Synchronize only the resolved `source` and `scope`.
- Do not install multiple sibling projections of one capability.
- Do not delete installed-only Skills merely because they are absent from the source.
- Do not turn `<auto>` into permission for destructive conflict resolution.
- Do not treat in-context loading, generated files, staged drafts, or approval-pending content as installed or synchronized.
- Do not stop the controller merely because installed-Skill inspection is unavailable when the canonical prerequisite instructions can still run in context.
- Do not silently replace persistent sync with non-persistent load.
- Do not claim inspection, installation, update, migration, or persistence that the current target did not actually perform.

## Report

Return actual states only, omitting empty groups:

### Bootstrap Control

Report the pinned prerequisite revision, whether both canonical control Skills were applied in context, and whether missing prerequisite persistence completed or remains pending.

### Installed

### Updated

### Renamed / Migrated

### Already Current

### Pending User Action

### Skipped

### Conflicts

### Orphan Candidates

### Unsupported

### Limitations

Do not use `Loaded` as a successful sync state. If a transient load was used only to keep the current run operational, mention it under `Bootstrap Control` or `Limitations` with its scope and non-persistent nature.

For pending actions, include only the shortest native action the user must take to complete persistent installation. Keep the report concise and omit internal reasoning or file-by-file discovery logs unless a conflict needs evidence.