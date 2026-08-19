# CI Design Patterns

Choose patterns only after inspecting the target. Combine only what covers real failure classes.

## Minimal Deterministic PR

Use when important contracts are static or deterministic.

```text
change
→ syntax/schema/format
→ affected deterministic tests
→ merge evidence
```

Good for small prompt, Skill, Rule, documentation, or script repositories. Do not add model evaluation merely because an LLM consumes the assets.

## Targeted Impact Routing

Use when the repository has many independent assets or test suites.

```text
changed asset
→ resolve affected identity/subsystem
→ select matching checks
→ run only those targets
```

Prefer path filters or naming conventions while they stay clear. Move to a small router script when workflow syntax becomes awkward. Add a dependency manifest only when stable repository conventions are insufficient.

Representative mapping:

```text
skill A       → contract(A) + fixture-shape(A) + optional smoke(A)
shared loader → dependent contracts + compatibility regression
rule          → rule contract + affected projection check
script X      → script-specific tests
CI router     → router tests + representative root checks
```

The router is CI code; test it deterministically.

## Harness / Projection Gate

Use when canonical assets are translated, projected, packaged, or adapted for runtimes.

Typical evidence:

- canonical configuration validity;
- isolated or dry-run generation;
- generated file/package fidelity;
- supporting-file preservation;
- forbidden generated surfaces;
- meaningful round-trip or `generate --check` invariants.

This proves transformation fidelity, not live runtime behavior.

## Semantic and Runtime Eval

Use only when deterministic evidence cannot cover the important behavior risk.

For PR feedback, prefer a small representative smoke set:

```text
semantic change
→ trigger / high-risk adversarial cases
→ bounded model/provider execution
→ threshold or regression interpretation
```

Move expensive evidence to scheduled/manual or promotion boundaries, including broad provider/model matrices, large adversarial suites, repeated stochastic samples, latency/cost collection, and live runtime parity.

Keep fixture shape validation separate from model execution.

## Progressive Evidence

A useful default for repositories that need several evidence depths is:

```text
PR       → static + affected deterministic + optional semantic smoke
main     → broader deterministic / integration regression
schedule → exhaustive semantic/runtime/provider evaluation
```

This is not mandatory. Small repositories may need only the PR tier.

## Maintenance Automation

Use for derived-state upkeep rather than merge confidence: formatting, index/route regeneration, synchronized projections, generated documentation, or similar writes.

Prefer clear source authority and idempotent generation. Where practical, validate on PR and write only after merge. Avoid commit loops and workflows that silently overwrite intentional semantic tuning.
