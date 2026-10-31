---
description: review-changes Skill의 계약·수용 사례·회귀 기준을 유지보수할 때 사용합니다.
---

# Review Changes — Maintenance Specification

> Status: Draft v0.1. Defines behavior and regression criteria for the standalone `review-changes` Skill.

## Responsibility

Input: explicit Git range, commit, path set, or implicit staged/unstaged working-tree edits. Output: evidence-backed Markdown review of **defects introduced by those changes**. The report is not a general repository audit, dependency advisory scan, style formatter or automatic patch generator.

## Source ownership

- [`SKILL.md`](../../../src/rulesync/.rulesync/skills/review-changes/SKILL.md): agent behavior and finding-quality contract (canonical).
- [`templates/review.md`](../../../src/rulesync/.rulesync/skills/review-changes/templates/review.md): report layout and HTML rendering conventions.
- `spec.md`: acceptance criteria, test scenarios and evolution guidance.

## Required behavior

1. Preserve the user's comparison boundary; do not infer PR base silently.
2. Default to both staged and unstaged diffs when local worktree access is available; distinguish each, and identify uncovered untracked/binary files. If only remote API evidence is available, describe that narrower scope.
3. Ground each actionable finding in a changed behavior, reachable trigger and observable impact, with verified line references.
4. Classify finding evidence (`CONFIRMED`, `SUPPORTED`, `HYPOTHESIS`) separately from priority (`BLOCKER`, `HIGH`, `MEDIUM`, `LOW`). Unsupported hypotheses are follow-up questions, not firm defects.
5. Do not modify application files, Git index, dependencies or settings during review; report output only on request.
6. Keep essential results visible in Markdown; optional `<details>` carries specifics without script execution.
7. Identify partial coverage and unexecuted tests accurately. An empty finding list is not proof of correctness.

## Acceptance cases

| ID | Scenario | Pass condition |
|---|---|---|
| RC-01 | Staged + unstaged edits | Both scopes included and distinguished |
| RC-02 | Untracked file | Not silently marked reviewed |
| RC-03 | Confirmed regression | Trigger, impact, changed line and test/reproduction provided |
| RC-04 | Plausible bug with missing assumption | Explicitly bounded evidence and uncertainty |
| RC-05 | Pre-existing defect unrelated to diff | Not reported as newly introduced |
| RC-06 | No actionable finding | Honest empty result plus coverage limits |
| RC-07 | Truncated / binary diff | Missing coverage disclosed |
| RC-08 | Generated Markdown | Valid local links and script-free HTML details |
| RC-09 | GitHub API-only review | Explicit base/head and remote-only coverage disclosed |

## Regression procedure

Use a small repository fixture with one changed function introducing a boundary-case failure, one harmless formatting change, one untracked file and distinct staged/unstaged edits. Verify the finding ID, evidence status, severity, links, diff scope and no-write behavior. Avoid claiming the real coding agent was evaluated unless the fixture was actually run through the intended host.

## Compatibility

Preserve status meaning, stable `R#` identifiers, report portability and the explicit comparison boundary. Changes to evidence thresholds are breaking semantic changes; update the Skill, template and this specification together. Prefer stronger evidence and fewer false positives over additional output sections.
