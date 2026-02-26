---
description: Run test with dynamic routing based on delta impact
---

# Test Workflow

## 1. [SCAN]

- **Action**: Execute `git status` and `git diff` to evaluate change scope.
- **Classification**:
  - `[STATE: GLOBAL]`: If `~/pyproject.toml` or (>3) modules are modified.
  - `[STATE: LOCAL]`: If changes are confined to specific feature files or `~/tests/`.

## 2. [TEST]

- **ROUTE**:
  - **IF** `[STATE: GLOBAL]`:
    - **RUN**: `~/scripts/test.*` (Full Validation)
  - **ELSE** (Default to `LOCAL`):
    - **RUN**: `~/scripts/test_fast.*` (Optimized targeting)

## 3. [REPORT]

- **Outcome**: Summarize pass/fail counts and key error logs.
- **Next**:
  - **IF** Fail: Analyze root cause -> suggest fix -> loop back to **[SCAN]**.
  - **IF** Pass: Proceed to next task or `commit.md`.
