# Source Workspace (`src/`)

Primary workspace for developing, editing, validating, and distributing AI agent assets (skills, prompts, rules, agents).

---

## Guidelines

- **Branching**: Develop features inside dedicated branches following `<lead-id>/<type>/<name>` format (e.g., `mols/feat/git-commit-vcs`).
- **Structure**: Create task-specific subdirectories per asset type or feature.
- **Testing & Validation**: Validate assets using `agent-asset-studio` and add test cases in `tests/`.
- **Deployment**: Commit and merge feature branches into `main` after validation passes.
