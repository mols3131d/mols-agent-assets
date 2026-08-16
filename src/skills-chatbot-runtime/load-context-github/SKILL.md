---
name: load-context-github
description: >-
  Load repository-specific context before concrete GitHub work. Use before any
  @GitHub or GitHub tool/connector/plugin/integration call and for work on a specific
  repository, GitHub URL, file/path, PR/review, issue, branch/ref, commit, check,
  workflow, release, or repository change, including read-only and follow-up tasks.
  Discover only the repository instructions and live metadata that can affect the
  current task before task-level action.
metadata:
  - target:
      - "OpenAI ChatGPT"
---

# Load GitHub Context

Use this Skill as a **context loader**, not as a Git/GitHub workflow. It discovers the
repository/ref/path instructions and live GitHub context that govern the current task,
then hands execution to the relevant task capability.

## Trigger Boundary

Activate for either condition:

- a concrete GitHub repository/resource/path/ref/object is being read or changed;
- a GitHub tool, connector, plugin, or integration will be called.

Read-only work and follow-up work on an already identified repository/PR/issue are
included. General Git or GitHub explanation with no concrete target and no GitHub tool
use does not require this Skill.

A GitHub integration may be used first to **identify or discover context**. Complete the
relevant context loading before the first task-level action or repository mutation.

## Core Contract

1. **Identify live target** — confirm the repository and the ref/branch/PR/issue or
   other object relevant to the task. Do not rely on remembered repository state.
2. **Repository is authority** — discover repository conventions from the target ref,
   repository files, and relevant live metadata. Do not invent them from common practice.
3. **Scope by target** — load only instructions that actually apply to the current path,
   object, agent, or operation. Keep unrelated repositories and path scopes isolated.
4. **Distinguish rules from context** — do not treat nearby README text, filenames, or
   tool-specific guidance as normative without evidence of scope and intent.
5. **Load progressively** — start with explicit/high-signal instruction sources and live
   task metadata; expand only when a target path, task object, unresolved rule, or required
   reference makes more context material to the next action.
6. **Stop when sufficient** — do not recursively read the repository after the governing
   context and task constraints are known.

## Loading Sequence

### 1. Identify

Resolve only what the current request needs:

- repository;
- target ref/branch;
- PR/issue/check/workflow/release or other task object;
- target paths when known;
- operation class: read, review, edit, commit, PR, merge, release, etc.

If target paths are not yet known, inspect only root instruction-bearing sources or live
metadata that can govern the current task. Read a root `README.md` only when component
purpose, navigation, workflow context, or a referenced required source is materially
needed; do not preload it by default. When changed files or concrete paths become known,
add their scoped context.

### 2. Load Conditional Context

Read `references/instruction-discovery.md` when:

- concrete target paths or changed files exist;
- nested/scoped instructions may apply;
- instruction scope or precedence needs resolution;
- repository-level instruction locations beyond the root must be interpreted.

Read only the relevant section of `references/task-context.md` when the task concerns a
PR/review, issue, commit, branch/merge/history, CI/check/workflow, security/permission,
or release surface.

Do not load either reference merely because it exists.

### 3. Follow Required References

If an applicable repository instruction points to another required Git/VCS/governance
source, follow it only as far as the current task requires. Do not turn navigation links
into an unbounded crawl.

### 4. Recheck Before Action

Before task-level action, confirm that:

- the target repository/ref/object is correct;
- every known target path has the applicable root-to-target instruction context;
- any path selector or tool/agent scope actually matches;
- repository-specific conventions are evidenced rather than assumed;
- unresolved instruction conflicts that affect a mutation are surfaced instead of guessed.

## Important Instruction Semantics

Preserve these invariants even when the detailed reference is not loaded:

- For PR/review work, use the actual head-ref instructions; compare base instructions
  when a difference can materially affect the judgment.
- Nested `AGENTS.md` must not be lost by loading only the nearest file.
- `README.md` is primarily context/navigation and is not automatically an override or a
  mandatory context source.
- `applyTo`, path selectors, override semantics, and agent/tool-specific instructions
  apply only when their declared scope matches.
- If no repository rule is found, do not fabricate one. A safe default may be used, but
  do not present it as repository convention.

## Safety Boundary

Context loading must not silently widen the user's requested scope or create unrelated
side effects.

Do not expose secrets or credentials. Without explicit user intent, do not force-push,
rewrite history, perform destructive deletion, change permissions/protection, merge,
release, delete repositories, or perform similarly high-impact mutations.

This Skill does **not** own implementation, testing, naming, PR authoring, review
methodology, branch naming, commit formatting, merge strategy, or GitHub tool-call
orchestration. Those come from repository context and the relevant task Skill.

## Maintenance

When modifying this Skill, preserve `.docs/baseline/DIRECTIVE.md`. Shorter wording or a
cleaner structure is not an improvement if it weakens its trigger surface, root-to-target
instruction discovery, instruction/context distinction, path isolation, safety boundary,
or context-loader responsibility.
