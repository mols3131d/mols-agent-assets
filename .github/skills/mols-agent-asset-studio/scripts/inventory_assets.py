from __future__ import annotations

import argparse
import json
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}


def classify(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root)
    name = path.name
    if name == "SKILL.md":
        return "skill"
    if name == "AGENTS.md" or name.endswith(".instructions.md"):
        return "instruction"
    if name.endswith(".prompt.md"):
        return "prompt"
    if "agents" in rel.parts and name.endswith((".agent.md", ".md")):
        return "custom-agent"
    if "hooks" in rel.parts and name.endswith(".json"):
        return "hook"
    if name == "mcp.json":
        return "mcp-config"
    return None


def inventory(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        kind = classify(path, root)
        if kind:
            rows.append({"type": kind, "path": rel.as_posix()})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory agent assets in a repository."
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = inventory(args.root.resolve())
    if args.format == "json":
        text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    else:
        lines = ["| Type | Path |", "|---|---|"]
        lines += [f"| {row['type']} | `{row['path']}` |" for row in rows]
        text = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
