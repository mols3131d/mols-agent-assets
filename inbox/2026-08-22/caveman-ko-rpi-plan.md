# caveman-ko RPI Plan

Based on: `inbox/2026-08-22/caveman-ko-rpi-research.md`

## Active Scope

- Goal: improve experimental `caveman-ko` behavior and maintainability.
- In scope: `SKILL.md`, route metadata, upstream attribution/license notice, experimental maintainer status, focused eval fixtures.
- Out of scope: renaming the Skill, promoting it to stable, changing repository-wide Skill conventions, adding runtime scripts or a new eval framework.
- Acceptance: narrower trigger boundary; preserved caveman identity; explicit semantic/clarity floor; runtime-safe persistence; small intensity control; honest output-compression scope; upstream MIT notice; experimental status outside deployable package; focused trigger/behavior eval coverage; repository Gate passes.

## Work

1. Rewrite `description` around explicit caveman-style intent and add a negative boundary for ordinary brevity/token-saving requests.
2. Refactor the body around semantic preservation, intensity, and activation lifetime. Remove brittle absolute presentation rules that do not prevent a material failure.
3. Keep one public `intensity` control: omitted/`default` → `full`, `auto` → least aggressive level that satisfies explicit intent, or explicit `lite|full|ultra`.
4. Treat slash-like forms as user intent syntax, not proof of runtime command registration.
5. Replace unconditional persistence with turn/conversation behavior derived from explicit user intent and observable context continuity.
6. State that the Skill compresses generated prose only and does not promise fixed token savings or input/context/reasoning compression.
7. Add the upstream MIT notice to the distributed Skill package and record derivation in maintainer context.
8. Delete package WIP `README.md`; add minimal `docs/skills/caveman-ko/README.md` that owns experimental maturity, provenance, and promotion criteria.
9. Add `evals/skills/caveman-ko/trigger-evals.json` with realistic positive and near-miss negative prompts.
10. Add `evals/skills/caveman-ko/behavior-evals.json` for intensity, exact-token preservation, uncertainty/negation/units, high-stakes clarity, activation lifetime, deactivation, and token-scope honesty.
11. Regenerate/update `route/skills.jsonl` from the changed canonical description.
12. Review against repository conventions, upstream behavior, and Agent Skills guidance. If material findings remain, run another bounded loop; otherwise stop on saturation.

## Validation

- inspect diff and active references;
- verify JSON fixtures parse structurally;
- verify route line matches canonical frontmatter;
- verify license notice and provenance are present without copying unrelated upstream runtime behavior;
- PR Gate: deterministic tests, Rulesync source, distribution route, Markdown normalization;
- semantic/adversarial review of false triggers, semantic loss, authority conflicts, and token-saving claims.
