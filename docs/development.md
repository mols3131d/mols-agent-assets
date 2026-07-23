# Asset Development Guide

Guide for creating, editing, optimizing, and deploying AI agent assets (skills, prompts, rules, agents) in `mols-agent-assets`.

---

## Directory Roles

- `src/`: Unified workspace for creating, editing, testing, and distributing agent assets.
- `tests/`: Automated test suite for assets and tools.

## Development Pipeline

1. **Branching (`<lead-id>/<type>/<name>`)**:
   - Create a feature branch using `<lead-id>/<type>/<name>` structure (e.g., `mols/feat/git-commit-vcs`) to work on new or modified assets in `src/`.

2. **Authoring (`src/`)**:
   - Write and edit assets directly in markdown (`.md`) format within `src/`.

3. **Optimization & Validation (`mols-agent-asset-studio`)**:
   - Use the `mols-agent-asset-studio` skill to validate structure and optimize context size.
   - Verify changes using the test suite (`uv run pytest tests/`).

4. **Deployment (Branch Merge)**:
   - Commit and merge the feature branch into `main` after validation passes.
