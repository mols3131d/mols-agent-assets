# PR #253 — Durable Handoff

## Current Decision

**PR #253 is still open and unmerged.** 저장소 내 330개 Markdown 파일 및 652개 내부 상대 링크/앵커에 대한 **전수조사(Exhaustive Audit)**가 완료되어 [exhaustive-consistency-audit.md](exhaustive-consistency-audit.md)에 등록되었습니다. 로컬 트리 기준 결손 링크 0건(Pass), 스키마 100% 통과로 내부 정합성은 확인되었습니다. 다만, 최신 `origin/main`의 디렉터리 재배치(PR #264)로 인해 발생한 47개 링크 이동 반영 및 `inbox/README.md` H2 제목 정비가 병합 전 필수 선행 작업으로 남아 있습니다.

## Target and Recovery

- Repository: https://github.com/mols3131d/mols-agent-assets
- Pull request: https://github.com/mols3131d/mols-agent-assets/pull/253
- Base originally reviewed: `23d649b2eac6e9115ce0e97a823d59de4d37b3c5`
- Write branch: `mols/docs/document-consistency-audit`
- Last confirmed work-stage commit **before this handoff file is added**: `6e924097e884d5daea92d84742a7813a34a8bb36` (merged `origin/main` at `9c08b43`)
- Exhaustive audit artifact: [exhaustive-consistency-audit.md](exhaustive-consistency-audit.md)

**Never assume the last recorded SHA is still the active head.** Re-query the PR and latest Actions on resume.

## Artifacts by Work Unit

| Stage | Durable artifact | Essential content |
| --- | --- | --- |
| Goal, boundaries, continuation | [work-plan.md](work-plan.md) | Research → plan → repair → verification gates and no-merge boundary |
| Exhaustive Audit | [exhaustive-consistency-audit.md](exhaustive-consistency-audit.md) | 330개 MD 파일 전수조사, 6대 축 검증 결과 및 origin/main 분기 분석 |
| Review | [review.md](review.md) | Baseline diff, F1/F2 importance, required outcomes, gaps |
| Research | [consistency-evidence.md](consistency-evidence.md) | Scoped link check, route, command and retired-name relationships |
| Implementation | [remediation-log.md](remediation-log.md) | Exact commits and why one runbook heading changed |
| Validation | [validation.md](validation.md) | Verified revision-specific checks and explicit non-verified areas |
| Index | [README.md](README.md) | Original directory reports and fixes, with current workstream links |

## Applied Changes

1. The earlier 29-file PR diff resolved six heading policy groups across nine active Markdown files and annotated two historical planning documents. Those commits precede the present review.
2. Commit `e5006c6cfbdb444c51b1b45523b7e4eb6f1d4afc` corrected the runbook H1 to `Maximum Removal of Non-Rotatable Sensitive Data Exposed on GitHub`, preserving the narrow meaning lost in the prior change.
3. Added review, relation evidence, decision ledger and validation documents to make the work independently resumable.
4. Verified the actual `80d4c8e16ea05c21229c1200cda6787a46f4069a` Git tree has **440 blobs / 325 Markdown files**; the initial PR head before the work plan had **439 / 324**. Corrected evidence to match the specific pinned revision.

## Open Work / No-Completion Claims

- **F1 remains bounded:** verified local targets in 93 `docs/` / `catalog/` Markdown, retired references in 27 active maintainer Markdown, and sampled command-to-config relationships. A full semantic consistency audit across all paths and external dependencies has not been performed.
- **External anchors:** no proof that changes to GitHub heading fragment identifiers preserve outside consumers.
- **Validation after last commit:** check the latest PR Gate at exact latest SHA before final recommendation; old success cannot be carried over by assumption.
- **Review:** current records are self-review evidence; do not treat them as independent human approval or permission to merge.
- **Runtime checks:** no local formatter, provider Promptfoo eval or repository script execution has been conducted through the GitHub connector in this session.

## Resume Procedure

1. Read root [`CHATBOT.md`](../../CHATBOT.md), [`AGENTS.md`](../../AGENTS.md), [`.agents/route/ROUTE.md`](../../.agents/route/ROUTE.md) and use `github-context` plus task-relevant documentation/review guidance.
2. Query PR #253 live: `head_sha`, `base_sha`, state, mergeability, changed filenames, reviews and checks.
3. Read this handoff, [work-plan.md](work-plan.md), [review.md](review.md), [consistency-evidence.md](consistency-evidence.md), [remediation-log.md](remediation-log.md), and [validation.md](validation.md) at that exact head. If files disagree, privilege live diff/evidence over a stale narrative and record the reconciliation.
4. For additional review: follow concrete canonical links into source, config and tests; classify new findings with checked counterexamples. Repair only verified defects in the same branch and update the affected artifact rather than erasing the original finding.
5. Confirm relative link targets and run status again after all writes. Update the PR description `revision.head` to current exact SHA, citing current PR Gate outcome and explicitly preserving non-verified scope.
6. Stop before merge unless the user explicitly grants merge authority; CI/PR readiness and merge approval are separate decisions.

## Boundary of This Handoff

This document is durable progress state, **not** a promise of automatic background execution or a claim that future checks have run. The latest valid CI evidence must be retrieved after the last Git commit.
