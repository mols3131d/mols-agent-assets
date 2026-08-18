# Git Commit Skill Help Guide (`--help`)

Help guide for `vcs-git-commit` skill providing prompt patterns, option flag combinations, convention configuration, and practical scenarios.

---

## 1. Basic Usage

Triggers automatically when requesting commit actions using natural language prompts.

- **Default Commit Request**:
  - `"Commit my changes"` / `"Please commit current work"`
  - *Behavior*: Selective logical staging ➔ Read `.gitmessage` convention ➔ Format & execute commit ➔ Report summary in chat

---

## 2. Options and Flags

Control skill execution by combining option flags or natural language expressions:

### Stage All Changes (`--all`)

- **Example**: `"Commit all files"`, `"Run commit --all"`
- **Purpose**: Stage all modified and untracked files (`git add -A`) instead of selective domain staging.

### Generate Briefing Document (`--doc`)

- **Example**: `"Commit and create a summary document"`, `"Run commit --doc"`
- **Purpose**: Output a formal briefing document instead of a chat summary.

### Autopilot Hook Self-Fix (`--autopilot`)

- **Example**: `"Run commit on autopilot"`, `"Commit --autopilot"`
- **Purpose**: Automatically fix pre-commit hook errors or delegate to subagents instead of stopping for manual intervention.

### Message Only (`--message-only`)

- **Example**: `"Generate commit message only"`, `"Draft message --message-only"`
- **Purpose**: Generate and display the formatted commit message in a code block without executing `git commit` (skips Step 4 Commit Execution).

---

## 3. Customizing Commit Conventions

- **Mechanism**: `vcs-git-commit` prioritizes template structure and comment rules defined in `.gitmessage` at the repository root.
- **How to Customise**:
  1. Edit `.gitmessage` in the repository root (template format, allowed commit types, line caps, or comment guidelines).
  2. The agent automatically detects and applies updated `.gitmessage` rules on subsequent commit requests.
  3. If `.gitmessage` does not exist, the fallback specification (`references/default-gitmessage.md`) applies.

---

## 4. Practical Scenarios

1. **Custom Commit Message Override**:
   - Prompt `"feat: implement login API"` overrides convention discovery and applies the custom message directly.
2. **Handling Pre-commit Hook Failures**:
   - Default mode stops and briefs hook error output. Request `"Fix hook error and re-commit --autopilot"` to auto-repair and complete commit.
