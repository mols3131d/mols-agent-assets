from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIND = ROOT / ".agentsmesh" / "skills" / "mols-skill-find" / "SKILL.md"
INSTALL = ROOT / ".agentsmesh" / "skills" / "mols-skill-install" / "SKILL.md"


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
    ]
    for phrase in required:
        assert phrase in install


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
