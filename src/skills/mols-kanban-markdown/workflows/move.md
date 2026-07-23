# Workflow: Move Cards

## Goal

Automatically move Kanban cards to their correct directories based on their frontmatter `status` and fix link paths inside and pointing to the moved cards.

## Parameters

- **Target Path**: Kanban workspace folder path (`<kanban_path>/`).

## Procedure

1. Execute `scripts/move_cards.py` passing the target path.
2. Read output and report which cards have been moved.
