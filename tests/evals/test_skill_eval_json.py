from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals" / "skills"


def test_skill_eval_json_files_are_valid() -> None:
    files = sorted(EVALS.rglob("*.json"))
    assert files, "no Skill eval JSON fixtures found"

    for path in files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise AssertionError(f"invalid eval JSON: {path.relative_to(ROOT)}: {error}") from error
