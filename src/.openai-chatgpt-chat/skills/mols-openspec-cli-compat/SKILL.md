---
name: mols-openspec-cli-compat
description: >-
  Use in OpenAI ChatGPT Chat when carrying out OpenSpec change/spec work
  (propose, inspect, status, update, apply, validate, sync, archive) requires
  selecting or composing Chat runtime tools or adapting an unavailable CLI.
  Use authoritative OpenSpec workflows and available repository, file, code
  analysis, and verification capabilities to finish the task safely.
  Not for OpenSpec installation, unrelated ChatGPT setup, or customization only.
---

# OpenSpec CLI Compatibility for Chat

Complete OpenSpec tasks using the **actual capabilities of the active Chat session**, not an assumed terminal. Prefer the official OpenSpec workflow and native CLI when available; otherwise compose existing tools while preserving material OpenSpec semantics. This Skill is an execution adapter, not a new CLI or workflow owner.

## Authority and scope

- The target project's resolved OpenSpec root, version, effective configuration, schemas, templates, artifacts, and official OpenSpec Skill/workflow are the source of truth. For exact version-sensitive behavior consult the current [Skills](https://openspec.dev/docs/skills) and [CLI](https://openspec.dev/docs/cli) sources, then the project version where known.
- The **current Chat session** determines available tools, app connections, file access, code execution, permissions, and approvals. Tool listings and official product feature descriptions are discovery hints, not evidence of active access. Do not assume ChatGPT Work's browser/computer access or Codex's terminal is available in Chat.
- User and repository instructions govern scope, source/ref, execution identity and writes. Never switch a connected account or install an integration without authorization.

## Procedure

1. **Resolve the requested OpenSpec outcome.** Identify project/repository, ref, change or spec, effective root/store, applicable workflow, read/write scope, and success condition. Use the actual repository instructions and existing OpenSpec config/artifacts. If no root resolves, do not silently initialize: an explicit OpenSpec request requires a choice of init, registered store, or proceeding outside OpenSpec; an implicit selection may instead proceed without OpenSpec under the official workflow.
2. **Start from native behavior.** When the correct project's OpenSpec CLI or official OpenSpec Skill is genuinely executable, use it. Do not infer local CLI availability from Python support or a GitHub app connection. If native execution is missing, load only the official operation contract and effective project-specific inputs necessary for a faithful alternative.
3. **Probe only task-relevant Chat capabilities.** Prefer connected repository/app tools for authoritative remote reads and writes; uploaded files or Chat Project sources for supplied context; allowed Python/code analysis for parsing, deterministic transforms, dependency checking and local diffs; web for current public OpenSpec documentation; connected CI/check tools for observed project validation. Discover exact actions and scopes as needed, rather than enumerating every possible tool.
4. **Compose a feasible path to completion.** A typical path is: fetch the source at a known ref → resolve schema/config and required artifacts → produce/analyze changes locally where useful → run available deterministic and semantic checks → apply permitted remote edits through the source connector → read back diff/files and available checks. File uploads, GitHub remote state, and analysis sandboxes are distinct surfaces; do not assume the Python sandbox has network/API access or the repository working tree. Use manual authoring directly when an executor adds no value.
5. **Preserve the required contract.** Establish inputs, dependencies, ordering, output, side effects, and validation for any CLI-dependent step. Native, materially equivalent adapted execution, valid partial work, optional skip, and blocked/handoff are distinct outcomes. Never label a locally inferred result as the original CLI's successful output.
6. **Gate writes and multi-file changes.** Confirm target ref, actor, authorization, concurrent edits, and recovery strategy. Prefer a dedicated branch and coherent commit. For `sync`/`archive`, preserve conflict handling and multi-file consistency; if the available tools cannot safely complete the full operation, keep the consequential change unapplied and provide the exact handoff.
7. **Verify, then report.** Use real project-native tests/OpenSpec CLI/connected CI when available; otherwise report precisely which local checks or reviews were completed. Finish all independently useful authorized work before handing off only the remaining requirement. Distinguish `Native`, `Adapted`, `Partial`, `Blocked` with evidence at the task level, not boilerplate per command.

## Operation-specific boundaries

- **Read/list/show:** repository file inspection can establish visible artifacts, but may omit CLI-computed metadata or externally registered stores. Identify the snapshot and coverage.
- **Status/instructions:** resolve schema dependencies, project configuration, templates, and other effective inputs before reproducing any CLI-derived status or instructions. If effective inputs or version-specific logic are missing, provide observed facts or a tentative analysis, **not** an authoritative CLI status/instruction result.
- **New/proposal/artifact changes:** reuse the governing OpenSpec workflow and project templates. Creating a plausible Markdown file alone is not proof of CLI scaffolding or readiness. For implementation, inspect code and tracked tasks, change authorized project sources, and mark tasks complete only with observed evidence.
- **Apply/verify/validate:** prefer the real OpenSpec validator and target tests when available. Manual review, static checks, and inferred correctness are distinct evidence; never present them as a passing `openspec validate` or implementation verification.
- **Sync/archive:** these may update canonical specs and move or remove multiple paths. Check merge semantics, conflicts, required confirmations, and recovery/atomicity before mutation. If the complete operation cannot be reproduced safely, leave the archive/sync unapplied and hand off rather than creating a partially archived change.
- **Init/update/config/store operations:** do not recreate installation, generated instruction files, global or external store state from assumptions; prefer native execution or an explicit user handoff when its side effects cannot be preserved.

## Result contract

For each material operation, report **Native / Adapted / Partial / Blocked**, the exact project/ref and observable evidence, any missing CLI validation, and the next action when unfinished. Mark uncertainty explicitly; do not claim ChatGPT Chat, a plugin, or this Skill is installed merely because its source was readable.

## Non-goals

This Skill does not install OpenSpec or ChatGPT plugins, author a replacement schema engine, customize project schemas/profiles, or create an additional workflow manager. Work/Codex or a terminal can be a precise user-approved handoff when required, not a silent Chat mode change.
