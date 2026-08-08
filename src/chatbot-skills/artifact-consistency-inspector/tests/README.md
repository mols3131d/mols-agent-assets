# Tests

Maintainer-facing deterministic contract tests for `artifact-consistency-inspector`. Never load these fixtures as evidence for a repository being inspected.

## Run

```bash
python tests/run_tests.py
```

The suite uses only the Python standard library and requires no network or repository write access.

## Coverage

- package structure and relative references
- `SKILL.md` front matter and read-only runtime contract
- absence of coding-agent directory defaults
- report front matter, compact heading template, Summary states, and filename rules
- ordered `rule_sources` and in-place `auto` expansion contract
- no universal source-type precedence
- rule-source conflict and inferred-convention behavior
- result and coverage state decisions
- gap classification tie-breaker
- omission safeguards
- PR, file, repository-wide, access-blocked, no-finding, and rule-source scenarios
- ZIP shape and archive integrity

## Boundary

These are deterministic contract tests. They do not execute live ChatGPT repository retrieval or measure model reasoning quality. That requires separate live evaluation against accessible repositories.
