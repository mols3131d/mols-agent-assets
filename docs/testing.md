# Testing & Quality Assurance Guide

Guide for automated testing, static analysis, and code quality tools.

---

## Test Directory Layout

| Path | Purpose |
| :--- | :--- |
| `tests/scripts/` | Tests for repository automation scripts |
| `tests/skills/` | Test suites and fixtures for agent skills |

## Verification Commands

```bash
# Run unit tests
uv run pytest

# Static type checking & linting
uv run ty check
uv run ruff check .
```
