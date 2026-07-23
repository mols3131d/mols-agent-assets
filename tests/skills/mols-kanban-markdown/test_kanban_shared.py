import importlib.util
from pathlib import Path

# Load shared.py dynamically since directory contains hyphens
script_path = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "skills"
    / "mols-kanban-markdown"
    / "scripts"
    / "shared.py"
)
spec = importlib.util.spec_from_file_location("shared", script_path)
assert spec is not None and spec.loader is not None
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)

parse_jsonc = shared.parse_jsonc
parse_frontmatter = shared.parse_frontmatter


def test_parse_jsonc():
    jsonc_text = """
    {
        // Single line comment
        "key": "value", /* Inline comment */
        "url": "https://example.com/api" // URL should remain intact
    }
    """
    data = parse_jsonc(jsonc_text)
    assert data["key"] == "value"
    assert data["url"] == "https://example.com/api"


def test_parse_frontmatter():
    valid_md = """---
title: Hello World
status: todo
---
# Hello
"""
    data = parse_frontmatter(valid_md)
    assert data is not None
    assert data["title"] == "Hello World"
    assert data["status"] == "todo"

    invalid_md = "# Just Markdown"
    assert parse_frontmatter(invalid_md) is None
