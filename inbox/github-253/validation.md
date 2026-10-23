# PR #253 — Validation Ledger

## Read-Only Checks Completed

| Check | Status | Scope / exact evidence |
| --- | --- | --- |
| PR baseline | ✅ Pass | PR #253 base `23d649b2eac6e9115ce0e97a823d59de4d37b3c5` and head are separately tracked; no assumption that current `main` is the same baseline |
| Relative Markdown links in `docs/` | ✅ Pass | At `80d4c8e16ea05c21229c1200cda6787a46f4069a`, 61 Markdown files checked for inline relative link target path existence against complete recursive Git tree; 0 missing files/directories observed |
| Relative Markdown links in `catalog/` | ✅ Pass | Same revision; 32 Markdown files checked; 0 missing files/directories observed |
| Active maintainer legacy names | ✅ Pass | At `e5006c6cfbdb444c51b1b45523b7e4eb6f1d4afc`, 27 Markdown files under `docs/skills/` and `docs/subagents/` scanned for `mols-rpi`, `mols-markdown-for-human`, `mols-agent-asset-validator`, and `review-lead/quality/adversarial`; observed legacy names were in `mols-loops` rename and DualVantage migration descriptions |
| Relative Markdown links in `inbox/` | ✅ Pass (historical pre-existing files) | At `a8f5bd705db1c6077c43a0baf3a18a0fb22300dc`, 68 Markdown files scanned by the same tree-based checker. Apparent missing paths are only newly authored references to the not-yet-created `validation.md`/`handoff.md` and literal inline example `[text](relative-url)`. The two actual report files are created in this workstream; rerun on final SHA. |
| Execution entrypoint spot check | ✅ Pass | `docs/development/validation.md` → `package.json` `rulesync:validate`; `docs/development/evaluation.md` / `evals/README.md` → `mise.toml` and `package.json` `mols-loops` eval tasks. Checked declaration name agreement, not execution |
| Source and history boundaries | ✅ Pass (sample) | `docs/skills/mols-loops/README.md` names `mols-rpi` as old identity; `docs/subagents/mols-review-dualvantage/maintenance.md` classifies legacy review callers. Verified current owner rather than deleting valid migration docs |
| Runbook scope review | ✅ Pass | `e5006c6cfbdb444c51b1b45523b7e4eb6f1d4afc` changed only the H1 to include maximum removal + non-rotatable; prior text, command/code remain untouched |
| Original PR Gate | ✅ Pass (obsolete for later revisions) | [GitHub Actions run #40020033915](https://github.com/mols3131d/mols-agent-assets/actions/runs/40020033915) succeeded at `ff86e43b782e4fb24055b90d34275d425c66db0f`. Recheck latest HEAD at end. |

## Validation Still Not Established

- ⚪ Not Verified — `semantic-exhaustiveness`: checks establish consistency for a **bounded relation graph**, not every relationship among all 439 repository blobs / 324 Markdown files at the original analysis snapshot.
- ⚪ Not Verified — `external-fragments`: changed H1–H3 text may alter GitHub fragment URLs used outside this repo. Presence/absence of external consumers is unknown.
- ⚪ Not Verified — `external-http-targets`: physical links to websites or third-party documentation were not crawled; the local Git tree cannot establish their current validity.
- ⚪ Not Verified — `runtime-and-local-formatter`: no full local checkout, rumdl/format-changed, Promptfoo provider run or native Rulesync generation executed in this session.
- ⚪ Not Verified — `GitHub-merge-approval`: CI success does not constitute a human approval, and the current user did not authorize a merge.

## Check Semantics and Reproducibility

The link checker read file content via GitHub connector at a fixed SHA and compared relative `[label](path)` destinations to blobs/directories in the recursive tree, resolving `..`, `.` and stripping `#fragment`. This is **not** a full CommonMark parser: reference-style links, escaped paths, code-span false positives (e.g. the literal `[text](relative-url)` in [consistency-evidence.md](consistency-evidence.md)), and external endpoints require separate checking. In particular, a code literal is *not* a broken document link.

These statements are fixed to the revisions above. The newest run result and file changes must be added separately rather than changing previously observed data.

## Final-Head Verification

**Status: pending latest-head confirmation at document creation time.** Obtain latest PR head and current `PR Gate` after all report writes; record both in [handoff.md](handoff.md). If any further commit changes the head, check the workflow for that new head before claiming passing validation for the updated PR.
