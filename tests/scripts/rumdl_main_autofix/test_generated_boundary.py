from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
RUMDL = ROOT / ".rumdl.toml"
AUTOFIX = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
SKILL_INDEXES = ROOT / ".github" / "workflows" / "skill-indexes.yml"
RULESYNC = ROOT / ".github" / "workflows" / "rulesync.yml"


def test_rulesync_source_and_runtime_surfaces_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert "src/rulesync/** rulesync-source" in attributes
    assert "src/rulesync/.rulesync/skills/INDEX.jsonl linguist-generated" in attributes
    for forbidden in [
        ".github/skills/** linguist-generated",
        ".github/agents/** linguist-generated",
        ".agents/rules/** linguist-generated",
        ".agents/skills/** linguist-generated",
        ".agents/agents/** linguist-generated",
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

    assert 'uvx rumdl@0.2.6 fmt "${files[@]}"' in workflow
    assert "git check-attr rulesync-source" not in workflow
    assert "git check-attr linguist-generated" not in workflow
    assert "generate_skill_indexes.py" not in workflow
    assert "rulesync generate" not in workflow


def test_skill_index_workflow_owns_index_generation() -> None:
    workflow = SKILL_INDEXES.read_text(encoding="utf-8")
    assert "python scripts/generate_skill_indexes.py" in workflow
    assert "src/rulesync/.rulesync/skills/INDEX.jsonl" in workflow


def test_pr_verifier_uses_isolated_rulesync_workspace() -> None:
    workflow = RULESYNC.read_text(encoding="utf-8")

    assert "Validate canonical Markdown normalization" in workflow
    assert "npm run rulesync:doctor" in workflow
    assert "npm run rulesync:validate" in workflow
    assert "Validate generated Markdown normalization" not in workflow
    assert "git check-attr linguist-generated" not in workflow
    assert "npx rulesync generate" not in workflow
