# Rule Scope

Use this reference only when deciding which targets should receive a rule and whether multiple rule scopes overlap.

## Intended Scope

Describe the target set independently of where the rule is currently stored. Classify it as one of:

- project-wide;
- one contiguous directory subtree;
- a cross-cutting file, extension, path, or repeated-directory pattern; or
- a combined scope that may require more than one selector or owner.

Do not infer intended scope from the current file location alone.

## Overlap

Compare the actual target sets of repeated rules or selectors.

- Full overlap: both reach the same targets.
- Containment: one target set is entirely inside another.
- Partial overlap: only some targets are shared.
- Disjoint: no targets are shared.

Overlap does not by itself prove duplication. Rule equivalence is decided separately.

## Representability

Determine whether the runtime can express the intended target set exactly with one supported scope mechanism. If not, record the smallest exact combination that can represent it.

Do not choose the canonical source or owner file in this reference.

## Verification Boundaries

Check intended targets and nearby non-targets around directory and pattern boundaries. When the complete affected set can be enumerated, verify it completely; otherwise report the scope check as sampled.
