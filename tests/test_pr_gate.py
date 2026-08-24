from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "targeted-tests.yml"
MISE = ROOT / "mise.toml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_pr_gate_is_minimal_read_only_deterministic_gate() -> None:
    workflow = workflow_text()

    assert "name: PR Gate" in workflow
    assert "    paths:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "git push" not in workflow
    assert "contents: write" not in workflow
    assert "actions/setup-python@v6" in workflow
    assert "astral-sh/setup-uv@v9" in workflow
    assert 'version: "0.12.1"' in workflow
    assert "enable-cache: true" in workflow
    assert "uv run --locked" in workflow
    assert "pytest -q tests" in workflow

    for delegated_surface in (
        "Classify change impact",
        "mise run check",
        "rulesync:doctor",
        "generate_distribution_routes.py",
        "generate_repository_routes.py",
        "generate_docs_indexes.py",
        "rumdl fmt",
        "promptfoo",
    ):
        assert delegated_surface.lower() not in workflow.lower()


def test_behavioral_eval_is_local_not_pr_gate() -> None:
    workflow = workflow_text()
    mise = MISE.read_text(encoding="utf-8")

    assert "promptfoo" not in workflow.lower()
    assert "[tasks.eval-mols-rpi-smoke]" in mise
    assert "npm run eval:promptfoo:mols-rpi:smoke" in mise
    assert "[tasks.eval-mols-rpi]" in mise
    assert "npm run eval:promptfoo:mols-rpi" in mise
