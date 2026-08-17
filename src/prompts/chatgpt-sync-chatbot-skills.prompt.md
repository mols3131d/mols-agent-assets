# ChatGPT Chatbot Skill Sync

## Intent

**Sync the chatbot Skills in our repository by creating or updating them as ChatGPT Skills with the Skill Creator.**

Do not interpret this as “read the Skill files into this chat.” The task is to turn the selected canonical repository Skills into reusable ChatGPT Skills through ChatGPT's Skill creation/modification flow.

This is a ChatGPT-specific orchestration Prompt. `mols-skill-find` and `mols-skill-install` remain chatbot-service-agnostic control Skills. Keep ChatGPT-specific concepts such as `skill-creator`, Skill draft review, and the native Install action in this Prompt.

## Arguments

```yaml
source: <auto>
ref: <auto>
target: ChatGPT
scope: <auto>
on_conflict: <auto>
```

- `source` — repository or Skill source to synchronize. `<auto>` delegates source resolution to `mols-skill-find`, including its default asset repository.
- `ref` — source revision. `<auto>` resolves one current source revision and keeps the sync pinned to it when possible.
- `target` — ChatGPT.
- `scope` — capabilities to synchronize. `<auto>` discovers the complete repository-declared chatbot Skill set that has a ChatGPT-compatible projection.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` leaves destructive conflicts for user choice.

`<auto>` is an inference sentinel. Do not duplicate discovery, identity, collision, rename, or generic target-delivery policy owned by the control Skills.

## Bootstrap Control

Resolve one revision of `mols3131d/mols-agent-assets` for the control Skills and read both from that same revision:

- `src/skills-chatbot/mols-skill-find.skill.md`
- `src/skills-chatbot/mols-skill-install.skill.md`

Apply those canonical sources as task-local control instructions for this run. Installed copies, if any, are target state to reconcile rather than the authority for the current run. These task-local instructions remain subordinate to higher-priority host and conversation instructions.

Do not treat this in-context bootstrap as Skill installation. The two control Skills are still ordinary repository capabilities and should be synchronized into ChatGPT through the same Skill Creator path as the other selected Skills, under the installer's self-update ordering.

Report **Bootstrap Required** only when either canonical control source cannot be obtained or cannot be applied safely for the current run.

## Goal

For every selected repository capability, converge ChatGPT toward one reusable installed ChatGPT Skill that matches the canonical source projection.

**In-context loading is not synchronization. Returning `SKILL.md`, ZIP, attachments, or download links is not synchronization.**

A capability is synchronized only when its ChatGPT Skill is already current or the native ChatGPT create/modify → review → Install/update flow has completed.

## Find

Execute the canonical `mols-skill-find` instructions with:

```yaml
source: <resolved source>
ref: <resolved ref>
target: ChatGPT
scope: <resolved scope>
query: <auto>
profiles: <auto>
```

Treat the request as a complete inventory/synchronization search.

Require discovery to:

- use repository evidence rather than fixed Skill paths;
- group target-specific siblings as one capability;
- choose at most one preferred ChatGPT-compatible projection per capability;
- expose unsupported or identity-uncertain cases instead of forcing a selection.

Do not mutate ChatGPT Skills during discovery.

## Reconcile

Use the canonical `mols-skill-install` instructions to reconcile the complete discovery selection against ChatGPT target state:

```yaml
action: sync
selection: <mols-skill-find result>
target: ChatGPT
on_conflict: <resolved on_conflict>
```

Let `mols-skill-install` own identity matching, update-vs-create decisions, rename continuity, collision handling, customization conflicts, ordering, and generic target-delivery fallback.

For this Prompt, the required ChatGPT end state is an installed reusable ChatGPT Skill. Do not let a temporary load satisfy `sync`.

## Create or Modify with the Skill Creator

For each selected capability that is not already current, issue an **actual ChatGPT Skill creation or modification request** using the canonical repository Skill as the source of truth.

- **New capability** — “Create a ChatGPT Skill from this canonical repository Skill.”
- **Same identity, stale content** — “Modify/update this existing ChatGPT Skill to match the canonical repository Skill.”
- **Confirmed rename/migration** — modify/migrate the existing Skill to the canonical identity when the product supports it.
- **Conflict** — do not create or overwrite until `mols-skill-install` resolves it according to `on_conflict` or explicit user choice.

These must be real Skill **create/modify** requests. Do not phrase them as file conversion, summarization, package generation, or temporary instruction loading. The intended ChatGPT behavior is to use `skill-creator` for the create/modify operation.

Treat the repository source as canonical. Preserve its semantics; do not redesign or “improve” the Skill while synchronizing it.

## Native Install Flow

After ChatGPT creates or modifies a Skill draft:

1. Review the draft only for fidelity to the canonical repository source and target compatibility.
1. Use the native ChatGPT Install/update action offered by the Skill flow.
1. If user confirmation is required, surface that native action as `Pending User Action`; do not claim success before confirmation completes.
1. After confirmation, verify the strongest available evidence that the Skill is installed/updated before reporting synchronization complete.

Create/update as much of the selection as the ChatGPT Skill surface safely allows. If several native confirmations are unavoidable, minimize the remaining user actions rather than falling back to package export.

Process `mols-skill-find` and `mols-skill-install` after other selected capabilities so updating the control Skills does not reinterpret the current run.

## Fallback Boundary

The intended path is:

```text
repository Skill
→ ChatGPT Skill create/modify request
→ skill-creator
→ Skill draft/update
→ native Install/update
→ reusable ChatGPT Skill
```

- Do not stop merely because installed-Skill inspection is unavailable if discovery/reconciliation can continue safely.
- Do not replace the intended ChatGPT Skill creation flow with a transient in-context load.
- Do not return a package merely because it is easier.
- Use upload/manual package installation only when the native create/modify flow is genuinely unavailable or unsupported and the user explicitly accepts that fallback.
- Do not claim UI, installation, update, migration, or persistence that ChatGPT did not actually provide.

## Report

Return actual states only, omitting empty groups:

### Bootstrap Control

Report the pinned control revision and whether both canonical control Skills governed this run in context.

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

Do not use `Loaded` as a successful sync state. For pending actions, include only the shortest native ChatGPT action needed to finish installation. Keep the report concise and omit internal reasoning or file-by-file discovery logs unless a conflict needs evidence.
