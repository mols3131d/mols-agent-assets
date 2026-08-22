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

No additional material pattern-design finding remains after Loop 2.

## Pattern Check

- Self-contained capsule: yes.
- Reusable rather than project-local policy: yes.
- Core vs implementation example separated: yes.
- No mandatory taxonomy or schema introduced: yes.
- Vendor detail routed to upstream authority: yes.
- KISS/DRY: two dimensions, three heuristics, one example; no new bundle or supporting schema.

## Evidence Boundary

- Repository pattern and Agent Asset design principles were used as local design authority.
- Current Agent Skills and VS Code documentation were checked for portability and `context: fork` semantics.
- Runtime-specific Subagent behavior was not generalized beyond the architectural pattern.

## Validation

- Initial PR Gate found Markdown normalization only: ordered-list style and duplicate heading anchor.
- Those formatting issues were corrected without changing the pattern design.
- Merge-result PR Gate #900 passed deterministic tests and changed Markdown normalization.

## Status

`completed`. Two substantive design loops converged and validation introduced no new material pattern finding, so recursion stops on saturation.
