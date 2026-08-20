# Rule

Use this reference for Rules, scoped instructions, inherited policy, selectors,
precedence, projections, and rule deduplication.

## Principle

Make Rule structure simpler only after preserving intended application and source
authority.

**Physical repetition is not automatically duplicate authority.** The same
requirement may need more than one physical representation because scopes,
selectors, attachment modes, precedence, or target projection differ.

## Resolve

For repeated or overlapping Rule guidance, decide in this order:

1. **Application** — where does each candidate currently and intentionally apply?
2. **Requirement** — are the candidates semantically the same requirement, or are
   they exceptions or scope-specific variants?
3. **Authority** — which editable source owns the requirement? Is another copy
   inherited, generated, projected, or merely a peer duplicate?
4. **Placement** — which supported Rule container, scope, selector, or attachment
   preserves the intended application and precedence with the least context?

Do not move or deduplicate text before these four questions are sufficiently
resolved.

## Fast path

Deduplicate directly when all of the following are clear:

- the requirement is equivalent;
- intended application is equivalent;
- the copies are editable peers under the same authority;
- no selector, precedence, attachment, inheritance, or projection difference
  requires physical repetition.

Otherwise preserve the candidate until its application and authority are known.

## Ownership and projection

- Keep one authoritative editable owner when the runtime can preserve application
  from that owner.
- Do not use precedence as a reason to maintain duplicate policy owners.
- Treat generated or projected copies as derived, not independent authority.
- Do not hand-edit derived copies merely to make files look physically DRY.
- If a canonical source change requires synchronization or projection outside the
  authorized scope, preserve the boundary and report the needed follow-up.
- Prefer the project's native Rule model over introducing a shared schema or
  indirection layer solely to reduce repetition.

## Guardrails

- Preserve policy meaning while changing placement or duplication.
- Preserve genuine exceptions and narrower overrides.
- Do not assume one vendor's Rule paths, selectors, or precedence model applies to
  another runtime.
- Do not redesign runtime loading merely to achieve DRY.
- Leave materially ambiguous candidates unchanged and expose the ambiguity instead
  of guessing.

## Check

Compare before and after for:

- intended target coverage and nearby non-target coverage;
- source authority;
- selector, scope, attachment, inheritance, and precedence relationships;
- generated or projected copies;
- remaining duplicate owners.

Static inspection can verify declarative structure. Relevance-based or
agent-requested Rule selection remains unverified without actual runtime or
evaluation evidence.
