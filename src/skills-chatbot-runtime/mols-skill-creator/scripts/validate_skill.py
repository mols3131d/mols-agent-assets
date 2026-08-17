#!/usr/bin/env python3
"""Validate a directory-based skill source package without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---\n"):
        return {}, "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, "frontmatter closing delimiter not found"
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"unsupported frontmatter line: {line}"
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    return fields, None


def validate(root: Path) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        errors.append("missing required file: SKILL.md")

    # Personal repository convention: maintainer-only docs belong in .docs/.
    # A docs/ directory is not universally invalid because an external Skill may use it
    # as a runtime resource, so require classification rather than assuming intent.
    if (root / "docs").exists():
        warnings.append("docs/ present; classify runtime-required material vs maintainer-only .docs/")

    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        fields, error = parse_frontmatter(text)
        if error:
            errors.append(error)
        else:
            name = fields.get("name", "")
            description = fields.get("description", "")
            if not name:
                errors.append("frontmatter.name is required")
            elif not NAME_RE.fullmatch(name):
                errors.append("frontmatter.name must be lowercase hyphen-case")
            if name and root.name != name:
                warnings.append(f"folder name '{root.name}' differs from skill name '{name}'")
            if not description:
                errors.append("frontmatter.description is required")
            elif len(description) < 40:
                warnings.append("description may be too short to explain function and triggers")
        line_count = len(text.splitlines())
        if line_count > 500:
            warnings.append(f"SKILL.md has {line_count} lines; consider progressive disclosure")

    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).split("#", 1)[0]
            if not raw:
                continue
            target = (md.parent / raw).resolve()
            if not target.exists():
                errors.append(f"broken relative link in {md.relative_to(root)}: {match.group(1)}")

    for forbidden in ["__pycache__", ".pytest_cache", ".mypy_cache"]:
        if any(path.name == forbidden for path in root.rglob(forbidden)):
            warnings.append(f"cache directory present: {forbidden}")

    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.skill.resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    result = validate(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARN: {item}")
        if not result["errors"]:
            print("PASS")

    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
