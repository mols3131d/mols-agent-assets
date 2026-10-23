# PR #253 — Remediation Log

## Accepted Work and Revision Ledger

| Stage | Commit | Outcome |
| --- | --- | --- |
| Initial review basis | `ff86e43b782e4fb24055b90d34275d425c66db0f` | 29-file diff, original 6 heading groups, active docs 9, historical notes 2; initial PR Gate success |
| Durable work plan | `80d4c8e16ea05c21229c1200cda6787a46f4069a` | Added [work-plan.md](work-plan.md) and restart contract |
| PR review | `47b13d786cbb1cd2b276933b99bcef5f91fd81c9` | Added [review.md](review.md) with F1/F2 |
| Runbook scope repair | `e5006c6cfbdb444c51b1b45523b7e4eb6f1d4afc` | Replaced lossy H1; `non-rotatable` and `maximum removal` preserved |
| Relationship evidence | `d5ff207270cacd3006843f3cdfea94597c6150b2` | Added [consistency-evidence.md](consistency-evidence.md) for live paths, current assets, commands and limits |

## Finding F2 — Corrected

- File: [GitHub sensitive-data removal runbook](../../docs/references/tooling/github-sensitive-data-removal-runbook.md)
- Previous H1 at reviewed head: `# GitHub Sensitive Data Removal Runbook`
- Current H1 after correction: `# Maximum Removal of Non-Rotatable Sensitive Data Exposed on GitHub`
- Reason: restore lost source-level scope while retaining the English H1–H3 language policy.
- Changed representation: **one H1 line only**; no modification to commands, credential handling, rewrite procedure or cited GitHub constraints.
- Follow-up: read back the exact head and check whether CI and document formatting pass.

## Finding F1 — Strengthened Evidence, Not Exhaustively Closed

- Added scope-bounded relation checks across current file tree, local links, source routing, tooling commands and named retired assets; see [consistency-evidence.md](consistency-evidence.md).
- Direct links from 61 `docs/` Markdown and 32 `catalog/` Markdown were checked against one immutable Git tree; 27 active maintainer docs scanned for explicit legacy names.
- No missing local target or new active orphan was demonstrated by these checks, **but absence outside this scope remains unverified**. A truthful completion statement must not imply all 324 Markdown files or all possible semantic relations were reviewed.
- Additional bounded checks and their results belong in [validation.md](validation.md). Record any genuinely broken reference in a new finding before modifying its owner.

## Historical Material Decision

- Preserve old review/plan accounts, rather than migrating old text mechanically to current names. Migrated identity statements in `docs/skills/mols-loops` and `docs/subagents/mols-review-dualvantage` are deliberate and have active maintenance value.
- Old `inbox/` owner statements already annotated at the prior PR head remain preserved.
- No files or source packages have been deleted.

## Implementation Boundaries

- All write actions were committed to the PR branch through the GitHub connector; no `main` writes.
- Did not invoke a toolchain inside a local checkout or execute sensitive history cleanup; no local runtime evidence is claimed.
- A commit SHA identifies changes, not a successful check. The final head-dependent CI/result is recorded in [validation.md](validation.md).

## Follow-up

Use [handoff.md](handoff.md) as the active state pointer; refresh it after each material commit or validation change. Review [review.md](review.md) against the latest diff, closing an issue only if its required outcome has evidence.
