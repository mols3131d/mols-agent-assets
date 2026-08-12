# Change Safety

Use this reference for behavior-preserving refactors, replacement, consolidation,
rename, deletion, or other broad changes.

## Preserve Deliberately

Before claiming preservation, capture the observable facts that must survive:

- activation conditions and meaningful exclusions;
- authority and capability fields;
- commands, paths, API names, versions, and numeric thresholds;
- required outputs, safety rules, stop conditions, and permissions;
- ordering where sequence changes behavior.

Literal invariant checks can protect fragile facts, but they do not prove full
semantic equivalence. Do not claim behavioral parity without runtime evidence.

## Consolidation Decisions

Lexical similarity is only a discovery signal.

| Decision | Use when |
| --- | --- |
| `Merge` | Purpose, authority, owner, runtime, and release lifecycle are compatible |
| `Compose` | Related assets should remain independently invocable |
| `Route` | One shallow entrypoint should select bounded specialists |
| `Keep separate` | Permission, ownership, safety, runtime, or release lifecycle differs |
| `Deprecate` | Another accepted asset covers the complete responsibility |

Compare responsibility, activation, outputs, tools, authority, safety, owner, and
runtime before choosing. Map every retired responsibility to its destination or
an explicit retirement rationale. Do not merge only to reduce file count.

## Recovery

Before destructive, broad rename, replacement, consolidation, or deletion work:

- prefer an existing Git commit or dedicated branch as the rollback point;
- do not overwrite unrelated work;
- outside Git, snapshot only the approved target set with a cleanup condition;
- never package backup copies with runtime assets.

## Mutation Rule

Apply one coherent change batch inside the approved boundary, then verify the
stated preservation requirements and affected deterministic checks. Correct
concrete failures; do not repeat ceremonial loops.
