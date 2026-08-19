from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
WORKFLOW = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
GENERATED_MARKERS = {
    ".github/copilot-instructions.md linguist-generated agentsmesh-managed",
    ".github/skills/** linguist-generated agentsmesh-managed",
    ".github/agents/** linguist-generated agentsmesh-managed",
    ".agents/rules/** linguist-generated agentsmesh-managed",
    ".agents/skills/** linguist-generated agentsmesh-managed",
}


def test_agentsmesh_sources_and_projections_are_marked_managed() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    assert ".agentsmesh/** agentsmesh-managed" in attributes
    for marker in GENERATED_MARKERS:
        assert marker in attributes


def test_rumdl_autofix_filters_agentsmesh_managed_files_via_attributes() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "git check-attr agentsmesh-managed" in workflow
    assert '[[ "$attr" == *": agentsmesh-managed: set" ]] && continue' in workflow
    assert 'uvx rumdl@0.2.6 fmt "${files[@]}"' in workflow

    assert ".agentsmesh/" not in workflow
    for marker in GENERATED_MARKERS:
        path = marker.split(" ", 1)[0]
        assert path not in workflow
