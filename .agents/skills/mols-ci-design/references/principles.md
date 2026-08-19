# CI Design Principles

Design CI as an evidence system, not a collection of workflows.

## Evidence Tiers

Prefer the cheapest evidence that can detect the failure.

1. **Static** — syntax, schema, frontmatter, references, placement, formatting.
1. **Deterministic** — scripts, generators, contract tests, regression invariants.
1. **Harness / projection** — target generation, adapter fidelity, package surface, isolated or round-trip validation.
1. **Semantic** — routing, instruction following, task behavior, adversarial cases.
1. **Live runtime** — real provider/tool invocation, integration behavior, latency/cost, runtime parity.

A lower tier does not prove a higher one.

## Selection Rules

Use these defaults unless target evidence requires otherwise:

- deterministic before probabilistic;
- affected before exhaustive;
- PR smoke before full matrix;
- local/static before network/model calls;
- existing provider and checks before new machinery;
- no cache until repeated setup cost is material;
- no model grader when deterministic assertions are sufficient.

## Change Impact

Use the smallest maintainable mapping that is sufficient:

1. provider path filters;
1. repository naming/layout conventions;
1. a small selector/router script;
1. an explicit dependency manifest only when simpler mechanisms cannot represent the relationships reliably.

Avoid large unexplained path switches that become stale when assets move.

## Responsibility Boundaries

| Responsibility | Default role |
| --- | --- |
| PR gate | read-only merge confidence |
| main/post-merge | broader deterministic or integration regression |
| scheduled/manual | expensive, exhaustive, provider-specific, or stochastic eval |
| maintenance | formatting, regeneration, synchronization, indexing, other writes |

Do not make maintenance a merge gate merely because it is automated.

## Semantic and Runtime Evidence

Use semantic/runtime evaluation only when an important contract cannot be reduced to deterministic assertions. Typical examples are routing precision, adversarial boundaries, model-dependent task success, and live harness/provider parity.

Keep fixture validation separate from eval execution. For stochastic results, define an appropriate threshold, baseline, sample policy, or non-blocking interpretation instead of treating one sample as deterministic.

## Safety and Performance

- Default merge gates to least privilege and read-only repository access where practical.
- Keep secrets away from untrusted PR execution unless the trust model explicitly permits them.
- Treat third-party actions, downloaded tools, model APIs, and generated commits as trust boundaries.
- Cancel superseded PR runs when supported and useful.
- Bound expensive jobs with timeouts and samples/retries.
- Avoid broad matrices unless each dimension detects a distinct failure class.

## Authority

CI validates repository authority; it does not silently redefine it.

Generated files, indexes, projections, eval results, and maintenance commits are derived unless the repository says otherwise. When generated content is intentionally semantically tuned, validate factual invariants rather than forcing byte identity unless byte identity is the actual contract.
