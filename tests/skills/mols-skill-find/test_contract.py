from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILL = (
    ROOT
    / "src"
    / "rulesync"
    / ".rulesync"
    / "skills"
    / "mols-skill-find"
    / "SKILL.md"
)
DEFAULT_SOURCE = "https://github.com/mols3131d/mols-agent-assets"
EXPECTED_ARGUMENTS = {
    "sources",
    "query",
    "mode",
    "target",
    "constraints",
    "strategy",
    "fallback",
}


def load() -> tuple[dict[str, object], str]:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end >= 0
    frontmatter = yaml.safe_load(text[4:end])
    assert isinstance(frontmatter, dict)
    return frontmatter, text[end + 5 :]


def test_discovery_arguments_are_auto_first_and_source_agnostic() -> None:
    frontmatter, body = load()
    metadata = frontmatter["metadata"]
    assert isinstance(metadata, dict)
    assert "default-source" not in metadata

    block = re.search(r"## Arguments\n\n```yaml\n(.*?)\n```", body, re.DOTALL)
    assert block is not None
    arguments = {
        line.split(":", 1)[0]
        for line in block.group(1).splitlines()
        if line and not line.startswith(" ")
    }
    assert arguments == EXPECTED_ARGUMENTS
    assert all(f"{name}: <auto>" in block.group(1) for name in EXPECTED_ARGUMENTS)

    assert "profiles:" not in body
    assert "skills-chatbot" not in body
    assert "flat variant" not in body
    assert "runtime variant" not in body
    assert "agent/chatbot" not in body


def test_declared_default_is_visible_in_canonical_skill() -> None:
    _, body = load()
    assert DEFAULT_SOURCE in body
    assert "## Defaults" in body
    assert "fallback: none" in body


def test_auto_resolution_keeps_defaults_declarative_and_bounded() -> None:
    _, body = load()
    required = [
        "Explicit values always win.",
        "declared `Defaults`",
        "fallback: external",
        "build a source plan from applicable evidence rather than choosing one source prematurely",
        "Do not fetch a remote repository merely to rediscover Skills already exposed",
        "An index is an optimization and authority hint, not a universal requirement.",
        "Do not invent target profiles or sibling classes.",
    ]
    for phrase in required:
        assert phrase in body

    assert "<none>" in body
    assert "first-match" in body
    assert "merge" in body
    assert "exhaustive" in body
    assert "sync-prep" in body


def test_strategy_and_source_access_are_separate_axes() -> None:
    _, body = load()
    assert "It controls how ordered source results are combined" in body
    assert "`index` in SourceSpec controls index use for that source." in body
    assert "Do not use `strategy` to override `sources` order, SourceSpec scope, or `index` policy." in body
