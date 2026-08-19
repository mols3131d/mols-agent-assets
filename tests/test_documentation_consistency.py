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


def test_repository_convention_entrypoints_exist() -> None:
    conventions = DOCS / "references" / "common" / "conventions"
    expected = {
        "rulesync-repository-conventions.md",
        "agent-assets-naming-convention.md",
        "chatbot-repository-bootstrap.md",
    }

    assert expected <= {path.name for path in conventions.glob("*.md")}
