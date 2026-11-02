---
name: mols-openspec-cli-compat
description: >-
  Use in OpenAI ChatGPT Chat for OpenSpec change/spec workflows such as propose,
  inspect, status, update, apply, verify, validate, sync, or archive when the task
  needs Chat tool composition or an unavailable CLI step must be adapted.
  Preserve the project's OpenSpec contract and complete supported work with
  connected repositories, files, analysis, and verification. Not for CLI
  installation, general chatbot setup, or schema/profile customization alone.
---

# OpenSpec CLI Compatibility for Chat

Complete OpenSpec work with **the capabilities actually available in Chat**. This Skill connects official OpenSpec workflows to authorized Chat tools; it neither invents CLI results nor replaces OpenSpec's own workflow instructions.

## Authority and activation

- A project's resolved OpenSpec root (including an external store, if applicable), installed version, effective configuration, schema, templates, existing artifacts, and selected official workflow determine the meaning of the work. Consult the project-specific sources and the official [OpenSpec Skills](https://openspec.dev/docs/skills) / [CLI](https://openspec.dev/docs/cli) contracts as needed.
- The current Chat session determines accessible apps, files, code execution, network restrictions, active identities, and permitted actions. A product feature listing, repository URL, or general Python executor does **not** prove that the project's CLI or installed Skills are executable. Chat is not automatically Work or Codex.
- This Skill owns only Chat execution adaptation. Project instructions and OpenSpec workflows keep authority over task scope, code changes, artifact semantics, confirmation, and verification. Reuse an accessible native workflow without adding a parallel process.

## Execution

1. **Locate the exact task state.** Identify the user's requested outcome, project, branch/commit or supplied-file snapshot, OpenSpec root/store, change/spec, and affected paths. Read relevant project instructions and the minimal effective config, schema and artifacts. If a store is referenced but cannot be resolved, expose the error rather than using a guessed local root.
2. **Respect root resolution.** When OpenSpec was *implicitly* selected and no project root exists, follow the official behavior and continue the user's request without imposing OpenSpec. For an *explicit* OpenSpec request without a root, stop before writing and request the needed choice: initialize, use an accessible registered store, or continue without OpenSpec. Do not create `openspec/` silently.
3. **Prefer native behavior, then discover useful Chat tools.** If the proper OpenSpec Skill or CLI can act on the **same authoritative project state**, use it. Otherwise inspect only task-relevant available actions: connected repository/app tools for remote reads/writes; Project/attached files for supplied data; allowed Python/code analysis for parsing and deterministic checks; web for public version-sensitive contracts; existing CI/check results for project verification. Neither install new tools nor enumerate every integration by default.
4. **Connect distinct states explicitly.** When useful: fetch exact files/ref with an authorized connector → derive the needed artifacts/diff using Chat or a supported executor → run available checks → apply approved changes through the writable source connector → read back remote files/diff and checks. Attached files and Python sandboxes are not implicitly the repository working tree; Python analysis may have no outbound network/API access. Do not add a code-execution step when direct text/file tooling is sufficient.
5. **Reconstruct only demonstrable semantics.** For a missing CLI command, identify required inputs, schema dependencies, ordering, outputs, filesystem effects, failure conditions, and checks. A matching file shape or LLM judgment is not CLI output. Prefer a useful, accurately scoped partial result if the equivalent operation cannot be verified.
6. **Gate changes.** Verify source/ref, affected files, current connected identity, permission, concurrent edits and recovery before writes. Keep changes coherent on a dedicated branch where appropriate. Never change accounts to bypass permissions. Do not perform a destructive or partial multi-path `sync`/`archive` without conflict resolution and a safe update/recovery mechanism.
7. **Report by evidence.** Use **Native** only for an observed original operation, **Adapted** when material behavior and checks were actually preserved, **Partial** for independently useful incomplete work, and **Blocked** when essential capability or authority is missing. Name changed paths/ref, checks performed, missing CLI/project validation, and the smallest required handoff. Never label manual inspection a passing CLI invocation.

## Operation-specific safeguards

- **Explore / list / show:** explore is read-only unless the user requests capturing a proposal; file enumeration shows only the inspected snapshot. Local/global OpenSpec stores and CLI-computed metadata may be absent.
- **Propose / new / continue / update:** these are distinct workflows. `propose` creates the schema-required *planning artifacts* without implementation code; `new` creates an empty change scaffold; `continue` adds the next ready artifact; `update` revises existing artifacts and follows the workflow's confirmation requirements. Resolve templates, dependencies, and output paths from the target project before writing. Do not silently claim that a plausible Markdown file is a complete proposal.
- **Status / instructions / templates:** CLI output is computed from the selected schema, project config, dependencies, resolved templates, and root. Prefer the actual `openspec status --change <id> --json` or `openspec instructions <artifact> --change <id>` in the project's CLI environment. Without equivalent inputs/logic, state directly observable artifact facts and the precise unverified CLI step, not fabricated readiness or instructions.
- **Apply / verify:** apply changes *code* and the real tracked task source(s), checking off only completed tasks based on evidence; do not assume every schema uses `tasks.md`. The separate verify workflow is report-only unless the user independently authorizes fixes. Run permitted project tests, and distinguish them from a mere checkbox or semantic review.
- **Validate:** only the original CLI's observed exit/result is an `openspec validate` result. Native CI, syntax checks and manual coherence reviews are useful, but are separate evidence tiers.
- **Sync / archive:** sync merges change deltas into canonical specs without archiving or changing code. Archive checks readiness, asks about outstanding spec sync and incomplete tasks, and moves the change into the archive. Resolve conflicts and obtain required confirmations; if transactional integrity or recovery cannot be preserved using the available remote tools, do not leave a half-synced or half-archived state.
- **Init / update / config / schemas / store / workset:** installation, generated agent instructions, global config and registered stores may depend on local machine state. Prefer original tooling and hand off any unreproducible side effects rather than reconstructing them from an incomplete repository view.

## Non-goals

Do not install OpenSpec/ChatGPT plugins, redefine schemas, build a replacement CLI/parser, provision a generic Chat harness, or schedule background work unless independently requested and authorized. Work/Codex/terminal execution may be an **explicit handoff**, not a silent mode change.
