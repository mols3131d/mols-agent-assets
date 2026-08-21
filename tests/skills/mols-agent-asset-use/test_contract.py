from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"
SKILL = SKILLS / "mols-agent-asset-use" / "SKILL.md"
LEGACY = {"mols-skill-find", "mols-skill-install"}
EXPECTED_ARGUMENTS = {
    "sources",
    "query",
    "asset_types",
    "target",
    "state",
    "constraints",
    "fallback",
    "on_conflict",
}


def load() -> tuple[dict[str, object], str]:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end >= 0
    frontmatter = yaml.safe_load(text[4:end])
    assert isinstance(frontmatter, dict)
    return frontmatter, text[end + 5 :]


def test_unifies_discovery_and_delivery_for_agent_assets() -> None:
    frontmatter, body = load()
    assert frontmatter["name"] == "mols-agent-asset-use"
    description = str(frontmatter["description"])
    for term in ["Skills", "Rules", "prompts", "agents", "hooks", "MCP"]:
        assert term in description

    block = re.search(r"# Arguments\n\n```yaml\n(.*?)\n```", body, re.DOTALL)
    assert block is not None
    arguments = {
        line.split(":", 1)[0]
        for line in block.group(1).splitlines()
        if line and not line.startswith(" ")
    }
    assert arguments == EXPECTED_ARGUMENTS
    assert all(f"{name}: <auto>" in block.group(1) for name in EXPECTED_ARGUMENTS)


def test_least_persistent_state_is_the_default() -> None:
    _, body = load()
    required = [
        "least persistent state",
        "current-task/session use without durable intent → `use`",
        "install, register, keep, reuse later, or equivalent durable intent → `persist`",
        "Do not infer persistence from convenience.",
        "direct invocation or use when the asset is already available",
        "temporary context or session load",
        "Do not create persistent state merely to make future use easier.",
    ]
    for phrase in required:
        assert phrase in body


def test_discovery_is_bounded_and_mutation_is_separate() -> None:
    _, body = load()
    required = [
        "Keep selection read-only until the requested end state requires target mutation.",
        "external search only when explicitly permitted",
        "An index is an optimization and authority hint, not a requirement.",
        "Names are signals, not identity.",
        "Discovery does not grant mutation authority",
    ]
    for phrase in required:
        assert phrase in body


def test_conflicts_do_not_auto_destroy_target_state() -> None:
    _, body = load()
    assert "Without sufficient identity evidence" in body
    assert "`override` requires explicit caller choice." in body
    assert "`<auto>` reports the conflict and valid choices." in body


def test_legacy_skill_entrypoints_are_removed() -> None:
    assert all(not (SKILLS / name / "SKILL.md").exists() for name in LEGACY)
