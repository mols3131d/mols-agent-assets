#!/usr/bin/env python3
"""Initialize Kanban workspace directory with configuration files and default guides."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def initialize_kanban(kanban_path: str | Path) -> None:
    path = Path(kanban_path).resolve()

    # 1. Create Directories
    directories = [
        path,
        path / ".configs",
        path / "backlog",
        path / "active",
        path / "archive",
    ]
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {d}")

    # Resolve skill assets path
    # Script is at src/skills/mols-kanban-markdown/scripts/initialize.py
    skill_path = Path(__file__).parent.parent
    assets_dir = skill_path / "assets" / "default"

    # 2. Copy Reference Configuration Files
    copy_targets = [
        (assets_dir / "config.jsonc", path / ".configs" / "config.jsonc"),
        (assets_dir / "template.md", path / ".configs" / "template.md"),
        (assets_dir / "default_AGENTS.md", path / "AGENTS.md"),
    ]

    for src, dst in copy_targets:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied {src.name} to {dst}")
        else:
            print(f"Warning: Source file {src} does not exist", file=sys.stderr)

    # 3. Initialize Kanban Index Document
    readme_path = path / "README.md"
    if not readme_path.exists():
        readme_content = (
            f"# Kanban Board\n\n"
            f"Initialized on {Path(kanban_path).name}.\n\n"
            f"Use this space to track task cards in "
            f"`backlog/`, `active/`, and `archive/` directories.\n"
        )
        readme_path.write_text(readme_content, encoding="utf-8")
        print(f"Created README.md in {path}")

    # 4. Verify Directory Integrity
    expected_paths = [
        path / ".configs" / "config.jsonc",
        path / ".configs" / "template.md",
        path / "AGENTS.md",
        path / "README.md",
    ]

    missing_paths = [p for p in expected_paths if not p.exists()]
    if missing_paths:
        print("Verification failed! Missing files:", file=sys.stderr)
        for p in missing_paths:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    print("Kanban board successfully initialized!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python initialize.py <kanban_path>", file=sys.stderr)
        sys.exit(1)

    initialize_kanban(sys.argv[1])
