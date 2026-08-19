from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals" / "regression" / "chatbot-harness-compatibility.json"


def test_chatbot_harness_compatibility_contract() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    sources = contract["sources"]

    for source, required in contract["required"].items():
        text = (ROOT / sources[source]).read_text(encoding="utf-8")
        for phrase in required:
            assert phrase in text, f"missing required contract phrase in {sources[source]}: {phrase}"

    for source, forbidden in contract.get("forbidden", {}).items():
        text = (ROOT / sources[source]).read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, f"retired contract phrase remains in {sources[source]}: {phrase}"
