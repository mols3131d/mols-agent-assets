# Common Agent Asset Principles RPI Review

Based on:

- `common-agent-asset-principles-rpi-research.md`
- `common-agent-asset-principles-rpi-plan.md`

## Loop 1

### Loop 1 Findings

| Finding | Disposition |
| --- | --- |
| `design-principles.md` lacked an explicit mechanism-selection gate | Added: prefer an established native/deterministic owner when it directly owns the concern, while keeping semantic judgment in readable instruction |
| Local Delta was justified mainly by description rather than evidence/need | Strengthened YAGNI with current requirement, observed failure, accepted policy, or credible invariant |
| DRY could read as one universal authority rather than one owner per concern | Clarified concern-specific authority and composition/linking instead of duplicate semantic owners |
| Context cost was implicit | Added a Context Test as an application of KISS + Progressive Disclosure rather than a new named principle |
| Instruction conflict guidance could encourage invented precedence | Added scope/conflict rules: use runtime/authority precedence only when actually defined; otherwise remove or separate conflicts |
| Instruction force and fallback behavior were under-specified | Added true-invariant use of `must`/`never`/`only`, default + escape behavior, negative-boundary fallback, and observable stop/failure handling |
| Examples/templates could silently become hidden rules | Defined examples as subordinate calibration/clarification and templates as format contracts only when appropriate |

## Loop 2

### Loop 2 Findings

| Finding | Disposition |
| --- | --- |
| Mechanism-first wording could be read as preferring a target-native convenience even when it breaks canonical source authority or portability | Restricted the mechanism gate: the stronger mechanism must not create competing authority or break required portability |
| `Example` was called `evidence`, conflicting with this repository's evidence terminology | Reframed examples as expression/calibration tools, not evidence |
| “narrowest scope” could encourage file/directory fragmentation | Changed to scope no broader than intended applicability and explicitly preserved coherent instructions under one activation/owner |
| Mechanism examples were duplicated across both documents | Kept the detailed mechanism decision in Design Principles and reduced Instruction Authoring to a link-backed gate |

## Loop 3

### Loop 3 Findings

| Finding | Disposition |
| --- | --- |
| Local Delta still began with “local rule or reference,” narrowing a common Agent Asset principle | Changed to `Local Agent Asset content` |
| Multi-target authority explanation in the common design reference was too implementation-shaped | Compressed it to competing-authority / required-portability criteria |
| “same behavior once” could be misread as forbidding generated/target projections | Clarified that one semantic authoritative owner is required while generated/projection representations are not new semantic owners |

## Full Review

Checked the two documents together against:

- responsibility boundary between durable common design meaning and instruction expression;
- Standard First, YAGNI, SRP, DRY, KISS, Progressive Disclosure;
- Instruction Bottleneck, Context Noise Bottleneck, Stability, and Human Comprehension Debt;
- current Agent Skills, OpenAI, Anthropic, and GitHub official guidance;
- nearby `agent-assets` ownership and Skill-specific convention references.

No additional material design finding remains. The documents stay vendor-neutral at the normative layer; vendor-specific precedence, loading, path and representation semantics remain upstream-owned. Repository testing/eval workflow remains outside these references.

## Validation

- Latest `main` remained `143cae3483d5898feb87310d0ea0871db651c694` during merge-result validation.
- Initial PR Gate #928 passed 201 deterministic tests and failed only changed-Markdown normalization: missing EOF newlines in three RPI artifacts and duplicate `Findings` heading anchors in this review artifact.
- Those mechanical Markdown issues were corrected without changing the design.
- Merge-result PR Gate #933 passed deterministic tests and changed-Markdown normalization. Rulesync source, distribution routes, and Promptfoo were correctly out of change-impact scope.

## Status

`completed`. Three substantive design loops converged. Mechanical normalization and validation-record updates are not additional design loops. Validation introduced no new material finding, so recursion stops on saturation.
