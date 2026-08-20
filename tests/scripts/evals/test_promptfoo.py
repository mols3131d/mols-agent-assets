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


def test_generator_reuses_canonical_fixture_without_semantic_duplication() -> None:
    canonical = _canonical_cases()
    generated = ADAPTER.generate_tests({"semantic": False})

    assert [test["vars"]["case_id"] for test in generated] == list(ADAPTER.DEFAULT_CASE_IDS)
    for test in generated:
        case = canonical[test["vars"]["case_id"]]
        assert test["vars"]["task"] == case["prompt"]
        assert test["vars"]["mode"] == case["mode"]
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

    assert passing["pass"] is True
    assert mismatch["pass"] is False
    assert malformed["pass"] is False


def test_fixture_provider_is_plumbing_only() -> None:
    result = ADAPTER.call_api(
        "ignored",
        {"config": {"mode": "fixture"}},
        {"vars": {"expected_activation": False}},
    )
    payload = json.loads(result["output"])

    assert payload["activation"] is False
    assert "not runtime behavior evidence" in payload["response"]


def test_ollama_runtime_gets_skill_and_task_but_not_expected_assertions(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self) -> bytes:
            payload = {
                "message": {
                    "content": json.dumps(
                        {"activation": True, "response": "RPI response"}, ensure_ascii=False
                    )
                }
            }
            return json.dumps(payload).encode("utf-8")

    def fake_urlopen(api_request, timeout):
        captured["timeout"] = timeout
        captured["body"] = json.loads(api_request.data.decode("utf-8"))
        return FakeResponse()

    monkeypatch.setattr(ADAPTER.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("PROMPTFOO_RUNTIME_MODEL", "qwen2.5:test")

    task = "이 작업 RPI로 진행해줘."
    result = ADAPTER.call_api(task, {"config": {"mode": "ollama"}}, {"vars": {}})
    body = captured["body"]
    canonical = _canonical_cases()["explicit-rpi-activates"]
    system = body["messages"][0]["content"]

    assert result.get("error") is None
    assert body["model"] == "qwen2.5:test"
    assert body["messages"][1]["content"] == task
    assert ADAPTER.SKILL_PATH.read_text(encoding="utf-8") in system
    assert canonical["assertions"][0] not in system


def test_runner_defaults_are_local_and_non_sharing() -> None:
    env = RUNNER.build_env({"PROMPTFOO_DISABLE_TELEMETRY": "0"})

    assert env["PROMPTFOO_DISABLE_TELEMETRY"] == "0"
    assert env["PROMPTFOO_DISABLE_UPDATE"] == "1"
    assert env["PROMPTFOO_DISABLE_REMOTE_GENERATION"] == "true"
    assert env["PROMPTFOO_DISABLE_SHARING"] == "1"
    assert env["PROMPTFOO_CONFIG_DIR"] == str(ROOT / ".tmp" / "promptfoo")
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
