from __future__ import annotations

import pytest
from frontmatter import parse_frontmatter_document, read_frontmatter


def test_parse_frontmatter_returns_mapping_and_body():
    parsed = parse_frontmatter_document(
        "---\r\nname: sample\r\ntags: [one, two]\r\n---\r\n# Body\r\n"
    )

    assert parsed == ({"name": "sample", "tags": ["one", "two"]}, "# Body")


@pytest.mark.parametrize(
    "content",
    [
        "# No frontmatter\n",
        "---\nname: missing-end\n",
        "---\n- not\n- a mapping\n---\n",
        "---\nname: [invalid\n---\n",
    ],
)
def test_parse_frontmatter_rejects_invalid_documents(content):
    assert parse_frontmatter_document(content) is None


def test_read_frontmatter_handles_missing_and_existing_file(tmp_path):
    assert read_frontmatter(tmp_path / "missing.md") is None

    path = tmp_path / "document.md"
    path.write_text("---\nname: document\n---\nBody\n", encoding="utf-8")
    assert read_frontmatter(path) == ({"name": "document"}, "Body")
