# CI Design Principles

Design CI as an evidence system, not a collection of workflows.

## Evidence Tiers

Prefer the cheapest evidence that can actually detect the failure.

1. **Static structure** — syntax, schema, frontmatter, references, file placement, formatting.
2. **Deterministic behavior** — scripts, generators, contract tests, regression invariants.
3. **Harness or projection compatibility** — target generation, adapter fidelity, package surface, round-trip or isolated validation.
4. **Semantic behavior** — trigger selection, instruction following, task behavior, adversarial cases.
5. **Live runtime evidence** — real provider/tool invocation, integration behavior, latency/cost or runtime parity.

Passing a lower tier does not prove a higher tier.

## Cost Ordering

Use these defaults:

- deterministic before probabilistic;
- affected before exhaustive;
- PR smoke before full matrix;
- local/static checks before network/model calls;
- narrow provider/target coverage before cross-provider matrices;
- scheduled/manual exhaustive evaluation when PR execution would be disproportionately expensive.

Do not add a model grader merely because the repository contains prompts or Skills.

## Change Impact

Map changes to checks through the smallest maintainable mechanism.

Prefer, in order when sufficient:

1. provider-native path filters;
2. repository naming/layout conventions;
3. a small selector script;
4. an explicit dependency/impact manifest only when simpler mechanisms cannot represent the relationships reliably.

Do not encode a large path switch statement without considering how it will stay synchronized with asset moves and new asset types.

## Gate Boundaries

Separate these responsibilities:

- **PR gate** — read-only checks required for merge confidence;
- **main/post-merge verification** — broader checks justified after integration;
- **scheduled/manual eval** — expensive, exhaustive, provider-specific, or stochastic evaluation;
- **maintenance automation** — formatting, regeneration, synchronization, index updates, or other repository writes.

A maintenance job should not become a merge gate merely because it is automated.

## Semantic Evaluation

Use semantic/runtime evaluation when the important contract cannot be reduced to deterministic assertions.

Good candidates include:

- Skill or tool routing precision;
- behavioral regressions across prompt/instruction changes;
- adversarial instruction boundaries;
- task success that depends on model judgment;
- live provider or harness parity.

Keep fixtures and scoring contracts versioned. Distinguish test-fixture validation from actually executing the eval.

When results are stochastic, design around thresholds, repeated samples, baselines, or non-blocking evidence as appropriate rather than pretending one sample is deterministic.

## Permissions and Secrets

Default merge gates to read-only repository permissions.

Introduce write permissions only for an explicitly separated write responsibility. Keep secrets away from untrusted PR execution unless the provider and repository trust model explicitly supports it.

Treat third-party actions, downloaded tools, model APIs, and generated commits as trust boundaries.

## Performance

Optimize measured bottlenecks, not imagined ones.

- Use concurrency cancellation for superseded PR runs when supported.
- Add caching only when repeated dependency/setup cost is material and the cache trust boundary is acceptable.
- Avoid broad matrices by default.
- Give expensive jobs explicit timeouts and bounded retries/samples.
- Prefer direct targeted tests over collecting an entire suite and filtering late when practical.

## Authority

CI validates repository authority; it must not silently redefine it.

Generated files, indexes, projections, eval results, and maintenance commits are derived unless the repository explicitly declares otherwise.

When generated content is intentionally semantically tuned, validate factual invariants instead of forcing byte-for-byte regeneration unless byte identity is the actual contract.
