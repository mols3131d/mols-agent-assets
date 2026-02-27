---
description: git commit workflow. Feature Commit.
---

# Commit Workflow

- **Constraint** -> **Local-Only**: `git commit` | No Push
- **Granularity** -> **Logical Unit Commit**
- **Std** -> **Conventional Commits**

## Steps

1. **[SCAN]**: `git status` + `git diff` -> Delta
2. **[GROUP]**: Cluster ~ Feature logic | Technical Domain
3. **[STAGE]**: `git add` matching targeted cluster
4. **[EXEC]**: `git commit -m "<type>(<scope>): <desc>"`
   - `<scope>` -> `<feature-id>` | `<domain>`
5. **[REPORT]**: Summary of commits & current git state.
