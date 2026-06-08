---
name: test-run-pytest
description: >
  Read when executing tests, checking test coverage results, or diagnostic test failures.
  Do not read when running test suite is not needed.
---

# Test Suite Runner

Runs pytest and reports test coverage details.

## Steps
1. Run `pytest -v --cov=src/` or specific target test path.
2. Parse any test failures and provide correction recommendations.
