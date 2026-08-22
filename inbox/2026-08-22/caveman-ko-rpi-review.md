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
| No focused regression surface | Fixed: trigger and behavior fixtures added |

Loop 1 closed with material improvement, but upstream comparison exposed a new provenance/license question, so another Loop was justified.

## Loop 2

### Additional research

Compared the local Skill with `JuliusBrussee/caveman` and its MIT license. The local asset retains substantial lineage from the upstream response Skill. Upstream also makes clear that response compression does not imply input/context/reasoning-token compression or a universal reduction percentage.

### Findings and disposition

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
- Trigger and behavior JSON files are **eval fixtures**, not proof that a particular model/runtime passes them.
- No repeated live model trials are claimed by this review.
- Repository PR Gate remains required before acceptance.

## Status

`in_progress` until the branch is validated against the latest `main` and PR Gate completes. If those checks pass without a new material finding, stop the recursion on saturation rather than adding another wording-only Loop.
