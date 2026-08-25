from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "optional-validation.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_optional_validation_is_manual_and_default_off() -> None:
    workflow = workflow_text()

    assert "workflow_dispatch:" in workflow
    for name in ("docs_indexes", "routes", "rulesync"):
        assert f"      {name}:" in workflow
    assert workflow.count("        default: false") == 3
    assert "pull_request:" not in workflow
    assert "push:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "contents: write" not in workflow
    assert "git push" not in workflow


def test_optional_validation_keeps_heavy_or_unrelated_checks_out() -> None:
    workflow = workflow_text().lower()

    assert "generate_docs_indexes.py --check" in workflow
    assert "generate_distribution_routes.py" in workflow
    assert "generate_repository_routes.py" in workflow
    assert "rulesync:doctor" in workflow
    assert "promptfoo" not in workflow
    assert "rumdl" not in workflow
    assert "mise run check" not in workflow
