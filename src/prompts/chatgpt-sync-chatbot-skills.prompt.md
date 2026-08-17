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

Before discovery, verify that both prerequisite Skills are installed and available in the current ChatGPT environment:

- `mols-skill-find`
- `mols-skill-install`

If either Skill is unavailable, use ChatGPT's `skill-creator` Skill to create each missing prerequisite from the canonical flat source in `mols3131d/mols-agent-assets`:

- `src/skills-chatbot/mols-skill-find.skill.md`
- `src/skills-chatbot/mols-skill-install.skill.md`

Bootstrap is independent of the requested `source`; these prerequisite Skills always come from this repository. Treat the repository files as canonical and preserve their semantics instead of redesigning or improving them during bootstrap.

For each missing prerequisite:

1. Read the canonical source.
1. Ask `skill-creator` to create the corresponding ChatGPT Skill from that source.
1. Use the native Skill draft / Install flow offered by ChatGPT.
1. If installation requires user approval, present the native Install option and do not continue until the Skill is installed.
1. Verify that the installed Skill is available in the current ChatGPT environment.

A generated `SKILL.md`, ZIP, downloadable package, attachment, or pasted Skill body is **not** a successful bootstrap. Do not return one as a substitute for creating and installing the ChatGPT Skill.

Do not use `mols-skill-find` or `mols-skill-install` to bootstrap themselves.

If ChatGPT cannot create or install a missing prerequisite through its native Skill creation surface, report **Bootstrap Required**, identify the missing prerequisite Skill and the unavailable capability, and stop before discovery or other mutation. Do not fall back to returning a Skill package for manual upload unless the user explicitly asks for that workflow.

## Prerequisites

After bootstrap, use the following installed Skills as the canonical owners of discovery and installation behavior:

- `mols-skill-find`
- `mols-skill-install`

Do not reproduce their identity, sibling-selection, rename, collision, package, or mutation rules inside this Prompt.

## Goal

Synchronize the selected repository Skill source with the current ChatGPT installation state.

The result should converge each repository capability to the single target-specific Skill projection that best fits ChatGPT, then create, update, or migrate it as an actual ChatGPT Skill through ChatGPT's `skill-creator` and native Skill review/install surface when safe. Ambiguous or destructive conflicts remain explicit user decisions.

For this Prompt, current-chat loading is not a successful substitute for persistent ChatGPT Skill synchronization.

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

Let `mols-skill-install` own installed-state inspection, identity reconciliation, conflict handling, package/resource preservation, and mutation ordering.

For the current ChatGPT target, require `mols-skill-install` to use ChatGPT's `skill-creator` as the native creation/update path for every selected capability that needs mutation:

1. Read the selected canonical projection and the runtime resources required by that projection.
1. Ask `skill-creator` to create or modify the corresponding ChatGPT Skill while preserving the source capability's semantics, activation contract, boundaries, and required resources.
1. Use the native Skill draft and Install/Update flow returned by ChatGPT.
1. Pre-fill everything the native surface permits; leave only unavoidable user approval or conflict decisions.
1. Treat the item as pending until the native installation/update completes.
1. Verify the installed state when the current ChatGPT environment exposes it.

Do not redesign or improve repository Skill semantics during synchronization. `skill-creator` is a target projection/install mechanism here, not an invitation to rewrite the capability.

Process Skills that control the current sync run after the other selected capabilities. Updating a control Skill must not reinterpret the in-progress run against the newly installed version.

A successful ChatGPT mutation means the capability is created, installed, updated, or migrated in the current ChatGPT Skill surface. A current-chat load, ZIP, generated file, attachment, pasted Skill body, or download link does not count as installation.

If ChatGPT exposes `skill-creator` but requires native review or user confirmation, surface the shortest native Install/Update action and keep the item pending until the user completes it. Do not replace that flow with manual upload merely to avoid the confirmation step.

If `skill-creator` or the native Skill creation/install surface is unavailable in the current ChatGPT environment, report that target capability as unavailable. Do not silently downgrade persistent sync to current-chat loading.

Do not directly mutate Skills outside `mols-skill-install` after bootstrap.

## Sync Boundary

- Synchronize only the resolved `source` and `scope`.
- Do not install multiple sibling projections of one capability.
- Do not delete installed-only Skills merely because they are absent from the source.
- Do not turn `<auto>` into permission for destructive conflict resolution.
- Do not treat generated Skill artifacts or current-chat loading as equivalent to installed ChatGPT Skills.
- Do not claim inspection, installation, update, rename, or migration that the current ChatGPT environment could not actually perform.

## Report

If bootstrap ran, report only prerequisite Skills whose native ChatGPT installation completed. Then return the final states produced by `mols-skill-install`, omitting empty groups:

### Bootstrapped Prerequisites

### Installed

### Updated

### Renamed / Migrated

### Pending User Action

### Skipped

### Conflicts

### Orphan Candidates

### Unsupported

### Limitations

Do not report a Skill as installed while its native Install/Update action is still pending user confirmation.

Keep the report concise. Do not include internal reasoning, repeated Skill rules, or file-by-file discovery logs unless a conflict requires evidence for a user decision.
