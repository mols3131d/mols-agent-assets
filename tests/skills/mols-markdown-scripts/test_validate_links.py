from __future__ import annotations

import tempfile
from pathlib import Path

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
