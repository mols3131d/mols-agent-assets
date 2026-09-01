from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.agent_assets import skills_promptfoo as evaluator

ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT / "evals" / "promptfoo"


def _write_generic_skill(root: Path, skill_name: str = "example-skill") -> None:
    skill = (
        root
        / "src"
        / "rulesync"
        / ".rulesync"
        / "skills"
        / skill_name
        / "SKILL.md"
    )
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\n"
        f"name: {skill_name}\n"
        "description: Use for example iterative work.\n"
        "---\n\n"
        "# Example Skill\n\nFollow the example behavior contract.\n",
        encoding="utf-8",
    )

    fixture = root / "evals" / "skills" / skill_name / "cases.json"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(
        json.dumps(
            {
                "version": 1,
                "cases": [
                    {
                        "id": "activates",
                        "mode": "activation",
                        "prompt": "Use the example skill.",
                        "expected_selection": {
                            "selected_skills": [skill_name],
                            "primary_skill": skill_name,
                        },
                    },
                    {
                        "id": "rejects",
                        "mode": "activation-negative",
                        "prompt": "Do something unrelated.",
                        "expected_selection": {
                            "selected_skills": [],
                            "primary_skill": None,
                        },
                    },
                    {
                        "id": "behaves",
                        "mode": "behavior",
                        "prompt": "Apply the behavior contract.",
                        "assertions": ["Follows the example behavior contract"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )


def _fake_response(payload: dict):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self) -> bytes:
            response = {"message": {"content": json.dumps(payload, ensure_ascii=False)}}
            return json.dumps(response).encode("utf-8")

    return FakeResponse()


def test_generic_skill_generates_trigger_and_behavior_without_python_adapter(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_generic_skill(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    trigger = evaluator.generate_tests(
        {"skill": "example-skill", "suite": "trigger", "semantic": False}
    )
    behavior = evaluator.generate_tests(
        {"skill": "example-skill", "suite": "behavior", "semantic": False}
    )

    assert [case["vars"]["case_id"] for case in trigger] == ["activates", "rejects"]
    assert [case["vars"]["case_id"] for case in behavior] == ["behaves"]
    assert all(case["metadata"]["skill"] == "example-skill" for case in trigger + behavior)
    assert all(case["vars"]["skill"] == "example-skill" for case in trigger + behavior)
    assert trigger[0]["providers"] == ["example-skill-trigger"]
    assert behavior[0]["providers"] == ["example-skill-behavior"]
    assert trigger[0]["assert"][0]["value"] == (
        "file://../../scripts/agent_assets/skills_promptfoo.py:assert_trigger"
    )


def test_mols_rpi_fixture_projects_all_cases_through_generic_evaluator() -> None:
    fixture = json.loads(
        evaluator.fixture_path("mols-rpi").read_text(encoding="utf-8")
    )["cases"]
    expected_trigger = [
        case["id"]
        for case in fixture
        if evaluator._case_suite(case["mode"]) == evaluator.TRIGGER_SUITE
    ]
    expected_behavior = [
        case["id"]
        for case in fixture
        if evaluator._case_suite(case["mode"]) == evaluator.BEHAVIOR_SUITE
    ]

    trigger = evaluator.generate_tests(
        {"skill": "mols-rpi", "suite": "trigger", "semantic": False}
    )
    behavior = evaluator.generate_tests(
        {"skill": "mols-rpi", "suite": "behavior", "semantic": False}
    )

    assert [case["vars"]["case_id"] for case in trigger] == expected_trigger
    assert [case["vars"]["case_id"] for case in behavior] == expected_behavior


def test_generator_rejects_missing_skill_and_cross_suite_case() -> None:
    with pytest.raises(ValueError, match="skill"):
        evaluator.generate_tests({"suite": "trigger"})

    with pytest.raises(ValueError, match="belongs to behavior"):
        evaluator.generate_tests(
            {
                "skill": "mols-rpi",
                "suite": "trigger",
                "case_ids": ["scope-expansion-is-review-gated"],
                "semantic": False,
            }
        )


def test_trigger_contract_uses_selected_skill_name_not_mols_rpi() -> None:
    case = {
        "expected_selection": {
            "selected_skills": ["example-skill"],
            "primary_skill": "example-skill",
        }
    }
    expected, candidates = evaluator._trigger_case_contract(
        case,
        "activation",
        "example-skill",
    )

    assert expected["selected_skills"] == ["example-skill"]
    assert candidates == []

    with pytest.raises(ValueError, match="redefine example-skill"):
        evaluator._routing_candidates(
            [{"name": "example-skill", "description": "duplicate"}],
            "example-skill",
        )


def test_trigger_grader_checks_exact_selected_set_and_primary() -> None:
    expected = {
        "selected_skills": ["agent-skill-authoring", "mols-rpi"],
        "primary_skill": "agent-skill-authoring",
    }
    passing = evaluator.assert_trigger(
        json.dumps(
            {
                "selected_skills": ["mols-rpi", "agent-skill-authoring"],
                "primary_skill": "agent-skill-authoring",
            }
        ),
        {"vars": {"expected_selection": expected}},
    )
    mismatch = evaluator.assert_trigger(
        json.dumps(
            {
                "selected_skills": ["mols-rpi", "agent-skill-authoring"],
                "primary_skill": "mols-rpi",
            }
        ),
        {"vars": {"expected_selection": expected}},
    )

    assert passing["pass"] is True
    assert mismatch["pass"] is False
    assert evaluator.assert_trigger("not-json", {"vars": {}})["pass"] is False


def test_fixture_provider_is_skill_agnostic() -> None:
    expected = {"selected_skills": [], "primary_skill": None}
    trigger = evaluator.call_api(
        "ignored",
        {
            "config": {
                "skill": "example-skill",
                "mode": "fixture",
                "suite": "trigger",
            }
        },
        {"vars": {"expected_selection": expected}},
    )
    behavior = evaluator.call_api(
        "ignored",
        {
            "config": {
                "skill": "example-skill",
                "mode": "fixture",
                "suite": "behavior",
            }
        },
        {"vars": {}},
    )

    assert json.loads(trigger["output"]) == expected
    assert "not runtime behavior evidence" in behavior["output"]


def test_trigger_provider_uses_only_skill_discovery_metadata(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_generic_skill(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {
                "selected_skills": ["example-skill"],
                "primary_skill": "example-skill",
            }
        )

    monkeypatch.setattr(evaluator.request, "urlopen", fake_urlopen)
    result = evaluator.call_api(
        "Use the example skill.",
        {
            "config": {
                "skill": "example-skill",
                "mode": "ollama",
                "suite": "trigger",
            }
        },
        {"vars": {"routing_candidates": []}},
    )

    system = captured[0]["messages"][0]["content"]
    assert "description: Use for example iterative work." in system
    assert "# Example Skill" not in system
    assert json.loads(result["output"])["primary_skill"] == "example-skill"


def test_behavior_provider_uses_full_selected_skill(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_generic_skill(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response({"response": "Applied the example behavior contract."})

    monkeypatch.setattr(evaluator.request, "urlopen", fake_urlopen)
    result = evaluator.call_api(
        "Apply the behavior contract.",
        {
            "config": {
                "skill": "example-skill",
                "mode": "ollama",
                "suite": "behavior",
            }
        },
        {"vars": {}},
    )

    system = captured[0]["messages"][0]["content"]
    assert "# Example Skill" in system
    assert "Routing has already selected" in system
    assert result["output"] == "Applied the example behavior contract."


def test_promptfoo_configs_use_generic_skill_evaluator() -> None:
    for name in ("mols-rpi.yaml", "mols-rpi-smoke.yaml"):
        config = yaml.safe_load((CONFIG_DIR / name).read_text(encoding="utf-8"))
        for provider in config["providers"]:
            assert provider["id"].endswith("skills_promptfoo.py:call_api")
            assert provider["config"]["skill"] == "mols-rpi"
        for generated in config["tests"]:
            assert generated["path"].endswith("skills_promptfoo.py:generate_tests")
            assert generated["config"]["skill"] == "mols-rpi"
        assert config["sharing"] is False
        assert config["writeLatestResults"] is False
        assert config["commandLineOptions"]["cache"] is False
        assert config["commandLineOptions"]["write"] is False
        assert config["commandLineOptions"]["noShare"] is True
