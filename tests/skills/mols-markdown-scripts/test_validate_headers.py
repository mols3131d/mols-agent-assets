from __future__ import annotations

import tempfile
from pathlib import Path

from validate_headers import validate_headers


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
