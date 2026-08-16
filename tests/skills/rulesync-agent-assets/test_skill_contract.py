from pathlib import Path


ROOT = Path(__file__).parents[3] / "src" / "skills" / "rulesync-agent-assets"
SKILL = ROOT / "SKILL.md"
BASELINE = ROOT / ".docs" / "baseline"


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_skill_keeps_three_routes() -> None:
    text = _skill_text()

    assert "Reuse" in text
    assert "Canonical fan-out" in text
    assert "Native bridge" in text
    assert "`generate`" in text
    assert "`convert`" in text


def test_reuse_requires_evidence() -> None:
    text = _skill_text()

    assert "Reuse requires evidence" in text
    assert "similarity alone is not evidence" in text


def test_skill_resolves_authority_before_mutation() -> None:
    text = _skill_text()

    assert "Repository or project authority" in text
    assert "caller-selected source" in text
    assert "stop before" in text


def test_skill_requires_preview_and_preserves_source() -> None:
    text = _skill_text()

    assert "Preview every Rulesync write" in text
    assert "Generated targets remain derived artifacts" in text
    assert "Do not silently rename, copy, relocate, normalize, or rewrite" in text


def test_skill_does_not_require_custom_wrapper() -> None:
    text = _skill_text()

    assert "Do not add a wrapper script" in text


def test_caller_and_baseline_documents_exist() -> None:
    assert (ROOT / "README.md").is_file()
    assert (BASELINE / "intent.md").is_file()
    assert (BASELINE / "requirements.md").is_file()
    assert (BASELINE / "decisions.md").is_file()


def test_frontmatter_keeps_runtime_compatibility_out_of_metadata() -> None:
    frontmatter = _skill_text().split("---", 2)[1]
    metadata = frontmatter.split("metadata:", 1)[1]

    assert "compatibility:" in frontmatter
    assert "Conversion routes require" in frontmatter
    assert "author: mols3131d" in metadata
    assert "version:" not in metadata
    assert "backend:" not in metadata
    assert "portability:" not in metadata
