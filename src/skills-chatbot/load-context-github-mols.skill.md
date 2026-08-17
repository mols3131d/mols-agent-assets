---
name: load-context-github-mols
description: >-
  Add mols-specific GitHub conventions alongside load-context-github when the current
  GitHub target is personally governed by the user. Activate for a personal
  `mols3131d` repository unless the task identifies it as team/company/shared, or when
  the user explicitly says the target is their own. Keep applying on follow-ups to
  that target. Do not activate from access, admin rights, authorship, or collaboration
  alone; in mixed-target tasks, apply only to the personal targets.
---

# Load Mols GitHub Context

This Skill is a **personal overlay**. Apply it only with `load-context-github`.

## Activation

Evaluate personal scope **per GitHub target**, not once for the whole conversation.
Activate when the base loader applies and either condition holds:

- the target is under `mols3131d` and there is no evidence that it is a team, company,
  organization, or shared-project repository;
- the user explicitly identifies the target as their own or personally governed.

Keep the overlay active for follow-up requests that continue the same personal target,
even when the user does not repeat its name.

Do not infer personal scope from collaborator access, organization membership, admin
permission, authorship, contribution history, or familiarity. If ownership/governance is
unclear, use only the base loader until evidence establishes personal scope.

When one task spans multiple repositories or GitHub objects, apply this overlay only to
the personal targets. Never export its defaults to external or shared targets.

## Personal Conventions

### Instruction Fallback

Unless the repository explicitly defines a different applicable instruction policy, use:

`CHATBOT.md` → if absent `AGENTS.md` → if absent `README.md`

Apply the fallback per relevant path/scope. Repository-local selectors and explicit
overrides still govern when present.

This is a mols convention, not a GitHub, Copilot, Agent Skills, or general repository standard.

### Change Defaults

Unless repository-local rules or an explicit user instruction say otherwise:

- do not commit normal change work directly to `main`;
- use a dedicated branch;
- open PRs as draft by default;
- self-review before presenting the change as complete;
- do not mark ready, merge, or otherwise finalize without explicit user intent.

## Boundary

This overlay owns only cross-repository personal conventions. Project-specific branch
names, commit formats, tests, inbox policy, release process, architecture, and other local
rules must be discovered from the live repository by `load-context-github`.