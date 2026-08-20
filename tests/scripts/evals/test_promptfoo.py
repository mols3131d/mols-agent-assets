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


def test_generator_reuses_canonical_fixture_without_semantic_duplication() -> None:
    canonical = _canonical_cases()
    generated = ADAPTER.generate_tests({"semantic": False})

    assert [test["vars"]["case_id"] for test in generated] == list(ADAPTER.DEFAULT_CASE_IDS)
    for test in generated:
        case = canonical[test["vars"]["case_id"]]
        assert test["vars"]["task"] == case["prompt"]
        assert test["vars"]["mode"] == case["mode"]
        assert test["vars"]["expected_activation"] is (case["mode"] != "activation-negative")
        assert [check["type"] for check in test["assert"]] == ["python"]


def test_semantic_grader_projects_canonical_assertions(monkeypatch) -> None:
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:test-grader")
    canonical = _canonical_cases()
    generated = ADAPTER.generate_tests({"semantic": True})

    for test in generated:
        case = canonical[test["vars"]["case_id"]]
        semantic = next(check for check in test["assert"] if check["type"] == "llm-rubric")
        assert semantic["provider"] == "ollama:chat:test-grader"
        for criterion in case["assertions"]:
            assert criterion in semantic["value"]


def test_runtime_envelope_requires_exact_keys_and_types() -> None:
    assert ADAPTER._runtime_envelope_error({"activation": True, "response": "ok"}) is None
    assert ADAPTER._runtime_envelope_error(["not", "an", "object"]) is not None
    assert ADAPTER._runtime_envelope_error(
        {"activation": True, "response": "ok", "debug": "hidden"}
    ) is not None
    assert ADAPTER._runtime_envelope_error({"activation": "true", "response": "ok"}) is not None


def test_deterministic_grader_checks_envelope_and_activation() -> None:
    passing = ADAPTER.get_assert(
        json.dumps({"activation": False, "response": "normal answer"}),
        {"vars": {"expected_activation": False}},
    )
    mismatch = ADAPTER.get_assert(
        json.dumps({"activation": True, "response": "wrong route"}),
        {"vars": {"expected_activation": False}},
    )
    malformed = ADAPTER.get_assert("not-json", {"vars": {}})
    extra = ADAPTER.get_assert(
        json.dumps({"activation": False, "response": "normal answer", "debug": "unexpected"}),
        {"vars": {"expected_activation": False}},
    )

    assert passing["pass"] is True
    assert mismatch["pass"] is False
    assert malformed["pass"] is False
    assert extra["pass"] is False


def test_fixture_provider_is_plumbing_only() -> None:
    result = ADAPTER.call_api(
        "ignored",
        {"config": {"mode": "fixture"}},
        {"vars": {"expected_activation": False}},
    )
    payload = json.loads(result["output"])

    assert payload["activation"] is False
    assert "not runtime behavior evidence" in payload["response"]


def test_activation_routes_with_metadata_then_executes_full_skill(monkeypatch) -> None:
    captured: list[dict] = []
    responses = iter(
        [
            {"activation": True, "response": "selected"},
            {"response": "Research before Plan; Review controls the next transition."},
        ]
    )

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(next(responses))

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("PROMPTFOO_RUNTIME_MODEL", "qwen2.5:test")

    task = "이 작업 RPI로 진행해줘."
    result = ADAPTER.call_api(
        task,
        {"config": {"mode": "ollama"}},
        {"vars": {"mode": "activation"}},
    )
    payload = json.loads(result["output"])
    skill = ADAPTER.SKILL_PATH.read_text(encoding="utf-8")
    canonical = _canonical_cases()["explicit-rpi-activates"]

    assert len(captured) == 2
    assert captured[0]["model"] == "qwen2.5:test"
    assert captured[0]["messages"][1]["content"] == task
    assert captured[0]["format"] == ADAPTER.RUNTIME_ENVELOPE_SCHEMA
    assert ADAPTER._skill_frontmatter(skill) in captured[0]["messages"][0]["content"]
    assert "# Mols RPI" not in captured[0]["messages"][0]["content"]
    assert captured[1]["format"] == ADAPTER.BEHAVIOR_RESPONSE_SCHEMA
    assert skill in captured[1]["messages"][0]["content"]
    assert canonical["assertions"][0] not in captured[1]["messages"][0]["content"]
    assert payload["activation"] is True
    assert "Research before Plan" in payload["response"]


def test_negative_activation_never_loads_skill_body(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {"activation": False, "response": "for와 while은 반복 조건이 다릅니다."}
        )

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)

    result = ADAPTER.call_api(
        "Python for loop와 while loop 차이를 설명해줘.",
        {"config": {"mode": "ollama"}},
        {"vars": {"mode": "activation-negative"}},
    )
    payload = json.loads(result["output"])

    assert len(captured) == 1
    assert captured[0]["format"] == ADAPTER.RUNTIME_ENVELOPE_SCHEMA
    assert "# Mols RPI" not in captured[0]["messages"][0]["content"]
    assert payload["activation"] is False


def test_behavior_mode_skips_routing_and_uses_full_skill(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_urlopen(api_request, timeout):
        captured.append(json.loads(api_request.data.decode("utf-8")))
        return _fake_response(
            {"response": "Review에서 확장을 제안하고 Research와 Plan을 갱신해야 합니다."}
        )

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)

    result = ADAPTER.call_api(
        "작업 중 보니 범위를 넓혀야 해.",
        {"config": {"mode": "ollama"}},
        {"vars": {"mode": "scope-control"}},
    )
    payload = json.loads(result["output"])
    skill = ADAPTER.SKILL_PATH.read_text(encoding="utf-8")

    assert len(captured) == 1
    assert captured[0]["format"] == ADAPTER.BEHAVIOR_RESPONSE_SCHEMA
    assert skill in captured[0]["messages"][0]["content"]
    assert payload["activation"] is True
    assert "Research" in payload["response"]


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


def test_promptfoo_configs_keep_results_disposable() -> None:
    expected_ids = list(ADAPTER.DEFAULT_CASE_IDS)
    expected_semantic = {
        "mols-rpi-smoke.yaml": False,
        "mols-rpi.yaml": True,
    }

    for name, semantic in expected_semantic.items():
        config = yaml.safe_load((CONFIG_DIR / name).read_text(encoding="utf-8"))
        assert config["sharing"] is False
        assert config["writeLatestResults"] is False
        assert config["commandLineOptions"]["cache"] is False
        assert config["commandLineOptions"]["write"] is False
        assert config["commandLineOptions"]["noShare"] is True
        assert config["tests"][0]["config"]["case_ids"] == expected_ids
        assert config["tests"][0]["config"]["semantic"] is semantic
