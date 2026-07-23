#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
#   "pyromark>=0.9.13",
#   "rumdl>=0.2.6",
# ]
# ///
"""Move Kanban cards to target directories.

This script moves cards based on their status and fixes links using pyromark and rumdl.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import pyromark

# Allow standalone CLI execution without relative import error
sys.path.insert(0, str(Path(__file__).resolve().parent))

from shared import get_card_files, parse_frontmatter


def get_markdown_links(content: str) -> list[tuple[str, tuple[int, int]]]:
    """Extract markdown link destinations and their character offsets using pyromark.

    This ensures code blocks, inline code, and non-link syntax are correctly ignored.
    """
    links: list[tuple[str, tuple[int, int]]] = []
    events = list(pyromark.events_with_range(content))

    for event, byte_range in events:
        event_data = cast(dict[str, Any], event)
        if "Start" in event_data:
            start_val = cast(dict[str, Any], event_data["Start"])
            if "Link" in start_val:
                link_info = cast(dict[str, Any], start_val["Link"])
                if "dest_url" in link_info:
                    dest = link_info["dest_url"]
                    # byte_range is a dict like {'start': 29, 'end': 58}
                    if (
                        isinstance(byte_range, dict)
                        and "start" in byte_range
                        and "end" in byte_range
                    ):
                        links.append((dest, (byte_range["start"], byte_range["end"])))

    return links


def update_links_in_content(
    content: str, old_rel_path: Path, new_rel_path: Path
) -> str:
    """Update relative links inside markdown content when a card moves."""
    links = get_markdown_links(content)
    if not links:
        return content

    # Sort links in reverse order of position to replace strings from end to start
    # without breaking offsets
    links_sorted = sorted(links, key=lambda x: x[1][0], reverse=True)
    new_content = content

    for target, (start, end) in links_sorted:
        if re.match(r"^(https?://|mailto:|/|#)", target):
            continue

        parts = target.split("#", 1)
        target_path_str = parts[0]
        anchor = f"#{parts[1]}" if len(parts) > 1 else ""

        if not target_path_str:
            continue

        try:
            resolved_target = (old_rel_path.parent / target_path_str).resolve()
            new_rel = os.path.relpath(resolved_target, new_rel_path.parent)
            new_rel_str = Path(new_rel).as_posix()
            new_target = f"{new_rel_str}{anchor}"

            # Original substring in markdown e.g. [label](old_target)
            slice_str = new_content[start:end]
            if f"({target})" in slice_str:
                new_slice = slice_str.replace(f"({target})", f"({new_target})", 1)
                new_content = new_content[:start] + new_slice + new_content[end:]
        except Exception:
            pass

    return new_content


def update_inbound_links(
    kanban_path: Path, old_rel_path: Path, new_rel_path: Path
) -> None:
    """Update links in OTHER markdown files that point to the moved card."""
    all_md_files = list(kanban_path.glob("**/*.md"))
    old_abs = (kanban_path / old_rel_path).resolve()
    new_abs = (kanban_path / new_rel_path).resolve()

    for md_file in all_md_files:
        if md_file.resolve() == new_abs:
            continue

        content = md_file.read_text(encoding="utf-8")
        links = get_markdown_links(content)
        if not links:
            continue

        links_sorted = sorted(links, key=lambda x: x[1][0], reverse=True)
        new_content = content
        has_changed = False

        for target, (start, end) in links_sorted:
            if re.match(r"^(https?://|mailto:|/|#)", target):
                continue

            parts = target.split("#", 1)
            target_path_str = parts[0]
            anchor = f"#{parts[1]}" if len(parts) > 1 else ""

            if not target_path_str:
                continue

            try:
                resolved_target = (md_file.parent / target_path_str).resolve()
                if resolved_target == old_abs:
                    new_rel = os.path.relpath(new_abs, md_file.parent)
                    new_rel_str = Path(new_rel).as_posix()
                    new_target = f"{new_rel_str}{anchor}"

                    slice_str = new_content[start:end]
                    if f"({target})" in slice_str:
                        new_slice = slice_str.replace(
                            f"({target})", f"({new_target})", 1
                        )
                        new_content = (
                            new_content[:start] + new_slice + new_content[end:]
                        )
                        has_changed = True
            except Exception:
                pass

        if has_changed:
            md_file.write_text(new_content, encoding="utf-8")
            print(f"Updated inbound links in {md_file.relative_to(kanban_path)}")


def validate_with_rumdl(kanban_path: Path) -> None:
    """Validate links in Kanban workspace using rumdl check command."""
    md_files = list(kanban_path.glob("**/*.md"))
    if not md_files:
        return

    try:
        cmd = ["uv", "run", "rumdl", "check"] + [str(p) for p in md_files]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print("rumdl link check passed with 0 warnings/errors.")
        else:
            print(f"rumdl check warnings:\n{res.stdout}")
    except Exception as e:
        print(f"Failed to run rumdl check: {e}", file=sys.stderr)


def move_cards_by_status(kanban_path: str) -> None:
    path = Path(kanban_path).resolve()

    # 1. Map status to subdirectories
    status_dirs = {
        "backlog": path / "backlog",
        "todo": path / "active",
        "in_progress": path / "active",
        "review": path / "active",
        "done": path / "archive",
    }

    # Locate all markdown card files using shared helper
    cards = get_card_files(path)

    moves_performed = 0

    for card_path in cards:
        try:
            content = card_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {card_path.name}: {e}", file=sys.stderr)
            continue

        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            # Not a card, skip
            continue

        status = frontmatter.get("status")
        if not status:
            print(
                f"Warning: Card {card_path.name} has no status field. Skipping.",
                file=sys.stderr,
            )
            continue

        target_dir = status_dirs.get(status)
        if not target_dir:
            print(
                f"Warning: Unknown status '{status}' in {card_path.name}. Skipping.",
                file=sys.stderr,
            )
            continue

        # Target directory must exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # If card is not in target directory, move it
        if card_path.parent.resolve() != target_dir.resolve():
            dest_path = target_dir / card_path.name

            # Handle collision
            if dest_path.exists():
                print(
                    f"Collision: {dest_path.name} already exists "
                    f"in {target_dir}. Skipping move.",
                    file=sys.stderr,
                )
                continue

            # Perform link corrections in the card content itself
            old_rel = card_path.relative_to(path)
            new_rel = dest_path.relative_to(path)

            # Correct links in the card content
            updated_content = update_links_in_content(content, old_rel, new_rel)

            # Write content to destination
            dest_path.write_text(updated_content, encoding="utf-8")

            # Remove old card
            card_path.unlink()

            print(f"Moved card: {old_rel} -> {new_rel}")

            # Update inbound links in other markdown files
            update_inbound_links(path, old_rel, new_rel)
            moves_performed += 1

    if moves_performed == 0:
        print("No cards needed to be moved.")
    else:
        print(f"Completed moving {moves_performed} card(s) and fixed references.")
        validate_with_rumdl(path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python move_cards.py <kanban_path>", file=sys.stderr)
        sys.exit(1)

    move_cards_by_status(sys.argv[1])
