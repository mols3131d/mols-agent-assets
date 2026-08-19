from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

from .common import HEX_COLOR_RE, check_unknown_fields, load_yaml, safe_relative_path
from .model import ValidationResult

INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}
TOP_FIELDS = {"interface", "dependencies"}
DEPENDENCY_FIELDS = {"tools"}
TOOL_FIELDS = {"type", "value", "description", "transport", "url"}


def _check_quoted_strings(path: Path, result: ValidationResult) -> None:
    try:
        node = yaml.compose(path.read_text(encoding="utf-8"))
    except Exception:
        return

    def walk(current: Any, *, is_key: bool = False, context: str = "") -> None:
        if isinstance(current, MappingNode):
            for key, value in current.value:
                key_name = key.value if isinstance(key, ScalarNode) else "?"
                walk(key, is_key=True, context=context)
                walk(
                    value,
                    is_key=False,
                    context=f"{context}.{key_name}" if context else key_name,
                )
        elif isinstance(current, SequenceNode):
            for index, item in enumerate(current.value):
                walk(item, context=f"{context}[{index}]")
        elif (
            isinstance(current, ScalarNode)
            and not is_key
            and current.tag.endswith(":str")
        ):
            if current.style not in {"'", '"'}:
                result.error(f"{context}: OpenAI metadata string values must be quoted")

    if node is not None:
        walk(node)


def validate_openai_interface(
    path: Path, skill_root: Path, *, strict: bool
) -> ValidationResult:
    result = ValidationResult()
    loaded = load_yaml(path, result)
    if loaded is None:
        return result
    data, _ = loaded
    if not isinstance(data, dict):
        result.error("top level must be a mapping")
        return result
    check_unknown_fields(data, TOP_FIELDS, result, strict=strict, context="openai.yaml")
    _check_quoted_strings(path, result)

    interface = data.get("interface")
    if not isinstance(interface, dict):
        result.error("interface: required mapping")
    else:
        check_unknown_fields(
            interface, INTERFACE_FIELDS, result, strict=strict, context="interface"
        )
        for key in INTERFACE_FIELDS & set(interface):
            if not isinstance(interface[key], str) or not interface[key].strip():
                result.error(f"interface.{key}: expected non-empty string")
        short = interface.get("short_description")
        if isinstance(short, str) and not 25 <= len(short) <= 64:
            result.error("interface.short_description: must be 25-64 characters")
        color = interface.get("brand_color")
        if isinstance(color, str) and not HEX_COLOR_RE.fullmatch(color):
            result.error("interface.brand_color: expected #RRGGBB")
        prompt = interface.get("default_prompt")
        skill_name = skill_root.name
        if isinstance(prompt, str) and f"${skill_name}" not in prompt:
            result.error(f"interface.default_prompt: must mention ${skill_name}")
        for key in ("icon_small", "icon_large"):
            value = interface.get(key)
            if isinstance(value, str):
                rel = safe_relative_path(value, result, f"interface.{key}")
                if rel is not None and not (skill_root / rel).is_file():
                    result.error(f"interface.{key}: file does not exist: {value}")

    dependencies = data.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            result.error("dependencies: expected mapping")
        else:
            check_unknown_fields(
                dependencies,
                DEPENDENCY_FIELDS,
                result,
                strict=strict,
                context="dependencies",
            )
            tools = dependencies.get("tools")
            if not isinstance(tools, list):
                result.error("dependencies.tools: expected list")
            else:
                for index, item in enumerate(tools):
                    context = f"dependencies.tools[{index}]"
                    if not isinstance(item, dict):
                        result.error(f"{context}: expected mapping")
                        continue
                    check_unknown_fields(
                        item, TOOL_FIELDS, result, strict=strict, context=context
                    )
                    if item.get("type") != "mcp":
                        result.error(f"{context}.type: only 'mcp' is supported")
                    for key in ("value", "description"):
                        if not isinstance(item.get(key), str) or not item[key].strip():
                            result.error(f"{context}.{key}: required non-empty string")
                    for key in ("transport", "url"):
                        if key in item and not isinstance(item[key], str):
                            result.error(f"{context}.{key}: expected string")
    return result
