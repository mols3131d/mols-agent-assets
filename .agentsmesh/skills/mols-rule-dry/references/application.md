# Rule Application

Use this reference only when deciding when a rule currently applies, when it should apply, and how repeated application conditions relate.

## Current Application

Derive how each existing rule occurrence is currently attached from the runtime's supported rule model and project configuration. Relevant mechanisms may include project-wide loading, directory inheritance, path or glob selectors, relevance-based selection, explicit invocation, or another native rule mode.

Do not treat current placement or metadata as proof of intended application.

## Intended Application

Determine when the rule should be available or applied from project authority, rule meaning, surrounding structure, and other concrete evidence. Describe the intended application independently of the current file location.

Use the runtime's native concepts rather than forcing every rule into a directory or glob model. If intended application is ambiguous, preserve the current state and report the ambiguity.

## Relations

For declarative target sets, compare them as:

- Equal: both reach the same targets.
- Containment: one target set is entirely inside another.
- Partial overlap: only some targets are shared.
- Disjoint: no targets are shared.

For manually invoked rules, compare their explicit invocation contract. For relevance-based or agent-requested rules, compare the declared selection signals but do not pretend their runtime-selected target set is statically enumerable.

Overlap or similar attachment conditions do not by themselves prove duplication. Requirement equivalence is decided separately.

## Representability

Determine whether the runtime can express the intended application exactly with one supported rule mechanism. If not, record the smallest correct combination of native application mechanisms. Leave owner and file selection to placement.

Do not choose the canonical source or attachment-mode migration in this reference.

## Verification Boundaries

Verify declarative scopes, explicit invocation contracts, and metadata completely when the relevant set can be enumerated. For relevance-based or agent-requested attachment, static inspection can verify only the declared selection contract; actual runtime selection remains unverified unless an evaluation system is available.
