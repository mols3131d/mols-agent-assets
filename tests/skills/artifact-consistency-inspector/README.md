# Artifact Consistency Inspector Tests

Repository-owned deterministic contract tests for `artifact-consistency-inspector`.

## Run

```bash
uv run pytest tests/skills/artifact-consistency-inspector
```

## Coverage

- deployable package structure and relative references
- `SKILL.md` front matter and read-only runtime contract
- report front matter, compact heading template, Summary states, and filename rules
- ordered `rule_sources` and in-place `auto` expansion
- rule-source conflict and inferred-convention behavior
- result and coverage state decisions
- omission safeguards and deterministic scenarios
- ZIP shape and verification-surface exclusion

`scenarios/` is test fixture data owned by this suite. It is not copied into the deployable Skill package.
