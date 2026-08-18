from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = ROOT / "evals/skills/writing/trigger.json"


def test_trigger_eval_fixture_is_balanced_and_well_formed() -> None:
    cases = json.loads(CASES.read_text(encoding="utf-8"))

    assert isinstance(cases, list)
    positives = 0
    negatives = 0

    for index, case in enumerate(cases):
        assert isinstance(case, dict), index
        assert isinstance(case.get("query"), str) and case["query"].strip(), index
        assert isinstance(case.get("should_trigger"), bool), index
        assert isinstance(case.get("reason"), str) and case["reason"].strip(), index
        positives += case["should_trigger"] is True
        negatives += case["should_trigger"] is False

    assert positives >= 8
    assert negatives >= 8
