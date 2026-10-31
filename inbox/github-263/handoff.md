# PR #263 — check-dependencies integration record

## Scope

- PR: https://github.com/mols3131d/mols-agent-assets/pull/263
- Source: `src/rulesync/.rulesync/skills/check-dependencies/`
- Imported ZIP is the baseline; only narrowly justified integration and privacy changes are intended.
- Offline dependency inventory is default. Public registry and OSV requests still require explicit scope/privacy authorization.
- Supported: root npm lockfile / manifest and simple root Python requirements. No package modification or new package manager support.

## Changes made after import

- The Python requirements parser recognizes `--no-index` as a non-public source configuration and excludes pinned entries from *all* public lookup/OSV calls in `--online` mode.
- Added a regression test asserting no outbound calls under `--no-index`.
- Added a small root-pytest adapter at `tests/skills/check-dependencies/test_portable_suite.py` so GitHub PR Gate executes the bundled portable unit suite without modifying workflows.
- Regenerate `route/skills.jsonl` from canonical Skill frontmatter using the official generator semantics; do not maintain the entry by hand.
- Synchronize the work branch with the current `main` before final gate, because other Skill PRs changed the same generated route after this PR was created.

## Validation and boundaries

- Original ZIP: 9 bundled unit tests passed before this PR; subsequent test additions need current PR Gate evidence.
- Initial PR Gate failed because `distribution-routes` found stale `route/skills.jsonl`. This is a known integration blocker until regenerated and rechecked against the current merge candidate.
- Source frontmatter validation and 263 repository tests passed on the initial candidate. They do not prove later edits passed.
- External npm/PyPI/OSV integration and independent agent behavior eval were not executed. No public requests were authorized for this task.
- `UNKNOWN` origin entries may still represent private packages, including when package-manager configuration lives outside supported files. The Skill requires manual privacy review before any online run.

## Merge acceptance

1. Latest `main` integrated without discarding unrelated changes.
2. PR Gate including generated route drift and the bundled regression suite succeeds.
3. PR is non-Draft, review finds no material blocker, and GitHub permits merge.
4. Record final PR/merge result on GitHub. No extra package formats, installer, or CI workflow.
