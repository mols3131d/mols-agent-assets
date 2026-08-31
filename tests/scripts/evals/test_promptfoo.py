from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import yaml

ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "scripts" / "evals" / "run_promptfoo.py"
ADAPTER_PATH = ROOT / "scripts" / "evals" / "promptfoo_mols_rpi.py"
FIXTURE_PATH = ROOT / "evals" / "skills" / "mols-rpi" / "cases.json"
CONFIG_DIR = ROOT / "evals" / "promptfoo"


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUNNER = _load_module("run_promptfoo", RUNNER_PATH)
ADAPTER = _load_module("promptfoo_mols_rpi", ADAPTER_PATH)


def _canonical_cases() -> dict[str, dict]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return {case["id"]: case for case in payload["cases"]}


def _suite_case_ids(cases: dict[str, dict], suite: str) -> list[str]:
    return [
        case_id
        for case_id, case in cases.items()
        if ADAPTER._case_suite(case["mode"]) == suite
    ]


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


def test_trigger_generator_projects_all_canonical_trigger_cases_by_default() -> None:
    canonical = _canonical_cases()
    generated = ADAPTER.generate_tests({"suite": "trigger", "semantic": False})

    assert [test["vars"]["case_id"] for test in generated] == _suite_case_ids(
        canonical, "trigger"
    )
    for test in generated:
        case = canonical[test["vars"]["case_id"]]
        expected = case["expected_selection"]

        assert test["vars"]["task"] == case["prompt"]
        assert test["vars"]["mode"] == case["mode"]
        assert test["vars"]["expected_selection"] == expected
        assert test["vars"]["routing_candidates"] == case.get("routing_candidates", [])
        assert test["metadata"]["suite"] == "trigger"
        assert test["providers"] == [ADAPTER.TRIGGER_PROVIDER_LABEL]
        assert [check["type"] for check in test["assert"]] == ["python"]
        assert test["assert"][0]["metric"] == (
            "trigger-activation"
            if "mols-rpi" in expected["selected_skills"]
            else "trigger-rejection"
        )


def test_behavior_generator_projects_all_canonical_behavior_cases_by_default(
    monkeypatch,
) -> None:
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:test-grader")
    canonical = _canonical_cases()
    generated = ADAPTER.generate_tests(
        {"suite": "behavior", "semantic": True, "rubric_threshold": 0.85}
    )

    assert [test["vars"]["case_id"] for test in generated] == _suite_case_ids(
        canonical, "behavior"
    )
    for test in generated:
        case = canonical[test["vars"]["case_id"]]
        assert "expected_selection" not in test["vars"]
        assert "routing_candidates" not in test["vars"]
        assert test["metadata"]["suite"] == "behavior"
        assert test["providers"] == [ADAPTER.BEHAVIOR_PROVIDER_LABEL]

        semantic_checks = [
            check for check in test["assert"] if check["type"] == "llm-rubric"
        ]
        assert len(semantic_checks) == 1
        semantic = semantic_checks[0]
        assert semantic["provider"] == "ollama:chat:test-grader"
        assert semantic["threshold"] == 0.85
        assert semantic["metric"] == "behavior-contract"
        assert "observable assistant response" in semantic["value"]
        assert "hidden reasoning" in semantic["value"]
        for criterion in case["assertions"]:
            assert criterion in semantic["value"]


def test_generator_rejects_cross_suite_cases() -> None:
    try:
        ADAPTER.generate_tests(
            {
                "suite": "trigger",
                "case_ids": ["scope-expansion-is-review-gated"],
                "semantic": False,
            }
        )
    except ValueError as error:
        assert "belongs to behavior" in str(error)
    else:
        raise AssertionError("cross-suite case selection should fail")


def test_trigger_response_requires_exact_valid_selection() -> None:
    assert (
        ADAPTER._trigger_response_error(
            {"selected_skills": ["mols-rpi"], "primary_skill": "mols-rpi"}
        )
        is None
    )
    assert (
        ADAPTER._trigger_response_error({"selected_skills": [], "primary_skill": None})
        is None
    )
    assert ADAPTER._trigger_response_error(["not", "an", "object"]) is not None
    assert (
        ADAPTER._trigger_response_error(
            {
                "selected_skills": ["mols-rpi"],
                "primary_skill": "mols-rpi",
                "debug": True,
            }
        )
        is not None
    )
    assert (
        ADAPTER._trigger_response_error(
            {"selected_skills": ["mols-rpi", "mols-rpi"], "primary_skill": "mols-rpi"}
        )
        is not None
    )
    assert (
        ADAPTER._trigger_response_error(
            {"selected_skills": ["mols-rpi"], "primary_skill": "other"}
        )
        is not None
    )
    assert (
        ADAPTER._trigger_response_error(
            {"selected_skills": ["mols-rpi"], "primary_skill": None}
        )
        is not None
    )


def test_routing_candidates_accept_promptfoo_json_serialization() -> None:
    candidates = [
        {
            "name": "agent-skill-authoring",
            "description": "Create or modify Agent Skills.",
        }
    ]

    assert ADAPTER._routing_candidates(json.dumps(candidates)) == candidates
    try:
        ADAPTER._routing_candidates("not-json")
    except ValueError as error:
        assert "not valid JSON" in str(error)
    else:
        raise AssertionError("malformed routing candidate JSON should fail")


def test_trigger_grader_checks_exact_selected_set_and_primary() -> None:
    expected = {
        "selected_skills": ["agent-skill-authoring", "mols-rpi"],
        "primary_skill": "agent-skill-authoring",
    }
    passing = ADAPTER.assert_trigger(
        json.dumps(
            {
                "selected_skills": ["mols-rpi", "agent-skill-authoring"],
                "primary_skill": "agent-skill-authoring",
            }
        ),
        {"vars": {"expected_selection": expected}},
    )
    mismatch = ADAPTER.assert_trigger(
        json.dumps(
            {
                "selected_skills": ["mols-rpi", "agent-skill-authoring"],
                "primary_skill": "mols-rpi",
            }
        ),
        {"vars": {"expected_selection": expected}},
    )
    malformed = ADAPTER.assert_trigger(
        "not-json", {"vars": {"expected_selection": expected}}
    )
    missing_expected = ADAPTER.assert_trigger(
        json.dumps({"selected_skills": [], "primary_skill": None}),
        {"vars": {}},
    )

    assert passing["pass"] is True
    assert mismatch["pass"] is False
    assert malformed["pass"] is False
    assert missing_expected["pass"] is False


def test_behavior_output_grader_only_requires_observable_text() -> None:
    assert (
        ADAPTER.assert_behavior_output("Review에서 Research로 돌아갑니다.", {})["pass"]
        is True
    )
    assert ADAPTER.assert_behavior_output("  ", {})["pass"] is False


def test_fixture_provider_keeps_trigger_and_behavior_plumbing_separate() -> None:
    expected = {"selected_skills": [], "primary_skill": None}
    trigger = ADAPTER.call_api(
        "ignored",
        {"config": {"mode": "fixture", "suite": "trigger"}},
        {"vars": {"expected_selection": expected}},
    )
    behavior = ADAPTER.call_api(
        "ignored",
        {"config": {"mode": "fixture", "suite": "behavior"}},
        {"vars": {}},
    )

    assert json.loads(trigger["output"]) == expected
    assert "not runtime behavior evidence" in behavior["output"]


def test_trigger_provider_uses_only_discovery_metadata(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {"selected_skills": ["mols-rpi"], "primary_skill": "mols-rpi"}
        )

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("PROMPTFOO_RUNTIME_MODEL", "qwen2.5:test")

    task = "이 작업 RPI로 진행해줘."
    result = ADAPTER.call_api(
        task,
        {"config": {"mode": "ollama", "suite": "trigger"}},
        {"vars": {"mode": "activation", "routing_candidates": []}},
    )
    payload = json.loads(result["output"])
    skill = ADAPTER.SKILL_PATH.read_text(encoding="utf-8")

    assert len(captured) == 1
    assert captured[0]["model"] == "qwen2.5:test"
    assert captured[0]["messages"][1]["content"] == task
    assert captured[0]["format"] == ADAPTER.TRIGGER_RESPONSE_SCHEMA
    assert ADAPTER._skill_frontmatter(skill) in captured[0]["messages"][0]["content"]
    assert "# Mols RPI" not in captured[0]["messages"][0]["content"]
    assert payload == {"selected_skills": ["mols-rpi"], "primary_skill": "mols-rpi"}


def test_trigger_provider_does_not_generate_normal_answer_for_rejection(
    monkeypatch,
) -> None:
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response({"selected_skills": [], "primary_skill": None})

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)

    result = ADAPTER.call_api(
        "Python for loop와 while loop 차이를 설명해줘.",
        {"config": {"mode": "ollama", "suite": "trigger"}},
        {"vars": {"mode": "activation-negative", "routing_candidates": []}},
    )

    assert len(captured) == 1
    assert captured[0]["format"] == ADAPTER.TRIGGER_RESPONSE_SCHEMA
    assert "# Mols RPI" not in captured[0]["messages"][0]["content"]
    assert json.loads(result["output"]) == {
        "selected_skills": [],
        "primary_skill": None,
    }


def test_trigger_provider_routes_competing_metadata_and_keeps_specific_owner_primary(
    monkeypatch,
) -> None:
    captured: list[dict] = []
    candidate = {
        "name": "agent-skill-authoring",
        "description": (
            "Create or modify Agent Skills and their trigger or runtime instructions. "
            "Use as the primary capability when the requested work changes an Agent "
            "Skill."
        ),
    }

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {
                "selected_skills": ["agent-skill-authoring", "mols-rpi"],
                "primary_skill": "agent-skill-authoring",
            }
        )

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)

    result = ADAPTER.call_api(
        "이 Agent Skill을 RPI 개선 루프로 수정해줘.",
        {"config": {"mode": "ollama", "suite": "trigger"}},
        {"vars": {"mode": "activation", "routing_candidates": [candidate]}},
    )
    system = captured[0]["messages"][0]["content"]

    assert json.dumps([candidate], ensure_ascii=False, indent=2) in system
    assert (
        ADAPTER._skill_frontmatter(ADAPTER.SKILL_PATH.read_text(encoding="utf-8"))
        in system
    )
    assert "# Mols RPI" not in system
    assert json.loads(result["output"]) == {
        "selected_skills": ["agent-skill-authoring", "mols-rpi"],
        "primary_skill": "agent-skill-authoring",
    }


def test_behavior_provider_skips_routing_and_uses_full_skill(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {
                "response": (
                    "Review에서 확장을 제안하고 Research와 Plan을 갱신해야 합니다."
                )
            }
        )

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)

    result = ADAPTER.call_api(
        "작업 중 보니 범위를 넓혀야 해.",
        {"config": {"mode": "ollama", "suite": "behavior"}},
        {"vars": {"mode": "scope-control"}},
    )
    skill = ADAPTER.SKILL_PATH.read_text(encoding="utf-8")

    assert len(captured) == 1
    assert captured[0]["format"] == ADAPTER.BEHAVIOR_RESPONSE_SCHEMA
    assert skill in captured[0]["messages"][0]["content"]
    assert "Routing has already selected" in captured[0]["messages"][0]["content"]
    assert result["output"].startswith("Review에서")


def test_runner_defaults_are_local_and_non_sharing() -> None:
    env = RUNNER.build_env({"PROMPTFOO_DISABLE_TELEMETRY": "0"})
    state_dir = ROOT / ".tmp" / "promptfoo"

    assert env["PROMPTFOO_DISABLE_TELEMETRY"] == "0"
    assert env["PROMPTFOO_DISABLE_UPDATE"] == "1"
    assert env["PROMPTFOO_DISABLE_REMOTE_GENERATION"] == "true"
    assert env["PROMPTFOO_DISABLE_SHARING"] == "1"
    assert env["PROMPTFOO_CONFIG_DIR"] == str(state_dir)
    assert env["PROMPTFOO_LOG_DIR"] == str(state_dir / "logs")
    assert env["PROMPTFOO_CACHE_PATH"] == str(state_dir / "cache")
    assert env["PROMPTFOO_PYTHON"]
    assert RUNNER.parse_node_version("v22.22.0") == (22, 22, 0)


def test_promptfoo_configs_separate_suites_and_keep_results_disposable() -> None:
    canonical = _canonical_cases()
    runtime = yaml.safe_load((CONFIG_DIR / "mols-rpi.yaml").read_text(encoding="utf-8"))
    smoke = yaml.safe_load(
        (CONFIG_DIR / "mols-rpi-smoke.yaml").read_text(encoding="utf-8")
    )

    for config in (runtime, smoke):
        assert config["sharing"] is False
        assert config["writeLatestResults"] is False
        assert config["commandLineOptions"]["cache"] is False
        assert config["commandLineOptions"]["write"] is False
        assert config["commandLineOptions"]["noShare"] is True

        provider_labels = {provider["label"] for provider in config["providers"]}
        assert provider_labels == {
            ADAPTER.TRIGGER_PROVIDER_LABEL,
            ADAPTER.BEHAVIOR_PROVIDER_LABEL,
        }
        suites = {test["config"]["suite"] for test in config["tests"]}
        assert suites == {"trigger", "behavior"}

    runtime_tests = {
        test["config"]["suite"]: test["config"] for test in runtime["tests"]
    }
    smoke_tests = {test["config"]["suite"]: test["config"] for test in smoke["tests"]}

    assert runtime_tests["trigger"]["semantic"] is False
    assert runtime_tests["behavior"]["semantic"] is True
    assert runtime_tests["behavior"]["rubric_threshold"] == 0.8
    assert smoke_tests["trigger"]["semantic"] is False
    assert smoke_tests["behavior"]["semantic"] is False
    assert "case_ids" not in smoke_tests["trigger"]
    assert "case_ids" not in smoke_tests["behavior"]

    for suite in ("trigger", "behavior"):
        selected = runtime_tests[suite]["case_ids"]
        assert selected
        assert len(selected) == len(set(selected))
        assert all(case_id in canonical for case_id in selected)
        assert all(
            ADAPTER._case_suite(canonical[case_id]["mode"]) == suite
            for case_id in selected
        )
