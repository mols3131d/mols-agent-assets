#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
# ]
# ///
"""Shared utilities for mols-kanban-markdown scripts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_jsonc(text: str) -> Any:
    """Parse JSON text with comments (JSONC)."""
    lines = []
    in_multiline_comment = False

    for line in text.splitlines():
        if in_multiline_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                in_multiline_comment = False
            else:
                continue

        if "/*" in line:
            if "*/" in line:
                parts = line.split("/*", 1)
                before = parts[0]
                after = parts[1].split("*/", 1)[1]
                line = before + after
            else:
                line = line.split("/*", 1)[0]
                in_multiline_comment = True

        # Remove single line comments starting with // but not part of URL
        line = re.sub(r"(?<!http:)(?<!https:)//.*", "", line)

        stripped = line.strip()
        if stripped:
            lines.append(stripped)

    cleaned = "\n".join(lines)
    return json.loads(cleaned)


def parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter block from markdown content."""
    try:
        import yaml
    except ImportError as error:
        raise ImportError("dependency 'yaml' is missing") from error

    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None

    yaml_lines = []
    found_end = False
    for line in lines[1:]:
        if line == "---":
            found_end = True
            break
        yaml_lines.append(line)

    if not found_end:
        return None

    try:
        data = yaml.safe_load("\n".join(yaml_lines))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def load_kanban_config(kanban_path: Path) -> dict[str, Any] | None:
    """Load config.jsonc from a Kanban directory."""
    config_file = kanban_path / ".configs" / "config.jsonc"
    if not config_file.is_file():
        return None

    try:
        return parse_jsonc(config_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error loading config file {config_file}: {e}", file=sys.stderr)
        return None


def get_card_files(kanban_path: Path) -> list[Path]:
    """Retrieve all card markdown files in backlog, active, and archive folders."""
    target_dirs = ["backlog", "active", "archive"]
    markdown_files: list[Path] = []

    for d in target_dirs:
        dir_path = kanban_path / d
        if dir_path.is_dir():
            for md_file in dir_path.glob("**/*.md"):
                if md_file.name not in ["README.md", "AGENTS.md", "template.md"]:
                    markdown_files.append(md_file)

    if kanban_path.is_file() and kanban_path.suffix == ".md":
        markdown_files = [kanban_path]

    return markdown_files
