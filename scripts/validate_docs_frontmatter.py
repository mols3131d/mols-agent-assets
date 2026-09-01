#!/usr/bin/env python3
"""Validate repository documentation frontmatter from ``frontmatter.json``."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_DIR = ROOT / "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts"
sys.path.insert(0, str(VALIDATOR_DIR))

from validate_frontmatter import validate_frontmatter  # noqa: E402

WORKSPACE_TOKEN = "[[workspace]]"
ROLE_EXCLUDED_NAMES = {"AGENTS.md", "DIRECTIVE.md", "SKILL.md"}
ROLE_EXCLUDED_SUFFIXES = (".agent.md", ".instructions.md", ".prompt.md")
FIELD_TYPES = {"string": str}


def _load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("frontmatter config root must be an object")
    return data


def _schema(content_type: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fields = content_type.get("fields")
    if not isinstance(fields, list):
        raise ValueError("content type fields must be an array")

    schema: dict[str, dict[str, Any]] = {}
    for field in fields:
        if not isinstance(field, dict):
            raise ValueError("frontmatter field must be an object")
        name = field.get("name")
        type_name = field.get("type")
        if not isinstance(name, str) or not name:
            raise ValueError("frontmatter field name must be a non-empty string")
        if type_name not in FIELD_TYPES:
            raise ValueError(f"unsupported frontmatter field type: {type_name}")
        schema[name] = {
            "type": FIELD_TYPES[type_name],
            "required": field.get("required") is True,
        }
    return schema


def _content_types(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items = config.get("frontMatter.taxonomy.contentTypes")
    if not isinstance(items, list):
        raise ValueError("frontmatter content types must be an array")

    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise ValueError("frontmatter content type must have a string name")
        result[item["name"]] = item
    return result


def _matches_exclude(path: Path, patterns: list[str]) -> bool:
    for pattern in patterns:
        candidates = [pattern]
        if pattern.startswith("**/"):
            candidates.append(pattern[3:])
        if any(path.match(candidate) for candidate in candidates):
            return True
    return False


def _is_document(path: Path, relative: Path, exclude_patterns: list[str]) -> bool:
    name = path.name
    if name in ROLE_EXCLUDED_NAMES or name.startswith("."):
        return False
    if any(name.endswith(suffix) for suffix in ROLE_EXCLUDED_SUFFIXES):
        return False
    if name.startswith("__") and name.endswith("__.md"):
        return False
    return not _matches_exclude(relative, exclude_patterns)


def validate_docs_frontmatter(
    root: Path = ROOT,
    config_path: Path | None = None,
) -> list[str]:
    """Return repository-relative paths whose documentation frontmatter is invalid."""
    config_path = config_path or root / "frontmatter.json"
    config = _load_config(config_path)
    content_types = _content_types(config)
    page_folders = config.get("frontMatter.content.pageFolders")
    if not isinstance(page_folders, list):
        raise ValueError("frontmatter page folders must be an array")

    failures: list[str] = []
    for page_folder in page_folders:
        if not isinstance(page_folder, dict):
            raise ValueError("frontmatter page folder must be an object")
        configured_path = page_folder.get("path")
        names = page_folder.get("contentTypes")
        excludes = page_folder.get("excludePaths", [])
        if not isinstance(configured_path, str):
            raise ValueError("frontmatter page folder path must be a string")
        if (
            not isinstance(names, list)
            or len(names) != 1
            or not isinstance(names[0], str)
        ):
            raise ValueError("frontmatter page folder must declare one content type")
        if not isinstance(excludes, list) or not all(
            isinstance(item, str) for item in excludes
        ):
            raise ValueError("frontmatter excludePaths must be a string array")
        if names[0] not in content_types:
            raise ValueError(f"unknown frontmatter content type: {names[0]}")

        rendered = configured_path.replace(WORKSPACE_TOKEN, str(root))
        directory = Path(rendered)
        if not directory.is_absolute():
            directory = root / directory
        if not directory.is_dir():
            raise NotADirectoryError(directory)

        schema = _schema(content_types[names[0]])
        for path in sorted(directory.rglob("*.md")):
            relative = path.relative_to(directory)
            if not _is_document(path, relative, excludes):
                continue
            if not validate_frontmatter(path, schema=schema):
                failures.append(path.relative_to(root).as_posix())

    return failures


def main() -> int:
    try:
        failures = validate_docs_frontmatter()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if failures:
        for path in failures:
            print(f"FAIL {path}", file=sys.stderr)
        return 1

    print("PASS documentation frontmatter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
