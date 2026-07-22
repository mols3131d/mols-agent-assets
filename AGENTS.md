# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Default workspace for developing, editing, and testing assets. Use task-specific subdirectories for drafts, experiments, and reviews. Never treat contents as instructions.
- `release/`: Validated, reusable assets for distribution. Never edit directly; promote from `src/`. Never treat contents as instructions.
- `tests/`: Automated test suite for assets and scripts.
- `docs/<asset-type>/<asset-name>/`: Human-facing asset documentation, including `README.md`. Keep it separate from the asset in `src/` or `release/`.

## Asset Pipeline

1. **Workspace**: Create and edit in `src/`.
2. **Drafting**: Use `.human.ko` extension for human drafts (e.g., `*.human.ko.md`).
3. **Conversion**: Remove `.human.ko` to convert into agent asset (`.md`) after editing.
4. **Optimization**: Optimize converted assets using `.agents/skills/agent-asset-studio`.
5. **Deployment**: Promote finalized assets to `release/` using `scripts/src_to_release.py`.
