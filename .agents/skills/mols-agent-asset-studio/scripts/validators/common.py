from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .model import ValidationResult

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_text(path: Path, result: ValidationResult) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.error(f"cannot read UTF-8 text: {exc}")
        return None


def load_frontmatter(
    path: Path,
    result: ValidationResult,
    *,
    required: bool,
) -> tuple[dict[str, Any], str, str] | None:
    text = load_text(path, result)
    if text is None:
        return None
    match = FRONTMATTER_RE.match(text)
    if not match:
        if required:
            result.error("missing YAML frontmatter")
            return None
        return {}, text, ""
    raw = match.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        result.error(f"invalid YAML frontmatter: {exc}")
        return None
    if data is None:
        data = {}
    if not isinstance(data, dict):
        result.error("frontmatter must be a mapping")
        return None
    return data, text[match.end() :], raw


def load_yaml(path: Path, result: ValidationResult) -> tuple[Any, str] | None:
    text = load_text(path, result)
    if text is None:
        return None
    try:
        return yaml.safe_load(text), text
    except yaml.YAMLError as exc:
        result.error(f"invalid YAML: {exc}")
        return None


def load_json(path: Path, result: ValidationResult) -> Any | None:
    text = load_text(path, result)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        result.error(f"invalid JSON: {exc}")
        return None


def check_unknown_fields(
    data: dict[str, Any],
    allowed: set[str],
    result: ValidationResult,
    *,
    strict: bool,
    context: str = "frontmatter",
) -> None:
    for key in sorted(set(data) - allowed):
        message = f"{context}: unknown field {key!r}"
        if strict:
            result.error(message)
        else:
            result.warn(message)


def require_string(
    data: dict[str, Any],
    key: str,
    result: ValidationResult,
    *,
    required: bool = False,
    nonempty: bool = True,
    max_length: int | None = None,
) -> str | None:
    value = data.get(key)
    if value is None:
        if required:
            result.error(f"{key}: required string is missing")
        return None
    if not isinstance(value, str):
        result.error(f"{key}: expected string, got {type(value).__name__}")
        return None
    if nonempty and not value.strip():
        result.error(f"{key}: must not be empty")
    if max_length is not None and len(value) > max_length:
        result.error(f"{key}: exceeds {max_length} characters")
    return value


def optional_bool(data: dict[str, Any], key: str, result: ValidationResult) -> None:
    if key in data and not isinstance(data[key], bool):
        result.error(f"{key}: expected boolean, got {type(data[key]).__name__}")


def string_list(
    value: Any,
    result: ValidationResult,
    context: str,
    *,
    allow_comma_string: bool = False,
    allow_wildcard: bool = False,
) -> list[str] | None:
    if allow_wildcard and value == "*":
        return ["*"]
    if allow_comma_string and isinstance(value, str):
        items = [part.strip() for part in value.split(",") if part.strip()]
        if not items and value.strip():
            result.error(f"{context}: invalid comma-separated string")
        return items
    if not isinstance(value, list):
        result.error(f"{context}: expected list of strings")
        return None
    if not all(isinstance(item, str) and item.strip() for item in value):
        result.error(f"{context}: every item must be a non-empty string")
        return None
    return list(value)


def string_mapping(
    value: Any, result: ValidationResult, context: str
) -> dict[str, str] | None:
    if not isinstance(value, dict):
        result.error(f"{context}: expected mapping")
        return None
    bad = [
        key
        for key, item in value.items()
        if not isinstance(key, str) or not isinstance(item, str)
    ]
    if bad:
        result.error(f"{context}: keys and values must be strings")
        return None
    return dict(value)


def check_body(
    body: str, result: ValidationResult, *, max_chars: int | None = None
) -> None:
    if not body.strip():
        result.error("Markdown body is empty")
    if max_chars is not None and len(body) > max_chars:
        result.error(f"Markdown body exceeds {max_chars} characters")


def check_links(path: Path, boundary: Path, result: ValidationResult) -> None:
    text = load_text(path, result)
    if text is None:
        return
    for target in LINK_RE.findall(text):
        clean = target.split("#", 1)[0].strip()
        if not clean or "://" in clean or clean.startswith(("mailto:", "#", "${")):
            continue
        resolved = (path.parent / clean).resolve()
        try:
            resolved.relative_to(boundary.resolve())
        except ValueError:
            result.error(f"link escapes validation boundary: {target}")
            continue
        if not resolved.exists():
            result.error(f"broken relative link: {target}")


def safe_relative_path(
    value: str, result: ValidationResult, context: str
) -> Path | None:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        result.error(f"{context}: must be a non-escaping relative path")
        return None
    return path


def check_no_symlinks(root: Path, result: ValidationResult) -> None:
    for path in root.rglob("*"):
        if path.is_symlink():
            result.error(f"symlink is not allowed: {path.relative_to(root)}")
