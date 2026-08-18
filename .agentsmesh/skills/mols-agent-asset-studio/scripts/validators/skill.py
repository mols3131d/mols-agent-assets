from __future__ import annotations

from pathlib import Path

from .common import (
    NAME_RE,
    check_body,
    check_links,
    check_no_symlinks,
    check_unknown_fields,
    load_frontmatter,
    require_string,
    string_mapping,
)
from .model import ValidationResult
from .openai_interface import validate_openai_interface
from .structure import validate_structure

SPEC_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
OPENAI_FIELDS = {"name", "description"}


def validate_skill(root: Path, *, strict: bool, profile: str) -> ValidationResult:
    result = ValidationResult()
    skill = root / "SKILL.md"
    if not skill.is_file():
        result.error("missing SKILL.md")
        return result
    loaded = load_frontmatter(skill, result, required=True)
    if loaded is None:
        return result
    data, body, _ = loaded
    allowed = OPENAI_FIELDS if profile == "openai-skill" else SPEC_FIELDS
    check_unknown_fields(data, allowed, result, strict=strict)

    name = require_string(data, "name", result, required=True, max_length=64)
    description = require_string(
        data, "description", result, required=True, max_length=1024
    )
    if isinstance(name, str):
        if not NAME_RE.fullmatch(name):
            result.error(
                "name: expected lowercase kebab-case without consecutive hyphens"
            )
        if name != root.name:
            result.error(f"name: {name!r} must match directory {root.name!r}")
    if isinstance(description, str) and "use when" not in description.lower():
        result.warn("description should state activation conditions with 'Use when'")
    if "license" in data and not isinstance(data["license"], str):
        result.error("license: expected string")
    compatibility = data.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            result.error("compatibility: expected non-empty string")
        elif len(compatibility) > 500:
            result.error("compatibility: exceeds 500 characters")
    if "metadata" in data:
        string_mapping(data["metadata"], result, "metadata")
    if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
        result.error("allowed-tools: expected space-separated string")

    check_body(body, result)
    if body.count("\n") + 1 > 500:
        result.warn("SKILL.md exceeds 500 lines")
    check_no_symlinks(root, result)
    result.extend(validate_structure(root), prefix="structure")
    for markdown in root.rglob("*.md"):
        if not markdown.is_symlink():
            check_links(markdown, root, result)
    scripts = root / "scripts"
    if scripts.is_dir():
        for script in scripts.rglob("*.py"):
            if script.is_symlink():
                continue
            try:
                compile(script.read_text(encoding="utf-8"), str(script), "exec")
            except SyntaxError as exc:
                result.error(f"{script.relative_to(root)}: Python syntax error: {exc}")
    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.exists():
        result.extend(
            validate_openai_interface(openai_yaml, root, strict=strict),
            prefix="agents/openai.yaml",
        )
    return result
