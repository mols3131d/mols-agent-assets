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

Before discovery, read the current canonical flat sources for both control Skills from `mols3131d/mols-agent-assets`:

- `src/skills-chatbot/mols-skill-find.skill.md`
- `src/skills-chatbot/mols-skill-install.skill.md`

Use the repository default branch unless the user explicitly requests another prerequisite revision. These bootstrap sources are independent of the requested sync `source`.

For this run, the canonical source content is the authority for `mols-skill-find` and `mols-skill-install`, even when installed copies already exist. Treat installed copies as target state to reconcile, not as authority for the current run. This prevents stale installed control Skills from governing a sync of newer repository content.

Apply both canonical Skills as in-context instructions for the current run. This is sufficient to execute the workflow but is not persistent installation.

When the current ChatGPT product exposes native Skill creation, update, review, or installation, also use that surface to bring missing or stale prerequisite Skills toward the canonical versions. If user approval is required, surface the native action and report it as pending; continue the current run using the canonical in-context instructions.

Do not switch the current run to a newly installed or updated control Skill. Reconcile `mols-skill-find` and `mols-skill-install` after the other selected capabilities and use their new persistent versions on the next invocation.

Do not return a generated `SKILL.md`, ZIP, attachment, download, or pasted Skill body merely because native installation is unavailable. Manual import or package handoff is a fallback only when the target requires it or the user explicitly requests it.

Report **Bootstrap Required** and stop only when either canonical prerequisite source cannot be obtained or cannot be applied safely as instructions for the current run.

## Goal

Synchronize the selected repository Skill source with the current ChatGPT target.

Converge each repository capability to one target-appropriate Skill projection, then install, update, migrate, load, or stage it through the best supported target path. Prefer persistent native installation when available. Leave ambiguous or destructive conflicts for explicit user choice.

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

Let `mols-skill-install` own target-path selection, installed-state reconciliation, and mutation decisions, including direct mutation, native interactive flows, scoped loading, conflicts, migrations, unsupported packages, and last-resort manual handoff.

For ChatGPT, prefer an actual installed or updated Skill when the product exposes that capability. If native review or confirmation is required, surface the shortest available action and report it as pending until completed. Do not treat generated, staged, approval-pending, or in-context content as installed.

Process `mols-skill-find` and `mols-skill-install` after the other selected capabilities. Do not restart or reinterpret the current run after updating them.

## Sync Boundary

- Synchronize only the resolved `source` and `scope`.
- Do not install multiple sibling projections of one capability.
- Do not delete installed-only Skills merely because they are absent from the source.
- Do not turn `<auto>` into permission for destructive conflict resolution.
- Do not stop solely because installed-Skill inspection or native installation UI is unavailable when the capability can still be used safely in context.
- Do not claim inspection, installation, update, migration, loading, or persistence that the current target did not actually perform.

## Report

Return actual states only, omitting empty groups:

### Bootstrap Control

Report whether the canonical prerequisite Skills were applied in context and whether persistent prerequisite installation/update completed or remains pending.

### Installed

### Updated

### Renamed / Migrated

### Loaded

### Pending User Action

### Skipped

### Conflicts

### Orphan Candidates

### Unsupported

### Limitations

For loads, state scope and persistence. For pending actions, include only the shortest native action the user must take. Keep the report concise and omit internal reasoning or file-by-file discovery logs unless a conflict needs evidence.
