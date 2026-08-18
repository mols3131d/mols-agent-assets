from __future__ import annotations

import argparse
import zipfile
from dataclasses import asdict
from pathlib import Path

from asset_common import sha256
from reproducible_zip import FIXED_TIMESTAMP, canonical_json, write_bytes, write_file
from scan_secrets import is_secret_filename, scan_target
from validators.dispatch import validate_target

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tmp",
    "node_modules",
    "dist",
    "build",
}


def collect_files(root: Path) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    excluded: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed: {rel}")
        if not path.is_file():
            continue
        if is_secret_filename(path):
            excluded.append(rel.as_posix())
            continue
        files.append(path)
    return files, excluded


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Strictly validate, secret-scan, and reproducibly package one Agent Skill."
        )
    )
    parser.add_argument("skill_root", type=Path)
    parser.add_argument(
        "--profile", choices=("agent-skill", "openai-skill"), default="agent-skill"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-secret-finding", action="store_true")
    parser.add_argument("--allow-structure-warning", action="store_true")
    args = parser.parse_args()
    root = args.skill_root.resolve()
    output = (args.output or root.parent / f"{root.name}.skill.zip").resolve()
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        print("ERROR: output archive must be outside the skill root")
        return 1

    validation = validate_target(root, profile=args.profile, strict=True)
    structure_warnings = [
        item for item in validation.warnings if item.startswith("structure:")
    ]
    for warning in validation.warnings:
        print(f"WARN: {warning}")
    for error in validation.errors:
        print(f"ERROR: {error}")
    if not validation.ok:
        return 1
    if structure_warnings and not args.allow_structure_warning:
        print(
            "ERROR: packaging blocked by structural warnings; resolve them or "
            "explicitly use --allow-structure-warning"
        )
        return 1

    findings, named_exclusions = scan_target(root)
    if findings and not args.allow_secret_finding:
        for item in findings:
            print(
                f"ERROR: likely secret {item.path}:{item.line} "
                f"{item.kind} {item.redacted}"
            )
        print(
            "ERROR: packaging blocked; inspect findings or explicitly use "
            "--allow-secret-finding"
        )
        return 1
    if findings:
        print("WARN: packaging with explicitly accepted secret findings")

    try:
        files, excluded = collect_files(root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 2,
        "name": root.name,
        "validation_profile": args.profile,
        "reproducible": True,
        "zip_timestamp": "1980-01-01T00:00:00",
        "files": [
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in files
        ],
        "excluded_secret_named_files": sorted(set(excluded) | set(named_exclusions)),
        "accepted_secret_findings": [asdict(item) for item in findings]
        if args.allow_secret_finding
        else [],
    }
    with zipfile.ZipFile(output, "w") as archive:
        for path in files:
            write_file(
                archive, f"{root.name}/{path.relative_to(root).as_posix()}", path
            )
        write_bytes(archive, f"{root.name}/MANIFEST.json", canonical_json(manifest))
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad:
            print(f"ERROR: corrupt ZIP entry: {bad}")
            return 1
        if any(info.date_time != FIXED_TIMESTAMP for info in archive.infolist()):
            print("ERROR: archive contains non-deterministic timestamps")
            return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
