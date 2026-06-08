---
name: audit-tests
description: Reviews test coverage, test cases, mocking strategies, and unit/integration test code quality.
---

# Test Reviewer Skill

Procedural guidelines for reviewing test files, assertions, and test coverage.

## Goal

Ensure the codebase has robust, readable, and maintainable test coverage, focusing on correctness and regression prevention.

## Review Steps

1. **Verify Coverage & Tests Presence**:
   - Check if new features or bug fixes are accompanied by appropriate unit or integration tests.
   - If functional logic is modified but no tests are added or updated, verify if coverage is already sufficient or ask if tests are needed.

2. **Evaluate Test Case Quality**:
   - Verify that test cases cover happy paths, error paths, and boundary conditions (empty values, extremes).
   - Ensure assertions are meaningful (avoiding vague assertions like `assert True` or just checking that a function returns without error).
   - Check that tests are structured cleanly (e.g., Arrange-Act-Assert / AAA pattern).

3. **Inspect Mocking Strategies**:
   - Verify that external dependencies (database, third-party APIs, filesystem) are mocked out in unit tests to ensure fast and isolated test execution.
   - Ensure mocks are not over-engineered or hard to maintain. Check that mock expectations match actual logic.
   - Refer to guidelines in [principles.md](../../references/principles.md).
