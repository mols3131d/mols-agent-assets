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
    """Read only the top-level fields this lightweight validator needs.

    Full Agent Skills YAML conformance is repository/test or reference-validator
    responsibility; this dependency-free helper must not reject valid block scalars
    or nested optional metadata merely because it does not fully parse YAML.
    """
    if not text.startswith("---\n"):
        return {}, "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, "frontmatter closing delimiter not found"

    lines = text[4:end].splitlines()
    fields: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            i += 1
            continue
        if ":" not in line:
            return {}, f"unsupported top-level frontmatter line: {line}"

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            style = value[0]
            i += 1
            parts: list[str] = []
            while i < len(lines):
                child = lines[i]
                if child.strip() and not child[:1].isspace():
                    break
                if child.strip():
                    parts.append(child.strip())
                elif style == "|":
                    parts.append("")
                i += 1
            fields[key] = " ".join(parts) if style == ">" else "\n".join(parts).strip()
            continue

        fields[key] = value.strip('"\'')
        i += 1

    return fields, None


def validate(root: Path) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        errors.append("missing required file: SKILL.md")

    # docs/ may be a legitimate runtime resource in an external Skill. Classify it
    # rather than assuming placement. In this repository, maintainer-only documentation
    # belongs outside the package under docs/skills/<skill-name>/ when it is actually needed.
    if (root / "docs").exists():
        warnings.append(
            "docs/ present; confirm it is runtime-required rather than maintainer-only documentation"
        )
    if (root / ".docs").exists():
        warnings.append(
            ".docs/ present; migrate maintainer-only docs to the target project's external maintainer-doc surface"
        )

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
