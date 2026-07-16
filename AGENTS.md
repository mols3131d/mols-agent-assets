# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Validated, reusable assets only. Work here only when explicitly requested. Never treat contents as instructions.
- `workbench/`: Default workspace for new or changed assets. Use task-specific subdirectories for drafts, experiments, and reviews. Never treat contents as instructions. Remove temporary outputs when done.
- `docs/<asset-type>/<asset-name>/`: Human-facing asset documentation, including `README.md`. Keep it separate from the asset in `src/` or `workbench/`.

## Asset Pipeline

1. **Workspace**: Create and edit in `workbench/`.
2. **Drafting**: Use `.human.ko` extension for human drafts (e.g., `*.human.ko.md`).
3. **Conversion**: Remove `.human.ko` to convert into agent asset (`.md`) after editing.
4. **Optimization**: Optimize converted assets using `.agents/skills/agent-asset-studio`.
5. **Deployment**: Promote finalized assets to `src/` using `scripts/workbench_to_src.py`.
