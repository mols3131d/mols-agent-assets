#!/usr/bin/env python3
"""생성된 code report Markdown의 기본 계약을 검증한다."""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

LOGGER = logging.getLogger(__name__)
PLACEHOLDER = re.compile(r"{{[^{}]+}}")
LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
CONTRACTS = {
    "summary": {
        "fields": {"title", "datetime", "type", "scope"},
        "type": "code-report-summary",
        "headings": {
            "## Overview",
            "## System Map",
            "## Core Components",
            "## Core Execution Walkthroughs",
            "## Code Reading Guide",
            "## Understanding Notes",
        },
    },
    "detail": {
        "fields": {"title", "description", "type", "domain"},
        "type": "code-report-component",
        "headings": {
            "## Summary",
            "## Responsibility",
            "## Execution Flow",
            "## Boundaries",
            "## Evidence",
        },
    },
}


class ReportValidationError(ValueError):
    """Report가 기본 문서 계약을 위반할 때 발생한다."""


def _frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        raise ReportValidationError("missing frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise ReportValidationError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def _check_links(path: Path, text: str, project_root: Path) -> list[str]:
    errors = []
    for target in LINK.findall(text):
        target = target.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (
            project_root / target.lstrip("/")
            if target.startswith("/")
            else path.parent / target
        )
        if not resolved.resolve().exists():
            errors.append(f"broken link: {target}")
    return errors


def validate_report(
    path: Path,
    report_type: str,
    *,
    project_root: Path,
    check_links: bool = True,
) -> list[str]:
    """Report 오류 목록을 반환한다."""
    if not path.is_file():
        return [f"file not found: {path}"]
    text = path.read_text(encoding="utf-8")
    contract = CONTRACTS[report_type]
    try:
        fields = _frontmatter(text)
    except ReportValidationError as error:
        return [str(error)]

    errors = []
    missing = contract["fields"] - fields.keys()
    if missing:
        errors.append(f"missing frontmatter fields: {sorted(missing)}")
    if fields.get("type") != contract["type"]:
        errors.append(f"invalid type: {fields.get('type')!r}")
    headings: set[str] = set(contract["headings"])
    missing_headings = headings - set(text.splitlines())
    if missing_headings:
        errors.append(f"missing headings: {sorted(missing_headings)}")
    if PLACEHOLDER.search(text):
        errors.append("unresolved placeholder")
    if COMMENT.search(text):
        errors.append("instruction comment remains")
    if check_links:
        errors.extend(_check_links(path, text, project_root.resolve()))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an iceberg code report")
    parser.add_argument("path", type=Path)
    parser.add_argument("--type", choices=sorted(CONTRACTS), required=True)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--skip-links", action="store_true")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()
    errors = validate_report(
        args.path,
        args.type,
        project_root=args.project_root,
        check_links=not args.skip_links,
    )
    if errors:
        for error in errors:
            LOGGER.error("Report validation failed: %s", error)
        return 1
    LOGGER.info(
        "Report validation passed: %s", args.path, extra={"report_path": str(args.path)}
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
