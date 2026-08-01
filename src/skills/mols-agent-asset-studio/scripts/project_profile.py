from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from validators.project_profile import validate_project_profile

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


def discover_profile(
    root: Path, explicit: Path | None = None
) -> tuple[str, Path | None, dict[str, Any]]:
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
    result = validate_project_profile(selected, strict=True)
    if not result.ok:
        raise ValueError("; ".join(result.errors))
    data = yaml.safe_load(selected.read_text(encoding="utf-8"))
    return source, selected, data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover one authoritative Studio project profile."
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument(
        "--profile", type=Path, help="Explicit profile; overrides discovery"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        source, path, data = discover_profile(root, args.profile)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    payload = {
        "source": source,
        "path": path.relative_to(root).as_posix()
        if path and path.is_relative_to(root)
        else (path.name if path else None),
        "profile": data,
        "merge_policy": "single highest-precedence profile; no hidden merge",
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
