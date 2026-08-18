from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import check_unknown_fields, load_json, string_list, string_mapping
from .model import ValidationResult

TOP_FIELDS = {"mcpServers"}
SERVER_FIELDS = {"type", "tools", "command", "args", "env", "url", "headers"}
LOCAL_TYPES = {"local", "stdio"}
REMOTE_TYPES = {"http", "sse"}


def validate_mcp_servers_mapping(
    servers: Any,
    *,
    strict: bool,
    context: str = "mcpServers",
) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(servers, dict) or not servers:
        result.error(f"{context}: expected non-empty mapping")
        return result
    for name, config in servers.items():
        server_context = f"{context}.{name}"
        if not isinstance(name, str) or not name.strip():
            result.error(f"{context}: server names must be non-empty strings")
            continue
        if not isinstance(config, dict):
            result.error(f"{server_context}: expected mapping")
            continue
        check_unknown_fields(
            config, SERVER_FIELDS, result, strict=strict, context=server_context
        )
        server_type = config.get("type")
        if server_type not in LOCAL_TYPES | REMOTE_TYPES:
            result.error(f"{server_context}.type: expected local, stdio, http, or sse")
            continue
        if "tools" not in config:
            result.error(f"{server_context}.tools: required list of enabled tools")
        else:
            string_list(config["tools"], result, f"{server_context}.tools")
        if server_type in LOCAL_TYPES:
            if (
                not isinstance(config.get("command"), str)
                or not config["command"].strip()
            ):
                result.error(f"{server_context}.command: required non-empty string")
            if "args" not in config:
                result.error(f"{server_context}.args: required list")
            else:
                string_list(config["args"], result, f"{server_context}.args")
            if "url" in config or "headers" in config:
                result.error(
                    f"{server_context}: local server cannot define url or headers"
                )
        else:
            url = config.get("url")
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                result.error(f"{server_context}.url: required http(s) URL")
            if "command" in config or "args" in config or "env" in config:
                result.error(
                    f"{server_context}: remote server cannot define command, "
                    "args, or env"
                )
        if "env" in config:
            string_mapping(config["env"], result, f"{server_context}.env")
        if "headers" in config:
            string_mapping(config["headers"], result, f"{server_context}.headers")
    return result


def validate_github_mcp(path: Path, *, strict: bool) -> ValidationResult:
    result = ValidationResult()
    data = load_json(path, result)
    if data is None:
        return result
    if not isinstance(data, dict):
        result.error("top level must be an object")
        return result
    check_unknown_fields(data, TOP_FIELDS, result, strict=strict, context="MCP config")
    if "mcpServers" not in data:
        result.error("mcpServers: required object")
        return result
    result.extend(validate_mcp_servers_mapping(data["mcpServers"], strict=strict))
    return result
