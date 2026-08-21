---
name: vcs-git-commit
description: Prepare or create Git commits from an existing Git worktree. Use when the task is to inspect commit conventions, select or stage intended changes, write a commit message, execute git commit, or report the result. Do not use for push, pull requests, merge, conflict resolution, branch management, history rewriting, or non-Git version control.
---

# Git Commit

Commit only the intended work and leave unrelated worktree state untouched.

# Workflow

1. Inspect `git status --short` and only the staged or unstaged diffs needed to establish the commit scope.
1. Resolve scope and message requirements from explicit user intent and applicable repository guidance or configuration. Use recent history only as supporting evidence when needed.
1. If the user only wants a commit message, do not mutate the repository.
1. Stage only intended paths or hunks. Do not use `git add -A`, `git add .`, `git add --all`, or `git commit -a` to decide scope.
1. Re-read the staged diff. If it is empty, outside the intended scope, or mixed with unrelated pre-staged work, stop.
1. Write the message from the staged diff and resolved convention. If no convention exists, use a concise imperative summary and add a body only when useful. Use a user-supplied message only when it still matches the staged diff and repository requirements.
1. Run a normal `git commit` with hooks enabled. On failure, preserve state and report the failure; do not bypass hooks or edit product content as part of this Skill.
1. Verify the new commit and `git status --short`, then report the commit identifier, subject, and meaningful remaining changes.

# Guardrails

- Preserve unrelated staged, unstaged, and untracked work. Do not perform unrelated worktree or history management to simplify the commit.
- If repository policy forbids committing on the current branch, stop before committing and hand off branch preparation.
- Do not amend, create empty commits, bypass hooks, spoof metadata, push, create pull requests, merge, rebase, resolve conflicts, or manage branches.
- Do not operate on non-Git version control.
