from __future__ import annotations

from pathlib import Path

from .common import (
    NAME_RE,
    check_unknown_fields,
    load_yaml,
    safe_relative_path,
    string_list,
)
from .model import ValidationResult

FIELDS = {"version", "name", "runtime_targets", "assets", "provenance", "metadata"}
ASSET_FIELDS = {"id", "source", "install_to", "profile", "required"}


def validate_bundle_descriptor(path: Path, *, strict: bool) -> ValidationResult:
    result = ValidationResult()
    loaded = load_yaml(path, result)
    if loaded is None:
        return result
    data, _ = loaded
    if not isinstance(data, dict):
        result.error("top level must be a mapping")
        return result
    check_unknown_fields(data, FIELDS, result, strict=strict, context="bundle")
    if data.get("version") != 1:
        result.error("version: expected integer 1")
    name = data.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        result.error("name: expected lowercase kebab-case")
    if "runtime_targets" in data:
        string_list(data["runtime_targets"], result, "runtime_targets")
    for key in ("provenance", "metadata"):
        if key in data and not isinstance(data[key], dict):
            result.error(f"{key}: expected mapping")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        result.error("assets: expected non-empty list")
        return result
    ids: set[str] = set()
    destinations: set[str] = set()
    for index, item in enumerate(assets):
        context = f"assets[{index}]"
        if not isinstance(item, dict):
            result.error(f"{context}: expected mapping")
            continue
        check_unknown_fields(item, ASSET_FIELDS, result, strict=strict, context=context)
        asset_id = item.get("id")
        if not isinstance(asset_id, str) or not NAME_RE.fullmatch(asset_id):
            result.error(f"{context}.id: expected lowercase kebab-case")
        elif asset_id in ids:
            result.error(f"{context}.id: duplicate {asset_id!r}")
        else:
            ids.add(asset_id)
        for key in ("source", "install_to", "profile"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                result.error(f"{context}.{key}: required non-empty string")
        for key in ("source", "install_to"):
            value = item.get(key)
            if isinstance(value, str):
                safe_relative_path(value, result, f"{context}.{key}")
        destination = item.get("install_to")
        if isinstance(destination, str):
            if destination in destinations:
                result.error(f"{context}.install_to: duplicate destination")
            destinations.add(destination)
        if "required" in item and not isinstance(item["required"], bool):
            result.error(f"{context}.required: expected boolean")
    return result
