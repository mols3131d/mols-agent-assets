"""Markdown YAML frontmatter 공통 파서."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_frontmatter_document(content: str) -> tuple[dict[str, Any], str] | None:
    """문서의 YAML frontmatter와 본문을 반환한다."""
    try:
        import yaml
    except ImportError as error:
        raise ImportError("dependency 'yaml' is missing") from error

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    end = next(
        (index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"),
        None,
    )
    if end is None:
        return None

    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None

    return data, "\n".join(lines[end + 1 :])


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str] | None:
    """Markdown 파일의 frontmatter와 본문을 읽는다."""
    if not path.is_file():
        return None
    return parse_frontmatter_document(path.read_text(encoding="utf-8"))
