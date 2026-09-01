# Common Review

Use this reference for semantic review shared by Skill, Rule, and subagent work. Apply the relevant type-specific review reference for asset-specific failure modes.

## Review questions

Inspect only axes that can materially affect the requested behavior or maintenance boundary.

- **Ownership** — does one clear owner hold the responsibility?
- **Scope** — does the asset apply where intended without claiming broader authority?
- **Authority** — are canonical source, target-runtime behavior, project deltas, and asset-local requirements kept distinct?
- **Complexity** — are instructions, resources, indirection, and deterministic mechanics proportional to the problem?
- **Regression** — did the change preserve valid existing behavior and intentional local deltas?
- **Context cost** — is required context duplicated, stale, unreachable, or always loaded without benefit?
- **Failure visibility** — does the asset expose uncertainty or unsupported compatibility instead of silently inventing success?

## Findings

A material finding should identify a concrete defect, ambiguity, unnecessary cost, unsupported claim, or regression risk.

- Prefer root causes over repeated symptoms.
- Distinguish defects introduced by the change from pre-existing issues outside the requested scope.
- Do not manufacture findings to satisfy a review format.
- Leave materially ambiguous behavior unresolved when available evidence cannot support a safe conclusion.

Static review can establish semantic and structural concerns, but it does not prove runtime selection, target behavior, delegation, parity, or compatibility.
