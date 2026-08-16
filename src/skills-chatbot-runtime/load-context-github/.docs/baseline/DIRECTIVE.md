# Directive

## Purpose

`load-context-github` exists to make ChatGPT load the **repository-specific context that governs GitHub work before task-level action**.

It is a context loader, not a Git/GitHub workflow skill. Its job is to discover which repository, ref, target paths, instructions, and GitHub metadata govern the current task, then hand that context to the task-specific skill or tool.

## Essence

The skill must preserve these behaviors:

1. **Trigger on concrete GitHub work.**
   Load for specific repositories, GitHub resources, PRs, issues, branches/refs, files/paths, Actions/checks, releases, repository changes, follow-up work, and GitHub tool/connector/plugin/integration use. Read-only work is included.

1. **Load context before action.**
   GitHub tooling may be used to discover context, but repository-changing or task-level action must not begin until the relevant context is loaded.

1. **Treat the repository as the source of truth.**
   Do not invent repository conventions from memory or common practice. Determine applicable rules from the target ref/branch, repository files, and relevant live GitHub metadata.

1. **Resolve instructions by target path.**
   For each target path, inspect the complete ancestor chain from repository root to target directory. Load applicable `AGENTS.md`, relevant `README.md`, path-specific instructions, and required referenced guidance. Keep instruction chains isolated between repositories and unrelated paths.

1. **Distinguish instruction from context.**
   `AGENTS.md` is an instruction candidate with directory scope unless the repository defines otherwise. `README.md` is primarily context/navigation; treat it as normative only when it clearly states a rule applicable to the task. Do not infer precedence from filename or proximity alone.

1. **Load only task-relevant Git/GitHub context.**
   Add PR, issue, commit, branch, merge, CI, release, permission, protection, or validation context only when the task needs it. Follow required references, but do not recursively load the repository without purpose.

1. **Preserve safe boundaries.**
   Do not expand this skill into implementation, testing, naming, PR authoring, review methodology, or GitHub tool orchestration. Those belong to repository instructions or task-specific skills.

## Invariants

A refactor is acceptable only if all of the following remain true:

- Concrete GitHub work reliably triggers the skill, including read-only and follow-up work.
- General Git/GitHub explanation without a concrete target or GitHub tool use does not require the skill.
- Repository/ref/task object are identified from live context when relevant.
- PR/review work considers instructions from the actual head ref and compares base instructions when that difference affects judgment.
- Every target path receives the applicable root-to-target instruction chain.
- Nested `AGENTS.md` scope is not lost by reading only the nearest file.
- `README.md` is not automatically promoted to an override or normative instruction.
- `applyTo`, path selectors, override semantics, and agent/tool-specific instructions are applied only when their declared scope actually matches.
- Repository-specific rules are never fabricated when none are found.
- Context from one repository or scoped path is not leaked into another.
- Destructive, privileged, history-rewriting, merge, release, or similarly high-impact operations retain explicit safety constraints.
- The skill remains a **context loader**.

If a proposed change violates any invariant, reject or redesign the change even if it makes the skill shorter, more generic, or easier to reuse.

## Non-Goals

Do not turn this skill into a source of canonical repository workflow rules.

It must not define universal branch names, commit formats, PR templates, merge strategies, review standards, implementation processes, test procedures, or repository-specific conventions. It discovers those rules; it does not own them.

It must also avoid becoming a general repository-reading skill. Context discovery should stop when the information needed to perform the GitHub task safely and correctly has been obtained.

## Recovery

When the skill appears degraded, over-generalized, or partially rewritten, restore it from this directive rather than from wording or document shape.

Use this recovery order:

1. Re-establish the **context-loader boundary**.
1. Restore the **concrete GitHub trigger surface**, including tools and read-only/follow-up tasks.
1. Restore **live repository/ref identification** and repository-as-source-of-truth behavior.
1. Restore **root-to-target ancestor instruction discovery** for every target path.
1. Restore the distinction between **`AGENTS.md` instruction scope** and **`README.md` context/navigation**.
1. Restore task-specific Git/GitHub context discovery and reference following without broad recursive loading.
1. Restore instruction scope/precedence handling, path isolation, and safety constraints.
1. Remove workflow logic that belongs to other skills.

Exact headings, prose, ordering, and implementation details may change. The behaviors and boundaries above may not.

## Maintenance Rule

Changes to `SKILL.md` should be reviewed against this directive. If simplicity, deduplication, trigger tuning, or compatibility work conflicts with the directive, preserve the directive's meaning first.

This document is a maintenance and recovery contract. It should change only when the intended essence of `load-context-github` changes deliberately.
