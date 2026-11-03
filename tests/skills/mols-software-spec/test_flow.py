"""Deterministic contract tests for the portable software-spec workflow helper."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / "mols-software-spec"
SCRIPT = PACKAGE / "scripts" / "flow.py"
WORKFLOWS = PACKAGE / "assets" / "workflows"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def report_file(tmp_path: Path, report: dict) -> str:
    path = tmp_path / "review.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return str(path)


@pytest.mark.parametrize("preset", ["default", "focused"])
def test_bundled_workflows_validate(preset: str) -> None:
    result = run_cli("--workflow", str(WORKFLOWS / f"{preset}.json"), "validate")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["valid"] is True
    assert data["steps"][-1] == "review"
    assert "specification" in data["steps"]


def test_review_returns_to_specification_and_rechecks_dependents(tmp_path: Path) -> None:
    report = {"result": "rework", "findings": [{
        "target": "specification",
        "issue": "Missing concurrency guarantee",
        "evidence": ["specification.md#concurrent-writes"],
    }]}
    result = run_cli("route", "--review", report_file(tmp_path, report))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["return_to"] == "specification"
    assert data["recheck_steps"] == [
        "specification", "test-design", "test-implementation", "code-implementation", "review"
    ]
    assert "plan" not in data["recheck_steps"]


def test_review_test_code_finding_does_not_replan_unrelated_documents(tmp_path: Path) -> None:
    report = {"result": "rework", "findings": [{
        "target": "test-implementation", "issue": "Assertion is incorrect", "evidence": ["tests/test_api.py:50"]
    }]}
    result = run_cli("route", "--review", report_file(tmp_path, report))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["recheck_steps"] == [
        "test-implementation", "code-implementation", "review"
    ]


def test_multiple_findings_choose_earliest_return(tmp_path: Path) -> None:
    report = {"result": "rework", "findings": [
        {"target": "code-implementation", "issue": "bad branch", "evidence": ["src/api.py:10"]},
        {"target": "test-design", "issue": "missing case", "evidence": ["test-design.md#edge"]},
    ]}
    result = run_cli("route", "--review", report_file(tmp_path, report))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["return_to"] == "test-design"


def test_pass_is_only_candidate_completion(tmp_path: Path) -> None:
    result = run_cli("route", "--review", report_file(tmp_path, {
        "result": "pass", "evidence": ["CI run 412", "specification.md#acceptance"], "findings": []
    }))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "candidate_complete"
    assert "not validated" in json.loads(result.stdout)["warning"]


def test_pass_without_evidence_rejected(tmp_path: Path) -> None:
    result = run_cli("route", "--review", report_file(tmp_path, {"result": "pass", "evidence": []}))
    assert result.returncode == 2
    assert "evidence" in result.stderr


def test_unknown_review_target_rejected(tmp_path: Path) -> None:
    report = {"result": "rework", "findings": [{
        "target": "other", "issue": "unmatched", "evidence": ["review note"]
    }]}
    result = run_cli("route", "--review", report_file(tmp_path, report))
    assert result.returncode == 2
    assert "invalid target" in result.stderr


def test_blocked_does_not_claim_completion(tmp_path: Path) -> None:
    result = run_cli("route", "--review", report_file(tmp_path, {
        "result": "blocked", "reason": "No permission to inspect CI"
    }))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "blocked"


@pytest.mark.parametrize("mutation,fragment", [
    (lambda obj: obj["steps"][2]["after"].append("unavailable"), "dependency not earlier"),
    (lambda obj: obj["steps"][1]["artifacts"].append("made-up"), "unknown artifacts"),
    (lambda obj: obj["steps"][-1].update({"id": "other"}), "review must be the last"),
    (lambda obj: obj["steps"][3].update({"id": "proposal"}), "duplicate step"),
])
def test_invalid_workflow_rejected(tmp_path: Path, mutation, fragment: str) -> None:
    workflow = json.loads((WORKFLOWS / "default.json").read_text(encoding="utf-8"))
    mutation(workflow)
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps(workflow), encoding="utf-8")
    result = run_cli("--workflow", str(path), "validate")
    assert result.returncode == 2
    assert fragment in result.stderr


def test_focused_workflow_limits_recheck(tmp_path: Path) -> None:
    report = {"result": "rework", "findings": [{
        "target": "specification", "issue": "ambiguous status", "evidence": ["specification.md#state"]
    }]}
    result = run_cli(
        "--workflow", str(WORKFLOWS / "focused.json"),
        "route", "--review", report_file(tmp_path, report)
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["recheck_steps"] == [
        "specification", "code-implementation", "review"
    ]
