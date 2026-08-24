from __future__ import annotations

import csv
import io

from generate_index import generate_index, main


def _write(path, content):
    path.write_text(content, encoding="utf-8")


def test_generate_index_tsv_supports_path_and_blank_description(tmp_path):
    _write(
        tmp_path / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n")

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        globs=["*.md"],
        max_depth=0,
        include_without_frontmatter=True,
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [
        {"path": "ARCHITECTURE.md", "description": ""},
        {"path": "guide.md", "description": "Guide description."},
    ]


def test_generate_index_keeps_file_as_path_compatibility_alias(tmp_path):
    _write(tmp_path / "guide.md", "---\ntitle: Guide\n---\n# Guide\n")

    result = generate_index(tmp_path, fields=["file", "path"])

    assert list(csv.DictReader(io.StringIO(result))) == [
        {"file": "guide.md", "path": "guide.md"}
    ]


def test_generate_index_supports_exact_and_glob_exclusions(tmp_path):
    _write(tmp_path / "README.md", "# Readme\n")
    _write(tmp_path / "AGENTS.md", "# Agents\n")
    _write(tmp_path / ".private.md", "# Hidden\n")
    _write(tmp_path / "__system__.md", "# System\n")
    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n")

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        globs=["*.md"],
        include_without_frontmatter=True,
        exclude=["README.md", "AGENTS.md"],
        exclude_globs=[".*.md", "__*__.md"],
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [{"path": "ARCHITECTURE.md", "description": ""}]


def test_generate_index_cli_writes_tsv_with_exclusions(tmp_path):
    _write(tmp_path / "README.md", "# Readme\n")
    _write(
        tmp_path / "guide.md",
        "---\ndescription: Guide description.\n---\n# Guide\n",
    )
    output = tmp_path / "INDEX.tsv"

    assert (
        main(
            [
                str(tmp_path),
                "--format",
                "tsv",
                "--fields",
                "path",
                "description",
                "--globs",
                "*.md",
                "--exclude",
                "README.md",
                "AGENTS.md",
                "--exclude-glob",
                ".*.md",
                "__*__.md",
                "--include-without-frontmatter",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert output.read_text(encoding="utf-8") == (
        "path\tdescription\nguide.md\tGuide description.\n"
    )
