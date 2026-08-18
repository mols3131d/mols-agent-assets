# Duplicate Rules

Use this reference only when deciding whether repeated rule statements express the same requirement and what kind of repetition they create.

## Rule Unit

Compare the smallest requirement that can stand on its own without changing meaning. If one paragraph, bullet, or block contains multiple independent requirements, separate only the parts needed to resolve duplication; do not move or delete the whole block by association.

## Same Requirement

Treat statements as the same underlying rule requirement only when their operational requirement and exception or override intent are equivalent.

Similar wording is only a clue. Different wording may express the same requirement, and similar wording may express different policy.

Do not make scope, selector, or attachment mode part of semantic identity unless it is itself part of the requirement. Use the resolved application conditions to classify how the same requirement is repeated.

## Repetition Types

For statements with the same requirement:

- Same application condition -> duplicate occurrence.
- Narrower declarative scope already covered unchanged by a broader rule -> inherited or scoped restatement.
- Different scopes or attachment modes -> repeated rule across applications; a consolidation candidate, not automatically redundant.
- Narrower statement changes, limits, or overrides the broader requirement -> genuine exception, not duplication.

Repeated rules across applications may be consolidated only when the intended application remains exactly representable and precedence or attachment behavior does not change. Source authority and projection status are resolved separately in [ownership.md](ownership.md).

## Ambiguity

If requirement equivalence, exception intent, or application relationship is unclear, preserve the existing statements and report unresolved duplication. Do not infer policy merely to remove repetition.
