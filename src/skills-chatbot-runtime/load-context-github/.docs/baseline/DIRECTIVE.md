# Directive

## Purpose

`load-context-github` exists to make ChatGPT load the **repository-specific context that governs GitHub work before task-level action**.

It is a context loader, not a Git/GitHub workflow skill. Its job is to discover which repository, ref, target paths, instructions, repository-defined instruction projections/fallbacks, and GitHub metadata govern the current task, then hand that context to the task-specific skill or tool.

This file is a **non-runtime recovery baseline**. Runtime behavior must be complete from `SKILL.md` and its runtime resources; `.docs/baseline/` exists to preserve the intended purpose and invariants across refactors.

## Essence

The skill must preserve these behaviors:

1. **Trigger on concrete GitHub work.**
   Load for specific repositories, GitHub resources, PRs, issues, branches/refs, files/paths, Actions/checks, releases, repository changes, follow-up work, and GitHub tool/connector/plugin/integration use. Read-only work is included.

1. **Load context before action.**
   GitHub tooling may be used to discover context, but repository-changing or task-level action must not begin until the relevant context is loaded.

1. **Treat the repository as the source of truth.**
   Do not invent repository conventions from memory or common practice. Determine applicable rules from the target ref/branch, repository files, repository-defined instruction semantics, and relevant live GitHub metadata.

1. **Resolve instructions by target path and active surface.**
   For each target path, inspect the complete ancestor chain from repository root to target directory and discover applicable instruction families. Preserve repository-defined projections such as `AGENTS.md`, path/glob instructions, or chatbot-specific files when the repository actually defines them. Keep instruction chains isolated between repositories and unrelated paths.

1. **Respect repository-defined fallback semantics.**
   A repository may define a non-standard instruction chain for a particular surface. For example, `mols-agent-assets` uses `CHATBOT.md → AGENTS.md → README.md` for its text I/O chatbot convention. This is a repository-local example, not a universal GitHub or Agent standard. Do not replace evidenced local semantics with generic platform assumptions.

1. **Distinguish instruction from context without erasing declared fallbacks.**
   `README.md` is normally context/navigation rather than a universal Rule format. If the repository explicitly declares README as a fallback instruction source for the active surface, preserve that local behavior. Do not infer precedence from filename or proximity alone.

1. **Load only task-relevant Git/GitHub context.**
   Add PR, issue, commit, branch, merge, CI, release, permission, protection, validation, or additional instruction context only when the task needs it. Follow required runtime references, but do not recursively load the repository without purpose.

1. **Preserve safe boundaries.**
   Do not expand this skill into implementation, testing, naming, PR authoring, review methodology, or GitHub tool orchestration. Those belong to repository instructions or task-specific skills.

## Invariants

A refactor is acceptable only if all of the following remain true:

- Concrete GitHub work reliably triggers the skill, including read-only and follow-up work.
- General Git/GitHub explanation without a concrete target or GitHub tool use does not require the skill.
- Repository/ref/task object are identified from live context when relevant.
- PR/review work considers instructions from the actual head ref and compares base instructions when that difference affects judgment.
- Every target path receives the applicable root-to-target instruction context for the active surface.
- Nested `AGENTS.md` scope is not lost by reading only the nearest file.
- Repository-defined instruction families and fallback chains are preserved when explicitly evidenced.
- `CHATBOT.md` or another local instruction file is not promoted into a universal platform standard merely because one repository uses it.
- `README.md` is not automatically promoted to an override or universal normative instruction, but an explicit repository fallback is honored.
- `applyTo`, path selectors, override semantics, agent/tool-specific instructions, and local projections are applied only when their declared scope actually matches.
- Repository-specific rules are never fabricated when none are found.
- Context from one repository or scoped path is not leaked into another.
- Destructive, privileged, history-rewriting, merge, release, or similarly high-impact operations retain explicit safety constraints.
- The skill remains a **context loader**.

If a proposed change violates any invariant, reject or redesign the change even if it makes the skill shorter, more generic, or easier to reuse.

## Non-Goals

Do not turn this skill into a source of canonical repository workflow rules.

It must not define universal branch names, commit formats, PR templates, merge strategies, review standards, implementation processes, test procedures, or repository-specific conventions. It discovers those rules; it does not own them.

It must not claim that repository-local projections or fallback chains are official GitHub/Copilot/Agent standards.

It must also avoid becoming a general repository-reading skill. Context discovery should stop when the information needed to perform the GitHub task safely and correctly has been obtained.

## Recovery

When the skill appears degraded, over-generalized, or partially rewritten, restore it from this directive rather than from wording or document shape.

Use this recovery order:

1. Re-establish the **context-loader boundary**.
1. Restore the **concrete GitHub trigger surface**, including tools and read-only/follow-up tasks.
1. Restore **live repository/ref identification** and repository-as-source-of-truth behavior.
1. Restore **root-to-target ancestor instruction discovery** for every target path.
1. Restore **repository-defined instruction families and fallback semantics** for the active surface.
1. Restore the normal distinction between instruction and context while preserving explicitly declared local fallback sources.
1. Restore task-specific Git/GitHub context discovery and runtime reference following without broad recursive loading.
1. Restore instruction scope/precedence handling, path isolation, and safety constraints.
1. Remove workflow logic that belongs to other skills.

Exact headings, prose, ordering, and implementation details may change. The behaviors and boundaries above may not.

## Maintenance Rule

Changes to `SKILL.md` should be reviewed against this directive. If simplicity, deduplication, trigger tuning, compatibility work, or platform normalization conflicts with the directive, preserve the directive's meaning first unless the user intentionally changes the underlying purpose or requirement.

This document is a maintenance and recovery contract. It should change only when the intended essence, requirements, or durable decisions of `load-context-github` change deliberately.
