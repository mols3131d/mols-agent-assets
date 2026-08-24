from __future__ import annotations

import csv
import io

import pytest

from generate_index import generate_index, main


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
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


def test_generate_index_filesystem_path_overrides_frontmatter_path_fields(tmp_path):
    _write(
        tmp_path / "guide.md",
        "---\npath: wrong.md\nfile: wrong.md\ndescription: Guide.\n---\n# Guide\n",
    )

    result = generate_index(tmp_path, fields=["path", "file", "description"])

    assert list(csv.DictReader(io.StringIO(result))) == [
        {"path": "guide.md", "file": "guide.md", "description": "Guide."}
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


def test_generate_index_filters_multiple_and_compound_file_extensions(tmp_path):
    _write(tmp_path / "guide.md", "---\ndescription: Guide.\n---\n")
    _write(tmp_path / "component.mdx", "---\ndescription: Component.\n---\n")
    _write(tmp_path / "review.skill.md", "---\ndescription: Skill.\n---\n")
    _write(tmp_path / "notes.txt", "---\ndescription: Notes.\n---\n")

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        file_extensions=["mdx", ".skill.md"],
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [
        {"path": "component.mdx", "description": "Component."},
        {"path": "review.skill.md", "description": "Skill."},
    ]


def test_generate_index_can_include_directories_without_files(tmp_path):
    _write(tmp_path / "guide.md", "---\ndescription: Guide.\n---\n")
    _write(tmp_path / "alpha" / "nested.md", "---\ndescription: Nested.\n---\n")
    (tmp_path / "beta").mkdir()

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        max_depth=0,
        include_files=False,
        include_directories=True,
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [
        {"path": "alpha/", "description": ""},
        {"path": "beta/", "description": ""},
    ]


def test_generate_index_can_mix_files_and_directories(tmp_path):
    _write(tmp_path / "guide.md", "---\ndescription: Guide.\n---\n")
    _write(tmp_path / "nested" / "reference.md", "---\ndescription: Ref.\n---\n")

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        max_depth=0,
        include_directories=True,
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [
        {"path": "guide.md", "description": "Guide."},
        {"path": "nested/", "description": ""},
    ]


def test_generate_index_directory_entry_files_use_ordered_frontmatter(tmp_path):
    _write(tmp_path / "alpha" / "README.md", "# No frontmatter\n")
    _write(
        tmp_path / "alpha" / "index.md",
        "---\ndescription: Alpha fallback.\n---\n# Alpha\n",
    )
    _write(
        tmp_path / "beta" / "README.md",
        "---\ntitle: Beta\n---\n# Beta\n",
    )
    _write(
        tmp_path / "beta" / "index.md",
        "---\ndescription: Must not merge.\n---\n# Beta index\n",
    )

    result = generate_index(
        tmp_path,
        format="tsv",
        fields=["path", "description"],
        max_depth=0,
        include_files=False,
        include_directories=True,
        directory_entry_files=["README.md", "index.md"],
    )

    rows = list(csv.DictReader(io.StringIO(result), delimiter="\t"))
    assert rows == [
        {"path": "alpha/", "description": "Alpha fallback."},
        {"path": "beta/", "description": ""},
    ]


def test_generate_index_rejects_extensions_when_files_are_disabled(tmp_path):
    with pytest.raises(ValueError, match="include_files"):
        generate_index(
            tmp_path,
            include_files=False,
            file_extensions=[".md"],
        )


def test_generate_index_rejects_directory_entry_files_when_directories_are_disabled(
    tmp_path,
):
    with pytest.raises(ValueError, match="include_directories"):
        generate_index(tmp_path, directory_entry_files=["README.md"])


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


def test_generate_index_cli_supports_directory_entrypoint_projection(tmp_path):
    _write(
        tmp_path / "alpha" / "README.md",
        "---\ndescription: Alpha.\n---\n# Alpha\n",
    )
    (tmp_path / "beta").mkdir()
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
                "--no-files",
                "--directories",
                "--directory-entry-files",
                "README.md",
                "index.md",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert output.read_text(encoding="utf-8") == (
        "path\tdescription\nalpha/\tAlpha.\nbeta/\t\n"
    )
