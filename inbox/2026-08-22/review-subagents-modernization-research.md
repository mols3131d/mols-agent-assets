# Review Subagents Modernization Research

Baseline: `a90bd15b777553cce460ebc38f577bb1d5a3762a`

## Goal

Modernize `review-lead`, `review-quality`, and `review-adversarial` as a reusable review family without absorbing them into Agent Asset-specific validation or expanding to unverified runtimes.

## Evidence

### Current family

- `review-lead` owns reconciliation and final assessment but currently also carries edit tools and document-mutation responsibility.
- `review-quality` is read-oriented except for validation execution, but its Copilot tool list depends on VS Code extension-specific names such as `execute/runTests` and `vscodeGeneral/runTests`.
- `review-adversarial` is read-only and already separates hypotheses from verified defects.
- The lead always delegates both perspectives and is responsible for deduplication and final judgment.

### Responsibility overlap

`mols-agent-asset-validator` includes specialized quality and adversarial reviewers, but those reviewers are explicitly scoped to agent-facing assets. The reusable `review-*` family is generic repository/change review and therefore is not superseded by the validator family.

### Current runtime contracts

Rulesync 16.5.0 remains the repository-pinned version and supports tool-specific subagent metadata as passthrough sections.

- GitHub Copilot custom agents support stable tool aliases such as `read`, `search`, `execute`, `edit`, and `agent`. Omitting `tools` grants all available tools, so explicit least-capability lists remain useful.
- Copilot CLI uses the same custom-agent concepts but has a separate Rulesync target and section.
- Copilot/VS Code supports `user-invocable: false` for agents intended only as delegated specialists.
- Antigravity 2.0 uses the same custom-agent surface for IDE and CLI. Rulesync reads the shared `antigravity-ide` / `antigravity-cli` sections together, so the same specialist definitions can target both without duplicating the tool section.
- Antigravity requires explicit tool names; an omitted `tools` list defaults to no tools.

Official references:

- <https://docs.github.com/en/copilot/reference/custom-agents-configuration>
- <https://code.visualstudio.com/docs/agents/run/subagents>
- <https://antigravity.google/docs/subagents>
- <https://github.com/dyoshikawa/rulesync/blob/v16.5.0/src/features/subagents/copilot-subagent.ts>
- <https://github.com/dyoshikawa/rulesync/blob/v16.5.0/src/features/subagents/copilotcli-subagent.ts>
- <https://github.com/dyoshikawa/rulesync/blob/v16.5.0/src/features/subagents/antigravity-shared-subagent.ts>

## Findings

1. **P1 — Lead mutation surface is broader than its review responsibility.** A review coordinator should return the final assessment; persistence belongs to the caller or downstream workflow. Removing edit tools reduces accidental mutation and makes the family more portable.
1. **P1 — Quality reviewer Copilot tools are brittle.** Replace extension-specific test tool names with stable aliases `read`, `search`, and `execute`.
1. **P2 — Delegated specialists should not present as primary agents where the runtime supports that distinction.** Keep `review-lead` user-selectable; make quality/adversarial delegated-only in Copilot and preserve `mainAgent: false` in Antigravity.
1. **P2 — Runtime coverage is stale.** Add `copilotcli` and `antigravity-cli`, whose current contracts are close enough to the existing targets to preserve the family behavior.
1. **P2 — Reviewer return contracts are semantically aligned but structurally inconsistent.** Standardize around reviewed scope, evidence-linked candidate findings or hypotheses, validation performed, and unknowns. Only the lead assigns the final assessment.
1. **P2 — The lead should reconcile, not run a third complete review.** Preserve independence, validate material claims, deduplicate by root cause, and report incomplete delegation explicitly.

## Constraints

- Keep the three existing names and the `review-*` family.
- Keep the family generic; do not specialize it to Agent Assets or only source code.
- Do not add `targets: ["*"]` or Codex support without verified orchestration/tool parity.
- Do not add a new review framework, schema, or supporting package.
- Do not add behavioral eval infrastructure solely for this modernization; use direct semantic review plus repository deterministic validation unless a concrete repeated failure justifies fixtures.
