---
name: workflow-create-details
description:
---

One review result -> one validated detail. Finish before next.

1. Review target with selected engine or skill. Run relevant tests. Keep `PASS`, `FAIL`, `ERROR`, `SKIP` counts.
2. Set `domain` and `detail` slugs: lowercase letters, digits, hyphens.
3. Create detail in `<review_dir>`.
4. Fill verified issue, location, impact, recommendation, verification. Remove template comments and instructions.
5. Validate with `validate_detail.py`.
6. `FAIL` -> fix and rerun. Pass -> next review result.
