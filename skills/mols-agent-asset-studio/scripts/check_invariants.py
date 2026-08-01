from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check literal behavior invariants after refactor or consolidation."
    )
    parser.add_argument("target_root", type=Path)
    parser.add_argument("invariants", type=Path)
    args = parser.parse_args()
    root = args.target_root.resolve()
    data = yaml.safe_load(args.invariants.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        print("ERROR: invariants must be a mapping with version: 1")
        return 1
    errors: list[str] = []
    for rel in data.get("required_paths", []):
        if (
            not isinstance(rel, str)
            or Path(rel).is_absolute()
            or ".." in Path(rel).parts
        ):
            errors.append(f"required_paths: unsafe path {rel!r}")
            continue
        candidate = root / rel
        if candidate.is_symlink():
            errors.append(f"required_paths: symlink is not allowed: {rel}")
            continue
        try:
            candidate.resolve().relative_to(root)
        except ValueError:
            errors.append(f"required_paths: path escapes root: {rel}")
            continue
        if not candidate.exists():
            errors.append(f"missing required path: {rel}")
    files = data.get("files", {})
    if not isinstance(files, dict):
        errors.append("files: expected mapping")
        files = {}
    for rel, checks in files.items():
        if (
            not isinstance(rel, str)
            or Path(rel).is_absolute()
            or ".." in Path(rel).parts
        ):
            errors.append(f"files: unsafe path {rel!r}")
            continue
        path = root / rel
        if path.is_symlink():
            errors.append(f"files: symlink is not allowed: {rel}")
            continue
        try:
            path.resolve().relative_to(root)
        except ValueError:
            errors.append(f"files: path escapes root: {rel}")
            continue
        if not path.is_file():
            errors.append(f"missing invariant file: {rel}")
            continue
        if not isinstance(checks, dict):
            errors.append(f"files.{rel}: expected mapping")
            continue
        text = path.read_text(encoding="utf-8")
        for literal in checks.get("literal_strings", []):
            if not isinstance(literal, str) or literal not in text:
                errors.append(f"{rel}: missing literal {literal!r}")
        for heading in checks.get("headings", []):
            if not isinstance(heading, str) or heading not in text.splitlines():
                errors.append(f"{rel}: missing heading {heading!r}")
        for pattern in checks.get("regexes", []):
            if not isinstance(pattern, str):
                errors.append(f"{rel}: regex must be string")
                continue
            try:
                matched = re.search(pattern, text, re.MULTILINE) is not None
            except re.error as exc:
                errors.append(f"{rel}: invalid regex {pattern!r}: {exc}")
                continue
            if not matched:
                errors.append(f"{rel}: regex did not match {pattern!r}")
        position = -1
        for item in checks.get("ordered_strings", []):
            if not isinstance(item, str):
                errors.append(f"{rel}: ordered item must be string")
                continue
            found = text.find(item, position + 1)
            if found < 0:
                errors.append(f"{rel}: missing or out-of-order string {item!r}")
                break
            position = found
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS: {args.invariants}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
