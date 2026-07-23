#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0.2",
# ]
# ///
"""Move Kanban cards to target directories.

This script moves cards based on their status and fixes links.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


# Re-use YAML frontmatter parser
def parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter block from markdown content."""
    try:
        import yaml
    except ImportError as error:
        raise ImportError("dependency 'yaml' is missing") from error

    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None

    yaml_lines = []
    found_end = False
    for line in lines[1:]:
        if line == "---":
            found_end = True
            break
        yaml_lines.append(line)

    if not found_end:
        return None

    try:
        data = yaml.safe_load("\n".join(yaml_lines))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def update_links_in_content(
    content: str, old_rel_path: Path, new_rel_path: Path
) -> str:
    """Update relative links inside markdown content when a card moves.

    Fixes paths of other resources linked inside the card so they
    don't break after the card is moved.
    """

    # Regex to find markdown links: [text](path) or [text](path#anchor)
    # We only rewrite relative paths pointing to local files.
    def link_replacer(match: re.Match) -> str:
        link_text = match.group(1)
        link_target = match.group(2)

        # Keep web URLs and absolute paths unchanged
        if re.match(r"^(https?://|mailto:|/|#)", link_target):
            return match.group(0)

        # Parse path and optional anchor
        parts = link_target.split("#", 1)
        target_path_str = parts[0]
        anchor = f"#{parts[1]}" if len(parts) > 1 else ""

        if not target_path_str:
            return match.group(0)

        try:
            # Resolve target path relative to old card location
            resolved_target = (old_rel_path.parent / target_path_str).resolve()
            # Calculate new relative path from new card location to the same target
            # relative_to needs matching base, so we use os.path.relpath
            import os

            new_rel = os.path.relpath(resolved_target, new_rel_path.parent)

            # Windows path backslash to slash
            new_rel_str = Path(new_rel).as_posix()
            return f"[{link_text}]({new_rel_str}{anchor})"
        except Exception:
            return match.group(0)

    # Markdown links: [display](target)
    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replacer, content)
    return content


def update_inbound_links(
    kanban_path: Path, old_rel_path: Path, new_rel_path: Path
) -> None:
    """Update links in OTHER markdown files that point to the moved card."""
    all_md_files = list(kanban_path.glob("**/*.md"))

    for md_file in all_md_files:
        # Avoid checking the file itself
        # Resolve target paths to absolute to compute paths relative to md_file
        old_abs = (kanban_path / old_rel_path).resolve()
        new_abs = (kanban_path / new_rel_path).resolve()

        if md_file.resolve() == new_abs:
            continue

        content = md_file.read_text(encoding="utf-8")
        has_changed = False

        def inbound_replacer(match: re.Match) -> str:
            nonlocal has_changed
            link_text = match.group(1)
            link_target = match.group(2)

            if re.match(r"^(https?://|mailto:|/|#)", link_target):
                return match.group(0)

            parts = link_target.split("#", 1)
            target_path_str = parts[0]
            anchor = f"#{parts[1]}" if len(parts) > 1 else ""

            if not target_path_str:
                return match.group(0)

            try:
                resolved_target = (md_file.parent / target_path_str).resolve()
                if resolved_target == old_abs:
                    # Update to point to the new location
                    import os

                    new_rel = os.path.relpath(new_abs, md_file.parent)
                    new_rel_str = Path(new_rel).as_posix()
                    has_changed = True
                    return f"[{link_text}]({new_rel_str}{anchor})"
            except Exception:
                pass

            return match.group(0)

        new_content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", inbound_replacer, content)
        if has_changed:
            md_file.write_text(new_content, encoding="utf-8")
            print(f"Updated inbound links in {md_file.relative_to(kanban_path)}")


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

    # Locate all markdown files in backlog, active, archive
    source_dirs = [path / "backlog", path / "active", path / "archive"]
    cards: list[Path] = []
    for sd in source_dirs:
        if sd.exists():
            cards.extend(sd.glob("**/*.md"))

    moves_performed = 0

    for card_path in cards:
        if card_path.name in ["README.md", "AGENTS.md", "template.md"]:
            continue

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python move_cards.py <kanban_path>", file=sys.stderr)
        sys.exit(1)

    move_cards_by_status(sys.argv[1])
