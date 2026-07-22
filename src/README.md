# Source Workspace (`src/`)

Primary workspace for developing, editing, and testing AI agent assets.

---

## Guidelines

- **Structure**: Create task-specific subdirectories per asset or feature.
- **Testing**: Add or update test fixtures in `tests/`.
- **Promotion**: Promote validated assets to `release/`:

  ```bash
  uv run python scripts/src_to_release.py skills/<skill-name>
  ```
