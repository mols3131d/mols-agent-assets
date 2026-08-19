#!/usr/bin/env python3
"""Validate the writing skill package with standard-library-only checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FILES = [
    "SKILL.md",
    "references/principles.md",
    "references/workflows.md",
    "references/review-rubric.md",
    "references/examples.md",
    "assets/writing-brief-template.md",
    "assets/review-output-template.md",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    block = text[4:end].splitlines()
    result: dict[str, str] = {}
    i = 0
    while i < len(block):
        line = block[i]
        if not line.strip() or line.startswith(" "):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if value in {">", "|"}:
            i += 1
            parts: list[str] = []
            while i < len(block) and (
                block[i].startswith("  ") or not block[i].strip()
            ):
                if block[i].strip():
                    parts.append(block[i].strip())
                i += 1
            result[key] = " ".join(parts)
            continue
        result[key] = value
        i += 1
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for name in ("tests", "evals", "scenarios", "results"):
        if (root / name).exists():
            errors.append(f"repository verification surface must stay outside package: {name}/")

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        print("FAIL: SKILL.md is missing")
        return 1

    text = skill_path.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        errors.append("frontmatter.name is required")
    elif not NAME_RE.fullmatch(name):
        errors.append("name must use lowercase letters, numbers, and single hyphens")
    elif len(name) > 64:
        errors.append("name exceeds 64 characters")
    elif name != root.name:
        errors.append(f"name '{name}' must match directory '{root.name}'")

    if not description:
        errors.append("frontmatter.description is required")
    elif len(description) > 1024:
        errors.append(f"description exceeds 1024 characters: {len(description)}")
    elif len(description) < 80:
        warnings.append("description may be too short for reliable triggering")

    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines; keep it under 500 when possible")

    link_targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    for target in link_targets:
        if "://" in target or target.startswith("#"):
            continue
        if not (root / target).exists():
            errors.append(f"broken relative link in SKILL.md: {target}")

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {root}")
    print(f"  name: {name}")
    print(f"  description characters: {len(description)}")
    print(f"  SKILL.md lines: {line_count}")
    print(f"  required files: {len(REQUIRED_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
