# Review Subagents Modernization Review

Based on:

- `inbox/2026-08-22/review-subagents-modernization-research.md`
- `inbox/2026-08-22/review-subagents-modernization-plan.md`

## Loop 1

### Findings and disposition

| Finding | Disposition |
| --- | --- |
| `review-lead` carried edit capability despite coordination being its primary responsibility | Fixed: lead is read/delegate only and returns the final assessment to the caller |
| `review-quality` depended on extension-specific Copilot test tool names | Fixed: use stable `read`, `search`, `execute` aliases |
| delegated specialists could appear as primary agents in Copilot | Fixed: `user-invocable: false`; Antigravity already uses `mainAgent: false` |
| Antigravity/Copilot CLI target coverage lagged current Rulesync/runtime support | Fixed: add `antigravity-cli` and `copilotcli`; keep explicit targets rather than wildcard expansion |
| specialist return contracts were inconsistent | Fixed: both return bounded scope, evidence-linked candidate claims, validation/defense state, and unknowns; lead owns reconciliation |
| lead could accidentally become a third full reviewer | Fixed: direct work is limited to claim verification, conflict resolution, deduplication, and coverage accounting |

Loop 1 materially improved the family, but semantic review found that the new descriptions had narrowed the original generic review scope toward repository/VCS changes.

## Loop 2

### Finding and disposition

| Finding | Disposition |
| --- | --- |
| Runtime modernization accidentally narrowed the family from generic technical review to repository/change review | Fixed: all three now operate on a bounded technical artifact or change and explicitly avoid assuming a VCS or artifact type |

No additional material design finding remained after the scope correction.

## Current Contract

- `review-lead` = dual-perspective coordinator and final assessment owner.
- `review-quality` = intended behavior, correctness, regression, integration, maintainability, and validation perspective.
- `review-adversarial` = reachable failure, abuse, trust-boundary, recovery, and hidden-assumption perspective.
- Specialists remain independent and return candidate claims, not final disposition.
- All three are non-mutating review roles; validation commands are permitted only for quality review within the explicit execution boundary.
- Supported targets are explicit: Copilot IDE, Copilot CLI, Antigravity IDE, Antigravity CLI.
- Agent Asset-specific validation remains owned by `mols-agent-asset-validator`; this family stays generic.

## Evidence Boundary

- Source/frontmatter shape and tool-section behavior were checked against repository-pinned Rulesync 16.5.0 adapters and current Copilot/Antigravity documentation.
- No live target-runtime orchestration trial is claimed.
- Merge-result PR Gate run #849 passed deterministic tests, canonical Rulesync source validation, and changed Markdown normalization. Distribution route validation and Promptfoo smoke were outside the change-impact scope.

## Status

`completed`. Two substantive Loops converged, the merge-result Gate introduced no new material finding, and further wording-only iteration would not provide credible information or quality gain.
