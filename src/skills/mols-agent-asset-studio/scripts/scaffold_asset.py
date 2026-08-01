from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def ensure_new(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"target exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a minimal portable skill or explicit VS Code asset."
    )
    parser.add_argument(
        "type", choices=("skill", "vscode-agent", "vscode-instruction", "vscode-prompt")
    )
    parser.add_argument("name")
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument(
        "--description",
        default="Describe what this asset does. Use when the matching task occurs.",
    )
    parser.add_argument("--apply-to", default="**")
    args = parser.parse_args()
    if not NAME_RE.fullmatch(args.name):
        parser.error("name must be lowercase kebab-case")
    root = args.path.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.type == "skill":
        target = root / args.name
        ensure_new(target)
        target.mkdir()
        text = (
            f"---\nname: {q(args.name)}\n"
            f"description: {q(args.description)}\n---\n\n"
            f"# {args.name.replace('-', ' ').title()}\n\n"
            "## Goal\n\n## Workflow\n\n## Validation\n"
        )
        (target / "SKILL.md").write_text(text, encoding="utf-8")
    elif args.type == "vscode-agent":
        target = root / f"{args.name}.agent.md"
        ensure_new(target)
        target.write_text(
            f"---\nname: {q(args.name)}\n"
            f"description: {q(args.description)}\n"
            f"target: {q('vscode')}\n---\n\n"
            "# Role\n\n# Scope\n\n# Workflow\n\n# Output\n",
            encoding="utf-8",
        )
    elif args.type == "vscode-instruction":
        target = root / f"{args.name}.instructions.md"
        ensure_new(target)
        target.write_text(
            f"---\nname: {q(args.name)}\n"
            f"description: {q(args.description)}\n"
            f"applyTo: {q(args.apply_to)}\n---\n\n"
            "# Instructions\n",
            encoding="utf-8",
        )
    else:
        target = root / f"{args.name}.prompt.md"
        ensure_new(target)
        target.write_text(
            f"---\nname: {q(args.name)}\n"
            f"description: {q(args.description)}\n---\n\n"
            "# Task\n\n# Inputs\n\n# Output\n",
            encoding="utf-8",
        )
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
