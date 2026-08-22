from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals/regression/rulesync-source-isolation.json"
SUBAGENTS = ROOT / "src/rulesync/.rulesync/subagents"


def load_frontmatter(name: str) -> dict:
    path = SUBAGENTS / f"{name}.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", path
    end = lines.index("---", 1)
    return yaml.safe_load("\n".join(lines[1:end])) or {}


def supported_targets() -> set[str]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    return set(contract["library_workspace"]["supported_targets"])


def test_review_subagents_cover_supported_targets() -> None:
    expected = supported_targets()
    for name in ("review-lead", "review-quality", "review-adversarial"):
        assert set(load_frontmatter(name)["targets"]) == expected


def test_claude_review_subagents_preserve_read_only_contract() -> None:
    lead = load_frontmatter("review-lead")["claudecode"]
    quality = load_frontmatter("review-quality")["claudecode"]
    adversarial = load_frontmatter("review-adversarial")["claudecode"]

    assert lead["permissionMode"] == "plan"
    assert quality["permissionMode"] == "plan"
    assert adversarial["permissionMode"] == "plan"

    assert "Agent" in lead["tools"]
    assert "Agent" not in quality["tools"]
    assert "Agent" not in adversarial["tools"]
    assert "Bash" in quality["tools"]
    assert "Bash" not in adversarial["tools"]


def test_codex_review_subagents_use_read_only_sandbox() -> None:
    for name in ("review-lead", "review-quality", "review-adversarial"):
        assert load_frontmatter(name)["codexcli"]["sandbox_mode"] == "read-only"
