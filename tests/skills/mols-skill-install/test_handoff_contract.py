from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src" / "agentsmesh" / ".agentsmesh" / "skills"
FIND = SKILLS / "mols-skill-find" / "SKILL.md"
INSTALL = SKILLS / "mols-skill-install" / "SKILL.md"


def test_install_consumes_unified_find_handoff() -> None:
    find = FIND.read_text(encoding="utf-8")
    install = INSTALL.read_text(encoding="utf-8")

    for field in ["selected:", "source:", "compatibility:", "identity:"]:
        assert field in find

    required = [
        "Prefer a `mols-skill-find` selection record",
        "complete `sync-prep` selection set",
        "one concrete Skill package or target-native equivalent",
        "For a single-file Skill, use `SKILL.md`",
        "Process any Skill actively controlling the current discovery/install run after other selected capabilities.",
        "use the new version on the next invocation",
    ]
    for phrase in required:
        assert phrase in install


def test_install_resolves_current_runtime_by_capability() -> None:
    install = INSTALL.read_text(encoding="utf-8")

    required = [
        "Honor an explicit target first.",
        "requested end state and observable capability",
        "current runtime itself as a target candidate",
        "This is capability-based self-targeting, not a chatbot-specific rule.",
        "Do not infer target capability merely because the runtime can read a Skill",
        "requests to inspect, read, use as context, or run a Skill do not by themselves authorize persistent target-state mutation",
    ]
    for phrase in required:
        assert phrase in install

    assert "ChatGPT" not in install


def test_install_does_not_restore_retired_skill_taxonomy() -> None:
    install = INSTALL.read_text(encoding="utf-8").lower()
    retired = [
        "agent/chatbot",
        "flat skill",
        "runtime skill",
        "flat variant",
        "runtime variant",
        "target profile",
        "sibling projection",
    ]
    for phrase in retired:
        assert phrase not in install
