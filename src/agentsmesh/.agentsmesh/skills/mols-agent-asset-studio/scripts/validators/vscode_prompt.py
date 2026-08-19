from __future__ import annotations

from pathlib import Path

from .common import (
    check_body,
    check_links,
    check_unknown_fields,
    load_frontmatter,
    require_string,
    string_list,
)
from .model import ValidationResult

FIELDS = {"description", "name", "argument-hint", "agent", "model", "tools"}


def validate_prompt(path: Path, boundary: Path, *, strict: bool) -> ValidationResult:
    result = ValidationResult()
    loaded = load_frontmatter(path, result, required=False)
    if loaded is None:
        return result
    data, body, _ = loaded
    check_unknown_fields(data, FIELDS, result, strict=strict)
    for key in FIELDS - {"tools"}:
        require_string(data, key, result)
    if "tools" in data:
        string_list(data["tools"], result, "tools")
    check_body(body, result)
    check_links(path, boundary, result)
    return result
