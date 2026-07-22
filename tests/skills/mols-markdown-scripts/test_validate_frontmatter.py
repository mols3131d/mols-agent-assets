from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from validate_frontmatter import validate_frontmatter


def test_validate_frontmatter_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("---\ntitle: Test Doc\nstatus: active\n---\n# Title")

        required = {"title", "status"}
        assert validate_frontmatter(md_file, required) is True


def test_validate_frontmatter_missing_field():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("---\ntitle: Test Doc\n---\n# Title")

        required = {"title", "status"}
        # If status is missing, should return False
        assert validate_frontmatter(md_file, required) is False


def test_validate_frontmatter_no_yaml():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("---\ntitle: Test Doc\n---\n# Title")

        # Mock ImportError when importing yaml
        with patch.dict(sys.modules, {"yaml": None}):
            with pytest.raises(ImportError, match="dependency 'yaml' is missing"):
                validate_frontmatter(md_file, {"title"})


def test_validate_frontmatter_schema_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        md_file = tmp_path / "doc.md"
        md_file.write_text("""---
title: Super Doc
status: active
tags: [markdown, python]
metadata:
  author: Alice
---
# Title""")

        schema = {
            "title": {"type": str, "min_length": 5, "max_length": 20},
            "status": {"type": str, "allowed_values": {"active", "draft"}},
            "tags": {"type": list, "min_items": 1, "max_items": 5},
            "metadata": {"type": dict, "schema": {"author": {"type": str}}},
        }
        assert validate_frontmatter(md_file, schema=schema) is True


def test_validate_frontmatter_schema_failures():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # 1. Invalid Type
        md_file = tmp_path / "doc1.md"
        md_file.write_text("---\ntitle: 12345\n---")
        assert validate_frontmatter(md_file, schema={"title": {"type": str}}) is False

        # 2. Invalid Allowed Values
        md_file2 = tmp_path / "doc2.md"
        md_file2.write_text("---\nstatus: pending\n---")
        status_schema = {"status": {"allowed_values": {"active", "draft"}}}
        assert validate_frontmatter(md_file2, schema=status_schema) is False

        # 3. Invalid min_length
        md_file3 = tmp_path / "doc3.md"
        md_file3.write_text("---\ntitle: abc\n---")
        title_schema = {"title": {"min_length": 5}}
        assert validate_frontmatter(md_file3, schema=title_schema) is False

        # 4. Invalid max_items
        md_file4 = tmp_path / "doc4.md"
        md_file4.write_text("---\ntags: [a, b, c]\n---")
        tags_schema = {"tags": {"min_items": 1, "max_items": 2}}
        assert validate_frontmatter(md_file4, schema=tags_schema) is False

        # 5. Invalid Nested Schema
        md_file5 = tmp_path / "doc5.md"
        md_file5.write_text("""---
metadata:
  author: 123
---""")
        schema = {
            "metadata": {
                "type": dict,
                "schema": {"author": {"type": str, "min_length": 5}},
            }
        }
        assert validate_frontmatter(md_file5, schema=schema) is False


def test_validate_frontmatter_extra_rules():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # 1. Date Validation (is_date)
        md_date_ok = tmp_path / "date_ok.md"
        md_date_ok.write_text("---\ndate: 2026-07-22\n---")
        assert (
            validate_frontmatter(md_date_ok, schema={"date": {"is_date": True}}) is True
        )

        md_date_bad = tmp_path / "date_bad.md"
        md_date_bad.write_text("---\ndate: not-a-date\n---")
        assert (
            validate_frontmatter(md_date_bad, schema={"date": {"is_date": True}})
            is False
        )

        # 2. Regex Pattern (pattern)
        md_regex_ok = tmp_path / "regex_ok.md"
        md_regex_ok.write_text("---\nid: mols-123\n---")
        assert (
            validate_frontmatter(md_regex_ok, schema={"id": {"pattern": r"^mols-\d+$"}})
            is True
        )

        md_regex_bad = tmp_path / "regex_bad.md"
        md_regex_bad.write_text("---\nid: other-123\n---")
        assert (
            validate_frontmatter(
                md_regex_bad, schema={"id": {"pattern": r"^mols-\d+$"}}
            )
            is False
        )

        # 3. Item Type (item_type)
        md_list_ok = tmp_path / "list_ok.md"
        md_list_ok.write_text("---\ntags: [apple, banana]\n---")
        assert (
            validate_frontmatter(md_list_ok, schema={"tags": {"item_type": str}})
            is True
        )

        md_list_bad = tmp_path / "list_bad.md"
        md_list_bad.write_text("---\ntags: [apple, 123]\n---")
        assert (
            validate_frontmatter(md_list_bad, schema={"tags": {"item_type": str}})
            is False
        )

        # 4. Strict Mode (__strict__ / strict)
        md_strict_ok = tmp_path / "strict_ok.md"
        md_strict_ok.write_text("---\ntitle: Hello\n---")
        schema_strict = {"title": {"type": str}, "__strict__": True}
        assert validate_frontmatter(md_strict_ok, schema=schema_strict) is True

        md_strict_bad = tmp_path / "strict_bad.md"
        md_strict_bad.write_text("---\ntitle: Hello\nunknown: field\n---")
        assert validate_frontmatter(md_strict_bad, schema=schema_strict) is False
