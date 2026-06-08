---
name: test-builder
description: >
  Read when writing pytest test files, conftest fixtures, or setting up mocks.
  Do not read for writing production logic.
---

# Test Builder

Generates robust verification suites.

## Goal

Ensure comprehensive code coverage and mock external boundary operations safely.

## Code Generation Steps

1. **Structure with AAA**: Arrange data, Act on targets, Assert expectations.
2. **Fixture Reuse**: Place reusable mocks and setup states in `conftest.py`.
3. **Simulate Scenarios**: Test error retries via side-effects and time progression via `freezegun`.
4. **Execution**: Run `test-run-pytest` to verify test coverage.

## References Loaded

- [python-style-guide.md](../../references/python-style-guide.md) (Pytest markers, freezegun, retries)
