---
name: workflow-create-summary
description:
---

Create summary after all details are valid.

1. Create `__summary__.md` in `<review_dir>`.
2. Read all validated details.
3. Fill links and test counts. Remove template comments and instructions.
4. Validate with `validate_summary.py`.
5. `FAIL` -> fix and rerun. Pass -> finish.
