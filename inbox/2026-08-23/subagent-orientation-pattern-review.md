# Subagent Orientation Pattern Review

Based on:

- `subagent-orientation-pattern-research.md`
- `subagent-orientation-pattern-plan.md`

## Loop 1

### Loop 1 Findings

| Finding | Disposition |
| --- | --- |
| Responsibility orientation and context isolation were blended into one implied axis | Fixed: separate `Role-oriented ↔ Capability-oriented` from `Shared ↔ Isolated` |
| Capability-oriented was too close to being defined by isolation | Fixed: isolation is now a frequent fit and design reason, not the definition |
| Skill and Subagent could read as competing asset categories | Fixed: describe Skills as reusable capability packages and Subagents as possible delegated execution/context/tool/permission/specialist boundaries; allow composition |
| `vendor-neutral` wording could imply a portable common Subagent schema | Fixed: only the architectural idea of isolated delegated execution + bounded handoff is treated as vendor-neutral; runtime semantics remain external authority |
| GitHub Copilot `context: fork` risked becoming part of the core | Fixed: keep it only as a current implementation example linked to upstream documentation |

## Loop 2

### Loop 2 Findings

| Finding | Disposition |
| --- | --- |
| The dimension table and ASCII continuum diagrams repeated the same structure | Fixed: retain the compact table and remove redundant ASCII diagrams |
| Agent Skills portability was asserted locally without routing to its standard authority | Fixed: link Agent Skills directly and keep only the comparison needed for this pattern |
| The execution axis could look like a required binary runtime feature | Fixed: clarify that the ends are conceptual directions and runtimes may implement intermediate forms |

## Loop 3

### Loop 3 Findings

| Finding | Disposition |
| --- | --- |
| The execution-boundary choices linked separate context/tool/permission/handoff needs specifically to a `Capability-oriented Subagent`, partially recombining the two dimensions | Fixed: choose a `Subagent boundary` for those execution needs, then determine Role/Capability orientation independently from responsibility |

## Loop 4

### Loop 4 Review

No additional material pattern-design finding remains.

The whole capsule was re-reviewed for:

- taxonomy leakage between the two dimensions;
- overclaiming about Skill/Subagent portability;
- treating context isolation as exclusive to or guaranteed by Subagents;
- vendor-specific behavior becoming pattern core;
- handoff returning so much intermediate context that isolation is defeated;
- unnecessary structure or duplicated policy.

Current VS Code documentation was rechecked and still describes experimental `context: fork` as running a Skill in a dedicated subagent context with only the final result returned to the parent. The pattern keeps this as an implementation example rather than an invariant.

## Pattern Check

- Self-contained capsule: yes.
- Reusable rather than project-local policy: yes.
- Core vs implementation example separated: yes.
- No mandatory taxonomy or schema introduced: yes.
- Responsibility orientation and execution context remain independent: yes.
- Skills and Subagents remain composable rather than falsely exclusive: yes.
- Vendor detail routed to upstream authority: yes.
- KISS/DRY: two dimensions, three heuristics, one vendor example; no new bundle or supporting schema.

## Evidence Boundary

- Repository pattern and Agent Asset design principles were used as local design authority.
- Current Agent Skills and VS Code documentation were checked for portability and `context: fork` semantics.
- Runtime-specific Subagent behavior was not generalized beyond the architectural pattern.

## Validation

- An earlier PR Gate found Markdown normalization only: ordered-list style and duplicate heading anchor.
- Those formatting issues were corrected without changing the pattern design.
- PR Gate #901 passed on the prior head.
- During the new improve/review cycle, `main` advanced to `d6208679c3ef9a61d434e6039dfbb83472dce037`; final merge-result validation against current `main` is still required.

## Status

`in_progress` until the current head passes merge-result validation against the latest `main`. If validation introduces no material finding, stop recursion on saturation.
