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

This Skill contributes **personal mols conventions** for the GitHub target. Resolve live target context through `load-context-github`; this overlay does not replace the base loader.

## Scope Discipline

Keep personal conventions bound to targets that remain evidenced as personally governed. If newly loaded context shows that a target is team, company, organization, or shared, stop applying this overlay to that target. In mixed-target work, never carry personal defaults from an in-scope target into another target.

## Personal Conventions

### `CHATBOT.md` Compatibility Entry

For an in-scope personal repository, use repository-root `CHATBOT.md` as a compatibility entry when the active runtime is missing any repository context or Agent Asset loading behavior that the file declares. Treat each compatibility responsibility independently: skip behavior the runtime already provides and recover only the missing behavior.

When present, treat `CHATBOT.md` as a **harness compatibility entry**, not as a separate chatbot policy owner and not as a fallback peer of `AGENTS.md` or `README.md`.

Its intended responsibility is to recover harness behavior that the active chat runtime may omit, especially:

- applicable `AGENTS.md` hierarchy loading for known target paths;
- task-intent Skill discovery/loading from repository-declared surfaces;
- path/glob-scoped Rule discovery/loading for known target paths.

Partial harness support is valid. For example, if the runtime already loads applicable `AGENTS.md` files but does not discover repository Skills, keep the native `AGENTS.md` behavior and use the compatibility entry only for Skill discovery/loading.

The underlying `AGENTS.md`, Skill, and Rule sources retain their own authority, selectors, triggers, procedures, and precedence. Do not copy their bodies into `CHATBOT.md` merely for chat compatibility.

If root `CHATBOT.md` is absent, continue with `load-context-github` and the active harness's evidenced discovery behavior. Do **not** invent `CHATBOT.md → AGENTS.md → README.md` or another filename fallback chain.

This is a mols convention, not a GitHub, Copilot, Agent Skills, or general repository standard.

### Change Defaults

Unless repository-local rules or an explicit user instruction say otherwise:

- do not commit normal change work directly to `main`;
- use a dedicated branch;
- open PRs as draft by default;
- self-review before presenting the change as complete;
- do not mark ready, merge, or otherwise finalize without explicit user intent.

## Boundary

This overlay owns only cross-repository personal conventions. Project-specific branch names, commit formats, tests, inbox policy, release process, architecture, discovery roots, Skill inventory, Rule selectors, and other local rules must be discovered from the live repository by `load-context-github`.
