from __future__ import annotations

import csv
import io

import pytest
from generate_index import generate_index, main  # noqa: E402


@pytest.fixture
def markdown_directory(tmp_path):
    (tmp_path / "guide.md").write_text(
        """---
title: Markdown Guide
description: A guide for writing Markdown.
tags:
  - markdown
  - docs
status: published
---
# Guide
""",
        encoding="utf-8",
    )
    (tmp_path / "nested" / "api.md").parent.mkdir()
    (tmp_path / "nested" / "api.md").write_text(
        """---
title: API Reference
description: Reference for the API.
tags: [api, reference]
status: draft
---
# API
""",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# No frontmatter\n", encoding="utf-8")
    (tmp_path / "INDEX.md").write_text("# Existing index\n", encoding="utf-8")
    return tmp_path


def test_generate_index_csv_contains_core_frontmatter(markdown_directory):
    (markdown_directory / "special.md").write_text(
        """---
title: CSV, Guide
description: |-
    A description with a comma, and a newline.
    Second line.
tags: [csv]
status: published
---
""",
        encoding="utf-8",
    )

    result = generate_index(markdown_directory, format="csv")

    rows = list(csv.DictReader(io.StringIO(result)))

    assert [row["file"] for row in rows] == [
        "guide.md",
        "nested/api.md",
        "special.md",
    ]
    assert rows[0]["title"] == "Markdown Guide"
    assert rows[0]["description"] == "A guide for writing Markdown."
    assert rows[0]["tags"] == "markdown, docs"
    assert rows[1]["status"] == "draft"
    assert rows[2]["title"] == "CSV, Guide"
    assert rows[2]["description"] == (
        "A description with a comma, and a newline.\nSecond line."
    )
    assert '"special.md","CSV, Guide"' in result
    assert '"A description with a comma, and a newline.\nSecond line."' in result


def test_generate_index_keeps_lowercase_index_documents(tmp_path):
    (tmp_path / "indexing.md").write_text(
        "---\ntitle: Indexing Policy\ndescription: Indexing policy.\n---\n# Indexing\n",
        encoding="utf-8",
    )
    (tmp_path / "INDEX.md").write_text("# Existing index\n", encoding="utf-8")

    rows = list(csv.DictReader(io.StringIO(generate_index(tmp_path, format="csv"))))

    assert [row["file"] for row in rows] == ["indexing.md"]


def test_generate_index_markdown_table_escapes_cell_values(markdown_directory):
    (markdown_directory / "pipe.md").write_text(
        """---
title: Pipe | Guide
description: A | B
tags: [one]
---
""",
        encoding="utf-8",
    )

    result = generate_index(markdown_directory, format="table")

    assert "| File | Title | Description | Tags | Status |" in result
    assert "[Pipe \\| Guide](pipe.md)" in result
    assert "A \\| B" in result
    assert "INDEX.md" not in result


def test_generate_index_markdown_list_uses_headings_and_links(markdown_directory):
    result = generate_index(markdown_directory, format="list")

    assert "# Index" in result
    assert "## [Markdown Guide](guide.md)" in result
    assert "- **Description**: A guide for writing Markdown." in result
    assert "- **Tags**: markdown, docs" in result
    assert "## [API Reference](nested/api.md)" in result


def test_generate_index_list_groups_by_multiple_frontmatter_fields(markdown_directory):
    (markdown_directory / "guide.md").write_text(
        """---
title: Markdown Guide
description: A guide for writing Markdown.
tags: [markdown]
status: published
importance: high
---
""",
        encoding="utf-8",
    )
    result = generate_index(
        markdown_directory,
        format="list",
        group_by=["status", "importance"],
    )

    assert "## Status: draft" in result
    assert "### Importance: [unset]" in result
    assert "## Status: published" in result
    assert "### Importance: high" in result
    assert "#### [Markdown Guide](guide.md)" in result


def test_generate_index_list_group_options_support_unlabeled_and_input_order(
    markdown_directory,
):
    result = generate_index(
        markdown_directory,
        format="list",
        group_by=["status"],
        group_label=False,
        group_sort="input",
    )

    assert "## published" in result
    assert "## draft" in result
    assert "## Status: published" not in result
    assert result.index("## published") < result.index("## draft")


def test_generate_index_rejects_grouping_for_flat_formats(markdown_directory):
    with pytest.raises(ValueError, match="only supported"):
        generate_index(markdown_directory, format="csv", group_by=["status"])


def test_generate_index_rejects_unknown_format(markdown_directory):
    with pytest.raises(ValueError, match="format"):
        generate_index(markdown_directory, format="json")


def test_generate_index_rejects_non_directory(tmp_path):
    source = tmp_path / "document.md"
    source.write_text("---\ntitle: Document\n---\n", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        generate_index(source, format="csv")


def test_generate_index_requires_selected_frontmatter_fields(tmp_path):
    (tmp_path / "workflow.md").write_text(
        "---\nname: workflow\n---\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="description"):
        generate_index(
            tmp_path,
            format="csv",
            fields=["name", "description"],
            required_fields=["name", "description"],
        )


def test_generate_index_requires_frontmatter_when_fields_are_required(tmp_path):
    (tmp_path / "workflow.md").write_text("# Missing frontmatter\n", encoding="utf-8")

    with pytest.raises(ValueError, match="YAML frontmatter is required"):
        generate_index(tmp_path, required_fields=["name"])


def test_generate_index_rejects_duplicate_selected_field(tmp_path):
    for filename in ("one.md", "two.md"):
        (tmp_path / filename).write_text(
            "---\nname: duplicate\ndescription: Route.\n---\n",
            encoding="utf-8",
        )

    with pytest.raises(ValueError, match="duplicate frontmatter name"):
        generate_index(tmp_path, unique_fields=["name"])


def test_generate_index_honors_globs_and_max_depth(markdown_directory):
    result = generate_index(
        markdown_directory,
        fields=["file", "title"],
        globs=["*.md"],
        max_depth=0,
    )

    assert list(csv.DictReader(io.StringIO(result))) == [
        {"file": "guide.md", "title": "Markdown Guide"}
    ]


def test_generate_index_cli_writes_requested_output(tmp_path):
    (tmp_path / "workflow.md").write_text(
        "---\nname: workflow\ndescription: Test workflow.\n---\n",
        encoding="utf-8",
    )
    output = tmp_path / "custom-name.csv"

    assert (
        main(
            [
                str(tmp_path),
                "--fields",
                "name",
                "description",
                "--require-fields",
                "name",
                "description",
                "--unique-fields",
                "name",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert list(csv.DictReader(output.open(encoding="utf-8"))) == [
        {"name": "workflow", "description": "Test workflow."}
    ]
