# Rule Lifecycle

Use this reference for Rules, scoped instructions, inherited policy, selectors, precedence, projections, deduplication, review, validation, and bounded improvement.

## Principle

Make Rule structure simpler only after preserving intended application and source authority.

**Physical repetition is not automatically duplicate authority.** The same requirement may need more than one physical representation because scopes, selectors, attachment modes, precedence, inheritance, or target projection differ.

## Design

Resolve repeated or overlapping guidance in this order:

1. **Application** — where does each candidate currently and intentionally apply?
1. **Requirement** — are the candidates semantically the same requirement, or are they exceptions or scope-specific variants?
1. **Authority** — which editable source owns the requirement? Is another copy inherited, generated, projected, or merely a peer duplicate?
1. **Placement** — which supported Rule container, scope, selector, or attachment preserves the intended application and precedence with the least context?

Do not move or deduplicate text before these four questions are sufficiently resolved.

### Fast path

Deduplicate directly when all of the following are clear:

- the requirement is equivalent;
- intended application is equivalent;
- the copies are editable peers under the same authority;
- no selector, precedence, attachment, inheritance, or projection difference requires physical repetition.

Otherwise preserve the candidate until its application and authority are known.

### Ownership and projection

- Keep one authoritative editable owner when the runtime can preserve application from that owner.
- Do not use precedence as a reason to maintain duplicate policy owners.
- Treat generated or projected copies as derived, not independent authority.
- Do not hand-edit derived copies merely to make files look physically DRY.
- If a canonical source change requires synchronization or projection outside the authorized scope, preserve the boundary and report the needed follow-up.
- Prefer the project's native Rule model over introducing a shared schema or indirection layer solely to reduce repetition.

### Scope and precision

Put a requirement at the broadest scope that is still correct, not at the broadest scope that is convenient.

- Preserve genuine exceptions and narrower overrides.
- Do not widen a Rule to eliminate duplication when that changes non-target behavior.
- Do not narrow a Rule if callers would need to rediscover the same requirement in multiple locations.
- Keep selectors and attachment conditions as simple as possible while preserving intended coverage.
- Do not assume one vendor's Rule paths, selectors, or precedence model applies to another runtime.

## Review

Review the axes that can change application or maintenance cost:

- **Application** — does the Rule reach every intended target and avoid unrelated targets?
- **Requirement** — is the policy meaning preserved, including exceptions and narrower variants?
- **Authority** — is there one editable owner for each semantic requirement where the runtime permits it?
- **Placement** — is the requirement attached at the correct scope with the least necessary context?
- **Selectors and precedence** — do selectors, inheritance, attachment, and precedence relationships preserve intended behavior?
- **Duplication** — are remaining copies required by physical projection or scope, or are they competing semantic owners?
- **Projection** — are generated copies treated as derived and left unedited?
- **Portability** — have target-specific assumptions been isolated rather than generalized across runtimes?
- **Regression** — did the change alter nearby non-target coverage, exception behavior, or effective precedence?

Leave materially ambiguous candidates unchanged and expose the ambiguity instead of guessing.

## Validate

Use evidence that matches the claim:

- inspect source ownership, selectors, scope, inheritance, precedence, attachment, and projected copies directly;
- use repository or source-framework validation for machine-checkable Rule syntax and projection contracts;
- compare before and after target coverage when the change can widen or narrow application;
- inspect generated target representation only when projection correctness is part of the claim;
- require actual runtime or behavioral evidence before claiming relevance-based selection, effective precedence under dynamic host behavior, or target compatibility that static structure cannot prove.

A structurally valid Rule can still be semantically misplaced. Static inspection can verify declarative structure, not runtime relevance decisions that the host makes dynamically.
