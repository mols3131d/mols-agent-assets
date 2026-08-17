---
name: load-context-github-mols
description: >-
  Load mols-specific GitHub conventions for task-level work on targets governed by the
  user's personal conventions. Treat a `mols3131d` repository as personal unless live
  or task evidence marks it team, company, organization, or shared; an explicit statement
  that the target is the user's own also qualifies. Continue on follow-ups to the same
  target and re-evaluate when the target changes. Do not infer personal scope from access,
  admin rights, authorship, or collaboration; in mixed-target tasks, apply only to
  personal targets.
---

# Load Mols GitHub Context

This Skill contributes **personal mols conventions** for the GitHub target. Resolve live
target context through `load-context-github`; this overlay does not replace the base loader.

## Scope Discipline

Keep personal conventions bound to targets that remain evidenced as personally governed.
If newly loaded context shows that a target is team, company, organization, or shared,
stop applying this overlay to that target. In mixed-target work, never carry personal
defaults from an in-scope target into another target.

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
