#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyromark>=0.9.13",
# ]
# ///

"""Validate markdown header hierarchy."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _extract_heading_levels(events: Any) -> list[int]:
    """Extract heading levels from pyromark events."""
    levels = []
    for ev in events:
        if not isinstance(ev, dict):
            continue
        start = ev.get("Start")
        if not isinstance(start, dict):
            continue
        heading = start.get("Heading")
        if not isinstance(heading, dict):
            continue
        level_str = heading.get("level")
        if isinstance(level_str, str) and len(level_str) > 1:
            try:
                levels.append(int(level_str[1:]))
            except ValueError:
                pass
    return levels


def validate_headers(file_path: Path) -> bool:
    """Validate markdown heading hierarchy.

    Ensures:
        - Only one H1 heading exists.
        - No heading levels are skipped (e.g., H1 followed by H3).
    """
    import pyromark  # type: ignore[import-not-found]  # ty: ignore[unresolved-import]

    if not file_path.is_file():
        return False

    content = file_path.read_text(encoding="utf-8")
    events = pyromark.events(content)
    headings = _extract_heading_levels(events)

    if not headings:
        return True

    if headings.count(1) > 1:
        return False

    prev_level = 0
    for level in headings:
        if prev_level > 0 and level > prev_level + 1:
            return False
        prev_level = level

    return True


def main() -> None:
    pass


if __name__ == "__main__":
    main()
