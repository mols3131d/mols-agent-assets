---
description: Experimental maintainer context for the caveman-ko Skill, including maturity boundary and promotion criteria
---

# caveman-ko

Status: **Experimental**.

`caveman-ko` explores an intentionally rough, highly compressed speaking style while preserving technical meaning. Experimental status describes maturity, not discovery: the Skill may remain available for explicit invocation while its trigger and behavior are still being refined.

## Maintenance Boundary

- Runtime behavior stays in `src/rulesync/.rulesync/skills/caveman-ko/SKILL.md`.
- Repository eval fixtures stay in `evals/skills/caveman-ko/`.
- This capsule owns maturity and maintenance context only; it is not loaded as runtime instruction.
- Ordinary brevity is intentionally outside the Skill. False triggering on requests such as "짧게", "간결하게", or "토큰 아껴서" is a regression.

## Promotion Criteria

Consider stable status only after repeated evidence shows that:

- explicit caveman-style requests trigger reliably while ordinary brevity near-misses do not;
- `lite`, `full`, and `ultra` remain observably distinct;
- compression preserves negation, uncertainty, quantities, units, conditions, identifiers, and required safety clarity;
- one-turn, ongoing-mode, and deactivation behavior are understandable across supported runtimes;
- further validation loops stop producing material corrections rather than merely more wording.

Until then, prefer small evidence-led changes over feature expansion.
