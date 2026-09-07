---
title: "Artifact Consistency Report — mols-agent-assets legacy cleanup"
description: "Consistency differences observed across current Agent Asset, route, self-consumer, and working-artifact surfaces."
created: "2026-09-07T22:11:16+09:00"
updated: "2026-09-07T22:11:16+09:00"
author: "<author>"
type: "artifact-consistency-report"
repository: "mols3131d/mols-agent-assets"
target: "legacy cleanup audit"
coverage: "partial"
snapshot: "74b56fa52a3e02a25f727a6841b4c4201d028eec"
---

# Artifact Consistency Report

## Summary

| Item | Value |
|---|---|
| Repository | `mols3131d/mols-agent-assets` |
| Target | `legacy cleanup audit` |
| Scope | canonical Rulesync Skills, distribution/local routes, root Rulesync self-consumer, selected migration PRs, and inbox lifecycle evidence |
| Snapshot | `74b56fa52a3e02a25f727a6841b4c4201d028eec` |
| Result | `findings` |
| Coverage | `partial` |
| Confirmed observations | `4` |
| Unresolved observations | `1` |
| Verification loops | `3/3` |

Two explicitly deferred predecessor migrations remain live, two current Skill boundaries reference owners that no longer exist as executable Skills, and several completed work bundles remain in the current inbox surface.

## Findings

### CON-001 — `coding-context` predecessor remains publicly discoverable beside its successor

- **Status:** `verified`
- **Type:** `drift`
- **Relation:** `coding-context` ↔ `mols-coding-context`

#### Observed difference

The old canonical `coding-context` package still exists while `mols-coding-context` is now the designated main/core. The migration plan explicitly states `coding-context → mols-coding-context` and says the old canonical directory and live references are to be removed after the deletion gate. PR #222 merged the successor while explicitly deferring removal and runtime routing/behavior evaluation to a follow-up migration. The current distribution route still exposes both identities.

#### References

- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/coding-context/SKILL.md` — old generic coding-context owner still exists.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-coding-context/SKILL.md` — successor identifies itself as the main coding-context Skill.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/inbox/2026-09-07/mols-coding-context/migration.md` — explicit replacement and deletion gate.
- `https://github.com/mols3131d/mols-agent-assets/pull/222` — successor introduction; old owner removal and runtime eval deferred.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/route/skills.jsonl` — both identities remain in public discovery.

#### Potential impact

Generic code-facing requests may have two competing discovery candidates for substantially overlapping engineering-judgment responsibility. Removal cannot be treated as fully validated until the migration's runtime gate is either executed or intentionally revised.

### CON-002 — `mols-markdown-for-human` predecessor remains active after `mols-documentation` successor merge

- **Status:** `verified`
- **Type:** `drift`
- **Relation:** `mols-markdown-for-human` ↔ `mols-documentation`

#### Observed difference

PR #218 explicitly introduced `mols-documentation` as the successor capability to `mols-markdown-for-human` and described that PR as a pre-migration step. It deferred root self-consumer migration, local family routing, and removal of the old Skill to a follow-up. Current main still keeps the old Skill canonical package, selects it in `rulesync.jsonc`, locks it in `rulesync.lock`, and lists it in the local Markdown family, while the cross-runtime distribution route exposes both old and new capabilities. The current Markdown Rule already points authoring work to `mols-documentation`, showing the repository is in a split migration state.

#### References

- `https://github.com/mols3131d/mols-agent-assets/pull/218` — explicitly defines `mols-documentation` as successor and defers old-Skill removal/self-consumer migration.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-markdown-for-human/SKILL.md` — predecessor still exists.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-documentation/SKILL.md` — successor exists and subsumes general human-readable document authoring/structure.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/rulesync.jsonc` — root self-consumer still selects the predecessor.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/.agents/route/families.json` — local Markdown family still names the predecessor.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/.rulesync/rules/markdown.md` — current Rule routes human-readable document authoring to the successor.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/route/skills.jsonl` — both identities remain publicly discoverable.

#### Potential impact

Document-authoring requests can encounter duplicate or overlapping candidates, while different repository routing surfaces disagree about which capability owns the work. Runtime behavioral evaluation was explicitly not verified in the successor PR.

### CON-003 — `mols-agent-asset-find` still hands formal quality work to removed validator identity

- **Status:** `verified`
- **Type:** `stale-reference`
- **Relation:** `mols-agent-asset-find` ↔ removed `mols-agent-asset-validator`

#### Observed difference

The current `mols-agent-asset-find` boundary says formal validation, readiness, adversarial evaluation, regression validation, and validation-driven correction belong to `mols-agent-asset-validator`. PR #215 merged those responsibilities into `mols-agent-asset` and removed the validator canonical package. Current CHATBOT routing, root self-consumer selection, and canonical Skill inventory also use `mols-agent-asset`, not the removed validator.

#### References

- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-agent-asset-find/SKILL.md` — live stale owner reference.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-agent-asset/SKILL.md` — current consolidated owner.
- `https://github.com/mols3131d/mols-agent-assets/pull/215` — validator absorption and canonical package removal.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/CHATBOT.md` — current repository routing points review/validation/evaluation to `mols-agent-asset`.

#### Potential impact

A caller following the loaded Skill boundary can be directed toward a capability identity that no longer exists, creating failed handoff or unnecessary rediscovery.

### CON-004 — Markdown maintenance names a non-executable Mermaid family as the semantics owner

- **Status:** `verified`
- **Type:** `stale-reference`
- **Relation:** `mols-markdown-maintenance` ↔ `mols-mermaid` family / executable Mermaid Skills

#### Observed difference

The current `mols-markdown-maintenance` boundary says Mermaid diagram/chart semantics belong to `mols-mermaid`. There is no canonical executable Skill named `mols-mermaid`; the runtime owners are `mols-mermaid-diagram` and `mols-mermaid-chart`. `docs/skills/mols-mermaid/README.md` is a maintainer family entrypoint, not a runtime Skill. Other current authoring surfaces route directly to the two executable owners.

#### References

- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-markdown-maintenance/SKILL.md` — current ambiguous owner reference.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/docs/skills/mols-mermaid/README.md` — `mols-mermaid` is a maintainer family owner.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-mermaid-diagram/SKILL.md` — executable diagram owner.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/src/rulesync/.rulesync/skills/mols-mermaid-chart/SKILL.md` — executable chart owner.

#### Potential impact

A runtime interpreting the boundary as a Skill handoff can search for a nonexistent Skill identity or blur the distinction between maintainer-family documentation and executable capability routing.

### CON-005 — completed work bundles remain in the current inbox surface

- **Status:** `unresolved`
- **Type:** `drift`
- **Relation:** current `inbox/YYYY-MM-DD/` ↔ canonical artifacts and Git/PR history

#### Observed difference

Repository documentation says working research/review/draft/handoff artifacts may remain in the inbox until their knowledge disposition is decided, while ordinary completed process and previous state should generally be represented by Git history/PRs; archival copies are justified when the original itself remains worth revisiting. Several current inbox bundles correspond to already-established canonical results, including the Promptfoo adoption work, the Subagent Orientation pattern research/plan/review, and the 2026-08-22 legacy-audit checkpoint. Whether each original has continuing standalone preservation value is not established by this audit.

#### References

- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/inbox/README.md` — current vs archived artifact placement.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/docs/documentation/README.md` — working-knowledge and Git-history lifecycle policy.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/inbox/2026-08-20/promptfoo-eval-adoption-plan.md` — completed adoption-era working artifact.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/docs/references/tooling/promptfoo.md` — current Promptfoo reference exists.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/inbox/2026-08-23/subagent-orientation-pattern-research.md` — working artifact targeting the pattern.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/catalog/patterns/context-engineering/subagent-orientation.md` — current canonical pattern exists.
- `https://github.com/mols3131d/mols-agent-assets/blob/74b56fa52a3e02a25f727a6841b4c4201d028eec/inbox/2026-08-22/agent-assets-modernization-legacy-audit.md` — completed legacy checkpoint that states it is not a permanent registry.

#### Why unresolved

Inbox policy intentionally allows working artifacts and selective archival preservation. Static repository evidence proves these clusters are no longer the current canonical implementation, but not whether their original research content is still valuable enough to archive rather than delete.

#### Potential impact

Keeping completed work artifacts indefinitely in the current inbox can blur active work versus historical evidence and increase search/context noise, but indiscriminate deletion could remove research that still has standalone value.

## Coverage

- **Checked:** current canonical Rulesync Skill inventory; root `CHATBOT.md` and route contract; distribution route; local route families/all/Markdown projections; root Rulesync self-consumer config and lock; explicit successor/migration PRs for coding context, documentation, and Agent Asset validator; targeted old-name searches; selected inbox lifecycle clusters.
- **Resolved rule sources:** root `CHATBOT.md` → `AGENTS.md` → `.agents/route/ROUTE.md`; task-relevant `github-context`, `mols-agent-asset`, `artifact-consistency-inspector`, and `mols-loops`.
- **Rule-source conflicts:** none observed for the audit method.
- **Excluded:** full semantic review of every historical inbox artifact; external consumer repositories that may still request old public names; live runtime/model selection trials; generated vendor projections not committed to the repository.
- **Limitations:** GitHub code search is default-branch indexed and cannot prove absence by itself; absence conclusions were only used as counterevidence together with current canonical inventory and migration history. Runtime selection/behavior gates for the two predecessor migrations remain unexecuted in the cited PR evidence.
- **Assessment boundary:** this report identifies current consistency and lifecycle cleanup candidates; it does not itself authorize deletion or claim runtime behavioral parity.
