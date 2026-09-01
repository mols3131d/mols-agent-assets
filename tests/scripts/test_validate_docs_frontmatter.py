from __future__ import annotations

import json

import pytest

from scripts.validate_docs_frontmatter import validate_docs_frontmatter


def _write(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_config(root, *, title_type: str = "string") -> None:
    config = {
        "frontMatter.content.pageFolders": [
            {
                "path": "[[workspace]]/docs",
                "contentTypes": ["default"],
                "excludePaths": ["**/baseline/**"],
            }
        ],
        "frontMatter.taxonomy.contentTypes": [
            {
                "name": "default",
                "fields": [
                    {"name": "title", "type": title_type},
                    {"name": "description", "type": "string", "required": True},
                ],
            }
        ],
    }
    (root / "frontmatter.json").write_text(
        json.dumps(config), encoding="utf-8"
    )


def test_validate_docs_frontmatter_uses_config_and_role_exclusions(tmp_path) -> None:
    _write_config(tmp_path)
    _write(tmp_path / "docs/guide.md", "---\ndescription: Guide\n---\n# Guide\n")
    _write(
        tmp_path / "docs/titled.md",
        "---\ntitle: Titled\ndescription: Guide\n---\n# Guide\n",
    )

    for relative in (
        "docs/baseline/legacy.md",
        "docs/AGENTS.md",
        "docs/SKILL.md",
        "docs/DIRECTIVE.md",
        "docs/example.agent.md",
        "docs/example.instructions.md",
        "docs/example.prompt.md",
        "docs/__index__.md",
    ):
        _write(tmp_path / relative, "# Not a general document\n")

    assert validate_docs_frontmatter(tmp_path) == []


def test_validate_docs_frontmatter_rejects_required_and_optional_type_errors(tmp_path) -> None:
    _write_config(tmp_path)
    _write(tmp_path / "docs/.hidden.md", "# Missing frontmatter\n")
    _write(tmp_path / "docs/missing.md", "---\ntitle: Valid\n---\n")
    _write(
        tmp_path / "docs/description-type.md",
        "---\ndescription: [not, a, string]\n---\n",
    )
    _write(
        tmp_path / "docs/title-type.md",
        "---\ntitle: [not, a, string]\ndescription: Valid\n---\n",
    )

    assert validate_docs_frontmatter(tmp_path) == [
        "docs/.hidden.md",
        "docs/description-type.md",
        "docs/missing.md",
        "docs/title-type.md",
    ]


def test_validate_docs_frontmatter_fails_closed_on_unsupported_field_type(tmp_path) -> None:
    _write_config(tmp_path, title_type="unsupported")
    (tmp_path / "docs").mkdir()

    with pytest.raises(ValueError, match="unsupported frontmatter field type"):
        validate_docs_frontmatter(tmp_path)
