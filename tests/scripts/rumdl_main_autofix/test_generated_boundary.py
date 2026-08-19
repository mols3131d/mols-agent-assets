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
    # Root projection files used by major coding-agent targets.
    '"AGENTS.md" = ["MD047"]',
    '"CLAUDE.md" = ["MD047"]',
    '"GEMINI.md" = ["MD047"]',
    '"QWEN.md" = ["MD047"]',
    '"CONVENTIONS.md" = ["MD047"]',
    '"CRUSH.md" = ["MD047"]',
    '"replit.md" = ["MD047"]',
    # Current and predeclared vendor projection directories.
    '".codex/**/*.md" = ["MD047"]',
    '".agents/**/*.md" = ["MD047"]',
    '".claude/**/*.md" = ["MD047"]',
    '".grok/**/*.md" = ["MD047"]',
    '".gemini/**/*.md" = ["MD047"]',
    '".github/copilot-instructions.md" = ["MD047"]',
    '".github/instructions/**/*.md" = ["MD047"]',
    '".github/prompts/**/*.md" = ["MD047"]',
    '".github/skills/**/*.md" = ["MD047"]',
    '".github/agents/**/*.md" = ["MD047"]',
    '".amazonq/**/*.md" = ["MD047"]',
    '".kiro/**/*.md" = ["MD047"]',
    '".cursor/**/*.md" = ["MD047"]',
    '".windsurf/**/*.md" = ["MD047"]',
    '".junie/**/*.md" = ["MD047"]',
    '".augment/**/*.md" = ["MD047"]',
    '".cline/**/*.md" = ["MD047"]',
    '".continue/**/*.md" = ["MD047"]',
    '".roo/**/*.md" = ["MD047"]',
    '".trae/**/*.md" = ["MD047"]',
    '".factory/**/*.md" = ["MD047"]',
    '".opencode/**/*.md" = ["MD047"]',
    '".qwen/**/*.md" = ["MD047"]',
    '".warp/**/*.md" = ["MD047"]',
    '".kilo/**/*.md" = ["MD047"]',
    '".deepagents/**/*.md" = ["MD047"]',
    '".crush/**/*.md" = ["MD047"]',
    '".pi/**/*.md" = ["MD047"]',
    '".rovodev/**/*.md" = ["MD047"]',
    '".aider/**/*.md" = ["MD047"]',
    '".replit/**/*.md" = ["MD047"]',
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
    assert "even when the corresponding target directory does not exist yet" in config
    assert "When a new vendor target is added" in config
    assert "Grok is predeclared for a future AgentsMesh/plugin target" in config
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
