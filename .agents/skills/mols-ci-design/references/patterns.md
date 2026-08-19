# CI Design Patterns

Choose patterns after inspecting the target. Combine only the patterns that solve evidenced failure classes.

## Minimal Deterministic PR Gate

Use when most important contracts are static or deterministic.

Typical shape:

```text
changed files
→ syntax/schema/format checks
→ affected deterministic tests
→ merge decision
```

Good for small prompt, Skill, Rule, documentation, or script repositories where runtime evaluation is not required for every change.

Avoid adding a semantic layer merely because the assets are consumed by an LLM.

## Affected-Asset Targeting

Use when the repository has many independent assets or test suites.

Typical shape:

```text
changed asset
→ resolve affected asset identity / subsystem
→ select matching tests and deterministic eval-fixture checks
→ run only selected targets
```

Prefer path filters or naming conventions when they remain understandable. Use a selector script when relationships exceed what workflow syntax can express cleanly.

Escalate to a manifest only when dependencies cannot be derived reliably from stable repository conventions.

## Harness or Projection Gate

Use when canonical assets are translated, projected, packaged, or adapted for one or more runtimes.

Typical checks:

- canonical configuration validity;
- isolated or dry-run generation;
- generated package/file-set fidelity;
- supporting-file preservation;
- forbidden generated surfaces in canonical roots;
- round-trip or `generate --check` when the tool supports a meaningful invariant.

This proves transformation fidelity, not live runtime behavior.

## Semantic Smoke Eval

Use when a change can alter model-visible behavior and deterministic checks cannot cover the important risk.

Typical shape:

```text
relevant semantic change
→ small representative case set
→ bounded model/provider execution
→ threshold / regression comparison
```

Keep it small enough for PR feedback. Prefer trigger and high-risk adversarial cases over a broad benchmark.

Decide whether it is blocking based on evaluator stability, cost, and failure reproducibility.

## Scheduled or Manual Full Eval

Use for exhaustive or expensive evidence that is disproportionate for every PR.

Examples:

- multiple models/providers;
- large adversarial suites;
- repeated stochastic samples;
- full prompt/Skill regression sets;
- latency/cost collection;
- runtime parity checks across harnesses.

Run on schedule, manual dispatch, release candidate, or another explicit promotion boundary.

Do not present delayed full-eval evidence as if the PR gate already proved it.

## PR Smoke, Main Broader, Scheduled Full

Use when the repository benefits from progressive evidence depth.

```text
PR       → static + affected deterministic + optional semantic smoke
main     → broader deterministic / integration regression
schedule → exhaustive semantic/runtime/provider matrix
```

This is a useful default pattern, not a requirement. Small repositories may need only the PR tier.

## Maintenance Automation

Use for derived-state upkeep rather than merge confidence.

Examples:

- formatting;
- route/index regeneration;
- generated documentation;
- synchronized projections;
- dependency metadata refresh.

Prefer idempotent generation and clear source authority. Keep write permissions scoped to this responsibility.

Where practical, validate on PR and write only after merge. Avoid workflows that repeatedly fight contributor changes or create commit loops.

## Fixture Shape Gate vs Eval Execution

Keep these distinct.

```text
eval fixture changed
→ deterministic parse/schema/identity validation

behavior-sensitive asset changed
→ maybe execute applicable semantic eval
```

Valid JSON or a valid eval schema does not prove model behavior. Conversely, model execution should not be required merely to catch malformed fixtures.

## Changed-File Router

Use when provider path filters are too coarse but a full dependency framework is unnecessary.

A small router may map changed paths to logical checks such as:

```text
skill A         → contract(A) + eval-fixture-shape + optional smoke(A)
shared loader   → all dependent Skill contracts + compatibility regression
rule            → rule contract + affected projection check
script X        → script-specific tests
CI router       → router tests + representative root checks
```

The router itself becomes critical CI code. Give it deterministic tests and ensure changes to the router trigger representative coverage.

## Matrix Restraint

Use matrices only for dimensions that need simultaneous evidence.

Before adding a dimension such as provider, model, OS, runtime, or prompt variant, ask:

- can one representative value gate the PR?
- can the rest move to scheduled/manual evaluation?
- is the dimension genuinely independent?
- does each combination detect a distinct failure class?

Avoid Cartesian products that exist only because the CI platform makes them easy to express.
