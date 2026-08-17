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

`<auto>` is an inference sentinel. Do not duplicate source-discovery or installation policy that belongs to the prerequisite Skills.

## Bootstrap

Before discovery, make both prerequisite capabilities available for this run:

- `mols-skill-find`
- `mols-skill-install`

Prefer an already installed Skill when the current ChatGPT environment can establish that it is available. Do not require installed-state inspection as a prerequisite for continuing.

For each prerequisite that is not already established as available:

1. Read its canonical flat source from `mols3131d/mols-agent-assets`:
   - `src/skills-chatbot/mols-skill-find.skill.md`
   - `src/skills-chatbot/mols-skill-install.skill.md`
1. Try the most direct persistent ChatGPT Skill path available. When the product exposes native Skill creation, update, review, or installation, use that surface and preserve the canonical source semantics.
1. If native installation requires user approval, surface the native approval/Install action. Record it as pending until the user completes it; do not claim installation early.
1. Whether or not persistent installation is available, load the canonical flat Skill into the current conversation as a **transient bootstrap capability** when the model can read and follow it safely. Transient loading is sufficient to continue this sync run, but it is not installation.
1. Continue once both prerequisite capabilities are either installed or transiently loaded.

Bootstrap is independent of the requested `source`; these two prerequisite capabilities always come from the canonical repository paths above.

Do not return a generated `SKILL.md`, ZIP, downloadable package, attachment, or pasted Skill body merely because native installation is unavailable. Use transient loading first. Manual import or package handoff is a fallback only when the target requires it or the user explicitly requests it.

Do not recursively require an installed prerequisite to bootstrap itself. A transiently loaded canonical prerequisite may act as the implementation for the current run.

Report **Bootstrap Required** and stop only when a prerequisite cannot be made usable by any supported path: it cannot be read from the canonical source, cannot be safely loaded into the current execution context, and cannot be created or installed through a native target surface.

## Prerequisites

After bootstrap, use the installed or transiently loaded prerequisite capabilities as the canonical owners of discovery and installation behavior:

- `mols-skill-find`
- `mols-skill-install`

Do not reproduce their identity, sibling-selection, rename, collision, package, or mutation rules inside this Prompt.

## Goal

Synchronize the selected repository Skill source with the current ChatGPT installation state.

The result should converge each repository capability to the single target-specific Skill projection that best fits ChatGPT, then install, update, migrate, load, or stage it through the best supported target path. Persistent installation is preferred when available. Ambiguous or destructive conflicts remain explicit user decisions.

## Find

Execute `mols-skill-find` using the installed Skill or its transiently loaded canonical source with the resolved `source`, `ref`, `target`, and `scope`.

For default sync intent:

```yaml
query: <auto>
profiles: <auto>
```

Treat the request as an inventory/synchronization search so `mols-skill-find` returns the complete in-scope capability selection set rather than only one match.

Require discovery to:

- use repository evidence instead of fixed Skill paths;
- group target-specific sibling variants as one capability;
- select at most one preferred ChatGPT-compatible projection per capability;
- expose unsupported or identity-uncertain cases instead of forcing a selection.

Do not install anything during this phase.

## Install

Pass the complete discovery selection set to `mols-skill-install`, using the installed Skill or its transiently loaded canonical source:

```yaml
action: sync
selection: <mols-skill-find result>
target: <resolved target>
on_conflict: <resolved on_conflict>
```

Let `mols-skill-install` own target-path selection, installed-state reconciliation, and mutation decisions, including:

- direct installation or update when supported;
- native create/import/review/Install flows;
- transient or scoped loading when persistent installation is unavailable;
- confirmed rename migration;
- same-name identity collision;
- user customization conflicts;
- orphan reporting;
- unsupported target/package behavior;
- assisted manual import or package handoff only when better target-native paths are unavailable.

For a ChatGPT target, prefer an actual installed or updated ChatGPT Skill when the product exposes that capability. A ZIP, generated file, attachment, or download link does not count as installation.

When the ChatGPT product requires native review or user confirmation, surface that flow and report the item as pending until installation completes. Do not block the entire synchronization run merely because a prerequisite or other capability is currently only transiently loaded, unless persistent installation is itself required by the user's intent.

Process any Skill controlling the current discovery/install run after other selected capabilities. Do not restart or reinterpret the current run against a just-updated control Skill; use the new version on the next invocation.

## Sync Boundary

- Synchronize only the resolved `source` and `scope`.
- Do not install multiple sibling projections of one capability.
- Do not delete installed-only Skills merely because they are absent from the source.
- Do not turn `<auto>` into permission for destructive conflict resolution.
- Do not treat transiently loaded, generated, staged, or approval-pending content as installed.
- Do not claim inspection, installation, update, rename, migration, or persistence that the current ChatGPT environment could not actually perform.
- Do not stop solely because installed-Skill inspection or native installation UI is unavailable when the required capability can still be transiently loaded and executed safely.

## Report

Return the actual states produced by bootstrap and `mols-skill-install`, omitting empty groups:

### Bootstrapped / Loaded Prerequisites

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

For transient loads, include the scope and persistence boundary. Do not report a Skill as installed while its native Install action is still pending user confirmation.

Keep the report concise. Do not include internal reasoning, repeated Skill rules, or file-by-file discovery logs unless a conflict requires evidence for a user decision.
