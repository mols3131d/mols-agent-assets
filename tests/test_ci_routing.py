from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "targeted-tests.yml"


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


def test_eval_changes_run_promptfoo_smoke() -> None:
    workflow = workflow_text()

    assert "fetch-depth: 2" in workflow
    assert "evals/skills/mols-rpi/*" in workflow
    assert "scripts/evals/*" in workflow
    assert "promptfoo=true" in workflow
    assert "Run mols-rpi Promptfoo smoke" in workflow
    assert "npm run eval:promptfoo:mols-rpi:smoke" in workflow


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
