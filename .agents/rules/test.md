---
trigger: glob
globs: tests/**, tests_tmp/**
description: Testing standards and artifact management. Ensured strict isolation for test-generated data.
---

- Framework -> `pytest` exclusive.
- Artifacts -> ALL files/dirs/logs -> `~/tests_tmp/`.
- Isolation -> No pollution outside `tests_tmp/`.
- Setup -> `conftest.py` for mocks & shared logic.
- Quality -> Assertion-only. No hardcoded environment hacks.
