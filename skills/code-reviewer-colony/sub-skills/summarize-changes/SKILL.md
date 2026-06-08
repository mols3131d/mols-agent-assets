---
name: summarize-changes
description: Summarizes code changes in a clean tabular format with easy navigation links to changed files.
---

# Code Changes Summarizer Skill

Procedural guidelines for generating a clean, high-level summary of code changes in a structured table format with direct navigation links.

## Goal

Provide developers with an immediate, clear overview of what files were changed, why, and how, with clickable relative links to allow quick traversal to the relevant code.

## Review Steps

1. **Analyze File Diffs**:
   - Scan the git diff or changes list to identify all added, modified, deleted, or renamed files.
   - For each file, inspect the specific changes to understand the scope and intent.

2. **Summarize Key Changes**:
   - For each changed file, write a concise description of the modification (e.g., "Added input validation for the registration form", "Refactored database query to use parameterized queries").
   - Classify the type of change (e.g., Feature, Bug Fix, Refactor, Test, Config, Chore).

3. **Construct the Change Summary Table**:
   - Organize the information into a markdown table with the following columns:
     - **File Path / Link**: Clickable link to the file. Always use relative paths starting from the workspace root or relative to the review document.
     - **Status**: Visual indicator of the change state (e.g., `🟢 Added`, `🟡 Modified`, `🔴 Deleted`, `🔵 Renamed`).
     - **Change Type**: Category of the change.
     - **Summary of Changes**: Bullet points of key modifications in that file.
     - **Impact**: Code components or areas affected.

4. **Add High-Level Statistics**:
   - Include a brief summary count of total files changed, lines added, and lines deleted to give quick context.

## Example Summary Table

### Summary Statistics
- **Total Files Changed**: 3
- **Change Type Breakdown**: 1 Feature, 1 Refactor, 1 Test

### Changes Table

| File Path / Link | Status | Change Type | Summary of Changes | Impact |
| :--- | :--- | :--- | :--- | :--- |
| [auth.go](../../../code-reviewer-colony/scripts/analyze_diff.py) (example) | 🟢 Added | Feature | - Implemented JWT-based session verification.<br>- Added password hashing helper. | Authentication flow |
| [user_service.go](../../../code-reviewer-colony/sub-skills/INDEX.csv) | 🟡 Modified | Refactor | - Extracted profile update logic into helper function.<br>- Cleaned up redundant DB queries. | User profiles |
| [user_service_test.go](../../../code-reviewer-colony/references/principles.md) | 🟢 Added | Test | - Added unit tests for profile updates.<br>- Added mock database assertions. | Test coverage |
