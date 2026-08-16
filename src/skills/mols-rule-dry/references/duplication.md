# Duplicate Rules

Use this reference only when deciding whether repeated rule statements express the same requirement and what kind of repetition they create.

## Rule Unit

Compare the smallest requirement that can stand on its own without changing meaning. If one paragraph, bullet, or block contains multiple independent requirements, separate only the parts needed to resolve duplication; do not move or delete the whole block by association.

## Same Requirement

Treat statements as the same underlying rule requirement only when their operational requirement and exception or override intent are equivalent.

Similar wording is only a clue. Different wording may express the same requirement, and similar wording may express different policy.

Do not make target scope part of semantic identity. Use the resolved target sets to classify how the same requirement is repeated.

## Repetition Types

For statements with the same requirement:

- Same target set -> duplicate occurrence.
- Narrower target set fully covered by a broader unchanged rule -> inherited restatement.
- Different or disjoint target sets -> repeated rule across scopes; a consolidation candidate, not automatically redundant.
- Narrower statement changes, limits, or overrides the broader requirement -> genuine exception, not duplication.

Repeated rules across scopes may be consolidated only when the combined intended scope can be represented exactly and source authority remains valid.

## Ambiguity

If requirement equivalence or exception intent is unclear, preserve the existing statements and report unresolved duplication. Do not infer policy merely to remove repetition.
