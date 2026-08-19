from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "targeted-tests.yml"


def test_eval_changes_have_a_deterministic_test_target() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "fetch-depth: 2" in workflow
    assert '"evals/skills/**"' in workflow
    assert '"tests/evals/**"' in workflow
    assert "add_eval()" in workflow
    assert 'root_targets["tests/evals"]=1' in workflow
    assert "evals/skills/*)" in workflow
    assert 'add_eval "${name%%/*}"' in workflow


def test_canonical_skill_changes_validate_the_committed_index() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    skill_case = "src/rulesync/.rulesync/skills/*)"
    assert "add_skill_index()" in workflow
    assert 'root_targets["tests/scripts/generate_skill_indexes"]=1' in workflow
    assert skill_case in workflow
    assert "add_skill_index" in workflow.split(skill_case, 1)[1]
