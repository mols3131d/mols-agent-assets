# Agent TDD Workflow

- **Constraint** -> **Spec-First**: Requirements define the tests.
- **Granularity** -> **Atomic Feature/Issue**
- **Std** -> **Pytest** | **Ruff**

## Steps

1. **SPEC**: Read relevant documentation, issue, or PRD.
   - Files to check: `docs/`, `AGENTS.md`, or user prompt context.
2. **RED**: Create test cases in `tests/` based on **SPEC**.
   - // turbo
   - Run: `pytest tests/path/to/test_file.py`
   - **Expect**: Fail (Red).
3. **GREEN**: Implement minimal logic in `src/` to pass tests.
   - Focus on passing, not perfection.
   - // turbo
   - Run: `pytest tests/path/to/test_file.py`
   - **Loop**: If fail, analyze output and fix implementation.
4. **REFACTOR**: Improve code quality, readability, and DRY.
   - Ensure tests still pass.
   - Run: `ruff check src/`
5. **VERIFY**: Run full test suite related to the domain.
   - Ensure no regressions.
6. **REPORT**: Summary of feature implementation and test results.
