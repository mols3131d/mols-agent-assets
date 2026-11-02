# PR #253 — Consistency Evidence

## Revision and Method

- Target repository: `mols3131d/mols-agent-assets`; write target: `mols/docs/document-consistency-audit`
- Audited tree: `80d4c8e16ea05c21229c1200cda6787a46f4069a` (review snapshot following [work plan](work-plan.md)).
- Follow-up runbook correction: `e5006c6cfbdb444c51b1b45523b7e4eb6f1d4afc`.
- The PR original comparison base is `23d649b2eac6e9115ce0e97a823d59de4d37b3c5`, not the moving `main`.
- Git tree reports **440 blobs, 325 Markdown files** at the inspected snapshot. GitHub reads and computed filename relationships are evidence for the paths inspected, not a full runtime evaluation.

## Relation A — Markdown Links to Current File Tree

**Rule:** [Documentation Principles](../../docs/documentation/principles.md) requires discoverable/current documentation. A relative Markdown link should resolve against its containing file at the audited revision.

- **전수조사 완료**: [전체 문서 정합성 전수조사 보고서](exhaustive-consistency-audit.md)를 통해 저장소 내 추적 대상 **330개 Markdown 파일** 전체와 **652개 내부 상대 링크 및 앵커**를 전수 파싱하여 대상 파일 및 앵커 슬러그를 검증했습니다.
- Procedure: 모든 인라인 링크, 참조 링크, 이미지 링크 대상을 추출하고 `#fragment` 앵커 슬러그와 실제 파일/헤딩을 대조.
- Result: **0건 결손 (0 missing local link targets or broken anchors across all 330 tracked Markdown files).**
- Limits: 외부 HTTP 링크 유효성 및 외부 소비자의 헤딩 프래그먼트 의존성은 별도 미검증으로 유지. 최신 `origin/main`의 경로 이동(PR #264)으로 인한 47개 링크 갱신 필요.

## Relation B — Documented Entrypoints to Source

- [Repository README](../../README.md) routes readers to `docs/using-this-repository.md`, `catalog/`, `docs/references/`, `route/`, `.agents/route/` and `inbox/`. These targets existed in the audited Git tree.
- [Repository-local route](../../.agents/route/ROUTE.md) separates management-asset discovery from published [`route/`](../../route/README.md). Both entrypoints and the referenced indexes exist.
- [Asset Maintainer Documentation](../../docs/documentation/asset-maintainer-documentation.md) allows `docs/skills/<asset-or-family>/` to represent a family, not necessarily a standalone Skill. Therefore absence of a Skill sharing the family directory name is insufficient orphan evidence.
- Result: in these direct links, no confirmed missing target or false owner assertion. Generator completeness is not established.

## Relation C — Commands to Tooling Configuration

- [Validation](../../docs/development/validation.md) says `npm run rulesync:validate`; [`package.json`](../../package.json) declares `rulesync:validate` and its `rulesync_validate.py` entrypoint.
- [Evaluation](../../docs/development/evaluation.md) and [Evals README](../../evals/README.md) point to the Mols Loops eval surface. [`mise.toml`](../../mise.toml) declares `eval-mols-loops-smoke` and `eval-mols-loops`; [`package.json`](../../package.json) declares matching `eval:promptfoo:mols-loops*` scripts.
- [Validation](../../docs/development/validation.md) says `mise run generated-sync`; `mise.toml` includes `generated-sync`.
- Result: **sampled command names and entrypoint wiring agree** with checked configuration. No subprocess was executed by this read-only cross-check, so execution behavior and provider availability remain unverified.

## Relation D — Removed and Renamed Asset References

- [Mols Loops maintainer entrypoint](../../docs/skills/mols-loops/README.md) states `mols-rpi` was renamed to `mols-loops` with no compatibility alias. That makes its historical mentions legitimate but not current callable IDs.
- [DualVantage maintainer entrypoint](../../docs/subagents/mols-review-dualvantage/README.md) and [maintenance](../../docs/subagents/mols-review-dualvantage/maintenance.md) describe the actual family and legacy `review-lead`, `review-quality`, `review-adversarial` consumers as migration context.
- All **27** Markdown files under `docs/skills/` and `docs/subagents/` were scanned for the known retired names `mols-rpi`, `mols-markdown-for-human`, `mols-agent-asset-validator`, and legacy review Subagents. Found current maintainer references only in the above migration/compatibility descriptions, not new callable instructions for removed Skills.
- [Retired asset audit](retired-assets.md) documents the source and history scope. Two historical notes are annotated, without rewriting historical account: [Documentation research](../2026-08-31/documentation-principles-research-plan.md) and [Frontmatter audit](../2026-08-22/docs-frontmatter-audit.md).
- Limits: 27 active maintainer Markdown files is **not** every historical `inbox/` file; broad code-search zero results must not be interpreted as exhaustive absence.

## Relation E — Language Policy to Human-Readable Headings

- [Language policy](../../docs/language.md) requires English Markdown H1–H3 for ordinary docs, with exceptions for repository-management Agent Asset materials, exact/literal values, and preserved text.
- Existing PR edits changed headings in nine active document files, including the runbook. The [PR review](review.md) found the initial runbook H1 had narrowed the explicit meaning: missing non-rotatable and maximum-removal qualifiers. The H1 was corrected to `Maximum Removal of Non-Rotatable Sensitive Data Exposed on GitHub`; the frontmatter, commands and body were left untouched.
- Remaining heading/anchor invariants are subject to [validation](validation.md). The meaning of older external fragment links cannot be established by the repository itself.

## Open Evidence Boundaries

- Historic `inbox/` is durable provenance. A document describing a deleted Skill at its creation date is not automatically wrong; active current-operation instructions should be prioritized for remediation.
- The source tree and Markdown link parser do not show runtime compatibility, provider behavior, external HTTP status, CI enforcement, or subtle semantic drift.
- The initial audit reports were **sampled directories**, not an exhaustive inventory of all 324 Markdown files. Do not claim total consistency of the repository.

## Verification Reproduction

1. Fetch the exact PR head SHA and recursive tree from GitHub; do not silently substitute `main`.
2. Read [work plan](work-plan.md), [review](review.md), this relation matrix, and [remediation log](remediation-log.md).
3. Re-run path existence, reference check, and heading policy checks on files changed after the pinned snapshot.
4. Compare latest SHA with [validation](validation.md) and CI workflow execution. Update [handoff](handoff.md) with any remaining gaps.
