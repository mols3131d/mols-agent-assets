---
description: Load and apply all agent rules
---

# Init

## Take Over

1. [handover](`~/.agent/brain/handover.md`)
2. [feedback](`~/.agent/brain/feedback.md`)

## Run CMD

- to prepare the environment

1. [activate]
   - **IF** Virtual environment not active:
     - Run `scripts/activate.*`

2. [uv sync]
   - **SCAN**: Check for changes in `pyproject.toml` or `uv.lock`.
   - **IF** Delta exists (or environment is fresh):
     - Run `uv sync --all-groups`
