from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ATTRIBUTES = ROOT / ".gitattributes"
WORKFLOW = ROOT / ".github" / "workflows" / "rumdl-main-autofix.yml"
GENERATED_MARKERS = {
    ".github/copilot-instructions.md linguist-generated",
    ".github/skills/** linguist-generated",
    ".github/agents/** linguist-generated",
    ".agents/rules/** linguist-generated",
    ".agents/skills/** linguist-generated",
}


def test_agentsmesh_markdown_projections_are_marked_generated() -> None:
    attributes = ATTRIBUTES.read_text(encoding="utf-8")
    for marker in GENERATED_MARKERS:
        assert marker in attributes


def test_rumdl_autofix_filters_generated_files_via_attributes() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "git check-attr linguist-generated" in workflow
    assert '[[ "$attr" == *": linguist-generated: set" ]] && continue' in workflow
    assert 'uvx rumdl@0.2.6 fmt "${files[@]}"' in workflow

    for marker in GENERATED_MARKERS:
        path = marker.split(" ", 1)[0]
        assert path not in workflow
