from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals" / "skills"
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"


@pytest.mark.parametrize(
    "directory",
    sorted(path for path in EVALS.iterdir() if path.is_dir()),
    ids=lambda path: path.name,
)
def test_skill_eval_target_has_canonical_source(directory: Path) -> None:
    source = SKILLS / directory.name / "SKILL.md"
    assert source.is_file(), (
        f"{directory.relative_to(ROOT)} targets missing Skill "
        f"{source.relative_to(ROOT)}; remove or migrate its evals with the asset"
    )


def test_skill_eval_json_files_are_valid() -> None:
    files = sorted(EVALS.rglob("*.json"))
    assert files, "no Skill eval JSON fixtures found"

    for path in files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise AssertionError(
                f"invalid eval JSON: {path.relative_to(ROOT)}: {error}"
            ) from error
