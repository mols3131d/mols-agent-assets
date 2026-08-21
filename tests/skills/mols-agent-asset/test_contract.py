from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/rulesync/.rulesync/skills/mols-agent-asset"
LEGACY = {
    "load-context-agent-assets",
    "load-context-agent-skills",
    "mols-agent-asset-studio",
    "mols-rule-dry",
    "mols-skill-creator",
}


def test_authoring_skill_keeps_minimal_runtime_surface() -> None:
    files = {
        path.relative_to(SKILL).as_posix()
        for path in SKILL.rglob("*")
        if path.is_file()
    }
    assert files == {"SKILL.md", "references/skill.md", "references/rule.md"}


def test_authoring_skill_routes_only_supported_type_context() -> None:
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "(references/skill.md)" in body
    assert "(references/rule.md)" in body
    assert "mols-agent-asset-validator" in body
    assert "validator-primary" in body


def test_legacy_authoring_entrypoints_are_removed() -> None:
    skills = ROOT / "src/rulesync/.rulesync/skills"
    assert all(not (skills / name / "SKILL.md").exists() for name in LEGACY)


def test_eval_contract_exists_for_new_entrypoint() -> None:
    path = ROOT / "evals/skills/mols-agent-asset/cases.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = {case["id"] for case in data["cases"]}
    assert {
        "create-minimal-skill",
        "rule-simple-dedup",
        "rule-scope-overlap",
        "rule-generated-projection",
        "install-is-not-authoring",
        "formal-validation-is-validator",
        "validation-driven-fix-keeps-validator-primary",
        "prompt-authoring-is-out-of-scope",
        "hook-authoring-is-out-of-scope",
        "mcp-authoring-is-out-of-scope",
    } <= ids
