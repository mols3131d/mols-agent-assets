---
description: Experimental maintainer context for the caveman-ko Skill, including provenance, maturity boundary, and promotion criteria
---

# caveman-ko

Status: **Experimental**.

`caveman-ko` is a Korean-oriented experimental adaptation of the MIT-licensed [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) response Skill. It keeps the core idea—compress generated prose while preserving technical meaning—but intentionally diverges where local trigger, Korean-language, runtime, and clarity requirements need a different contract.

Provenance baseline: `JuliusBrussee/caveman` `skills/caveman/SKILL.md` at `bd22d86b32e4a99e09ff7482a35509faac7a6f65`.

The distributed package includes the upstream MIT notice in `src/rulesync/.rulesync/skills/caveman-ko/LICENSE`.

## Maintenance Boundary

- Runtime behavior stays in `src/rulesync/.rulesync/skills/caveman-ko/SKILL.md`.
- Repository eval fixtures stay in `evals/skills/caveman-ko/`.
- Current trigger and behavior fixtures are **capability eval contracts** for the experimental Skill, not evidence that a model/runtime passes them and not a blocking regression suite.
- This capsule owns provenance, maturity, and maintenance context only; it is not loaded as runtime instruction.
- Ordinary brevity is intentionally outside the Skill. Triggering on requests such as "짧게", "간결하게", or "토큰 아껴서" is a failure case.
- Do not copy upstream token-reduction percentages into the local contract without local evidence. The Skill affects generated prose, not input/context/reasoning-token volume.

## Promotion Criteria

Consider stable status only after repeated evidence shows that:

- explicit caveman-style requests trigger reliably while ordinary brevity near-misses do not;
- `lite`, `full`, and `ultra` remain observably distinct;
- compression preserves negation, uncertainty, quantities, units, conditions, identifiers, and required safety clarity;
- one-turn, ongoing-mode, and deactivation behavior are understandable across supported runtimes;
- further validation loops stop producing material corrections rather than merely more wording.

Stable behavior that remains worth protecting may then be promoted from capability evaluation into an appropriate regression contract under repository evaluation policy.

Until then, prefer small evidence-led changes over feature expansion.
