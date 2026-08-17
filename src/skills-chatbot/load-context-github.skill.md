---
name: load-context-github
description: >-
  Load repository-specific context before concrete GitHub work. Use before any
  @GitHub or GitHub tool/connector/plugin/integration call and for work on a specific
  repository, GitHub URL, file/path, PR/review, issue, branch/ref, commit, check,
  workflow, release, or repository change, including read-only and follow-up tasks.
  Discover only the repository instructions and live metadata that can affect the
  current task before task-level action.
---

# Load GitHub Context

Use this Skill as a **context loader**, not as a Git/GitHub workflow. Discover the
repository/ref/path instructions and live GitHub state that govern the current task,
then hand execution to the relevant task capability.

## Trigger Boundary

Activate when either condition is true:

- a concrete GitHub repository, resource, path, ref, or object is being read or changed;
- a GitHub tool, connector, plugin, or integration will be called.

Read-only and follow-up work are included. General Git/GitHub explanation with no
concrete target and no GitHub tool use does not require this Skill.

A GitHub integration may be used first to identify the target or load context. Complete
the relevant context loading before task-level action or repository mutation.

## Core Contract

1. **Identify live target** — confirm the repository and the ref/branch/PR/issue or other
   object relevant to the task. Do not rely on remembered repository state.
1. **Repository is authority** — discover conventions from the target ref, repository
   files, and relevant live metadata. Do not invent repository rules from common practice.
1. **Scope by target** — apply only instructions that govern the current path, object,
   agent, operation, and active surface. Keep unrelated repositories and path scopes isolated.
1. **Respect local semantics** — repository-defined instruction families, projections,
   fallbacks, selectors, and overrides may be non-standard. Apply them only when evidenced.
1. **Load progressively** — start with explicit/high-signal sources and task metadata;
   expand only when more context can materially change the next action.
1. **Stop when sufficient** — do not recursively read the repository after the governing
   context and task constraints are known.

## Procedure

### 1. Identify

Resolve only what the request needs:

- repository and target ref/branch;
- PR, issue, check, workflow, release, or other task object;
- target paths when known;
- operation class such as read, review, edit, commit, PR, merge, or release;
- active agent/chatbot surface when it changes instruction discovery.

If paths are not yet known, inspect only root instruction-bearing sources or live
metadata that can govern the task. Add path-scoped context when concrete paths become known.

### 2. Resolve Instructions

For every target path, inspect the ancestor chain from repository root to the target
directory. Reuse shared ancestors for multiple paths, but compute each path's effective
context separately.

Look for instruction-bearing sources that the active surface or repository actually
defines, for example:

- `CHATBOT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or repository-defined variants;
- `.github/copilot-instructions.md`;
- matching `.github/instructions/**/*.instructions.md`;
- `CONTRIBUTING.md`, `DEVELOPMENT.md`, `.github/CONTRIBUTING.md`, or governance docs;
- repository-defined path/glob instructions and bot/agent instructions;
- `README.md` only when explicitly referenced, materially needed for interpretation, or
  declared as a fallback instruction source.

Do not infer precedence or override semantics from filenames or proximity alone. Use the
active platform/tool semantics or explicit repository convention.

For `mols-agent-assets`, when its text-I/O chatbot convention governs the task, use the
repository-local fallback:

`CHATBOT.md` → if absent `AGENTS.md` → if absent `README.md`.

This is not a universal GitHub or Agent standard. Higher-authority system, user, platform,
tool, and permission constraints still apply.

For nested `AGENTS.md`, discover all applicable files along the root-to-target chain and
use the active surface's documented scope/precedence. On GitHub Copilot surfaces that
support nested agent instructions, the nearest applicable `AGENTS.md` wins among
applicable `AGENTS.md` files. Do not generalize that rule to unrelated instruction families.

When the active surface follows GitHub Copilot custom-instruction semantics, apply its
current documented precedence rather than a generic rule. Treat those semantics as
platform-specific and time-sensitive; verify them when they can affect the task.

Apply `applyTo`, path selectors, agent/tool scopes, and repository-defined overrides only
when their declared scope matches. If a mutation depends on an unresolved instruction
conflict, surface the conflict instead of guessing.

### 3. Load Task-Specific Context

Load only context that can constrain the current GitHub object or operation:

- **PR/review** — actual head-ref instructions, changed paths and their scoped rules,
  base instructions when head/base differences matter, and relevant templates,
  `CODEOWNERS`, checks, protection, or review guidance.
- **Issue** — relevant issue templates or contribution guidance only when they affect
  classification, required fields, workflow, or mutation.
- **Commit** — repository-owned commit guidance such as `.gitmessage`, contribution
  docs, or hook documentation. Do not assume Conventional Commits unless evidenced.
- **Branch/merge/history** — repository VCS guidance and live protection/rulesets when
  material. Do not invent branch names, merge strategies, or history policy.
- **CI/check/workflow/security/permissions** — start from the named or failing surface;
  load only the relevant workflow, validation docs, metadata, permissions, or security rules.
- **Release** — relevant versioning/release guidance, automation, and live release
  metadata only as needed.

Follow links from applicable instructions only as far as the current task requires.
If high-signal locations are insufficient, search for the repository's own terminology
around the unresolved rule instead of crawling broadly.

### 4. Recheck and Stop

Before task-level action, confirm:

- the repository/ref/object is correct;
- every known target path has its applicable instruction context;
- local fallback, selector, and precedence semantics were respected;
- repository-specific conventions are evidenced rather than assumed;
- partial or unresolved context that blocks a safe mutation is surfaced.

Stop when additional context is unlikely to change the next action.

## Safety Boundary

Context loading must not widen the requested scope or create unrelated side effects.

Do not expose secrets or credentials. Without explicit user intent, do not force-push,
rewrite history, perform destructive deletion, change permissions/protection, merge,
release, delete repositories, or perform similarly high-impact mutations.

This Skill does **not** own implementation, testing, naming, PR authoring, review
methodology, branch naming, commit formatting, merge strategy, or GitHub tool-call
orchestration. Those come from repository context and the relevant task capability.
