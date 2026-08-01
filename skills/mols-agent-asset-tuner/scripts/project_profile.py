from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DISCOVERY_PATHS = (Path(".agent-assets/studio.yaml"), Path("agent-assets.yaml"))
DEFAULT_PROFILE: dict[str, Any] = {
    "version": 1,
    "project": {"root": "."},
    "asset_roots": {"canonical": ["src/skills"], "runtime": []},
    "runtimes": [],
    "sources_of_truth": [],
    "validation": {"local_commands": [], "ci_lanes": []},
    "policy": {
        "allow_network": False,
        "allow_package_install": False,
        "allow_publish": False,
        "preserve_attribution": True,
    },
}


def _validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("profile must be a mapping with version: 1")
    for key in ("project", "asset_roots", "validation", "policy"):
        if key in data and not isinstance(data[key], dict):
            raise ValueError(f"{key} must be a mapping")
    if "runtimes" in data and (
        not isinstance(data["runtimes"], list)
        or not all(isinstance(x, str) for x in data["runtimes"])
    ):
        raise ValueError("runtimes must be a list of strings")
    return data


def discover_profile(root: Path, explicit: Path | None = None):
    if explicit is not None:
        selected = explicit.resolve()
        source = "explicit"
    else:
        selected = None
        source = "built-in-defaults"
        for rel in DISCOVERY_PATHS:
            candidate = root / rel
            if candidate.is_file():
                selected = candidate
                source = rel.as_posix()
                break
    if selected is None:
        return source, None, DEFAULT_PROFILE
    data = yaml.safe_load(selected.read_text(encoding="utf-8"))
    return source, selected, _validate(data)
