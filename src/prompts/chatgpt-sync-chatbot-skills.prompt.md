# ChatGPT Chatbot Skill Sync

## Arguments

```yaml
source: <auto>
ref: <auto>
target: <auto>
scope: <auto>
on_conflict: <auto>
```

- `source` — repository or Skill source to synchronize. `<auto>` delegates source resolution to `mols-skill-find`, including its repository fallback.
- `ref` — source revision. `<auto>` uses the live/current ref when known, otherwise the source default.
- `target` — ChatGPT Skill installation target. `<auto>` uses the current ChatGPT environment.
- `scope` — capabilities to synchronize. `<auto>` discovers repository-declared chatbot/ChatGPT Skill profiles and synchronizes their complete installable capability set.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` leaves destructive conflicts for user choice.

`<auto>` is an inference sentinel. Do not duplicate source-discovery or installation policy that belongs to the prerequisite Skills.

## Prerequisites

This Prompt assumes the following Skills are available and uses them as the canonical owners of discovery and installation behavior:

- `mols-skill-find`
- `mols-skill-install`

Do not reproduce their identity, sibling-selection, rename, collision, package, or mutation rules inside this Prompt.

If either Skill is unavailable, report **Bootstrap Required**, identify the missing Skill, and stop before discovery or mutation. The prerequisite must be installed through the current ChatGPT Skill installation surface before rerunning this Prompt.

## Goal

Synchronize the selected repository Skill source with the current ChatGPT installation state.

The result should converge each repository capability to the single target-specific Skill projection that best fits ChatGPT, then install, update, or migrate it when safe. Ambiguous or destructive conflicts remain explicit user decisions.

## Find

Invoke `mols-skill-find` with the resolved `source`, `ref`, `target`, and `scope`.

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

Pass the complete discovery selection set to `mols-skill-install`:

```yaml
action: sync
selection: <mols-skill-find result>
target: <resolved target>
on_conflict: <resolved on_conflict>
```

Let `mols-skill-install` own installed-state inspection and all mutation decisions, including:

- new installation;
- update of the same Skill;
- confirmed rename migration;
- same-name identity collision;
- user customization conflicts;
- orphan reporting;
- unsupported target/package behavior.

Do not directly mutate Skills outside `mols-skill-install`.

## Sync Boundary

- Synchronize only the resolved `source` and `scope`.
- Do not install multiple sibling projections of one capability.
- Do not delete installed-only Skills merely because they are absent from the source.
- Do not turn `<auto>` into permission for destructive conflict resolution.
- Do not claim inspection, installation, update, rename, or migration that the current ChatGPT environment could not actually perform.

## Report

Return the final states produced by `mols-skill-install`, omitting empty groups:

### Installed

### Updated

### Renamed / Migrated

### Skipped

### Conflicts

### Orphan Candidates

### Unsupported

### Limitations

Keep the report concise. Do not include internal reasoning, repeated Skill rules, or file-by-file discovery logs unless a conflict requires evidence for a user decision.
