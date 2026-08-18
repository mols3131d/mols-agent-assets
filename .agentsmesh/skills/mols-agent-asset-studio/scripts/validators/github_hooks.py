from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import check_unknown_fields, load_json, string_list, string_mapping
from .model import ValidationResult

GITHUB_EVENTS = {
    "agentStop",
    "errorOccurred",
    "notification",
    "permissionRequest",
    "postToolUse",
    "postToolUseFailure",
    "preCompact",
    "preToolUse",
    "sessionEnd",
    "sessionStart",
    "subagentStart",
    "subagentStop",
    "userPromptSubmitted",
    "userPromptTransformed",
}
GITHUB_PASCAL_EVENTS = {
    "AgentStop",
    "ErrorOccurred",
    "Notification",
    "PermissionRequest",
    "PostToolUse",
    "PostToolUseFailure",
    "PreCompact",
    "PreToolUse",
    "SessionEnd",
    "SessionStart",
    "SubagentStart",
    "SubagentStop",
    "UserPromptSubmitted",
    "UserPromptTransformed",
}
VSCODE_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "PreCompact",
    "SubagentStart",
    "SubagentStop",
    "Stop",
}
COMMAND_FIELDS = {
    "type",
    "bash",
    "powershell",
    "command",
    "windows",
    "linux",
    "osx",
    "cwd",
    "env",
    "timeout",
    "timeoutSec",
    "matcher",
}
HTTP_FIELDS = {
    "type",
    "url",
    "headers",
    "allowedEnvVars",
    "timeout",
    "timeoutSec",
    "matcher",
}
PROMPT_FIELDS = {"type", "prompt", "matcher"}
TOP_FIELDS = {"version", "disableAllHooks", "hooks"}


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _validate_hook_item(
    item: Any, event: str, result: ValidationResult, *, strict: bool, context: str
) -> None:
    if not isinstance(item, dict):
        result.error(f"{context}: expected object")
        return
    hook_type = item.get("type", "command")
    if hook_type == "command":
        check_unknown_fields(
            item, COMMAND_FIELDS, result, strict=strict, context=context
        )
        commands = [
            item.get(key)
            for key in ("bash", "powershell", "command", "windows", "linux", "osx")
        ]
        if not any(isinstance(value, str) and value.strip() for value in commands):
            result.error(
                f"{context}: command hook needs bash, powershell, command, "
                "windows, linux, or osx"
            )
        for key in (
            "bash",
            "powershell",
            "command",
            "windows",
            "linux",
            "osx",
            "cwd",
            "matcher",
        ):
            if key in item and not isinstance(item[key], str):
                result.error(f"{context}.{key}: expected string")
        if "env" in item:
            string_mapping(item["env"], result, f"{context}.env")
    elif hook_type == "http":
        check_unknown_fields(item, HTTP_FIELDS, result, strict=strict, context=context)
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            result.error(f"{context}.url: required http(s) URL")
        if (
            event.lower() in {"pretooluse", "permissionrequest"}
            and isinstance(url, str)
            and not url.startswith("https://")
        ):
            result.error(f"{context}.url: decision hooks require https://")
        if "headers" in item:
            string_mapping(item["headers"], result, f"{context}.headers")
        if "allowedEnvVars" in item:
            string_list(item["allowedEnvVars"], result, f"{context}.allowedEnvVars")
    elif hook_type == "prompt":
        check_unknown_fields(
            item, PROMPT_FIELDS, result, strict=strict, context=context
        )
        if event.lower() != "sessionstart":
            result.error(f"{context}: prompt hooks are only supported on sessionStart")
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            result.error(f"{context}.prompt: required non-empty string")
    else:
        result.error(f"{context}.type: expected command, http, or prompt")
    for key in ("timeout", "timeoutSec"):
        if key in item and not _positive_number(item[key]):
            result.error(f"{context}.{key}: expected positive number")


def validate_hooks_mapping(
    hooks: Any,
    *,
    strict: bool,
    profile: str,
    context: str = "hooks",
) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(hooks, dict) or not hooks:
        result.error(f"{context}: expected non-empty object")
        return result
    allowed = (
        VSCODE_EVENTS
        if profile == "vscode-hooks"
        else GITHUB_EVENTS | GITHUB_PASCAL_EVENTS
    )
    for event, items in hooks.items():
        if event not in allowed:
            result.error(f"{context}: unsupported {profile} event {event!r}")
            continue
        if not isinstance(items, list):
            result.error(f"{context}.{event}: expected array")
            continue
        for index, item in enumerate(items):
            _validate_hook_item(
                item,
                event,
                result,
                strict=strict,
                context=f"{context}.{event}[{index}]",
            )
    return result


def validate_hooks_file(path: Path, *, strict: bool, profile: str) -> ValidationResult:
    result = ValidationResult()
    data = load_json(path, result)
    if data is None:
        return result
    if not isinstance(data, dict):
        result.error("top level must be an object")
        return result
    check_unknown_fields(data, TOP_FIELDS, result, strict=strict, context="hook config")
    if profile == "github-hooks":
        if data.get("version") != 1:
            result.error("version: GitHub hook files require integer 1")
    elif "version" in data and data["version"] != 1:
        result.error("version: when present, expected integer 1")
    if "disableAllHooks" in data and not isinstance(data["disableAllHooks"], bool):
        result.error("disableAllHooks: expected boolean")
    if "hooks" not in data:
        result.error("hooks: required object")
    else:
        result.extend(
            validate_hooks_mapping(data["hooks"], strict=strict, profile=profile)
        )
    return result
