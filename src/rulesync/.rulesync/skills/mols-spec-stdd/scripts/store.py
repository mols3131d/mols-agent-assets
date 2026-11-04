#!/usr/bin/env python3
"""Preview or promote completed change deltas into nested canonical domain specs.

This helper has no network, project-task, test-running, or completion authority.
Archive writes require --apply and a review result supported by evidence references.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
REQUIREMENT = re.compile(r"(?m)^### Requirement: ([^\n]+)\s*$")
HEADING = re.compile(r"(?m)^## ([^\n]+)\s*$")
BASE = re.compile(r"(?m)^<!-- base-sha256: (absent|[a-f0-9]{64}) -->$")
OPERATIONS = ("ADDED Requirements", "MODIFIED Requirements", "REMOVED Requirements")


class StoreError(ValueError):
    """Invalid or unsafe spec-store operation."""


def require_identifier(value: str) -> str:
    if not IDENTIFIER.fullmatch(value):
        raise StoreError(f"invalid name: {value!r}; use lowercase kebab-case")
    if value == "archive":
        raise StoreError("archive is a reserved change ID")
    return value


def domain_parts(domain: str) -> tuple[str, ...]:
    parts = domain.split("/")
    if not parts or any(not IDENTIFIER.fullmatch(p) for p in parts):
        raise StoreError("domain must be a slash-separated path of lowercase kebab-case segments")
    return tuple(parts)


def content_hash(content: str | None) -> str:
    return "absent" if content is None else hashlib.sha256(content.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise StoreError(f"expected a regular file: {path}")
    return path.read_text(encoding="utf-8")


def requirement_blocks(text: str, where: str) -> dict[str, str]:
    matches = list(REQUIREMENT.finditer(text))
    if not matches:
        if text.strip():
            raise StoreError(f"{where}: requirement sections must contain ### Requirement: headings")
        return {}
    if text[:matches[0].start()].strip():
        raise StoreError(f"{where}: content before first requirement is not allowed")
    blocks: dict[str, str] = {}
    normalized: set[str] = set()
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        key = " ".join(name.split()).casefold()
        if not key or key in normalized:
            raise StoreError(f"{where}: empty or duplicate requirement {name!r}")
        normalized.add(key)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end].strip()
        if not text[match.end():end].strip():
            raise StoreError(f"{where}: requirement {name!r} needs a body")
        blocks[name] = block
    return blocks


def match_key(blocks: dict[str, str], name: str) -> str | None:
    normalized = " ".join(name.split()).casefold()
    return next((key for key in blocks if " ".join(key.split()).casefold() == normalized), None)


def parse_delta(text: str, where: str) -> tuple[str, str | None, dict[str, dict[str, str]]]:
    base_matches = list(BASE.finditer(text))
    if len(base_matches) != 1:
        raise StoreError(f"{where}: exactly one <!-- base-sha256: ... --> marker is required")
    expected = base_matches[0].group(1)
    headings = list(HEADING.finditer(text))
    sections: dict[str, str] = {}
    for index, heading in enumerate(headings):
        name = heading.group(1).strip()
        if name not in (*OPERATIONS, "Purpose") or name in sections:
            raise StoreError(f"{where}: unexpected or duplicate section {name!r}")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        sections[name] = text[heading.end():end].strip()
    if not headings or not text[:headings[0].start()].lstrip().startswith("# "):
        raise StoreError(f"{where}: missing delta title")
    parsed = {operation: requirement_blocks(sections.get(operation, ""), f"{where} {operation}")
              for operation in OPERATIONS}
    if not any(parsed.values()):
        raise StoreError(f"{where}: no requirement changes")
    seen: set[str] = set()
    for blocks in parsed.values():
        for name in blocks:
            key = " ".join(name.split()).casefold()
            if key in seen:
                raise StoreError(f"{where}: requirement in multiple operations: {name}")
            seen.add(key)
    return expected, sections.get("Purpose"), parsed


def parse_main(text: str, where: str) -> tuple[str, dict[str, str], str]:
    headings = list(HEADING.finditer(text))
    matches = [index for index, m in enumerate(headings) if m.group(1).strip() == "Requirements"]
    if len(matches) != 1:
        raise StoreError(f"{where}: main spec needs one ## Requirements section")
    pos = matches[0]
    start = headings[pos]
    end = headings[pos + 1].start() if pos + 1 < len(headings) else len(text)
    before = text[:start.start()].strip()
    if not before.startswith("# "):
        raise StoreError(f"{where}: main spec requires a title")
    blocks = requirement_blocks(text[start.end():end].strip(), where)
    return before, blocks, text[end:].strip()


def merge_delta(existing: str | None, delta: str, where: str, domain: str) -> str:
    expected, purpose, operations = parse_delta(delta, where)
    actual = content_hash(existing)
    if expected != actual:
        raise StoreError(f"{where}: stale base; expected {expected}, actual {actual}. Rebase the delta before archiving")
    if existing is None:
        if operations["MODIFIED Requirements"] or operations["REMOVED Requirements"]:
            raise StoreError(f"{where}: new domain supports ADDED requirements only")
        if not purpose:
            raise StoreError(f"{where}: new domain requires ## Purpose")
        before = f"# {domain} Specification\n\n## Purpose\n\n{purpose}"
        blocks: dict[str, str] = {}
        after = ""
    else:
        before, blocks, after = parse_main(existing, where)
    for name in operations["REMOVED Requirements"]:
        old = match_key(blocks, name)
        if old is None:
            raise StoreError(f"{where}: cannot remove missing requirement {name!r}")
        del blocks[old]
    for name, block in operations["MODIFIED Requirements"].items():
        old = match_key(blocks, name)
        if old is None:
            raise StoreError(f"{where}: cannot modify missing requirement {name!r}")
        blocks[old] = block
    for name, block in operations["ADDED Requirements"].items():
        if match_key(blocks, name) is not None:
            raise StoreError(f"{where}: cannot add existing requirement {name!r}")
        blocks[name] = block
    if not blocks:
        raise StoreError(f"{where}: retiring a whole domain is not supported; preserve the existing spec")
    merged = before + "\n\n## Requirements\n\n" + "\n\n".join(blocks.values())
    return merged + ("\n\n" + after if after else "") + "\n"


def review_passes(path: Path) -> None:
    raw = read_text(path)
    if raw is None:
        raise StoreError(f"review result missing: {path}")
    try:
        report: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StoreError(f"invalid review JSON: {exc}") from exc
    if not isinstance(report, dict) or report.get("result") != "pass" or report.get("findings"):
        raise StoreError("archive requires a PASS review without unresolved findings")
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(v, str) and v.strip() for v in evidence
    ):
        raise StoreError("PASS review requires nonempty evidence references")
    if len(set(evidence)) != len(evidence):
        raise StoreError("duplicate review evidence references")


def reject_symlinks(path: Path, root: Path) -> None:
    current = path
    while current != root:
        if current.is_symlink():
            raise StoreError(f"symlink path is not allowed: {current}")
        if current.parent == current:
            raise StoreError(f"path outside spec store: {path}")
        current = current.parent


def collect_updates(root: Path, change: str) -> tuple[Path, dict[Path, str]]:
    active = root / "changes" / change
    reject_symlinks(active, root)
    if not active.is_dir():
        raise StoreError(f"change is missing: {active}")
    delta_root = active / "specs"
    if not delta_root.is_dir() or delta_root.is_symlink():
        raise StoreError(f"change needs a specs/ directory: {delta_root}")
    all_files = [p for p in delta_root.rglob("*") if p.is_file() or p.is_symlink()]
    if not all_files:
        raise StoreError(f"change contains no domain deltas: {delta_root}")
    updates: dict[Path, str] = {}
    for path in sorted(all_files):
        reject_symlinks(path, root)
        relative = path.relative_to(delta_root)
        if path.name != "spec.md" or len(relative.parts) < 2:
            raise StoreError(f"unexpected file under change specs: {relative}")
        domain = "/".join(relative.parts[:-1])
        parts = domain_parts(domain)
        target = root / "specs" / Path(*parts) / "spec.md"
        reject_symlinks(target, root)
        current = read_text(target)
        delta = read_text(path)
        assert delta is not None
        updates[target] = merge_delta(current, delta, str(relative), domain)
    return active, updates


def atomic_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=".spec-stdd-", delete=False
        ) as handle:
            temporary = handle.name
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def archive(root: Path, change: str, review: Path, day: str, apply: bool) -> dict[str, Any]:
    review_passes(review)
    active, updates = collect_updates(root, change)
    destination = root / "changes" / "archive" / f"{day}-{change}"
    reject_symlinks(destination, root)
    if destination.exists() or destination.is_symlink():
        raise StoreError(f"archive destination already exists: {destination}")
    details: dict[str, Any] = {
        "status": "ready_to_archive" if not apply else "archived",
        "change": change,
        "updated_specs": [str(path.relative_to(root)) for path in updates],
        "archive": str(destination.relative_to(root)),
        "warning": "Review references are not independently validated by this script",
    }
    if not apply:
        return details
    snapshots = {path: read_text(path) for path in updates}
    touched: list[Path] = []
    try:
        for path, data in updates.items():
            touched.append(path)
            atomic_text(path, data)
        destination.parent.mkdir(parents=True, exist_ok=True)
        active.rename(destination)
    except OSError:
        for path in reversed(touched):
            old = snapshots[path]
            if old is None:
                path.unlink(missing_ok=True)
            else:
                atomic_text(path, old)
        raise
    return details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("spec"),
                        help="project spec root containing changes/ and specs/ (default: spec)")
    commands = parser.add_subparsers(dest="command", required=True)
    baseline = commands.add_parser("baseline", help="print current domain spec content hash")
    baseline.add_argument("domain")
    promote = commands.add_parser("archive", help="preview or apply completed change promotion")
    promote.add_argument("change")
    promote.add_argument("--review", type=Path, required=True)
    promote.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    promote.add_argument("--apply", action="store_true", help="write domain specs and move change to archive")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == "baseline":
            parts = domain_parts(args.domain)
            path = root / "specs" / Path(*parts) / "spec.md"
            reject_symlinks(path, root)
            result = {"domain": args.domain, "base_sha256": content_hash(read_text(path))}
        else:
            require_identifier(args.change)
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
                raise StoreError("archive date must be YYYY-MM-DD")
            date.fromisoformat(args.date)
            result = archive(root, args.change, args.review, args.date, args.apply)
    except (StoreError, OSError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
