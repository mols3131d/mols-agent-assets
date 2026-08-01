from __future__ import annotations

import argparse
import hashlib
import zipfile
from dataclasses import asdict
from pathlib import Path

import yaml
from reproducible_zip import FIXED_TIMESTAMP, canonical_json, write_bytes, write_file
from scan_secrets import is_secret_filename, scan_target
from validators.bundle import validate_bundle_descriptor
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_asset_files(source: Path):
    if source.is_symlink():
        raise ValueError(f"symlink is not allowed: {source}")
    if source.is_file():
        if not is_secret_filename(source):
            yield source, Path(source.name)
        return
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed: {path}")
        if path.is_file() and not is_secret_filename(path):
            yield path, rel


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Strictly validate and reproducibly package a mixed agent asset bundle."
        )
    )
    parser.add_argument("descriptor", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-secret-finding", action="store_true")
    parser.add_argument("--allow-structure-warning", action="store_true")
    args = parser.parse_args()
    descriptor = args.descriptor.resolve()
    descriptor_result = validate_bundle_descriptor(descriptor, strict=True)
    for error in descriptor_result.errors:
        print(f"ERROR: {error}")
    if not descriptor_result.ok:
        return 1
    data = yaml.safe_load(descriptor.read_text(encoding="utf-8"))
    base = descriptor.parent
    output = (args.output or base.parent / f"{data['name']}.bundle.zip").resolve()
    source_roots = [(base / item["source"]).resolve() for item in data["assets"]]
    if output == descriptor:
        print("ERROR: output collides with bundle descriptor")
        return 1
    for source_root in source_roots:
        try:
            output.relative_to(
                source_root if source_root.is_dir() else source_root.parent
            )
        except ValueError:
            continue
        print(
            f"ERROR: output must be outside every asset source boundary: {source_root}"
        )
        return 1

    archive_entries: dict[str, Path] = {}
    manifest_assets = []
    accepted_findings = []
    for item in data["assets"]:
        source = (base / item["source"]).resolve()
        if not source.exists():
            if item.get("required", True):
                print(f"ERROR: missing required asset: {item['source']}")
                return 1
            print(f"WARN: optional asset missing: {item['source']}")
            continue
        try:
            source.relative_to(base.resolve())
        except ValueError:
            print(f"ERROR: source escapes descriptor root: {item['source']}")
            return 1
        validation = validate_target(
            source, profile=item["profile"], strict=True, boundary=base
        )
        structure_warnings = [
            warning
            for warning in validation.warnings
            if warning.startswith("structure:")
        ]
        for warning in validation.warnings:
            print(f"WARN: {item['id']}: {warning}")
        for error in validation.errors:
            print(f"ERROR: {item['id']}: {error}")
        if not validation.ok:
            return 1
        if structure_warnings and not args.allow_structure_warning:
            print(f"ERROR: {item['id']}: packaging blocked by structural warnings")
            return 1
        findings, excluded = scan_target(source)
        if findings and not args.allow_secret_finding:
            for finding in findings:
                print(
                    f"ERROR: {item['id']}: likely secret "
                    f"{finding.path}:{finding.line} {finding.kind}"
                )
            return 1
        accepted_findings.extend(
            {"asset": item["id"], **asdict(finding)} for finding in findings
        )
        destination = Path(item["install_to"])
        file_rows = []
        for path, rel in iter_asset_files(source):
            archive_rel = destination / (rel if source.is_dir() else Path())
            archive_name = archive_rel.as_posix()
            if archive_name in archive_entries:
                print(f"ERROR: bundle path collision: {archive_name}")
                return 1
            archive_entries[archive_name] = path
            file_rows.append(
                {
                    "path": archive_name,
                    "sha256": digest(path),
                    "bytes": path.stat().st_size,
                }
            )
        manifest_assets.append(
            {
                "id": item["id"],
                "source": item["source"],
                "install_to": item["install_to"],
                "profile": item["profile"],
                "files": sorted(file_rows, key=lambda row: row["path"]),
                "excluded_secret_named_files": sorted(excluded),
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 2,
        "name": data["name"],
        "runtime_targets": sorted(data.get("runtime_targets", [])),
        "reproducible": True,
        "zip_timestamp": "1980-01-01T00:00:00",
        "assets": sorted(manifest_assets, key=lambda row: row["id"]),
        "accepted_secret_findings": accepted_findings
        if args.allow_secret_finding
        else [],
    }
    normalized_descriptor = yaml.safe_dump(
        data, allow_unicode=True, sort_keys=True
    ).encode("utf-8")
    with zipfile.ZipFile(output, "w") as archive:
        for archive_name, path in sorted(archive_entries.items()):
            write_file(archive, f"{data['name']}/{archive_name}", path)
        write_bytes(archive, f"{data['name']}/asset-bundle.yaml", normalized_descriptor)
        write_bytes(
            archive, f"{data['name']}/BUNDLE-MANIFEST.json", canonical_json(manifest)
        )
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
