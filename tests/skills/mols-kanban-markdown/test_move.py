import subprocess
import sys
import tempfile
from pathlib import Path


def test_validate_directory_and_move_cards():
    repo_root = Path(__file__).resolve().parents[3]
    init_script = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "initialize.py"
    )
    dir_val_script = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "validate_directory.py"
    )
    move_script = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "move_cards.py"
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "test-kanban"

        # 1. Test directory validation on uninitialized directory
        res = subprocess.run(
            [sys.executable, str(dir_val_script), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert res.returncode != 0
        assert (
            "does not exist or is not a directory" in res.stdout
            or "does not exist or is not a directory" in res.stderr
        )

        # 2. Initialize
        subprocess.run([sys.executable, str(init_script), str(tmp_path)], check=True)

        # 3. Test directory validation on initialized directory (should pass)
        res = subprocess.run(
            [sys.executable, str(dir_val_script), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 0

        # 4. Create an item in backlog with status=done (should be moved to archive)
        card_content = """---
id: KBN-002
title: Done Card
status: done
priority: low
description: Task that is completed
tags: []
---
# Done Card

See details in [relative document](../docs/spec.md).
"""
        card_file = tmp_path / "backlog" / "KBN-002.md"
        card_file.write_text(card_content, encoding="utf-8")

        # Create the relative document linked by card
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        spec_file = docs_dir / "spec.md"
        spec_file.write_text(
            "# Specification\nLink back to [Card](../backlog/KBN-002.md)",
            encoding="utf-8",
        )

        # 5. Run move_cards script
        move_res = subprocess.run(
            [sys.executable, str(move_script), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert move_res.returncode == 0
        assert "Moved card: backlog/KBN-002.md -> archive/KBN-002.md" in move_res.stdout

        # Verify card is moved to archive
        assert not card_file.exists()
        new_card_file = tmp_path / "archive" / "KBN-002.md"
        assert new_card_file.exists()

        # Verify internal link in card is fixed
        # Check if the link got updated correctly.
        moved_content = new_card_file.read_text(encoding="utf-8")
        assert "[relative document](../docs/spec.md)" in moved_content

        # Verify inbound link in docs/spec.md is fixed
        updated_spec_content = spec_file.read_text(encoding="utf-8")
        assert "[Card](../archive/KBN-002.md)" in updated_spec_content
