from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import (
    check_body,
    check_links,
    check_unknown_fields,
    load_frontmatter,
    optional_bool,
    require_string,
    string_list,
    string_mapping,
)
from .github_hooks import validate_hooks_mapping
from .github_mcp import validate_mcp_servers_mapping
from .model import ValidationResult

FIELDS = {
    "name",
    "description",
    "target",
    "tools",
    "model",
    "disable-model-invocation",
    "user-invocable",
    "infer",
    "mcp-servers",
    "metadata",
    "argument-hint",
    "agents",
    "handoffs",
    "hooks",
}
FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
TOOL_AGENT_ALIASES = {"agent", "custom-agent", "Task", "*"}


def _validate_handoffs(value: Any, result: ValidationResult, *, strict: bool) -> None:
    if not isinstance(value, list):
        result.error("handoffs: expected list")
        return
    allowed = {"label", "agent", "prompt", "send", "model"}
    for index, item in enumerate(value):
        context = f"handoffs[{index}]"
        if not isinstance(item, dict):
            result.error(f"{context}: expected mapping")
            continue
        check_unknown_fields(item, allowed, result, strict=strict, context=context)
        for key in ("label", "agent"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                result.error(f"{context}.{key}: required non-empty string")
        for key in ("prompt", "model"):
            if key in item and not isinstance(item[key], str):
                result.error(f"{context}.{key}: expected string")
        if "send" in item and not isinstance(item["send"], bool):
            result.error(f"{context}.send: expected boolean")


def validate_agent(
    path: Path, boundary: Path, *, strict: bool, profile: str
) -> ValidationResult:
    result = ValidationResult()
    loaded = load_frontmatter(path, result, required=True)
    if loaded is None:
        return result
    data, body, _ = loaded
    check_unknown_fields(data, FIELDS, result, strict=strict)
    require_string(data, "description", result, required=True)
    require_string(data, "name", result)
    require_string(data, "argument-hint", result)
    if not FILENAME_RE.fullmatch(path.stem.replace(".agent", "")):
        result.error("filename contains unsupported characters")

    target = data.get("target")
    if target is not None and target not in {"vscode", "github-copilot"}:
        result.error("target: expected 'vscode' or 'github-copilot'")
    if profile == "github-agent" and target == "vscode":
        result.error("target conflicts with github-agent profile")
    if profile == "vscode-agent" and target == "github-copilot":
        result.error("target conflicts with vscode-agent profile")

    tools: list[str] | None = None
    if "tools" in data:
        tools = string_list(data["tools"], result, "tools", allow_comma_string=True)
    if "agents" in data:
        agents = string_list(data["agents"], result, "agents", allow_wildcard=True)
        if (
            agents is not None
            and tools is not None
            and not (set(tools) & TOOL_AGENT_ALIASES)
        ):
            result.error(
                "agents: explicit tools must include the "
                "agent/custom-agent/Task alias or '*'"
            )

    model = data.get("model")
    if model is not None:
        if profile == "github-agent" or target == "github-copilot":
            if not isinstance(model, str):
                result.error("model: GitHub cloud custom agents require a string")
        elif not isinstance(model, str):
            string_list(model, result, "model")

    for key in ("disable-model-invocation", "user-invocable", "infer"):
        optional_bool(data, key, result)
    if "infer" in data:
        result.warn("infer is retired; use user-invocable and disable-model-invocation")
    if "metadata" in data:
        string_mapping(data["metadata"], result, "metadata")
    if "handoffs" in data:
        _validate_handoffs(data["handoffs"], result, strict=strict)
    if "mcp-servers" in data:
        result.extend(
            validate_mcp_servers_mapping(data["mcp-servers"], strict=strict),
            prefix="mcp-servers",
        )
    if "hooks" in data:
        result.extend(
            validate_hooks_mapping(
                data["hooks"], strict=strict, profile="vscode-hooks", context="hooks"
            )
        )

    cloud = profile == "github-agent" or target == "github-copilot"
    vscode = profile == "vscode-agent" or target == "vscode"
    if cloud:
        for key in ("argument-hint", "agents", "handoffs", "hooks"):
            if key in data:
                result.error(f"{key}: not supported by GitHub cloud custom agents")
        check_body(body, result, max_chars=30_000)
    else:
        check_body(body, result)
    if vscode:
        for key in ("mcp-servers", "metadata"):
            if key in data:
                result.error(f"{key}: not used by VS Code custom agents")
    if target is None and profile == "agent":
        mixed = set(data) & {"mcp-servers", "metadata"} and set(data) & {
            "argument-hint",
            "agents",
            "handoffs",
            "hooks",
        }
        if mixed:
            result.warn(
                "agent mixes GitHub-cloud-only and VS-Code-only fields; "
                "set target and split adapters"
            )

    check_links(path, boundary, result)
    return result
