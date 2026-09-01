from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.agent_assets import skills_promptfoo as evaluator

ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT / "evals" / "promptfoo"


@pytest.mark.parametrize("skill", ["..", "../other", "nested/skill", "nested\\skill"])
def test_skill_name_rejects_path_components(skill: str) -> None:
    with pytest.raises(ValueError, match="directory name"):
        evaluator._skill_name({"skill": skill})


def test_provider_rejects_generated_skill_mismatch() -> None:
    result = evaluator.call_api(
        "ignored",
        {
            "config": {
                "skill": "other-skill",
                "mode": "fixture",
                "suite": "trigger",
            }
        },
        {
            "vars": {
                "skill": "mols-rpi",
                "expected_selection": {
                    "selected_skills": [],
                    "primary_skill": None,
                },
            }
        },
    )

    assert result["output"] == ""
    assert "does not match generated test skill" in result["error"]


def test_load_cases_rejects_malformed_fixture_shape(
    tmp_path: Path,
    monkeypatch,
) -> None:
    fixture = tmp_path / "evals" / "skills" / "example-skill" / "cases.json"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(json.dumps(["not-an-object"]), encoding="utf-8")
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    with pytest.raises(ValueError, match="unsupported eval fixture shape"):
        evaluator._load_cases("example-skill")


def test_generator_validates_semantic_and_threshold_types() -> None:
    with pytest.raises(ValueError, match="semantic must be a boolean"):
        evaluator.generate_tests(
            {"skill": "mols-rpi", "suite": "behavior", "semantic": "false"}
        )

    with pytest.raises(ValueError, match="rubric_threshold"):
        evaluator.generate_tests(
            {
                "skill": "mols-rpi",
                "suite": "behavior",
                "semantic": True,
                "rubric_threshold": True,
            }
        )


def test_semantic_behavior_projection_preserves_rubric_contract(monkeypatch) -> None:
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:test-grader")
    cases = evaluator._load_cases("mols-rpi")
    case_id = next(
        case_id
        for case_id, case in cases.items()
        if evaluator._case_suite(case["mode"]) == evaluator.BEHAVIOR_SUITE
    )
    generated = evaluator.generate_tests(
        {
            "skill": "mols-rpi",
            "suite": "behavior",
            "case_ids": [case_id],
            "semantic": True,
            "rubric_threshold": 0.85,
        }
    )

    semantic = next(
        check for check in generated[0]["assert"] if check["type"] == "llm-rubric"
    )
    assert semantic["provider"] == "ollama:chat:test-grader"
    assert semantic["threshold"] == 0.85
    assert semantic["metric"] == "behavior-contract"
    assert "observable assistant response" in semantic["value"]
    for assertion in cases[case_id]["assertions"]:
        assert assertion in semantic["value"]


def test_routing_candidates_accept_serialized_json_and_reject_malformed_json() -> None:
    candidates = [
        {
            "name": "agent-skill-authoring",
            "description": "Create or modify Agent Skills.",
        }
    ]

    assert evaluator._routing_candidates(json.dumps(candidates), "mols-rpi") == candidates
    with pytest.raises(ValueError, match="not valid JSON"):
        evaluator._routing_candidates("not-json", "mols-rpi")


@pytest.mark.parametrize(
    "payload",
    [
        ["not", "an", "object"],
        {
            "selected_skills": ["mols-rpi", "mols-rpi"],
            "primary_skill": "mols-rpi",
        },
        {"selected_skills": ["mols-rpi"], "primary_skill": None},
        {"selected_skills": [], "primary_skill": "mols-rpi"},
    ],
)
def test_trigger_response_rejects_invalid_selection_envelopes(payload: object) -> None:
    assert evaluator._trigger_response_error(payload) is not None


def test_behavior_output_grader_requires_observable_text() -> None:
    assert evaluator.assert_behavior_output("observable response", {})["pass"] is True
    assert evaluator.assert_behavior_output("   ", {})["pass"] is False


def test_runtime_promptfoo_config_selects_valid_cases_and_semantics() -> None:
    fixture = evaluator._load_cases("mols-rpi")
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-rpi.yaml").read_text(encoding="utf-8")
    )
    generated_by_suite = {
        entry["config"]["suite"]: entry["config"] for entry in config["tests"]
    }

    assert generated_by_suite["trigger"]["semantic"] is False
    assert generated_by_suite["behavior"]["semantic"] is True
    assert generated_by_suite["behavior"]["rubric_threshold"] == 0.8

    for suite, generated in generated_by_suite.items():
        selected = generated["case_ids"]
        assert selected
        assert len(selected) == len(set(selected))
        assert all(case_id in fixture for case_id in selected)
        assert all(
            evaluator._case_suite(fixture[case_id]["mode"]) == suite
            for case_id in selected
        )
