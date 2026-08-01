from __future__ import annotations

import argparse
import json
from pathlib import Path

from project_profile import discover_profile

CANDIDATES = [
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    ".github/copilot-instructions.md",
    "docs/ARCHITECTURE.md",
    "docs/architecture.md",
    "docs/DECISIONS.md",
    "docs/decisions.md",
]
SKIP = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a bounded project profile and resolve Studio policy."
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-absolute-root", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    present = [path for rel in CANDIDATES if (path := root / rel).is_file()]
    skills = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("SKILL.md")
        if not path.is_symlink()
        and not any(part in SKIP for part in path.relative_to(root).parts)
    )
    try:
        profile_source, profile_path, policy = discover_profile(root, args.profile)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    payload = {
        "root": str(root) if args.include_absolute_root else ".",
        "evidence_files": [path.relative_to(root).as_posix() for path in present],
        "skills": skills,
        "studio_profile": {
            "source": profile_source,
            "path": profile_path.relative_to(root).as_posix()
            if profile_path and profile_path.is_relative_to(root)
            else None,
            "data": policy,
        },
        "notes": [
            "This is a mechanical inventory, not an interpretation of project intent.",
            "Read authoritative evidence in project-profile.md order before tuning.",
        ],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
