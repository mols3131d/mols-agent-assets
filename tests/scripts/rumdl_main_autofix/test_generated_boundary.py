from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"
AUTOFIX = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
AGENTSMESH = ROOT / ".github" / "workflows" / "agentsmesh.yml"


def test_agentsmesh_source_and_runtime_surfaces_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert "src/agentsmesh/** agentsmesh-source" in attributes
    assert "src/agentsmesh/skills/INDEX.jsonl linguist-generated" in attributes
    for forbidden in [
        ".github/skills/** linguist-generated",
        ".github/agents/** linguist-generated",
        ".agents/rules/** linguist-generated",
        ".agents/skills/** linguist-generated",
    ]:
        assert forbidden not in attributes


def test_rumdl_config_keeps_repository_markdown_policy() -> None:
    config = RUMDL.read_text(encoding="utf-8")
    assert "[MD054]" not in config
    assert 'disable = ["MD013", "MD025", "MD033", "MD041"]' in config
    assert "[MD057]" in config
    assert "compact-paths = false" in config


def test_main_autofix_formats_source_without_native_projection() -> None:
    workflow = AUTOFIX.read_text(encoding="utf-8")

    assert "git check-attr agentsmesh-source" in workflow
    assert 'uvx rumdl@0.2.6 fmt "${files[@]}"' in workflow
    assert "python scripts/generate_skill_indexes.py" in workflow
    assert "agentsmesh generate" not in workflow
    assert ".github/skills" not in workflow
    assert ".agents/skills" not in workflow


def test_pr_verifier_uses_temporary_agentsmesh_projection() -> None:
    workflow = AGENTSMESH.read_text(encoding="utf-8")

    assert "Validate canonical Markdown normalization" in workflow
    assert "npm run agentsmesh:lint" in workflow
    assert "npm run agentsmesh:check" in workflow
    assert "npm run agentsmesh:generate:check" in workflow
    assert "Validate generated Markdown normalization" not in workflow
    assert "git check-attr linguist-generated" not in workflow
    assert "npx agentsmesh generate" not in workflow
