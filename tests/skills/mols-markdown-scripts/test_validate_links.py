from __future__ import annotations

import tempfile
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

from validate_links import validate_links


def test_validate_links_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "ok.md"
        # Heading and valid fragment link
        md_file.write_text("# Heading\n\n[Valid link](#heading)\n")

        assert validate_links(md_file) is True


def test_validate_links_failure():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "bad.md"
        # Invalid fragment link (no matching heading)
        md_file.write_text("[Invalid link](#non-existent-header)\n")

        assert validate_links(md_file) is False


def test_validate_links_non_existent():
    assert validate_links(Path("non_existent_file.md")) is False


def test_validate_links_passes_selected_rules_and_handles_tool_failure(tmp_path):
    document = tmp_path / "document.md"
    document.write_text("# Title\n", encoding="utf-8")

    with patch("validate_links.subprocess.run") as run:
        assert validate_links([document], executable="tool --flag") is True
        assert run.call_args.args[0] == [
            "tool",
            "--flag",
            "check",
            "--config",
            "MD051.enabled = true",
            "--config",
            "MD052.enabled = true",
            str(document),
        ]

    with patch(
        "validate_links.subprocess.run",
        side_effect=CalledProcessError(1, ["tool"]),
    ):
        assert validate_links(document, executable="tool") is False
