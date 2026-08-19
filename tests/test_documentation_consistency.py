from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_docs_have_no_empty_markdown_placeholders() -> None:
    empty = [
        path.relative_to(ROOT)
        for path in DOCS.rglob("*.md")
        if not path.read_text(encoding="utf-8").strip()
    ]
    assert empty == []


def test_current_guidance_uses_custom_exception_model() -> None:
    readme_ko = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_en = (ROOT / "README.en.md").read_text(encoding="utf-8")
    development = (DOCS / "development.md").read_text(encoding="utf-8")

    assert "과도기" not in readme_ko
    assert "transitional" not in readme_en.lower()
    assert "not yet migrated" not in readme_en
    assert "src/rules/" not in development

    assert "custom/non-standard" in readme_en
    assert "custom/non-standard" in development


def test_completed_migration_records_are_not_current_docs() -> None:
    obsolete = {
        "agentsmesh-migration-plan.md",
        "agentsmesh-migration-census.md",
        "agentsmesh-migration-report.md",
        "skill-configuration.md",
    }
    assert obsolete.isdisjoint({path.name for path in DOCS.iterdir() if path.is_file()})
