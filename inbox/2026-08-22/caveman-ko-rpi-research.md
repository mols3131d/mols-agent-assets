# caveman-ko RPI Research

Baseline: `112d897c1be13d6b08c2b8416cd0122b3eb95cfa`

## Goal

Improve experimental `caveman-ko` without turning it into a general brevity Skill or a framework. Preserve its distinctive caveman-style compression while reducing false triggers, semantic loss, brittle runtime assumptions, and maintenance ambiguity.

## Evidence

### Current asset

- `description` auto-triggers on generic brevity/token-efficiency phrases such as `be brief`, `less tokens`, `짧게 말해`, and `토큰 아껴서 말해`. These requests do not necessarily ask for caveman-style language.
- `ACTIVE EVERY RESPONSE` claims persistence without a runtime/session boundary.
- Several absolute rules (`No tool-call narration`, `No self-reference`, `Code, commits, and PRs: write normal`) can conflict with higher-priority runtime requirements or explicit user intent.
- Compression safeguards protect code and identifiers, but the core invariant does not explicitly protect negation, uncertainty, units, scope, or safety-critical qualifiers.
- `README.md` is maintainer-only WIP status inside the deployable Skill package, while current repository convention places maintainer knowledge under `docs/<asset-type>/<owner>/`.

### Upstream provenance

`caveman-ko` is substantially derived from `JuliusBrussee/caveman`'s `skills/caveman/SKILL.md`: the activation wording, persistence model, lite/full/ultra levels, compression rules, examples, and auto-clarity structure have clear lineage.

The upstream repository currently documents an important scope limit: the response Skill shortens generated prose; it does not compress input context or reasoning tokens, and token reduction varies by workload. Its MIT license requires the copyright and permission notice to accompany copies or substantial portions.

Therefore the local adaptation should:

- keep provenance visible;
- include the applicable MIT notice in the distributed package;
- avoid promising a fixed token reduction;
- preserve useful upstream corrections such as protecting negation, numbers, units, technical tokens, and clarity-sensitive sequences while adapting behavior for Korean and local runtime conventions.

### Repository conventions

- Skill `description` owns activation and negative boundary; body owns runtime behavior.
- Prefer the smallest deployable package; add resources only for concrete runtime/loading/mechanical benefit.
- Argument surfaces are useful for real behavior choices such as verbosity/intensity, but should stay small and distinguish `default` from `auto`.
- Maintainer-only knowledge should not be hidden in the runtime package.

### External Agent Skills guidance

- Refine Skills against realistic execution and near-miss cases instead of relying on one draft.
- Avoid over-broad descriptions; test both should-trigger and should-not-trigger prompts.
- Keep Skill context lean and remove instructions that do not prevent a material failure.
- Prefer a clear default over an option menu and calibrate strictness to fragility.
- Compare against the prior version and iterate until further loops provide little material gain.

## Findings

1. **P1 — Trigger overreach.** Generic brevity is adjacent behavior, not caveman mode. Activation should require explicit caveman/primitive-style intent or direct Skill invocation.
1. **P1 — Semantic preservation needs a clearer floor.** `ultra` can otherwise encourage dropping negation, uncertainty, units, conditions, or scope.
1. **P1 — Persistence is overclaimed.** Persistence should be scoped to observable conversational context and explicit ongoing intent.
1. **P1 — Upstream MIT notice is missing.** The adaptation retains substantial upstream structure/content but the current package carries only `license: MIT`, not the required upstream copyright/permission notice.
1. **P2 — Absolute presentation rules are too broad.** Higher-authority/runtime-required content and explicit artifact style must win.
1. **P2 — Intensity control is useful but under-specified.** Keep one public `intensity` control with `default | auto | lite | full | ultra`; do not add a larger configuration surface.
1. **P2 — Experimental lifecycle belongs in maintainer docs.** Keep the runtime package focused and move WIP/maturity information out.
1. **P2 — No eval surface exists.** Add compact trigger and behavior cases, especially near-miss negatives and semantic-preservation cases.

## Constraints

- Keep `caveman-ko` experimental.
- Do not rename it.
- Do not make ordinary concise-answer requests trigger it.
- Do not add supporting runtime files unless they provide concrete runtime, legal, loading, or deterministic benefit.
- Preserve `agentsskills.license: MIT` and satisfy upstream MIT attribution.
