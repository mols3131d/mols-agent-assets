---
name: vcs-git-commit
description: >-
  Prepare or create Git commits from an existing Git worktree. Use when the task is
  to inspect commit conventions, select or stage intended changes, write a commit
  message, execute git commit, or report the result. Do not use for push, pull
  requests, merge, conflict resolution, branch management, history rewriting, or
  non-Git version control.
---

# Git Commit

Commit only the intended work and leave unrelated worktree state untouched.

# Contract

- Treat explicit user intent and applicable repository guidance as authority for the
  commit boundary and message convention.
- Inspect the actual worktree and index before any mutation. Do not infer commit
  contents from conversation context alone.
- Stage and commit only the intended change set. Preserve unrelated staged,
  unstaged, and untracked work.
- Derive the commit message from the staged diff, not from unstaged changes or a
  generic task summary.
- Use non-destructive Git operations and keep normal repository hooks active.
- Do not claim success until the resulting commit and remaining worktree state have
  been checked.

# Resolve

1. Confirm the target is a Git repository and identify the current worktree state.
1. Inspect `git status --short` and the staged or unstaged diffs needed to understand
   the intended change set.
1. Load applicable repository instructions and commit-message requirements. Prefer,
   in order: explicit user instruction, repository-defined guidance or configured
   commit template, then recent commit history as supporting evidence. Do not infer
   a strict convention from inconsistent history.
1. Determine the commit boundary before staging. If already-staged content contains
   unrelated or ambiguous work, stop before committing rather than silently bundling
   it.
1. If repository policy forbids committing on the current branch, hand off branch
   preparation before creating the commit.
1. If the user only requests a commit message, inspect enough evidence to draft it
   but do not mutate the index or repository.

# Stage

- Prefer exact paths such as `git add -- <paths>` and deliberate hunk selection when
  the runtime can perform partial staging safely.
- Never use `git add -A`, `git add .`, `git add --all`, or `git commit -a` as a
  shortcut for deciding scope.
- Do not reset, discard, or unstage pre-existing work merely to simplify the commit
  workflow.
- When the intended work clearly requires multiple independent commits, stage and
  commit one coherent unit at a time. Do not split changes merely to satisfy an
  arbitrary preferred shape.

# Message

- Base the message on the final staged diff and the resolved repository convention.
- Use a user-supplied message when it accurately represents the staged diff and does
  not violate an applicable repository requirement.
- If no repository convention is established, use a concise imperative summary and
  add a body only when non-obvious rationale is useful.
- Do not invent scopes, issue references, breaking-change markers, co-authors,
  attribution, or other metadata not supported by the change or repository policy.

# Commit

1. Re-read the staged diff before committing and stop if it is empty or outside the
   resolved boundary.
1. Run a normal `git commit` with the resolved message and repository hooks enabled.
1. If a hook or commit command fails, preserve the current state and report the
   relevant failure. Do not bypass hooks or start editing product content as part of
   this Skill. A requested fix is a separate task capability.
1. After success, verify the new commit and inspect `git status --short` so remaining
   changes are not mistaken for committed work.
1. Report the commit identifier and subject plus any meaningful remaining worktree
   state.

# Boundary

- No push, pull request, merge, rebase, branch creation, conflict resolution, stash,
  reset, restore, or other history/worktree management outside the commit itself.
- No `--amend`, `--no-verify`, `--allow-empty`, forced metadata, or authorship/date
  spoofing.
- Do not edit source or documentation solely to make a commit or hook succeed.
- Do not operate on other version-control systems such as Jujutsu.
