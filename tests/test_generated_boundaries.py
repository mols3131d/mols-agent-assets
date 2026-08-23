from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"


def test_rulesync_source_and_runtime_surfaces_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert "src/rulesync/** rulesync-source" in attributes
    assert "route/skills.jsonl linguist-generated" in attributes
    generated_index = "src/rulesync/.rulesync/skills/INDEX.jsonl linguist-generated"
    assert generated_index not in attributes
    for forbidden in [
        ".github/skills/** linguist-generated",
        ".github/agents/** linguist-generated",
        ".agents/rules/** linguist-generated",
        ".agents/skills/** linguist-generated",
        ".agents/agents/** linguist-generated",
        ".agents/routes/** linguist-generated",
    ]:
        assert forbidden not in attributes


def test_rumdl_config_keeps_repository_markdown_policy() -> None:
    config = RUMDL.read_text(encoding="utf-8")
    assert "[MD054]" not in config
    assert 'disable = ["MD013", "MD025", "MD033", "MD041"]' in config
    assert "[per-file-ignores]" not in config
    assert "[MD057]" in config
    assert "compact-paths = false" in config
