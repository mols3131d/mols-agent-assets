# CI Design Principles

Design CI as an evidence system for repository admission, not a collection of workflows.

The doctrine is:

- keep admission to `main` strict;
- require only evidence that can change that admission decision;
- obtain required evidence with the smallest reliable scope and cost.

If the target uses another canonical integration branch, treat it as the equivalent admission boundary.

## Admission Boundary

A failure is merge-critical when knowing it would make the current change unacceptable on `main`.

Merge-critical failures require blocking pre-merge evidence. Do not move them post-merge merely because the check is expensive.

Conversely, do not block admission for evidence that would not change the merge decision. Pure style, formatting, exhaustive diagnostics, and maintenance are non-blocking by default unless representation itself affects parseability, correctness, compatibility, or an explicit repository contract.

Optimize verification execution, not the standard for admission.

## Evidence Tiers

Prefer the cheapest evidence that can prove the required claim.

1. **Static** — syntax, schema, frontmatter, references, placement, parseability, representation invariants.
1. **Deterministic** — scripts, generators, contract tests, regression invariants.
1. **Harness / projection** — target generation, adapter fidelity, package surface, isolated or round-trip validation.
1. **Semantic** — routing, instruction following, task behavior, adversarial cases.
1. **Live runtime** — real provider/tool invocation, integration behavior, latency/cost, runtime parity.

A lower tier does not prove a higher one. Do not buy higher-tier evidence when a cheaper tier proves the merge-critical claim.

## Selection Rules

Use these defaults unless target evidence requires otherwise:

- merge-critical before optional breadth;
- deterministic before probabilistic;
- affected before exhaustive;
- local/static before network/model calls;
- existing provider and checks before new machinery;
- no cache until repeated setup cost is material;
- no broad matrix unless each dimension protects a distinct admission risk;
- no model grader when deterministic assertions are sufficient.

Risk determines strictness. File type, workflow ceremony, or the mere existence of a tool does not.

## Change Impact

Use the smallest maintainable mapping that is sufficient:

1. provider path filters;
1. repository naming/layout conventions;
1. a small selector/router script;
1. an explicit dependency manifest only when simpler mechanisms cannot represent the relationships reliably.

Impact selection must fail safe. When the affected scope cannot be established with enough confidence, broaden validation or fail the selector rather than silently omitting relevant checks.

Avoid large unexplained path switches that become stale when assets move.

## Delegated Development

CI should support safe delegated development, including agent-authored changes, without requiring exhaustive verification for every change.

Within the delegated scope, a change must not become mergeable merely because its relevant verification was not selected. The admission design should make important coverage omissions visible or fail safe.

This is an automation threshold, not a claim that CI alone guarantees correctness. Human review, release controls, or runtime monitoring may still own risks outside the merge contract.

## Responsibility Boundaries

| Responsibility | Default role |
| --- | --- |
| PR / admission gate | blocking evidence for failures unacceptable on `main` |
| main / post-merge | non-admission diagnostics, broader confidence, or follow-up validation |
| scheduled / manual | expensive, exhaustive, provider-specific, or stochastic evidence not required for admission |
| maintenance | formatting, regeneration, synchronization, indexing, other writes |

Do not make maintenance a merge gate merely because it is automated. Do not classify a merge-critical failure as post-merge merely to keep PR CI fast.

## Semantic and Runtime Evidence

Use semantic/runtime evaluation only when an important merge-critical or explicitly requested claim cannot be reduced to cheaper assertions. Typical examples are routing precision, adversarial boundaries, model-dependent task success, and live harness/provider parity.

If such evidence is required for admission, keep it bounded but blocking. If it is useful only for broader confidence, move it to scheduled/manual or post-merge execution.

Keep fixture validation separate from eval execution. For stochastic results, define an appropriate threshold, baseline, sample policy, or non-blocking interpretation instead of treating one sample as deterministic.

## Safety and Performance

- Default merge gates to least privilege and read-only repository access where practical.
- Keep secrets away from untrusted PR execution unless the trust model explicitly permits them.
- Treat third-party actions, downloaded tools, model APIs, and generated commits as trust boundaries.
- Cancel superseded PR runs when supported and useful.
- Bound expensive jobs with timeouts and samples/retries.
- Prefer smaller selected work over broad always-on execution.

## Authority

CI validates repository authority; it does not silently redefine it.

Generated files, indexes, projections, eval results, formatting, and maintenance commits are derived unless the repository says otherwise. When generated content is intentionally semantically tuned, validate factual invariants rather than forcing byte identity unless byte identity is the actual contract.
