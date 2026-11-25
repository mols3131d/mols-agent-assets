from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.agent_assets import skills_promptfoo as evaluator

ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT / "evals" / "promptfoo"
REFERENCE_PATHS = {
    "references/bootstrap.md",
    "references/default-workflow.md",
    "references/dispatch.md",
}


def test_stdd_reference_suite_covers_exactly_annotated_cases() -> None:
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-stdd-references.yaml").read_text(encoding="utf-8")
    )
    assert config["prompts"] == ["{{task}}"]
    provider = config["providers"][0]
    assert provider["id"].endswith("skills_promptfoo.py:call_api")
    assert provider["config"]["mode"] == "ollama"
    assert provider["config"]["suite"] == "behavior"
    assert set(provider["config"]["reference_paths"]) == REFERENCE_PATHS
    assert config["sharing"] is False
    assert config["writeLatestResults"] is False
    assert config["commandLineOptions"]["noShare"] is True

    suite = config["tests"][0]
    assert suite["path"].endswith("skills_promptfoo.py:generate_tests")
    assert suite["config"]["semantic"] is False
    cases = evaluator._load_cases("mols-stdd")
    expected = {
        case_id
        for case_id, case in cases.items()
        if "expected_loaded_references" in case
    }
    assert expected
    assert set(suite["config"]["case_ids"]) == expected
    assert len(suite["config"]["case_ids"]) == len(expected)

    generated = evaluator.generate_tests(suite["config"])
    assert len(generated) == len(expected)
    for result in generated:
        case_id = result["vars"]["case_id"]
        selected = json.loads(result["vars"]["expected_loaded_references"])
        assert set(selected).issubset(REFERENCE_PATHS)
        assert selected == cases[case_id]["expected_loaded_references"]
        assert any(
            assertion["metric"] == "reference-loading"
            for assertion in result["assert"]
        )
        assert not any(
            assertion["metric"] == "behavior-contract"
            for assertion in result["assert"]
        )


def test_stdd_native_suite_retains_behavior_without_reference_claims() -> None:
    config = yaml.safe_load(
        (CONFIG_DIR / "mols-stdd.yaml").read_text(encoding="utf-8")
    )
    behavior = next(
        suite for suite in config["tests"]
        if suite["config"]["suite"] == "behavior"
    )
    assert behavior["config"]["omit_reference_checks"] is True
    assert behavior["config"]["semantic"] is True

    generated = evaluator.generate_native_tests(behavior["config"])
    expected = [
        case["id"]
        for case in evaluator._load_cases("mols-stdd").values()
        if evaluator._case_suite(case["mode"]) == evaluator.BEHAVIOR_SUITE
    ]
    assert [item["vars"]["case_id"] for item in generated] == expected
    for item in generated:
        assert "expected_loaded_references" not in item["vars"]
        assert not any(
            assertion["metric"] == "reference-loading"
            for assertion in item["assert"]
        )
        assert any(
            assertion["metric"] == "behavior-contract"
            for assertion in item["assert"]
        )
