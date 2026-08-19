# CI Design Patterns

Choose patterns only after inspecting the target. Combine only what protects real admission risks or useful non-blocking confidence.

## Minimal Deterministic PR

Use when important contracts are static or deterministic.

```text
change
→ classify merge risk
→ syntax / schema / contract
→ affected deterministic tests
→ strict admission evidence
```

Good for small prompt, Skill, Rule, documentation, or script repositories. Pure style does not need to block merge unless representation affects correctness or an explicit contract. Do not add model evaluation merely because an LLM consumes the assets.

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

The router is CI code; test it deterministically. If it cannot resolve impact with enough confidence, broaden the selected checks or fail safe rather than returning an empty or incomplete set.

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

For merge-critical behavior, prefer the smallest representative blocking set that can support the admission decision:

```text
semantic change
→ trigger / high-risk adversarial cases
→ bounded model/provider execution
→ threshold or regression interpretation
```

Move evidence that does not affect admission to scheduled/manual or post-merge execution, including broad provider/model matrices, large adversarial suites, repeated stochastic samples, latency/cost collection, and live runtime parity.

Keep fixture shape validation separate from model execution.

## Progressive Evidence

A useful default for repositories that need several evidence depths is:

```text
PR       → blocking merge-critical static + affected deterministic + required semantic smoke
main     → non-admission broader regression or diagnostics
schedule → exhaustive semantic/runtime/provider evaluation
```

This is not mandatory. Small repositories may need only the PR tier. A failure that makes the change unacceptable on `main` belongs before merge even when its check is expensive.

## Maintenance Automation

Use for derived-state upkeep rather than merge confidence: pure formatting, style normalization, index/route regeneration, synchronized projections, generated documentation, or similar writes.

Prefer clear source authority and idempotent generation. Where practical, validate merge-critical invariants on PR and write only after merge. Avoid commit loops and workflows that silently overwrite intentional semantic tuning.
