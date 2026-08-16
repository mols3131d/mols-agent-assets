# Duplication

Use this reference when repeated natural-language asset content must be classified or a consolidation decision is not obvious.

## Compare the Smallest Unit

Compare the smallest requirement, responsibility, procedure, or context block that can stand on its own without changing meaning. Do not move or delete an entire paragraph, section, or asset because only part of it is repeated.

## Semantic Identity

Textual similarity is only a discovery signal. First decide whether two units express the same underlying requirement, responsibility, procedure, or context. Compare operational meaning and specialization or exception intent.

Do not make activation, scope, tools, permissions, or lifecycle part of semantic identity unless they are themselves part of what the unit means. Those dimensions usually decide whether consolidation is safe, not whether the repeated content is conceptually the same.

## Repetition Types

For semantically identical or shared content, classify the relationship:

- **Duplicate occurrence**: the same unit appears more than once with no distinct behavior.
- **Inherited or referenced restatement**: a broader or canonical source already supplies the unit unchanged.
- **Shared responsibility**: multiple assets independently own the same responsibility or procedure.
- **Specialization or exception**: one occurrence intentionally changes or extends the shared content.
- **Required physical copy**: delivery or runtime requires repeated text while authority remains elsewhere.

The first three are DRY candidates. Specializations and required physical copies are normally preserved.

## Consolidation Compatibility

Use the matching asset-type reference to decide whether a DRY candidate can actually share one owner. Preserve separate occurrences when consolidation would change discoverability, activation, scope, authority, tools or permissions, outputs, dependencies, context isolation, precedence, or lifecycle.

A shared responsibility is not automatically a duplicate asset. Consolidate only when the relevant asset boundaries are compatible.

## Cross-Type Repetition

Repetition across skill, rule, prompt, and agent assets is not redundant by default. A cross-type restatement may be removed only when an existing canonical source is guaranteed to apply in every context that needs the content and authority remains the same.

Moving content to a different asset type changes activation semantics and is a separate design change unless explicitly requested.

## Ambiguity

If semantic identity, specialization intent, consolidation compatibility, or canonical availability is unclear, preserve the current content and report unresolved duplication.
