---
name: mols-openspec-cli-compat
description: >-
  Use in OpenAI ChatGPT Chat mode when an OpenSpec change/spec workflow requires
  openspec CLI behavior but the project's native CLI or official OpenSpec
  skills cannot perform that behavior in the active runtime. Select verified
  existing-tool adaptations, bounded partial results, or precise handoff.
  Do not use for ordinary native OpenSpec execution, OpenSpec customization,
  or installing the CLI.
---

# OpenSpec CLI Compatibility

Preserve the **material behavior of OpenSpec operations** in ChatGPT Chat when the original CLI path is unavailable. This Skill adapts execution; it does not replace OpenSpec workflows, own project policy, or implement a second OpenSpec CLI.

## Authority and scope

- The selected project's installed OpenSpec version, configuration, schemas, templates, and actual state govern its behavior. Consult the corresponding official contract when a version-sensitive decision matters; do not assume upstream latest applies to an older project.
- OpenSpec's own workflow/Skill instructions own proposal, implementation, sync, verification, and archive semantics. This Skill owns only the decision about **how to perform a required CLI-dependent operation** with available Chat runtime capabilities.
- Applicable repository instructions and user authorization govern repository work. Tool availability does not grant write permission, and a read-only connector does not imply a working filesystem or terminal.

## Procedure

1. **Resolve the operation.** Identify the requested OpenSpec operation, project/root, branch or commit, change/spec identifier, read/write scope, and required result. Read only applicable repository instructions and OpenSpec artifacts. If a required source, target version, or authoritative configuration is inaccessible, record the gap rather than inventing it.
2. **Check native execution in the correct environment.** Prefer an authorized OpenSpec CLI or already available official OpenSpec Skill/tool running against the **same project state**. A general-purpose code executor or GitHub file connector is not proof that the project's CLI can run. Do not install dependencies or move the operation to another machine/account without authority.
3. **Identify the exact contract at risk.** For an operation that cannot run natively, determine its necessary inputs, effective config/schema, artifact dependencies, expected output, side effects, failure semantics, and validation criteria. Use the official [CLI](https://openspec.dev/docs/cli) and [Skills](https://openspec.dev/docs/skills) references when relevant. Do not expand command behavior from memory or invent defaults.
4. **Choose the smallest valid outcome.**
   - **Native:** execute and observe the original operation in the right project environment.
   - **Adapted:** use an authorized existing tool only if its inputs, output, relevant ordering, side effects, and required verification are demonstrably preserved. Record the difference and evidence; do not call an unverified imitation equivalent.
   - **Partial:** produce a separately useful and clearly scoped result without claiming the missing CLI operation succeeded.
   - **Optional skip:** omit only a step that the governing workflow and user goal genuinely allow to be omitted.
   - **Blocked / handoff:** stop the affected operation when required state, capability, permission, or fidelity cannot be preserved. Specify the required CLI action, environment, and prerequisites.
5. **Execute with safeguards.** Before writes, confirm target ref, identity, authorization, conflicting changes, and recovery boundary. Prefer a dedicated branch and coherent commit for related changes; read the final diff and project state where possible. Do not silently substitute another connected account or treat locally produced files as remote repository changes.
6. **Report evidence.** Distinguish original commands actually run, adapted operations actually observed, manual or semantic inspection, skipped steps, and pending verification. State what was changed, where, what remains, and the exact handoff for any required unfinished operation.

## Operation-specific boundaries

- **Read/list/show:** repository file inspection can establish visible artifacts, but may omit CLI-computed metadata or externally registered stores. Identify the snapshot and coverage.
- **Status/instructions:** resolve schema dependencies, project configuration, templates, and other effective inputs before reproducing any CLI-derived status or instructions. If effective inputs or version-specific logic are missing, provide observed facts or a tentative analysis, **not** an authoritative CLI status/instruction result.
- **New/proposal/artifact changes:** reuse the governing OpenSpec workflow and project templates. Creating a plausible Markdown file alone is not proof that the CLI's scaffolding or artifact readiness contract is satisfied.
- **Validate/verify:** prefer the real OpenSpec validator and target tests when available. Manual review, schema inspection, and inferred correctness are distinct evidence; never present them as a passing `openspec validate` or implementation verification.
- **Sync/archive:** these may update canonical specs and move or remove multiple paths. Check merge semantics, conflicts, required confirmations, and recovery/atomicity before mutation. If the complete operation cannot be reproduced safely, leave the archive/sync unapplied and hand off rather than creating a partially archived change.
- **Init/update/config/store operations:** do not recreate installation, generated instruction files, global or external store state from assumptions; prefer native execution or an explicit user handoff when its side effects cannot be preserved.

## Result contract

For each material operation, report **Native / Adapted / Partial / Blocked**, the exact project/ref and observable evidence, any missing CLI validation, and the next action when unfinished. Mark uncertainty explicitly; do not claim ChatGPT Chat, a plugin, or this Skill is installed merely because its source was readable.

## Non-goals

This Skill does not install OpenSpec or ChatGPT plugins, author a replacement schema engine, customize project schemas/profiles, or create an additional workflow manager. If native execution already covers the request, leave this compatibility layer unused.
