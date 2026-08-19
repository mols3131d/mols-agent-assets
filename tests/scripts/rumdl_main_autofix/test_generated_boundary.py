from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"
AUTOFIX = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
AGENTSMESH = ROOT / ".github" / "workflows" / "agentsmesh.yml"
GENERATED_MARKERS = {
    ".github/copilot-instructions.md linguist-generated",
    ".github/skills/** linguist-generated",
    ".github/agents/** linguist-generated",
    ".agents/rules/** linguist-generated",
    ".agents/skills/** linguist-generated",
}
GENERATED_MD047_IGNORES = {
    '".github/copilot-instructions.md" = ["MD047"]',
    '".github/skills/**/*.md" = ["MD047"]',
    '".github/agents/**/*.md" = ["MD047"]',
    '".agents/rules/**/*.md" = ["MD047"]',
    '".agents/skills/**/*.md" = ["MD047"]',
}


def test_agentsmesh_source_and_generated_markers_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert ".agentsmesh/** agentsmesh-source" in attributes
    assert "agentsmesh-managed" not in attributes
    for marker in GENERATED_MARKERS:
        assert marker in attributes


def test_rumdl_config_matches_agentsmesh_serialization() -> None:
    config = RUMDL.read_text(encoding="utf-8")
    assert "[MD054]" not in config
    assert 'disable = ["MD013", "MD025", "MD033", "MD041"]' in config
    assert 'disable = ["MD013", "MD025", "MD033", "MD041", "MD047"]' not in config
    assert "[per-file-ignores]" in config
    for ignore in GENERATED_MD047_IGNORES:
        assert ignore in config
    assert "Keep this list aligned with every Markdown projection target in agentsmesh.yaml." in config
    assert "If another vendor target is added later" in config
    assert "[MD057]" in config
    assert "compact-paths = false" in config


def test_main_autofix_formats_source_then_regenerates_then_formats_generated() -> None:
    workflow = AUTOFIX.read_text(encoding="utf-8")

    source_fmt = 'uvx rumdl@0.2.6 fmt "${files[@]}"'
    generated_fmt = 'uvx rumdl@0.2.6 fmt "${generated[@]}"'

    assert "git check-attr agentsmesh-source" in workflow
    assert "git check-attr linguist-generated" in workflow
    assert source_fmt in workflow
    assert "npx agentsmesh generate" in workflow
    assert generated_fmt in workflow
    assert "npx agentsmesh check" in workflow
    assert "npx agentsmesh generate --check" in workflow

    assert workflow.index(source_fmt) < workflow.index("npx agentsmesh generate")
    assert workflow.index("npx agentsmesh generate") < workflow.index(generated_fmt)
    assert workflow.index(generated_fmt) < workflow.index("npx agentsmesh check")

    assert "rumdl@0.2.6 check" not in workflow
    assert "agentsmesh-managed" not in workflow
    assert "--disable MD047" not in workflow
    assert "--disable MD047,MD057" not in workflow


def test_pr_verifier_uses_shared_rumdl_config_for_all_markdown() -> None:
    workflow = AGENTSMESH.read_text(encoding="utf-8")

    assert "Validate canonical Markdown normalization" in workflow
    assert "Validate generated Markdown normalization" in workflow
    assert "git check-attr linguist-generated" in workflow
    assert "--disable MD047" not in workflow
    assert "--disable MD047,MD057" not in workflow
    assert "rumdl@0.2.6 check" not in workflow

    canonical_fmt = 'uvx rumdl@0.2.6 fmt "${markdown[@]}"'
    generated_fmt = 'uvx rumdl@0.2.6 fmt "${generated[@]}"'
    assert canonical_fmt in workflow
    assert generated_fmt in workflow
    assert workflow.index(canonical_fmt) < workflow.index(generated_fmt)
