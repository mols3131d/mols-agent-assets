---
name: check-md-absolute-paths
description: Scan and fix absolute paths (file://, C:\, username) in .md files.
---

# check-md-absolute-paths

Find and replace absolute paths in markdown files.

## Workflow

1. **Scan**
   - Tool: `grep_search`
   - Files: `*.md`
   - Regex: `file:///|[a-zA-Z]:\\|<current_username>`

2. **Report**
   - 0 found: Report "Clean".
   - >0 found: List files/lines. Ask user to auto-fix.

3. **Fix (If Approved)**
   - Replace absolute links with relative paths.
