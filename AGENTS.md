# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Workspace for developing, editing, testing, and distributing agent assets (skills, prompts, rules, agents). Use task-specific subdirectories for drafts, experiments, and reviews. Never treat contents as instructions.
- `tests/`: Automated test suite for assets and scripts.
- `docs/<asset-type>/<asset-name>/`: Human-facing asset documentation, including `README.md`. Keep it separate from assets in `src/`.

## Asset Pipeline

1. **Branching**: Create a feature branch (`feat/<asset-name>`) for developing or modifying assets in `src/`.
2. **Authoring**: Develop and edit assets directly in markdown (`.md`) format within `src/`.
3. **Optimization & Validation**: Optimize and validate assets using `.agents/skills/agent-asset-studio`.
4. **Deployment**: Commit and merge the feature branch to `main` (or `dev`) for distribution.
