from __future__ import annotations

import tempfile
from pathlib import Path

from validate_headers import _extract_heading_levels, main, validate_headers


def test_validate_headers_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n## Section\n### Subsection\n## Another Section")

        assert validate_headers(md_file) is True


def test_validate_headers_duplicate_h1():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n# Another Title\n## Section")

        assert validate_headers(md_file) is False


def test_validate_headers_skipped_level():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n### Subsection (skipping H2)")

        assert validate_headers(md_file) is False


def test_validate_headers_handles_missing_file_and_non_heading_events(tmp_path):
    assert validate_headers(tmp_path / "missing.md") is False
    assert _extract_heading_levels([{}, {"Start": {"Heading": {"level": "x"}}}]) == []


def test_validate_headers_cli_reports_pass_and_failure(tmp_path, capsys):
    valid = tmp_path / "valid.md"
    invalid = tmp_path / "invalid.md"
    valid.write_text("# Title\n## Section\n", encoding="utf-8")
    invalid.write_text("# First\n# Second\n", encoding="utf-8")

    assert main([str(valid)]) == 0
    assert "true" in capsys.readouterr().out
    assert main([str(valid), str(invalid)]) == 1
