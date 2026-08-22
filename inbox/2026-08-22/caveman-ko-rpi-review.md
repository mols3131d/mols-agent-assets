# caveman-ko RPI Review

Based on:

- `inbox/2026-08-22/caveman-ko-rpi-research.md`
- `inbox/2026-08-22/caveman-ko-rpi-plan.md`

## Loop 1

### Evidence

Static inspection of the current Skill, repository conventions, Agent Skills guidance, and focused trigger/behavior scenarios.

### Findings and disposition

| Finding | Disposition |
| --- | --- |
| Generic brevity and token-saving phrases falsely activate caveman style | Fixed: activation now requires explicit caveman-style intent or Skill naming; near-miss negatives added |
| `ACTIVE EVERY RESPONSE` overclaims persistence | Fixed: activation lifetime is one-answer by default and ongoing only when explicit conversation intent remains observable |
| Compression can erase negation, uncertainty, numbers, units, conditions, or scope | Fixed: explicit semantic-preservation invariants and behavior fixtures added |
| Absolute presentation/tool narration rules can conflict with higher authority or output contracts | Fixed: style is now an overlay and exact/constrained formats win |
| WIP README mixes maintainer maturity with deployable package | Fixed: package README removed; experimental maintainer capsule added |
| No focused behavior evaluation surface | Fixed: trigger and behavior capability fixtures added |

Loop 1 closed with material improvement, but upstream comparison exposed a new provenance/license question, so another Loop was justified.

## Loop 2

### Additional research

Compared the local Skill with `JuliusBrussee/caveman` and its MIT license. The local asset retains substantial lineage from the upstream response Skill. Upstream also makes clear that response compression does not imply input/context/reasoning-token compression or a universal reduction percentage.

### Additional findings and disposition

| Finding | Disposition |
| --- | --- |
| Upstream MIT notice missing from substantially derived package | Fixed: package `LICENSE` includes the upstream MIT notice |
| Provenance was implicit | Fixed: maintainer capsule identifies upstream and pins the reviewed Skill revision |
| Token-saving scope could be overread | Fixed: boundary now limits the claim to generated prose and rejects fixed reduction guarantees |
| `Reasoning stays full` implied control over internal reasoning | Fixed: replaced with `Compress delivery, not substance.` |

## Final Review

No additional material design issue was found in static semantic/adversarial review after Loop 2 corrections.

The resulting responsibility is intentionally narrow:

- explicit caveman-style speech only;
- one `intensity` control with `default | auto | lite | full | ultra`;
- generated-prose compression, not general brevity or a token optimizer;
- semantic and required-clarity preservation outrank compression;
- experimental maturity remains a maintainer concern rather than runtime context.

### Evidence boundary

- Repository structure, wording, provenance, license notice, route metadata, and fixture contents are directly inspectable evidence.
- Trigger and behavior JSON files are **capability eval fixtures**, not proof that a particular model/runtime passes them and not a blocking regression suite.
- No repeated live model trials are claimed by this review.

### Repository validation

The first merge-result PR Gate exposed Markdown-only normalization drift in the RPI artifacts: ordered-list numbering and one duplicate heading anchor. No Skill, Rulesync, route, or deterministic-test failure was found. Those Markdown issues were corrected.

PR Gate run #847 then passed:

- deterministic tests;
- canonical Rulesync source validation;
- distribution route regeneration check;
- changed Markdown normalization.

The Promptfoo smoke was correctly skipped because this change does not touch its routed `mols-rpi` eval surface. The new `caveman-ko` capability fixtures were not executed as live model/runtime trials.

## Status

`completed` — two substantive RPI loops converged. The later Markdown correction was mechanical validation cleanup, not another design loop. Further iteration without new behavioral evidence would be wording-only churn, so recursion stops on saturation.
