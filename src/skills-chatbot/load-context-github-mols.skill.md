---
name: load-context-github-mols
description: >-
  Add mols-specific GitHub conventions on top of load-context-github when the target
  is clearly the user's personal GitHub space, such as a repository owned by
  mols3131d or another repository explicitly identified as personally managed. Do not
  activate for another person's repository, an organization/team repository, or a
  shared project merely because the user can access or administer it.
---

# Load Mols GitHub Context

This Skill is a **personal overlay** for `load-context-github`.

Never use it instead of the base loader. When this Skill applies, load both:

1. `load-context-github`
2. `load-context-github-mols`

## Activation Boundary

Activate only when both conditions hold:

- `load-context-github` applies to the task;
- the target is evidenced as the user's personal GitHub space.

Strong evidence includes repository ownership by `mols3131d` or an explicit user statement
that the repository is their own/personal repository.

Do **not** infer personal scope from collaborator access, organization membership, admin
permission, authorship, contribution history, or familiarity with the project. Team,
company, organization, and other people's repositories use only the base loader unless
the user explicitly identifies the target as personally governed.

## Personal Conventions

### Instruction Fallback

For the user's personal repositories, use this chatbot-oriented fallback when the
repository does not explicitly define a different applicable rule:

`CHATBOT.md` → if absent `AGENTS.md` → if absent `README.md`

Apply the chain per relevant path/scope. Deeper applicable instructions may refine or
override broader ones when the repository declares that behavior.

This fallback is a **mols convention**, not a GitHub, Agent Skills, Copilot, or general
repository standard. Never export it to non-personal targets.

An explicit repository-local instruction policy takes precedence over this personal
default when it intentionally defines different semantics.

### GitHub Change Safety

For personal repositories, prefer the following defaults unless repository-local rules or
an explicit user instruction say otherwise:

- do not commit directly to `main` for normal change work;
- work on a dedicated branch;
- open PRs as draft by default;
- self-review the proposed changes before presenting the PR as complete;
- do not mark a PR ready, merge it, or perform similarly finalizing actions without an
  explicit user request.

These are defaults for the user's personal GitHub workflow, not requirements for external
or team repositories.

## Boundary

This overlay owns only the user's cross-repository personal conventions. Repository-specific
rules still come from the live target repository through `load-context-github`.

Do not hard-code project-specific inbox policy, branch names, test commands, commit
formats, release processes, or architecture here when they belong to one repository.
Discover those from that repository instead.
