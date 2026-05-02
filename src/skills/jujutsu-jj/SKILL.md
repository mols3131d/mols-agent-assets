---
name: Jujutsu-jj
description: "Jujutsu (jj) VCS for atomic commits; Use for version control (commit, log, status) or exploring history; jj, Jujutsu, git, vcs, commit"
fmContentType: agent-skill
---

# Jujutsu (jj) Protocol

## 1. Core State

- `@` (Working Copy) is an active commit. Changes auto-snapshot.
- `jj op log`: Operation history. `jj undo` reverts logic/VCS state.
- Commits are mutable. Refine current or `absorb` into parents.

## 2. Context Discovery

1. `jj log -n 10`: Current branch/state topology.
2. `jj st`: Pending file modifications at `@`.
3. `jj show @-`: Diff of preceding revision.

## 3. Atomic Workflow

### Initialize Task

```bash
jj new
jj desc -m "type: description"
```

### Refine & Finalize

- `jj absorb`: Auto-distribute changes to matching ancestors.
- `jj st`: Verify `@` is empty after absorb.

## 4. Git Alignment

| Action      | jj Command         | Note                            |
| ----------- | ------------------ | ------------------------------- |
| Status      | `jj st`            | Contextual summary.             |
| Commit      | `jj desc -m "..."` | Describes `@`.                  |
| History     | `jj log`           | Tree visualization.             |
| Partial Add | `jj absorb`        | **Preferred**. Non-interactive. |
| Branch      | `jj new`           | Stacked revision.               |
| Push        | `jj git push`      | Bookmark required.              |

## 5. Constraints

- **Zero Interactivity**: Never run `jj split` or `jj edit` (no args).
- **Inline Messages**: Always use `-m "message"`.
- **Atomic Intent**: One logical change per revision.
