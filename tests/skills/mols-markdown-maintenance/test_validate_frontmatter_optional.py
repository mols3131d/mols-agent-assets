from validate_frontmatter import validate_frontmatter


def test_schema_allows_missing_optional_field_but_validates_it_when_present(tmp_path):
    schema = {
        "title": {"type": str, "required": False},
        "description": {"type": str, "required": True},
    }

    without_title = tmp_path / "without-title.md"
    without_title.write_text("---\ndescription: Valid\n---\n", encoding="utf-8")
    assert validate_frontmatter(without_title, schema=schema) is True

    invalid_title = tmp_path / "invalid-title.md"
    invalid_title.write_text(
        "---\ntitle: [not, a, string]\ndescription: Valid\n---\n",
        encoding="utf-8",
    )
    assert validate_frontmatter(invalid_title, schema=schema) is False

    missing_description = tmp_path / "missing-description.md"
    missing_description.write_text("---\ntitle: Valid\n---\n", encoding="utf-8")
    assert validate_frontmatter(missing_description, schema=schema) is False
