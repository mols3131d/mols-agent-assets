# Review Subagents Modernization Plan

Based on: `inbox/2026-08-22/review-subagents-modernization-research.md`

## Active Scope

- Goal: modernize the three reusable `review-*` subagents while preserving their generic review responsibility.
- In scope: frontmatter targets/tools/invocability, role boundaries, delegation contract, evidence handling, return contract.
- Out of scope: renaming, deleting the family, Agent Asset validator internals, new review schemas, runtime scripts, unrelated assets.
- Acceptance: least-capability tool surfaces; current Copilot/Antigravity target coverage; independent specialist roles; no source mutation by reviewers; explicit evidence/unknown handling; Rulesync and Markdown validation pass.

## Work

1. Refactor `review-lead` into a read-only coordinator that delegates both specialist perspectives, validates and reconciles their claims, and returns one final assessment without editing repository files.
1. Replace Copilot extension-specific tool names with stable aliases and add equivalent `copilotcli` metadata where needed.
1. Add `antigravity-cli` to all three targets while reusing the shared Antigravity tool section.
1. Mark `review-quality` and `review-adversarial` delegated-only where the runtime exposes a primary-agent visibility control.
1. Tighten each description so planner routing can distinguish coordinator, quality, and adversarial responsibilities.
1. Standardize specialist output around scope, evidence-linked findings/hypotheses, validation, and unknowns; keep final severity/disposition with the lead.
1. Preserve existing scope discipline and evidence-first rules while removing duplicated or obsolete wording.
1. Run semantic/adversarial review and repository PR Gate. Replan only if a material conflict or runtime incompatibility appears.

## Validation

- compare changed frontmatter against Rulesync 16.5.0 target adapters;
- inspect all references to the three subagent names;
- `rulesync:doctor` via PR Gate;
- changed Markdown normalization via PR Gate;
- verify no unrelated asset changes;
- verify specialist independence and lead reconciliation boundary by static scenario review.
