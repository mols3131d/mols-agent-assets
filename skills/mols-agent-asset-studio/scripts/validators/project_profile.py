from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import check_unknown_fields, load_yaml, safe_relative_path, string_list
from .model import ValidationResult

FIELDS = {
    "version",
    "project",
    "asset_roots",
    "runtimes",
    "sources_of_truth",
    "validation",
    "policy",
}
COMMAND_FIELDS = {"id", "argv", "cwd", "timeout_sec", "required"}
CI_FIELDS = {"id", "required"}
POLICY_FIELDS = {
    "allow_network",
    "allow_package_install",
    "allow_publish",
    "preserve_attribution",
}


def _validate_commands(value: Any, result: ValidationResult, *, strict: bool) -> None:
    if not isinstance(value, list):
        result.error("validation.local_commands: expected list")
        return
    ids: set[str] = set()
    for index, item in enumerate(value):
        context = f"validation.local_commands[{index}]"
        if isinstance(item, str):
            result.warn(
                f"{context}: shell string is legacy-only and cannot be "
                "executed; use id + argv list"
            )
            continue
        if not isinstance(item, dict):
            result.error(f"{context}: expected mapping")
            continue
        check_unknown_fields(
            item, COMMAND_FIELDS, result, strict=strict, context=context
        )
        command_id = item.get("id")
        if not isinstance(command_id, str) or not command_id.strip():
            result.error(f"{context}.id: required non-empty string")
        elif command_id in ids:
            result.error(f"{context}.id: duplicate {command_id!r}")
        else:
            ids.add(command_id)
        argv = item.get("argv")
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(arg, str) and arg for arg in argv)
        ):
            result.error(f"{context}.argv: expected non-empty list of strings")
        cwd = item.get("cwd", ".")
        if not isinstance(cwd, str):
            result.error(f"{context}.cwd: expected string")
        else:
            safe_relative_path(cwd, result, f"{context}.cwd")
        timeout = item.get("timeout_sec", 120)
        if (
            not isinstance(timeout, int)
            or isinstance(timeout, bool)
            or not 1 <= timeout <= 3600
        ):
            result.error(f"{context}.timeout_sec: expected integer 1..3600")
        if "required" in item and not isinstance(item["required"], bool):
            result.error(f"{context}.required: expected boolean")


def _validate_ci(value: Any, result: ValidationResult, *, strict: bool) -> None:
    if not isinstance(value, list):
        result.error("validation.ci_lanes: expected list")
        return
    for index, item in enumerate(value):
        context = f"validation.ci_lanes[{index}]"
        if isinstance(item, str):
            continue
        if not isinstance(item, dict):
            result.error(f"{context}: expected string or mapping")
            continue
        check_unknown_fields(item, CI_FIELDS, result, strict=strict, context=context)
        if not isinstance(item.get("id"), str) or not item["id"].strip():
            result.error(f"{context}.id: required non-empty string")
        if "required" in item and not isinstance(item["required"], bool):
            result.error(f"{context}.required: expected boolean")


def validate_project_profile(path: Path, *, strict: bool) -> ValidationResult:
    result = ValidationResult()
    loaded = load_yaml(path, result)
    if loaded is None:
        return result
    data, _ = loaded
    if not isinstance(data, dict):
        result.error("top level must be a mapping")
        return result
    check_unknown_fields(data, FIELDS, result, strict=strict, context="project profile")
    if data.get("version") != 1:
        result.error("version: expected integer 1")
    if "project" in data and not isinstance(data["project"], dict):
        result.error("project: expected mapping")
    if "runtimes" in data:
        string_list(data["runtimes"], result, "runtimes")
    roots = data.get("asset_roots")
    if roots is not None:
        if not isinstance(roots, dict):
            result.error("asset_roots: expected mapping")
        else:
            for group, values in roots.items():
                items = string_list(values, result, f"asset_roots.{group}")
                if items:
                    for value in items:
                        safe_relative_path(value, result, f"asset_roots.{group}")
    if "sources_of_truth" in data and not isinstance(
        data["sources_of_truth"], (dict, list)
    ):
        result.error("sources_of_truth: expected mapping or list")
    validation = data.get("validation")
    if validation is not None:
        if not isinstance(validation, dict):
            result.error("validation: expected mapping")
        else:
            check_unknown_fields(
                validation,
                {"local_commands", "ci_lanes"},
                result,
                strict=strict,
                context="validation",
            )
            if "local_commands" in validation:
                _validate_commands(validation["local_commands"], result, strict=strict)
            if "ci_lanes" in validation:
                _validate_ci(validation["ci_lanes"], result, strict=strict)
    policy = data.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            result.error("policy: expected mapping")
        else:
            check_unknown_fields(
                policy, POLICY_FIELDS, result, strict=strict, context="policy"
            )
            for key, value in policy.items():
                if key in POLICY_FIELDS and not isinstance(value, bool):
                    result.error(f"policy.{key}: expected boolean")
    return result
