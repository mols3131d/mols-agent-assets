---
name: load-context-github
description: >-
  Load live repository instructions and GitHub state for task-level work on a
  concrete GitHub repository or object, including reads, reviews, changes, resolving
  a named target, and follow-ups to an already established target. Use with GitHub
  connector/tool calls scoped to such work. Skip generic Git/GitHub explanation and
  broad discovery with no repository or object scope.
---

# Load GitHub Context

Use this Skill only to resolve the **live GitHub context that governs the task**.
Execution belongs to the downstream task capability.

## Trigger

Activate when either condition holds:

- the task reads, reviews, changes, or otherwise acts on a concrete GitHub repository,
  path, ref, PR, issue, check, workflow, release, or other GitHub object;
- a GitHub connector/tool is used for task-level work scoped to such a target.

A named target that still needs ID/ref resolution counts as concrete. Follow-up requests
continue to use the already established target even when the user does not repeat its name.
If a follow-up switches repository/object scope, resolve and load context for the new target.

Do not activate for generic Git/GitHub explanation or broad discovery/search with no
repository or object scope. A narrow read may identify a target first; finish relevant
context loading before task-level action on that target.

## Contract

- Resolve the live repository and relevant ref/object. Do not rely on remembered state.
- Treat repository files, the target ref, and live GitHub metadata as authority for
  repository-specific rules.
- Scope instructions per target path, object, operation, and active agent/chatbot surface.
- Apply repository/platform selectors, fallback, and precedence only when evidenced.
- Load progressively. Stop when more context is unlikely to change the next action.

## Procedure

### 1. Identify the Target

Resolve only what the task needs: repository, ref/branch, GitHub object, target paths,
operation class, and active surface when it affects instruction discovery.

If target paths are not known yet, inspect only root instruction sources or live metadata
needed to identify them.

### 2. Resolve Applicable Instructions

For each target path, inspect the ancestor chain from repository root to the target
directory. Reuse shared ancestors, but compute effective context per path.

Use only instruction sources the repository or active surface actually defines, such as:

- `AGENTS.md` or repository-defined agent/chatbot instruction files;
- GitHub Copilot instruction files and matching path-scoped instructions;
- contribution, development, governance, or repository-defined path/glob rules;
- `README.md` only when explicitly required, materially needed, or declared as fallback.

Do not invent precedence from filenames or proximity. Apply declared selectors and the
active surface's current scope/precedence semantics. Verify time-sensitive platform
semantics when they can change the task.

If an instruction conflict blocks a safe mutation, surface the conflict instead of guessing.

### 3. Load Task Context

Load only the context required by the current operation.

| Condition | Load |
| --- | --- |
| PR or review | head-ref instructions, changed-path rules, relevant base-instruction differences, templates, `CODEOWNERS`, checks/protection when material |
| Issue | templates or contribution guidance that changes classification, required fields, or workflow |
| Commit, branch, merge, history | repository VCS guidance and live protection/rulesets when material |
| CI, workflow, security, permissions | the named/failing surface plus relevant workflow, validation, permission, or security context |
| Release | relevant versioning/release guidance, automation, and live release metadata |

Follow instruction links only as far as the task requires. If high-signal sources are
insufficient, search for the repository's own terminology around the unresolved rule
instead of crawling broadly.

### 4. Gate and Stop

Before handoff, confirm that:

- the repository/ref/object is correct;
- every known target path has its applicable instruction context;
- repository-specific rules are evidenced rather than assumed;
- any material incomplete or conflicting context is surfaced.

Then stop loading context.

## Boundary

This Skill is read-oriented context discovery. It does not own implementation, testing,
review methodology, naming, branch/commit/PR policy, merge strategy, release workflow,
or GitHub tool orchestration.

Do not expose secrets. Context loading must not widen task scope or perform destructive,
privileged, history-rewriting, merge, release, or similarly finalizing mutations.
