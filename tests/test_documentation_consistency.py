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


def test_readme_language_variants_are_not_used() -> None:
    variants = list(ROOT.glob("README.*.md"))
    for directory in ("src", "docs", "evals", "tests", "scripts"):
        variants.extend((ROOT / directory).rglob("README.*.md"))

    assert sorted(path.relative_to(ROOT) for path in variants) == []


def test_current_guidance_uses_rulesync_native_exception_model() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    development = (DOCS / "development.md").read_text(encoding="utf-8")

    assert "과도기" not in readme
    assert "src/rules/" not in development

    assert "Rulesync가 표현하지 못하는" in readme
    assert "Rulesync가 표현하지 못하는" in development
    assert "repository-local superset schema" not in readme
    assert "parallel taxonomy" in development


def test_retired_guidance_is_not_current_docs() -> None:
    obsolete = {
        "agentsmesh-migration-plan.md",
        "agentsmesh-migration-census.md",
        "agentsmesh-migration-report.md",
        "skill-configuration.md",
        "agent-assets-standard-baseline.md",
        "agent-assets-standard-personal.md",
        "agent-assets-rules-projections.md",
        "agent-assets-skills-standard-personal.md",
        "agent-assets-skills-target-profiles.md",
    }
    current = {path.name for path in DOCS.rglob("*.md")}
    assert obsolete.isdisjoint(current)
