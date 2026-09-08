import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUBAGENT_EVAL_ROOT = ROOT / "evals" / "subagents"


def test_subagent_behavior_fixtures_have_minimal_contract():
    paths = sorted(SUBAGENT_EVAL_ROOT.glob("*/cases.json"))
    assert paths, "expected at least one subagent behavioral fixture"

    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == 1, path
        assert data["contract"] in {"capability", "regression"}, path
        system = data["system_under_evaluation"]
        assert isinstance(system, list) and system, path
        assert all(isinstance(item, str) and item for item in system), path

        cases = data["cases"]
        assert isinstance(cases, list) and cases, path

        ids = []
        for case in cases:
            ids.append(case["id"])
            assert isinstance(case["mode"], str) and case["mode"], case
            assert isinstance(case["prompt"], str) and case["prompt"], case
            assertions = case["assertions"]
            assert isinstance(assertions, list) and assertions, case
            assert all(isinstance(item, str) and item for item in assertions), case

        assert len(ids) == len(set(ids)), f"duplicate case id in {path}"
