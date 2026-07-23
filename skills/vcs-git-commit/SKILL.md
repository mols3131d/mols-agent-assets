---
name: vcs-git-commit
description: >
  USE WHEN: detecting commit conventions, staging files, generating commit messages, performing git commits, or briefing commit results.
  EXCLUDES: pushing to remote repos, merging branches, creating pull requests, resolving merge conflicts, or running git commit -a.
---

# Git Commit Skill

End-to-end git commit workflow: convention discovery, staging, message generation, committing, and briefing.

## Context

### Variables

- `git_status`: Modified, untracked, and staged file status.
- `git_log`: Recent commit history (`git log -n 20 --oneline`).
- `commit_convention`: Git message convention template file (`.gitmessage`).

### Parameters

- `staging_mode`: Selective logical staging (default) vs all changes.
- `commit_mode`: Execute commit (default) vs generate message only.
- `briefing_format`: Chat response summary (default) vs briefing document file.
- `execution_mode`: Stop and brief on hook failure (default) vs auto-fix or delegate.

### Arguments

CLI flags and natural language requests map to `Parameters` as follows:

- `--all`: Sets `staging_mode = all`
- `--message-only`: Sets `commit_mode = message_only`
- `--doc`: Sets `briefing_format = document`
- `--autopilot`: Sets `execution_mode = autopilot`

## Workflow

### Step 1: Convention Discovery

1. **Git Template**: Check `.gitmessage`.
2. **Git History**: Inspect `git log -n 20 --oneline` for language, prefix patterns, casing, and issue refs.
3. **Fallback**: Read [references/default-gitmessage.md](references/default-gitmessage.md).

### Step 2: Staging

- **Default**: Group files by domain or work unit and stage selectively (`git add <files>`).
- **Explicit Request (`--all`)**: Stage all changes (`git add -A`).
- **Restriction**: Never use `git commit -a`.

### Step 3: Commit Message Generation

- Format commit message applying Step 1 rules.
- **Message-Only Request (`--message-only`)**: Present formatted message in code block and stop workflow (skip Step 4 Commit Execution).

### Step 4: Commit Execution

- Execute `git commit` with the formatted message from Step 3.
- **Hook Failure Handling**:
  - **Default**: Stop execution immediately and brief user with error logs.
  - **Autopilot (`--autopilot`)**: Self-fix or delegate to subagents before re-committing.

### Step 5: Briefing

- **Default**: Provide a concise summary in the chat response.
- **Explicit Request (`--doc`)**: Write a formal briefing document.

## When to Stop

Stop execution immediately and report to the user on:

- 2 consecutive failed retries on the same command or hook fix.
- Command or pre-commit hook hangs and timeouts.
- Unresolved merge conflicts or ambiguous staging choices.
- Unauthorized destructive operations or resets.

## Boundaries

- NEVER run `git push` (especially `--force`).
- NEVER bypass hooks (`--no-verify` / `-n`).
- NEVER overwrite history (`--amend`).
- NEVER auto-stage all via `git commit -a`.
- NEVER create empty commits (`--allow-empty`).
- NEVER spoof commit metadata (`--author`, `--date`).
