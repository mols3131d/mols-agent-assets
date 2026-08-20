from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"
AUTOFIX = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
DISTRIBUTION_ROUTES = ROOT / ".github" / "workflows" / "distribution-routes.yml"
RULESYNC = ROOT / ".github" / "workflows" / "rulesync.yml"


def test_rulesync_source_and_runtime_surfaces_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert "src/rulesync/** rulesync-source" in attributes
    assert "route/skills.jsonl linguist-generated" in attributes
    assert "src/rulesync/.rulesync/skills/INDEX.jsonl linguist-generated" not in attributes
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


def test_main_autofix_only_formats_markdown() -> None:
    workflow = AUTOFIX.read_text(encoding="utf-8")

    assert "mise install rumdl" in workflow
    assert 'mise exec -- rumdl fmt "${files[@]}"' in workflow
    assert "uvx rumdl" not in workflow
    assert "git check-attr rulesync-source" not in workflow
    assert "git check-attr linguist-generated" not in workflow
    assert "generate_distribution_routes.py" not in workflow
    assert "rulesync generate" not in workflow


def test_distribution_route_workflow_owns_generation() -> None:
    workflow = DISTRIBUTION_ROUTES.read_text(encoding="utf-8")
    assert "python scripts/generate_distribution_routes.py" in workflow
    assert "route/skills.jsonl" in workflow
    assert ".agents/routes" not in workflow
    assert "src/rulesync/.rulesync/skills/INDEX.jsonl" not in workflow


def test_pr_verifier_checks_canonical_rulesync_source_only() -> None:
    workflow = RULESYNC.read_text(encoding="utf-8")

    assert "Validate canonical Markdown normalization" in workflow
    assert "npm run rulesync:doctor" in workflow
    assert "rulesync:validate" not in workflow
    assert "--targets" not in workflow
    assert "Validate generated Markdown normalization" not in workflow
    assert "git check-attr linguist-generated" not in workflow
    assert "npx rulesync generate" not in workflow
