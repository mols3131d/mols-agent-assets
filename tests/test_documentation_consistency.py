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


def test_common_reference_entrypoints_exist() -> None:
    common = DOCS / "references" / "common"
    expected = {
        "rulesync.md",
        "naming.md",
        "chatbot-compatibility.md",
        "design-principles.md",
        "instruction-authoring.md",
        "front-matter-cms.md",
    }

    assert expected <= {path.name for path in common.glob("*.md")}
