# Eval Tests

Repository-owned deterministic checks for evaluation fixtures.

- `evals/skills/**/*.json` must parse as valid JSON.
- Skill-specific deterministic behavior checks remain under `tests/skills/<skill-name>/`.
- Model-based evaluation is not implied by these checks.
