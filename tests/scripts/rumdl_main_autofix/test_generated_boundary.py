from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
AUTOFIX = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
AGENTSMESH = ROOT / ".github" / "workflows" / "agentsmesh.yml"
GENERATED_MARKERS = {
    ".github/copilot-instructions.md linguist-generated",
    ".github/skills/** linguist-generated",
    ".github/agents/** linguist-generated",
    ".agents/rules/** linguist-generated",
    ".agents/skills/** linguist-generated",
}


def test_agentsmesh_source_and_generated_markers_have_separate_roles() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert ".agentsmesh/** agentsmesh-source" in attributes
    assert "agentsmesh-managed" not in attributes
    for marker in GENERATED_MARKERS:
        assert marker in attributes


def test_main_autofix_formats_source_then_regenerates_then_normalizes() -> None:
    workflow = AUTOFIX.read_text(encoding="utf-8")

    assert "git check-attr agentsmesh-source" in workflow
    assert "git check-attr linguist-generated" in workflow
    assert 'uvx rumdl@0.2.6 fmt "${files[@]}"' in workflow
    assert "npx agentsmesh generate" in workflow
    assert 'uvx rumdl@0.2.6 fmt "${managed[@]}"' in workflow
    assert "npx agentsmesh check" in workflow
    assert "npx agentsmesh generate --check" in workflow

    source_fmt = workflow.index('uvx rumdl@0.2.6 fmt "${files[@]}"')
    generate = workflow.index("npx agentsmesh generate")
    managed_fmt = workflow.index('uvx rumdl@0.2.6 fmt "${managed[@]}"')
    agentsmesh_check = workflow.index("npx agentsmesh check")
    assert source_fmt < generate < managed_fmt < agentsmesh_check

    assert "rumdl@0.2.6 check" not in workflow
    assert "agentsmesh-managed" not in workflow


def test_pr_verifier_checks_rumdl_format_idempotence() -> None:
    workflow = AGENTSMESH.read_text(encoding="utf-8")

    assert "Validate canonical Markdown normalization" in workflow
    assert "Validate generated Markdown normalization" in workflow
    assert "git check-attr linguist-generated" in workflow
    assert workflow.count("uvx rumdl@0.2.6 fmt") >= 2
    assert workflow.count("git diff --exit-code") >= 2
    assert "rumdl@0.2.6 check" not in workflow

    canonical = workflow.index("Validate canonical Markdown normalization")
    drift = workflow.index("Validate generated drift")
    generated = workflow.index("Validate generated Markdown normalization")
    assert canonical < drift < generated
