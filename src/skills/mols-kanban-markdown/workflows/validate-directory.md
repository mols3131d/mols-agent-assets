# Workflow: Validate Directory

## Goal

Validate the directory structure and the existence of mandatory configuration files of the Kanban workspace.

## Parameters

- **Target Path**: Kanban workspace folder path (`<kanban_path>/`).

## Procedure

1. Execute `scripts/validate_directory.py` passing the target path.
2. Read output and report any missing configuration files or folders.
