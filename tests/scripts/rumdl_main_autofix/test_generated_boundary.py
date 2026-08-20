from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"
PR_GATE = ROOT / ".github" / "workflows" / "targeted-tests.yml"


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


def test_pr_gate_owns_read_only_repository_admission() -> None:
    workflow = PR_GATE.read_text(encoding="utf-8")

    assert "name: PR Gate" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "git push" not in workflow
    assert "contents: write" not in workflow


def test_pr_gate_checks_markdown_routes_and_rulesync() -> None:
    workflow = PR_GATE.read_text(encoding="utf-8")

    assert "Validate changed Markdown normalization" in workflow
    assert 'rumdl fmt "${markdown[@]}"' in workflow
    assert "python scripts/generate_distribution_routes.py" in workflow
    assert "git diff --exit-code -- route/skills.jsonl" in workflow
    assert "Validate canonical Rulesync source" in workflow
    assert "npm run rulesync:doctor" in workflow
    assert "rulesync:validate" not in workflow
    assert "--targets" not in workflow
