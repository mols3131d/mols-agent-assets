from __future__ import annotations

import tempfile
from pathlib import Path

from format_markdown import format_markdown


def test_format_markdown_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        # Writing unformatted markdown (e.g. trailing spaces or double blank lines)
        md_file.write_text("# Title\n\n\n\nSome text with spaces  \n")

        assert format_markdown(md_file) is True

        # Read back formatted content
        formatted_content = md_file.read_text(encoding="utf-8")
        # rumdl should normalize blank lines and trailing spaces
        assert "\n\n\n" not in formatted_content


def test_format_markdown_non_existent():
    assert format_markdown(Path("non_existent_file.md")) is False


def test_format_markdown_custom_executable():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n\n\n\nSome text  \n")

        # Testing with "uv run rumdl" as custom executable
        assert format_markdown(md_file, executable="uv run rumdl") is True
        formatted_content = md_file.read_text(encoding="utf-8")
        assert "\n\n\n" not in formatted_content


def test_format_markdown_multiple_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md1 = tmp_path / "doc1.md"
        md2 = tmp_path / "doc2.md"
        md1.write_text("# Doc 1\n\n\n\nText 1  \n")
        md2.write_text("# Doc 2\n\n\n\nText 2  \n")

        # Pass a list of Path objects
        assert format_markdown([md1, md2]) is True

        content1 = md1.read_text(encoding="utf-8")
        content2 = md2.read_text(encoding="utf-8")
        assert "\n\n\n" not in content1
        assert "\n\n\n" not in content2
