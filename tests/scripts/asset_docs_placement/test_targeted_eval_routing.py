from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "targeted-tests.yml"


def test_eval_changes_run_full_deterministic_suite_and_promptfoo_smoke() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "fetch-depth: 2" in workflow
    assert "pytest -q tests" in workflow
    assert "evals/skills/mols-rpi/*" in workflow
    assert "scripts/evals/*" in workflow
    assert "promptfoo=true" in workflow
    assert "npm run eval:promptfoo:mols-rpi:smoke" in workflow


def test_canonical_skill_changes_validate_distribution_routes() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "src/rulesync/.rulesync/skills/*/SKILL.md" in workflow
    assert "routes=true" in workflow
    assert "python scripts/generate_distribution_routes.py" in workflow
    assert "git diff --exit-code -- route/skills.jsonl" in workflow
