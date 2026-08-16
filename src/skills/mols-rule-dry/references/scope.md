# Rule Scope

Use this reference only when deciding which targets currently receive a rule, which targets should receive it, and how repeated scopes relate.

## Current Scope

Derive the targets that each existing rule occurrence actually reaches from the runtime's directory and selector behavior. Record current scope before moving anything.

Do not treat current scope as intended scope merely because the rule is already there.

## Intended Scope

Determine the targets that should receive the rule from project authority, rule meaning, surrounding structure, and other concrete evidence. Classify the intended set as one of:

- project-wide;
- one contiguous directory subtree;
- a cross-cutting file, extension, path, or repeated-directory pattern; or
- a combined scope that may require more than one selector or owner.

If intended scope is ambiguous, preserve the current placements and report the ambiguity.

## Scope Relations

Compare current and repeated target sets using these relations:

- Equal: both reach the same targets.
- Containment: one target set is entirely inside another.
- Partial overlap: only some targets are shared.
- Disjoint: no targets are shared.

Overlap does not by itself prove duplication. Requirement equivalence is decided separately.

## Representability

Determine whether the runtime can express the intended target set exactly with one supported scope mechanism. If not, record the smallest exact combination that can represent it.

Do not choose the canonical source or owner file in this reference.

## Verification Boundaries

Check intended targets and nearby non-targets around directory and pattern boundaries. When the complete affected set can be enumerated, verify it completely; otherwise report the scope check as sampled.
