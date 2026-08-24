from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "targeted-tests.yml"
MISE = ROOT / "mise.toml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_pr_gate_is_stable_read_only_and_runs_full_deterministic_suite() -> None:
    workflow = workflow_text()

    assert "name: PR Gate" in workflow
    assert "    paths:" not in workflow
    assert "name: PR Gate\n    runs-on:" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "git push" not in workflow
    assert "contents: write" not in workflow
    assert "mise run check" in workflow
    assert "uv run --locked" in workflow
    assert "uv run --frozen" not in workflow
    assert "pytest -q tests" in workflow


def test_behavioral_eval_is_local_not_pr_gate() -> None:
    workflow = workflow_text()
    mise = MISE.read_text(encoding="utf-8")

    assert "promptfoo" not in workflow.lower()
    assert "[tasks.eval-mols-rpi-smoke]" in mise
    assert "npm run eval:promptfoo:mols-rpi:smoke" in mise
    assert "[tasks.eval-mols-rpi]" in mise
    assert "npm run eval:promptfoo:mols-rpi" in mise


def test_canonical_skill_changes_validate_distribution_routes() -> None:
    workflow = workflow_text()

    assert "src/rulesync/.rulesync/skills/*/SKILL.md" in workflow
    assert "routes=true" in workflow
    assert "python scripts/generate_distribution_routes.py" in workflow
    assert "git diff --exit-code -- route/skills.jsonl" in workflow


def test_markdown_and_rulesync_changes_use_read_only_validation() -> None:
    workflow = workflow_text()

    assert "Validate changed Markdown normalization" in workflow
    assert 'rumdl fmt "${markdown[@]}"' in workflow
    assert "Validate canonical Rulesync source" in workflow
    assert "npm run rulesync:doctor" in workflow
    assert "rulesync:validate" not in workflow
    assert "--targets" not in workflow
