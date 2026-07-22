# Asset Development Guide

Guide for creating, editing, optimizing, and promoting AI agent assets in `mols-agent-assets`.

---

## Directory Roles

- `src/`: Workspace for creating, editing, and experimenting on draft assets.
- `release/`: Production-ready, validated distribution assets. Never edit directly.
- `scripts/src_to_release.py`: Promotion script to move verified assets from `src/` to `release/`.

## Development Pipeline

1. **Drafting (`src/`)**:
   - Create new asset drafts using `.human.ko.md` extension for initial human-readable notes.
   - Remove `.human.ko` extension when converting into active markdown assets (`.md`).

2. **Optimization (`agent-asset-studio`)**:
   - Use the `agent-asset-studio` skill to compress, format, and structure asset files.

3. **Promotion to Release**:
   - Promote validated assets from `src/` to `release/`:

     ```bash
     uv run python scripts/src_to_release.py skills/<skill-name>
     ```
