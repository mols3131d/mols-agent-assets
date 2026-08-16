from pathlib import Path


SKILL = (
    Path(__file__).parents[3]
    / "src"
    / "skills"
    / "rulesync-agent-assets"
    / "SKILL.md"
)


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
