from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.agent_assets import skills_promptfoo as evaluator


def _fixtures(root: Path) -> tuple[Path, dict]:
    directory = root / "evals/skills/example-skill"
    directory.mkdir(parents=True)
    source = {
        "version": 1,
        "cases": [
            {
                "id": "source",
                "mode": "behavior",
                "prompt": 'Review the existing "project policy" only.',
                "assertions": ["Preserves the declared policy", "Claims no execution"],
            }
        ],
    }
    (directory / "cases.json").write_text(json.dumps(source), encoding="utf-8")
    samples = {
        "version": 1,
        "cases": [
            {
                "id": "known-bad",
                "source_case": "source",
                "response": "I replaced your policy.",
                "expected_criteria": [False, False],
            },
            {
                "id": "known-good",
                "source_case": "source",
                "response": "Keep the policy. No tools were run.",
                "expected_criteria": [True, True],
            },
        ],
    }
    path = directory / "grader-cases.json"
    path.write_text(json.dumps(samples), encoding="utf-8")
    return path, samples


def test_grader_reuses_source_contract_without_leaking_labels(tmp_path, monkeypatch):
    _fixtures(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    tests = evaluator.generate_grader_tests({"skill": "example-skill"})

    assert tests[0]["vars"]["task"] == tests[1]["vars"]["task"]
    assert tests[0]["providers"] == ["example-skill-grader"]
    assert tests[0]["vars"]["candidate_response"] == "I replaced your policy."
    assert tests[0]["metadata"]["expected_criteria"] == [False, False]
    assert tests[1]["metadata"]["expected_criteria"] == [True, True]
    assert "expected_criteria" not in tests[0]["vars"]
    assert tests[0]["assert"] == tests[1]["assert"]


@pytest.mark.parametrize(
    "changes",
    [
        {"source_case": "missing"},
        {"expected_criteria": [True]},
        {"expected_criteria": [1, False]},
        {"response": "  "},
        {"id": "known-good"},
    ],
)
def test_grader_rejects_broken_samples(tmp_path, monkeypatch, changes):
    path, samples = _fixtures(tmp_path)
    samples["cases"][0].update(changes)
    path.write_text(json.dumps(samples), encoding="utf-8")
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    with pytest.raises(ValueError):
        evaluator.generate_grader_tests({"skill": "example-skill"})


@pytest.mark.parametrize("content", ["", "not-json", '{"response":'])
def test_invalid_model_json_preserves_content_and_finish_metadata(monkeypatch, content):
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps(
                {
                    "message": {"content": content, "thinking": "private trace"},
                    "done_reason": "length",
                    "eval_count": 12,
                }
            ).encode()

    monkeypatch.setattr(
        evaluator.request, "urlopen", lambda *args, **kwargs: Response()
    )
    result = evaluator._ollama_request("task", "system", {})

    assert "content is not valid JSON" in result["error"]
    assert result["output"] == content
    assert result["metadata"] == {"done_reason": "length", "eval_count": 12}
    assert "private trace" not in json.dumps(result)


def test_transport_failure_stays_an_error(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("connection refused")

    monkeypatch.setattr(evaluator.request, "urlopen", fail)

    result = evaluator._ollama_request("task", "system", {})

    assert "transport/envelope failed" in result["error"]
    assert result["output"] == ""


@pytest.mark.parametrize(
    "value, expected", [(None, None), ("false", False), ("true", True)]
)
def test_runtime_thinking_override_is_explicit(monkeypatch, value, expected):
    captured = []
    if value is None:
        monkeypatch.delenv("PROMPTFOO_RUNTIME_THINK", raising=False)
    else:
        monkeypatch.setenv("PROMPTFOO_RUNTIME_THINK", value)

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({"message": {"content": '{"response":"ok"}'}}).encode()

    def urlopen(req, **kwargs):
        captured.append(json.loads(req.data))
        return Response()

    monkeypatch.setattr(evaluator.request, "urlopen", urlopen)
    evaluator._ollama_request("task", "system", {})

    if expected is None:
        assert "think" not in captured[0]
    else:
        assert captured[0]["think"] is expected


def test_invalid_thinking_override_does_not_call_provider(monkeypatch):
    monkeypatch.setenv("PROMPTFOO_RUNTIME_THINK", "auto")
    monkeypatch.setattr(
        evaluator.request, "urlopen", lambda *args, **kwargs: pytest.fail()
    )

    assert (
        "must be true or false"
        in evaluator._ollama_request("task", "system", {})["error"]
    )


def test_non_ollama_grader_configuration_is_preserved(tmp_path, monkeypatch):
    _fixtures(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "custom:existing-grader")

    generated = evaluator.generate_tests(
        {"skill": "example-skill", "suite": "behavior"}
    )

    semantic = [c for c in generated[0]["assert"] if c["type"] == "llm-rubric"]
    assert all(c["provider"] == "custom:existing-grader" for c in semantic)
