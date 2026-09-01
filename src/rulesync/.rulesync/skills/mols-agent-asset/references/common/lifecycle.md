# Common Lifecycle

Use this reference for the workflow shared by Skill, Rule, and subagent work. Type modules own type-specific design, review axes, and validation claims.

## Resolve

Before material design or change, resolve only what can affect the result:

1. responsibility and intended activation or application;
1. current owner, or whether the responsibility is genuinely new;
1. asset type;
1. canonical source or framework;
1. target runtime or deployment surface when target behavior matters;
1. applicable project authority and write boundary.

For new or materially changed behavior, check the abstraction against at least one concrete intended use. When selection or scope can be confused with a nearby case, also identify a representative non-use or near-miss. Do not turn this into a formal eval suite unless the task requires one.

If the owner or asset type is still ambiguous after relevant authority and nearby assets are read, preserve the ambiguity rather than creating a competing owner by guesswork.

## Calibrate

Use the least restrictive mechanism that is still reliable enough for the failure cost.

- Prefer outcome, constraints, and heuristics when multiple approaches are valid.
- Add stronger structure when a preferred pattern materially improves consistency.
- Use deterministic mechanics or narrowly specified sequences when ordering, reproducibility, or failure cost makes free-form judgment unsafe.
- Do not restate general model knowledge unless the task repeatedly fails without it.
- Do not add an abstraction layer only to make unlike assets look structurally uniform.

## Change

For creation, modification, simplification, refactoring, and adaptation:

1. Read the candidate owner and only the nearby authority or context that can change the decision.
1. State what should change and what must remain true: responsibility, activation or application, authority, safety, required capabilities, and applicable target compatibility.
1. Make the smallest coherent change. Prefer deletion, simplification, clearer ownership, or project-native mechanisms over another abstraction layer.
1. Add files only when they provide a concrete loading, ownership, runtime, or deterministic-mechanics benefit.
1. Re-read the result against the request, preserved invariants, source/target boundary, and affected links or paths.

## Review

Review is semantic judgment about whether the asset design and change are appropriate. Apply the relevant type module's review axes and the following common questions:

- Does one clear owner hold the responsibility?
- Does the asset apply where intended without claiming broader authority?
- Is source versus target authority preserved?
- Are instructions, resources, and indirection proportional to the problem?
- Did the change preserve valid existing behavior and explicit local deltas?
- Is any required context duplicated, stale, unreachable, or always loaded without benefit?
- Does the asset expose a failure or uncertainty instead of silently inventing compatibility?

A review finding should identify a concrete defect, ambiguity, unnecessary cost, or unsupported claim. Do not manufacture findings to satisfy a review format.

## Validate

Validation answers a specific claim with the cheapest sufficient evidence. Escalate only when the claim requires it.

1. **Inspection** — ownership, wording, links, scope, structure, and obvious semantic consistency.
1. **Deterministic project checks** — machine-checkable contracts already owned by the project or source framework.
1. **Projection or integration evidence** — generated target shape or integration behavior when that claim matters.
1. **Runtime or evaluation evidence** — actual selection, behavior, delegation, repeated trials, or compatibility when static evidence cannot establish the claim.

Do not create a parallel validator when an existing project or source-framework check owns the contract. Passing structural validation does not prove semantic quality or runtime behavior.

Record important checks that did not run as not run or unknown. Never convert simulation or inspection into a claim of actual runtime verification.

## Improve

When the task requests improvement, use review and validation findings to make bounded corrections:

1. rank findings by impact on the requested behavior or maintenance boundary;
1. correct the smallest owner that can remove the root cause;
1. re-review affected semantics;
1. re-run only checks whose claims may have changed;
1. stop when remaining findings are outside scope, evidence-blocked, or not worth additional complexity.

Do not use repeated rewriting as evidence of improvement. Improvement requires a clearer contract, removed defect, reduced unnecessary cost, or stronger evidence for a material claim.

## Formal Validation Boundary

Routine type-aware review and proportionate validation belong to this lifecycle. Use `mols-agent-asset-validator` when the primary task requires formal audit, readiness verdicts, systematic adversarial challenge, repeated behavioral trials, runtime/trace evidence, regression programs, independent reviewers, or validation-driven correction under those methods.
