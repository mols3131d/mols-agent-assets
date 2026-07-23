import subprocess
import sys
import tempfile
from pathlib import Path


def test_validate_frontmatter():
    repo_root = Path(__file__).resolve().parents[3]
    init_script_path = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "initialize.py"
    )
    val_script_path = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "validate_frontmatter.py"
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "test-kanban"

        # 1. Initialize
        init_res = subprocess.run(
            [sys.executable, str(init_script_path), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert init_res.returncode == 0

        # 2. Add a valid card
        valid_card_content = """---
id: KBN-001
title: Test Title
status: todo
priority: medium
description: This is a test description
tags: [test, init]
---
# Test Title
"""
        card_dir = tmp_path / "backlog"
        card_dir.mkdir(parents=True, exist_ok=True)
        card_file = card_dir / "KBN-001.md"
        card_file.write_text(valid_card_content, encoding="utf-8")

        # Validate should pass
        val_res = subprocess.run(
            [sys.executable, str(val_script_path), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert val_res.returncode == 0

        # 3. Add an invalid card (missing id, wrong status, tags not string list)
        invalid_card_content = """---
status: wrong_status
priority: low
description: Test
tags: [123, test_invalid]
---
# Invalid Card
"""
        invalid_card_file = card_dir / "invalid.md"
        invalid_card_file.write_text(invalid_card_content, encoding="utf-8")

        # Validate should fail
        val_res_fail = subprocess.run(
            [sys.executable, str(val_script_path), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert val_res_fail.returncode != 0
        assert (
            "is required but got None or missing" in val_res_fail.stderr
            or "is required but got None or missing" in val_res_fail.stdout
        )
        assert (
            "must be one of" in val_res_fail.stderr
            or "must be one of" in val_res_fail.stdout
        )
