---
name: iceberg-code-review-create-details
description: Create and validate detail documents.
---

# Create Details Workflow

Resolve context before creating details: read the supplied `summary_file_path`, use the latest review summary when it is omitted in autopilot mode, otherwise request it; then select `detail`, or every summary detail when it is omitted.

## Inputs

- `summary_file_path`: **required**. Path to a validated `__summary__.md` file.
  - If omitted in autopilot mode, use the latest review summary.
  - Otherwise, request it from the user.
- `detail`: Detail to create. Default: every detail in `__summary__.md`.
- `domain`: Slug naming the detail's domain.
- `<SKILL_DIR>`: Directory containing this skill's `scripts/` directory.
- `<PYTHON_EXEC>`: Selected Python interpreter.

## Details

### Select Details

- Determine a `domain` and `detail` slug for each detail document.
- Use lowercase letters, digits, and hyphens only for both slugs.
- Process every selected detail in sequence.

### Create `domain-detail.md`

```bash
<PYTHON_EXEC> "<SKILL_DIR>/scripts/create_detail.py" --summary-file "<summary_file_path>" --domain "<domain>" --detail "<detail>"
```

- Populate the generated `domain-detail.md` with the verified issue and location, impact, actionable recommendation, and verification method.
- Remove template comments and authoring instructions.

### Validate `domain-detail.md`

```bash
<PYTHON_EXEC> "<SKILL_DIR>/scripts/validate_detail.py" "<detail_file_path>"
```

- If validation reports `FAIL: ...`, fix the named issue and rerun `validate_detail.py`.
- Continue with the next detail only after validation succeeds.
