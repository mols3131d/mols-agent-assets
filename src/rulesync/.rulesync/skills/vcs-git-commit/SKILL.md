---
name: vcs-git-commit
description: Prepare or create Git commits from an existing Git worktree. Use when the task is to inspect commit conventions, select or stage intended changes, write a commit message, execute git commit, or report the result. Do not use for push, pull requests, merge, conflict resolution, branch management, history rewriting, or non-Git version control.
---

# Git Commit

Commit only the intended work and leave unrelated worktree state untouched.

# Workflow

1. Inspect `git status --short` and only the diffs needed to resolve commit scope and applicable message requirements. Treat recent history as supporting evidence, not authority.
1. If the user only wants a commit message, do not mutate the repository.
1. Stage only intended paths or hunks. Do not use `git add -A`, `git add .`, `git add --all`, or `git commit -a` to decide scope.
1. Re-read the staged diff. Stop if it is empty, outside scope, or mixed with unrelated pre-staged work. Write the message from this diff and the resolved convention; without one, use a concise imperative summary.
1. Run a normal `git commit` with hooks enabled. On failure, preserve state and report it; do not bypass hooks or edit product content as part of this Skill.
1. Verify the new commit and `git status --short`, then report the commit identifier, subject, and meaningful remaining changes.

# Guardrails

- Preserve unrelated staged, unstaged, and untracked work. Do not perform unrelated worktree or history management to simplify the commit.
- If repository policy forbids committing on the current branch, stop and hand off branch preparation.
- Do not amend, create empty commits, spoof metadata, push, create pull requests, merge, rebase, resolve conflicts, manage branches, or operate on non-Git version control.
