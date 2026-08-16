# Duplication

Use this reference only when deciding whether repeated natural-language asset content is actually redundant.

## Compare the Smallest Unit

Compare the smallest requirement, responsibility, procedure, or context block that can stand on its own without changing meaning. Do not move or delete an entire paragraph, section, or asset because only part of it is duplicated.

## Semantic Identity

Textual similarity is only a discovery signal. Treat two units as the same only when their operational meaning and relevant specialization or exception intent are equivalent.

Use the asset-type reference to determine which behavioral dimensions matter. The same text may mean different things when activation, scope, tools, permissions, output contracts, dependencies, or lifecycle differ.

## Repetition Types

Classify repeated content before removing it:

- **Duplicate occurrence**: the same unit is repeated with no behavioral distinction.
- **Inherited or referenced restatement**: a broader or canonical source already supplies the same unit unchanged.
- **Shared responsibility**: multiple assets own the same responsibility and may be consolidation candidates.
- **Specialization or exception**: a narrower asset intentionally changes or extends the common behavior.
- **Required physical copy**: delivery or runtime requires repeated text but authority remains elsewhere.

Only the first three are DRY candidates, and shared responsibility still requires compatible asset boundaries before consolidation.

## Cross-Type Repetition

Repetition across skill, rule, prompt, and agent assets is not redundant by default. A cross-type restatement may be removed only when an existing canonical source is guaranteed to apply in every context that needs the content and authority remains the same.

Moving content to a different asset type changes activation semantics and is a separate design change unless explicitly requested.

## Ambiguity

If semantic equivalence, specialization intent, or canonical availability is unclear, preserve the current content and report unresolved duplication.
