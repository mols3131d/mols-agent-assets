from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.agent_assets import skills_promptfoo as evaluator

ROOT = Path(__file__).resolve().parents[3]


def _write_skill_package(root: Path) -> None:
    package = root / "src" / "rulesync" / ".rulesync" / "skills" / "example-skill"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Test contracts.\n---\n"
        "# Example Skill\n"
        "Read references/oracle-validation.md only if the oracle is disputed.\n",
        encoding="utf-8",
    )
    folder = package / "references"
    folder.mkdir()
    (folder / "oracle-validation.md").write_text(
        "# Oracle Validation\nA VALID REFERENCE MARKER.\n", encoding="utf-8"
    )


def test_reference_paths_reject_traversal_and_duplicates() -> None:
    assert evaluator._reference_paths(["references/oracle-validation.md"]) == [
        "references/oracle-validation.md"
    ]
    for paths in (
        ["../outside.md"],
        ["references/../outside.md"],
        ["/references/oracle-validation.md"],
        ["references/oracle-validation.md", "references/oracle-validation.md"],
        ["references\\oracle-validation.md"],
    ):
        with pytest.raises(ValueError, match="invalid reference path"):
            evaluator._reference_paths(paths)


def test_conditional_reference_is_loaded_only_after_model_selection(
    tmp_path: Path, monkeypatch
) -> None:
    _write_skill_package(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    observed: list[str] = []

    def model_request(prompt: str, system: str, schema: dict):
        observed.append(system)
        if schema == evaluator.REFERENCE_SELECTION_SCHEMA:
            data = {"references": ["references/oracle-validation.md"]}
        else:
            data = {"response": "Inspected the independent oracle."}
        return data, json.dumps(data)

    monkeypatch.setattr(evaluator, "_ollama_request", model_request)
    result = evaluator.call_api(
        "The generated test contradicts an accepted behavior example.",
        {
            "config": {
                "skill": "example-skill",
                "suite": "behavior",
                "mode": "ollama",
                "reference_paths": ["references/oracle-validation.md"],
            }
        },
        {"vars": {"skill": "example-skill"}},
    )

    assert result["output"] == "Inspected the independent oracle."
    assert result["metadata"]["loaded_references"] == [
        "references/oracle-validation.md"
    ]
    assert result["tokenUsage"]["numRequests"] == 2
    assert len(observed) == 2
    assert "VALID REFERENCE MARKER" not in observed[0]
    assert "VALID REFERENCE MARKER" in observed[1]


def test_trivial_case_skips_reference_body_but_reports_decision(
    tmp_path: Path, monkeypatch
) -> None:
    _write_skill_package(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    observed: list[str] = []

    def model_request(prompt: str, system: str, schema: dict):
        observed.append(system)
        data = (
            {"references": []}
            if schema == evaluator.REFERENCE_SELECTION_SCHEMA
            else {"response": "A focused boundary test is enough."}
        )
        return data, json.dumps(data)

    monkeypatch.setattr(evaluator, "_ollama_request", model_request)
    response = evaluator.call_api(
        "A simple off-by-one test is requested.",
        {
            "config": {
                "skill": "example-skill",
                "suite": "behavior",
                "reference_paths": ["references/oracle-validation.md"],
            }
        },
        {"vars": {"skill": "example-skill"}},
    )

    assert response["metadata"]["loaded_references"] == []
    assert len(observed) == 2
    assert all("VALID REFERENCE MARKER" not in system for system in observed)


@pytest.mark.parametrize(
    "selected",
    [
        pytest.param(["references/../secrets.md"], id="traversal"),
        pytest.param(["references/unavailable.md"], id="unavailable"),
        pytest.param(
            ["references/oracle-validation.md", "references/oracle-validation.md"],
            id="duplicate",
        ),
        pytest.param([{}], id="object-element"),
        pytest.param([[]], id="array-element"),
        pytest.param(
            ["references/oracle-validation.md", {}], id="mixed-object-element"
        ),
        pytest.param(["references/oracle-validation.md", []], id="mixed-array-element"),
        pytest.param([None], id="null-element"),
        pytest.param([True], id="boolean-element"),
        pytest.param([1], id="number-element"),
        pytest.param(None, id="null-selection"),
        pytest.param("references/oracle-validation.md", id="string-selection"),
    ],
)
def test_invalid_model_reference_selection_fails_closed(
    tmp_path: Path, monkeypatch, selected: object
) -> None:
    _write_skill_package(tmp_path)
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    def model_request(prompt: str, system: str, schema: dict):
        raise_if_behavior = schema == evaluator.BEHAVIOR_RESPONSE_SCHEMA
        assert not raise_if_behavior
        data = {"references": selected}
        return data, json.dumps(data)

    def unexpected_reference_read(*args):
        pytest.fail("invalid reference selection must not load reference files")

    monkeypatch.setattr(evaluator, "_ollama_request", model_request)
    monkeypatch.setattr(
        evaluator, "_read_behavior_references", unexpected_reference_read
    )
    result = evaluator.call_api(
        "Disputed test oracle",
        {
            "config": {
                "skill": "example-skill",
                "suite": "behavior",
                "reference_paths": ["references/oracle-validation.md"],
            }
        },
        {"vars": {"skill": "example-skill"}},
    )
    assert result == {
        "error": "invalid or unavailable reference selection",
        "output": "",
    }


def test_reference_assertion_uses_actual_provider_metadata() -> None:
    path = "references/oracle-validation.md"
    variables = {"vars": {"expected_loaded_references": [path]}}
    passing = evaluator.assert_reference_loading(
        "meaningful output",
        {**variables, "metadata": {"loaded_references": [path]}},
    )
    missing = evaluator.assert_reference_loading(
        "meaningful output", {**variables, "metadata": {"loaded_references": []}}
    )
    no_trace = evaluator.assert_reference_loading("meaningful output", variables)

    assert passing["pass"] is True
    assert missing["pass"] is False
    assert no_trace["pass"] is False


@pytest.mark.parametrize(
    "paths",
    [[], ["references/oracle-validation.md"], ["references/a.md", "references/b.md"]],
)
def test_reference_expectation_remains_one_promptfoo_variable(
    tmp_path: Path, monkeypatch, paths: list[str]
) -> None:
    fixture = tmp_path / "evals" / "skills" / "example-skill" / "cases.json"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(
        json.dumps(
            {
                "version": 1,
                "cases": [
                    {
                        "id": "reference-transport",
                        "mode": "behavior",
                        "prompt": "Review this disputed oracle.",
                        "assertions": ["Uses an independent oracle."],
                        "expected_loaded_references": paths,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)

    generated = evaluator.generate_tests(
        {"skill": "example-skill", "suite": "behavior", "semantic": False}
    )
    expected = generated[0]["vars"]["expected_loaded_references"]

    # Promptfoo expands arrays of strings into separate evaluations.
    assert isinstance(expected, str)
    assert json.loads(expected) == paths


@pytest.mark.parametrize("paths", [[], ["references/oracle-validation.md"]])
def test_reference_assertion_decodes_transported_expectation(paths: list[str]) -> None:
    context = {
        "vars": {"expected_loaded_references": json.dumps(paths)},
        "providerResponse": {"metadata": {"loaded_references": paths}},
    }

    assert evaluator.assert_reference_loading("observable response", context)["pass"]


@pytest.mark.parametrize(
    "expected", ["not-json", "null", '{"paths": []}', '["../outside.md"]']
)
def test_reference_assertion_rejects_invalid_transported_expectation(
    expected: str,
) -> None:
    result = evaluator.assert_reference_loading(
        "observable response",
        {
            "vars": {"expected_loaded_references": expected},
            "metadata": {"loaded_references": []},
        },
    )

    assert result["pass"] is False


def test_test_design_eval_config_projects_all_cases_and_reference_checks() -> None:
    config = yaml.safe_load(
        (ROOT / "evals" / "promptfoo" / "mols-test-design.yaml").read_text(
            encoding="utf-8"
        )
    )
    cases = evaluator._load_cases("mols-test-design")
    provider = next(
        x for x in config["providers"] if x["config"]["suite"] == "behavior"
    )
    assert provider["config"]["reference_paths"] == ["references/oracle-validation.md"]

    for spec in config["tests"]:
        generator = spec["config"]
        generated = evaluator.generate_tests(generator)
        expected_ids = [
            case_id
            for case_id, case in cases.items()
            if evaluator._case_suite(case["mode"]) == generator["suite"]
        ]
        assert [test["vars"]["case_id"] for test in generated] == expected_ids
        if generator["suite"] == "behavior":
            annotated = {
                item["vars"]["case_id"]: item
                for item in generated
                if "expected_loaded_references" in item["vars"]
            }
            assert len(annotated) == 6
            for item in annotated.values():
                assert any(
                    check["value"].endswith(":assert_reference_loading")
                    for check in item["assert"]
                )
