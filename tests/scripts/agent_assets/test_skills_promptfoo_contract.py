from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.agent_assets import skills_promptfoo as evaluator

ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT / "evals" / "promptfoo"


def _write_skill(root: Path, skill_name: str = "example-skill") -> None:
    path = (
        root
        / "src"
        / "rulesync"
        / ".rulesync"
        / "skills"
        / skill_name
        / "SKILL.md"
    )
    path.parent.mkdir(parents=True)
    path.write_text(
        "---\n"
        f"name: {skill_name}\n"
        "description: Use for example work.\n"
        "---\n\n"
        "# Example Skill\n\nFollow the example behavior contract.\n",
        encoding="utf-8",
    )


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
                "skill": "mols-loops",
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
            {"skill": "mols-loops", "suite": "behavior", "semantic": "false"}
        )

    with pytest.raises(ValueError, match="rubric_threshold"):
        evaluator.generate_tests(
            {
                "skill": "mols-loops",
                "suite": "behavior",
                "semantic": True,
                "rubric_threshold": True,
            }
        )


def test_semantic_behavior_projection_preserves_rubric_contract(monkeypatch) -> None:
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:test-grader")
    cases = evaluator._load_cases("mols-loops")
    case_id = next(
        case_id
        for case_id, case in cases.items()
        if evaluator._case_suite(case["mode"]) == evaluator.BEHAVIOR_SUITE
    )
    generated = evaluator.generate_tests(
        {
            "skill": "mols-loops",
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

    assert evaluator._routing_candidates(json.dumps(candidates), "mols-loops") == candidates
    with pytest.raises(ValueError, match="not valid JSON"):
        evaluator._routing_candidates("not-json", "mols-loops")


@pytest.mark.parametrize(
    "payload",
    [
        ["not", "an", "object"],
        {
            "selected_skills": ["mols-loops", "mols-loops"],
            "primary_skill": "mols-loops",
        },
        {"selected_skills": ["mols-loops"], "primary_skill": None},
        {"selected_skills": [], "primary_skill": "mols-loops"},
    ],
)
def test_trigger_response_rejects_invalid_selection_envelopes(payload: object) -> None:
    assert evaluator._trigger_response_error(payload) is not None


def test_behavior_output_grader_requires_observable_text() -> None:
    assert evaluator.assert_behavior_output("observable response", {})["pass"] is True
    assert evaluator.assert_behavior_output("   ", {})["pass"] is False


def test_trigger_provider_rejection_only_routes_and_does_not_use_skill_body(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_skill(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    captured: list[str] = []

    def fake_request(prompt: str, system: str, schema: dict):
        captured.append(system)
        payload = {"selected_skills": [], "primary_skill": None}
        return payload, json.dumps(payload)

    monkeypatch.setattr(evaluator, "_ollama_request", fake_request)
    result = evaluator.call_api(
        "Do something unrelated.",
        {
            "config": {
                "skill": "example-skill",
                "mode": "ollama",
                "suite": "trigger",
            }
        },
        {"vars": {"skill": "example-skill", "routing_candidates": []}},
    )

    assert len(captured) == 1
    assert "description: Use for example work." in captured[0]
    assert "# Example Skill" not in captured[0]
    assert json.loads(result["output"]) == {
        "selected_skills": [],
        "primary_skill": None,
    }


def test_trigger_provider_preserves_competing_metadata_and_primary_selection(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_skill(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    candidate = {
        "name": "specific-owner",
        "description": "Own this specific task and remain primary when applicable.",
    }
    captured: list[str] = []

    def fake_request(prompt: str, system: str, schema: dict):
        captured.append(system)
        payload = {
            "selected_skills": ["specific-owner", "example-skill"],
            "primary_skill": "specific-owner",
        }
        return payload, json.dumps(payload)

    monkeypatch.setattr(evaluator, "_ollama_request", fake_request)
    result = evaluator.call_api(
        "Use both applicable Skills.",
        {
            "config": {
                "skill": "example-skill",
                "mode": "ollama",
                "suite": "trigger",
            }
        },
        {"vars": {"skill": "example-skill", "routing_candidates": [candidate]}},
    )

    assert json.dumps([candidate], ensure_ascii=False, indent=2) in captured[0]
    assert json.loads(result["output"]) == {
        "selected_skills": ["specific-owner", "example-skill"],
        "primary_skill": "specific-owner",
    }


def test_runtime_promptfoo_config_selects_valid_cases_and_semantics() -> None:
    fixture = evaluator._load_cases("mols-loops")
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-loops.yaml").read_text(encoding="utf-8")
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


def test_ollama_sibling_routing_reuses_native_cases_and_avoids_telemetry_claim() -> None:
    ollama = yaml.safe_load(
        (CONFIG_DIR / "agent-asset-routing-ollama.yaml").read_text(encoding="utf-8")
    )
    native = yaml.safe_load(
        (CONFIG_DIR / "agent-asset-routing-native.yaml").read_text(encoding="utf-8")
    )
    assert ollama["providers"][0]["id"].endswith(":call_api")
    assert ollama["providers"][0]["label"] == "asset-routing-ollama"
    assert ollama["providers"][0]["config"] == {
        "skill": "mols-agent-asset",
        "mode": "ollama",
        "suite": "trigger",
    }
    assert ollama["tests"][0]["path"].endswith(":generate_tests")
    assert ollama["sharing"] is False
    assert ollama["writeLatestResults"] is False
    fixture = ollama["tests"][0]["config"]
    assert fixture["semantic"] is False
    assert fixture["case_ids"] == native["tests"][0]["config"]["case_ids"]
    generated = evaluator.generate_tests(fixture)
    assert len(generated) == 6
    assert all(test["providers"] == ["asset-routing-ollama"] for test in generated)
    assert all(test["metadata"]["suite"] == "trigger" for test in generated)
    assert all(not any(check["type"] == "skill-used" for check in test["assert"]) for test in generated)
    assert all(not any(check["type"] == "llm-rubric" for check in test["assert"]) for test in generated)
    assert all("expected_selection" not in test["vars"]["task"] for test in generated)
    expected = {test["vars"]["case_id"]: test["vars"]["expected_selection"] for test in generated}
    assert expected["install-routes-to-find"] == {
        "selected_skills": ["mols-agent-asset-find"],
        "primary_skill": "mols-agent-asset-find",
    }
    assert expected["human-prose-does-not-activate"]["selected_skills"] == []


def test_ollama_sibling_routing_uses_competing_skill_metadata(monkeypatch) -> None:
    config = yaml.safe_load(
        (CONFIG_DIR / "agent-asset-routing-ollama.yaml").read_text(encoding="utf-8")
    )
    install = next(
        test
        for test in evaluator.generate_tests(config["tests"][0]["config"])
        if test["vars"]["case_id"] == "install-routes-to-find"
    )
    systems: list[str] = []

    def fake_request(prompt: str, system: str, schema: dict):
        systems.append(system)
        response = install["vars"]["expected_selection"]
        return response, json.dumps(response)

    monkeypatch.setattr(evaluator, "_ollama_request", fake_request)
    response = evaluator.call_api(
        install["vars"]["task"],
        {"config": config["providers"][0]["config"]},
        {"vars": install["vars"]},
    )
    assert len(systems) == 1
    assert "mols-agent-asset-find" in systems[0]
    assert "# Mols Agent Asset" not in systems[0]
    assert evaluator.assert_trigger(response["output"], {"vars": install["vars"]})["pass"] is True


def test_native_trigger_projects_real_skill_usage_without_answer_leak() -> None:
    config = {
        "skill": "mols-agent-asset",
        "suite": "trigger",
        "available_skills": ["mols-agent-asset", "mols-agent-asset-find"],
        "case_ids": [
            "skill-authoring-activates",
            "install-routes-to-find",
            "human-prose-does-not-activate",
        ],
    }
    generated = evaluator.generate_native_tests(config)
    assert [test["vars"]["case_id"] for test in generated] == config["case_ids"]
    assert [[check["type"] for check in test["assert"]] for test in generated] == [
        ["skill-used", "not-skill-used"],
        ["not-skill-used", "skill-used"],
        ["not-skill-used", "not-skill-used"],
    ]
    assert all("expected_selection" not in case["vars"] for case in generated)
    assert all(case["metadata"]["lane"] == "native" for case in generated)


def test_native_behavior_requires_usage_and_semantic_criteria(monkeypatch) -> None:
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:test-grader")
    generated = evaluator.generate_native_tests(
        {
            "skill": "mols-loops",
            "suite": "behavior",
            "case_ids": ["plan-is-not-permission"],
        }
    )
    assert generated[0]["assert"][0]["type"] == "skill-used"
    assert generated[0]["assert"][0]["value"] == "mols-loops"
    assert generated[0]["vars"]["task"].startswith("Use $mols-loops for this task:")
    assert "계획서에 배포한다고" in generated[0]["vars"]["task"]
    assert generated[0]["metadata"]["activation"] == "explicit"
    assert generated[0]["metadata"]["evidence_scope"] == "response-only"
    assert any(
        check["metric"] == "native-response-contract"
        for check in generated[0]["assert"]
    )
    assert any(check["type"] == "llm-rubric" for check in generated[0]["assert"])


def test_native_eval_rejects_unstaged_selected_skill() -> None:
    with pytest.raises(ValueError, match="missing expected Skills"):
        evaluator.generate_native_tests(
            {
                "skill": "mols-agent-asset",
                "suite": "trigger",
                "case_ids": ["install-routes-to-find"],
            }
        )


def test_native_configs_select_valid_cases() -> None:
    profiles = {
        "mols-loops-native.yaml": {"mols-loops", "mols-agent-asset"},
        "agent-asset-routing-native.yaml": {
            "mols-agent-asset",
            "mols-agent-asset-find",
        },
    }
    for filename, staged_skills in profiles.items():
        config = yaml.safe_load((CONFIG_DIR / filename).read_text(encoding="utf-8"))
        assert config["providers"][0]["id"] == "openai:codex-sdk"
        assert config["providers"][0]["config"]["sandbox_mode"] == "read-only"
        assert config["providers"][0]["config"]["cli_env"]["CODEX_HOME"] == "{{ env.CODEX_EVAL_HOME }}"
        assert config["sharing"] is False
        assert config["writeLatestResults"] is False
        for entry in config["tests"]:
            fixture = entry["config"]
            assert set(fixture["available_skills"]) == staged_skills
            assert entry["path"].endswith(":generate_native_tests")
            assert evaluator.generate_native_tests(fixture)


def test_native_behavior_and_routing_are_separate_conditions() -> None:
    routing = evaluator.generate_native_tests(
        {
            "skill": "mols-loops",
            "suite": "trigger",
            "case_ids": ["explicit-rpi-activates"],
        }
    )[0]
    behavior = evaluator.generate_native_tests(
        {
            "skill": "mols-loops",
            "suite": "behavior",
            "case_ids": ["plan-is-not-permission"],
        }
    )[0]
    assert routing["vars"]["task"] == "이 작업 RPI로 진행해줘."
    assert "Use $mols-loops" not in routing["vars"]["task"]
    assert behavior["vars"]["task"].startswith("Use $mols-loops")
    assert behavior["metadata"]["suite"] == "behavior"


@pytest.mark.parametrize("suite", ["trigger", "behavior"])
def test_native_eval_rejects_empty_case_selection(suite: str) -> None:
    with pytest.raises(ValueError, match="requires at least one case"):
        evaluator.generate_native_tests(
            {"skill": "mols-loops", "suite": suite, "case_ids": []}
        )


def test_native_competing_skill_routing_reuses_canonical_cases() -> None:
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-loops-native.yaml").read_text(encoding="utf-8")
    )
    trigger = next(entry["config"] for entry in config["tests"] if entry["config"]["suite"] == "trigger")
    assert {
        "specific-owner-remains-primary-when-rpi-composes",
        "specific-owner-one-shot-does-not-pull-rpi",
    } <= set(trigger["case_ids"])
    cases = {
        case["vars"]["case_id"]: case
        for case in evaluator.generate_native_tests(trigger)
    }
    composed = cases["specific-owner-remains-primary-when-rpi-composes"]
    one_shot = cases["specific-owner-one-shot-does-not-pull-rpi"]
    assert {(x["type"], x["value"]) for x in composed["assert"]} == {
        ("skill-used", "mols-loops"), ("skill-used", "mols-agent-asset")
    }
    assert {(x["type"], x["value"]) for x in one_shot["assert"]} == {
        ("not-skill-used", "mols-loops"), ("skill-used", "mols-agent-asset")
    }
    for case in (composed, one_shot):
        assert "expected_selection" not in case["vars"]
        assert case["metadata"]["evidence_scope"] == "skill-file-read-heuristic"


def test_native_composition_behavior_grades_response_only() -> None:
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-loops-native.yaml").read_text(encoding="utf-8")
    )
    behavior = next(entry["config"] for entry in config["tests"] if entry["config"]["suite"] == "behavior")
    assert "rpi-composes-with-domain-skill" in behavior["case_ids"]
    generated = evaluator.generate_native_tests(behavior)
    assert all(test["metadata"]["evidence_scope"] == "response-only" for test in generated)
    assert all(
        {check["metric"] for check in test["assert"]}
        == {"native-skill-use", "native-response-present", "native-response-contract"}
        for test in generated
    )
