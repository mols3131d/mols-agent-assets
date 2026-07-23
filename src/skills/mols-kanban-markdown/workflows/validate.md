# Workflow: Validate Kanban

## Goal

Validate Kanban cards against the defined config schemas using verification scripts.

## Parameters

- **Target Path**: Kanban workspace folder path (`<kanban_path>/`).

## Procedure

1. Execute `scripts/validate_frontmatter.py` passing the target path.
2. Read output and report any validation issues found.
