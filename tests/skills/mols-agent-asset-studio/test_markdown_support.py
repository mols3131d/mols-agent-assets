from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "src" / "skills" / "mols-agent-asset-studio" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from markdown_support import (  # noqa: E402  # ty: ignore[unresolved-import]
    read_markdown,
    write_workflow_index,
)


def test_read_markdown_delegates_frontmatter_parsing(tmp_path):
    path = tmp_path / "workflow.md"
    path.write_text(
        "---\nname: example\ndescription: Use when testing.\n---\n\n# Body\n",
        encoding="utf-8",
    )

    frontmatter, body = read_markdown(path)

    assert frontmatter == {"name": "example", "description": "Use when testing."}
    assert body == "\n# Body"


def test_read_markdown_rejects_missing_frontmatter(tmp_path):
    path = tmp_path / "workflow.md"
    path.write_text("# Body\n", encoding="utf-8")

    with pytest.raises(ValueError, match="유효한 YAML frontmatter"):
        read_markdown(path)


def test_write_workflow_index_uses_name_description_and_root_files(tmp_path):
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    (workflows / "first.md").write_text(
        "---\nname: first\ndescription: First workflow.\n---\n",
        encoding="utf-8",
    )
    nested = workflows / "nested"
    nested.mkdir()
    (nested / "ignored.md").write_text(
        "---\nname: ignored\ndescription: Nested workflow.\n---\n",
        encoding="utf-8",
    )

    output = workflows / "INDEX.csv"
    write_workflow_index(workflows, output)

    with output.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows == [{"name": "first", "description": "First workflow."}]
