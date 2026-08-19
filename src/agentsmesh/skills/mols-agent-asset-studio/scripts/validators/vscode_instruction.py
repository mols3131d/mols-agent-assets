from __future__ import annotations

from pathlib import Path

from .common import (
    check_body,
    check_links,
    check_unknown_fields,
    load_frontmatter,
    require_string,
)
from .model import ValidationResult

FIELDS = {"name", "description", "applyTo"}


def validate_instruction(
    path: Path, boundary: Path, *, strict: bool, profile: str
) -> ValidationResult:
    result = ValidationResult()
    if profile in {"agents-md", "copilot-instructions"}:
        text = path.read_text(encoding="utf-8")
        check_body(text, result)
        check_links(path, boundary, result)
        return result
    loaded = load_frontmatter(path, result, required=False)
    if loaded is None:
        return result
    data, body, _ = loaded
    check_unknown_fields(data, FIELDS, result, strict=strict)
    for key in FIELDS:
        require_string(data, key, result)
    check_body(body, result)
    check_links(path, boundary, result)
    return result
