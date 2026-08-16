from pathlib import Path


ROOT = Path(__file__).parents[3] / "src" / "skills" / "rulesync-agent-assets"
SKILL = ROOT / "SKILL.md"
BASELINE = ROOT / ".docs" / "baseline"


def test_skill_keeps_two_rulesync_source_models() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "Canonical fan-out" in text
    assert "Native bridge" in text
    assert "`generate`" in text
    assert "`convert`" in text


def test_skill_requires_preview_and_preserves_source() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "Preview every write" in text
    assert "Preserve the selected source of truth" in text
    assert "Do not silently rename, copy, relocate, or normalize" in text


def test_skill_does_not_require_custom_wrapper() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "Do not add a wrapper script" in text


def test_caller_and_baseline_documents_exist() -> None:
    assert (ROOT / "README.md").is_file()
    assert (BASELINE / "intent.md").is_file()
    assert (BASELINE / "requirements.md").is_file()
    assert (BASELINE / "decisions.md").is_file()


def test_frontmatter_keeps_compatibility_out_of_metadata() -> None:
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]

    assert "compatibility:" in frontmatter
    assert "author: mols3131d" in frontmatter
    assert 'version: "0.1.0"' in frontmatter
    assert "backend:" not in frontmatter
    assert "portability:" not in frontmatter
