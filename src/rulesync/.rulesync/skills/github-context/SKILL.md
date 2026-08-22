---
name: github-context
description: >-
  Load live repository instructions and GitHub state for task-level work on a concrete
  GitHub repository or object: repository, path, ref, PR, issue, check, workflow,
  release, or other named target. Use for reads, reviews, changes, connector/tool
  actions, target resolution, and follow-ups to an established target. A named target
  that still needs ID/ref resolution counts as concrete; re-resolve context when a
  follow-up switches target. Do not use for generic Git/GitHub explanation or broad
  discovery/search before any concrete target is established.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Load GitHub Context

This Skill resolves the **live GitHub context that governs the task**.
Execution belongs to the downstream task capability.

## Contract

- Resolve the live repository and relevant ref/object. Do not rely on remembered state.
- Treat repository files, the target ref, and live GitHub metadata as authority for repository-specific rules.
- Scope instructions and Agent Assets per target path, object, operation, and active harness semantics.
- Apply repository/platform selectors, discovery rules, fallback, and precedence only when evidenced.
- Load progressively. Stop when more context is unlikely to change the next action.
- When a narrow read establishes the concrete target, finish the context loading that can affect the task before downstream action depends on that context.

Do not classify the caller as chatbot versus coding agent to choose a separate policy model. Use the active harness capabilities and the repository's declared discovery surfaces.

## Procedure

### 1. Identify the Target

Resolve only what the task needs: repository, ref/branch, GitHub object, target paths, operation class, and active harness behavior when it affects discovery.

If target paths are not known yet, inspect only root instruction/discovery sources or live metadata needed to identify them.

### 2. Resolve Applicable Instructions

For each target path, inspect the ancestor chain from repository root to the target directory. Reuse shared ancestors, but compute effective context per path.

Use only instruction sources the repository or active harness actually defines, such as:

- applicable `AGENTS.md` hierarchy;
- GitHub Copilot instruction files and matching path-scoped instructions;
- contribution, development, governance, or repository-defined path/glob rules;
- `README.md` only when explicitly required, materially needed, or declared as fallback.

A repository-defined compatibility/bootstrap entry may route discovery, but it is instruction or policy authority only when the repository explicitly assigns that role.

Do not infer that files with different names form a fallback chain. Do not invent precedence from filenames or proximity. Apply declared selectors and the active harness's current scope/precedence semantics. Verify time-sensitive platform semantics when they can change the task.

If an instruction conflict blocks a safe mutation, surface the conflict instead of guessing.

### 3. Resolve Applicable Agent Assets

When the repository declares Agent Asset discovery surfaces, load only assets applicable to the current task.

- Skill: use declared index, catalog, root, or runtime catalog to select by task intent; read only selected Skill sources and required supporting resources.
- Rule: match known target paths against declared glob/path/selectors; load only matching Rules.
- Reuse already-loaded applicable assets from the same relevant revision. Do not recursively re-select this loader or another routing asset merely because it appears in a discovered catalog.
- Do not preload full catalogs when metadata or selectors can narrow the set.
- Re-evaluate applicability when task intent or target paths materially change.

A repository compatibility entry may point to these surfaces, but it does not become the owner of Skill or Rule semantics.

### 4. Load Task Context

Load only the context required by the current operation.

| Condition | Load |
| --- | --- |
| PR or review | head-ref instructions, changed-path rules, relevant base-instruction differences, templates, `CODEOWNERS`, checks/protection when material |
| Issue | templates or contribution guidance that changes classification, required fields, or workflow |
| Commit, branch, merge, history | repository VCS guidance and live protection/rulesets when material |
| CI, workflow, security, permissions | the named/failing surface plus relevant workflow, validation, permission, or security context |
| Release | relevant versioning/release guidance, automation, and live release metadata |

Follow instruction links only as far as the task requires. If high-signal sources are insufficient, search for the repository's own terminology around the unresolved rule instead of crawling broadly.

### 5. Gate and Stop

Before handoff, confirm that:

- the repository/ref/object is correct;
- every known target path has its applicable instruction context;
- applicable declared Skills and path-scoped Rules were considered when those surfaces exist;
- repository-specific rules are evidenced rather than assumed;
- any material incomplete or conflicting context is surfaced.

Then stop loading context.

## Boundary

This Skill is read-oriented context discovery. It does not own implementation, testing, review methodology, naming, branch/commit/PR policy, merge strategy, release workflow, or GitHub tool orchestration.

Do not expose secrets. Context loading must not widen task scope or perform destructive, privileged, history-rewriting, merge, release, or similarly finalizing mutations.
