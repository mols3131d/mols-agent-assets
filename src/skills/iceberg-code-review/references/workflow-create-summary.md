---
name: iceberg-code-review-create-summary
description: Create and validate the summary review document.
---

# Create Summary Workflow

```mermaid
flowchart TD
    A[workflow-create-summary.md<br/># Inputs] --> B{review_target_path available?}
    B -->|Yes| C[Review target]
    B -->|No, autopilot| D[Use working directory]
    B -->|No, interactive| E[Request review_target_path]
    D --> C
    E --> C
    C --> F[Run relevant tests]
    F --> G[create_summary.py]
    G --> H[__summary__.md]
    H --> I[Write summary and findings]
    I --> J[validate_summary.py]
    J --> K{Validation passed?}
    K -->|No| L[Fix reported failures]
    L --> J
    K -->|Yes| M[Validated __summary__.md]
```

## Inputs

- `review_target_path`: **required**. Review target file or directory.
  - If omitted in autopilot mode, use the current working directory.
  - Otherwise, request it from the user.
- `title_slug`: **required**. Lowercase letters, digits, and hyphens only.
- `<SKILL_DIR>`: Directory containing this skill's `scripts/` directory.
- `<PYTHON_EXEC>`: Selected Python interpreter.

## Details

### Review Target

- Apply a selected code-review skill when one is available.
- Review the specified code, PR, or diff.
- Choose and run tests appropriate to the review target and project environment.
- Collect `PASS`, `FAIL`, `ERROR`, and `SKIP` counts.

### Create `__summary__.md`

```bash
<PYTHON_EXEC> "<SKILL_DIR>/scripts/create_summary.py" --title-slug "<title_slug>" --workspace-dir "<workspace_absolute_path>"
```

- Record the absolute path emitted for `__summary__.md`.
- Populate all placeholders with the review findings and test results.
- Remove template comments and authoring instructions.

### Validate `__summary__.md`

```bash
<PYTHON_EXEC> "<SKILL_DIR>/scripts/validate_summary.py" "<summary_file_path>"
```

- If validation reports `FAIL: ...`, fix the named issue and rerun `validate_summary.py`.
- Continue only after validation succeeds.
