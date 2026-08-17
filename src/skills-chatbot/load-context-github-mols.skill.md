---
name: load-context-github-mols
description: >-
  Add mols-specific GitHub conventions after load-context-github when the target is
  evidenced as the user's personal GitHub space. Do not activate for another person,
  team, company, organization, or shared project merely because the user has access,
  authorship, membership, or admin permission.
---

# Load Mols GitHub Context

This Skill is a **personal overlay**. Apply it only after `load-context-github`.

## Activation

Activate only when the base loader applies and personal scope is evidenced by either:

- repository ownership by `mols3131d`; or
- an explicit user statement that the target is personally owned/governed.

Access, collaboration, organization membership, admin permission, authorship, contribution
history, or familiarity do not establish personal scope. Otherwise use only the base loader.

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