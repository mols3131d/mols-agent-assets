#!/usr/bin/env python3
"""Initialize a minimal directory-based skill source package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--description", default="TODO: Describe what the skill does and when to use it.")
    args = parser.parse_args()

    if not NAME_RE.fullmatch(args.name):
        print("error: name must use lowercase letters, digits, and hyphens", file=sys.stderr)
        return 2

    target = args.path / args.name
    if target.exists() and any(target.iterdir()):
        print(f"error: target is not empty: {target}", file=sys.stderr)
        return 2

    template_root = Path(__file__).resolve().parent.parent / "assets" / "templates"
    (target / ".docs" / "baseline").mkdir(parents=True, exist_ok=True)

    title = " ".join(part.capitalize() for part in args.name.split("-"))
    values = {
        "skill_name": args.name,
        "title": title,
        "description": args.description,
        "purpose": "TODO: Define the durable purpose.",
        "requirement": "TODO: Define a concrete requirement.",
        "allowed_scope": "TODO: Define allowed changes and operations.",
        "decision": "TODO: Record a major adopted decision.",
        "rejected_decision": "TODO: Record a major rejected decision when valuable.",
        "rationale": "TODO: Explain why.",
    }

    for source_name, relative_target in [
        ("SKILL.md", "SKILL.md"),
        ("DIRECTIVE.md", ".docs/baseline/DIRECTIVE.md"),
        ("WORKING.md", ".docs/WORKING.md"),
    ]:
        source = (template_root / source_name).read_text(encoding="utf-8")
        destination = target / relative_target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render(source, values), encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
