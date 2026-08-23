import pytest

from scripts import sync_agent_skills as sync


def test_resolve_agents_maps_and_deduplicates_repository_targets():
    assert sync.resolve_agents(
        [
            "claudecode",
            "codexcli",
            "copilot",
            "copilotcli",
            "antigravity-ide",
            "antigravity-cli",
        ]
    ) == [
        "claude-code",
        "codex",
        "github-copilot",
        "antigravity",
        "antigravity-cli",
    ]


def test_resolve_agents_rejects_unmapped_target():
    with pytest.raises(sync.SkillSyncError, match="target mapping"):
        sync.resolve_agents(["new-vendor"])


def test_build_command_preserves_lock_path_revision_and_skill():
    assert sync.build_command(
        "humanize-korean",
        {
            "source": "epoko77-ai/im-not-ai",
            "ref": "v2.3.0",
            "sourceType": "github",
            "skillPath": "codex/skills/humanize-korean/SKILL.md",
        },
        ["claude-code", "codex"],
    ) == [
        "skills",
        "add",
        "epoko77-ai/im-not-ai/codex/skills/humanize-korean#v2.3.0",
        "--skill",
        "humanize-korean",
        "--agent",
        "claude-code",
        "codex",
        "--yes",
    ]


def test_build_source_rejects_ambiguous_skill_path_source():
    with pytest.raises(sync.SkillSyncError, match="skillPath 설치는 지원하지 않습니다"):
        sync.build_source(
            {
                "source": "example/repo",
                "sourceType": "git",
                "sourceUrl": "https://example.com/example/repo.git",
                "skillPath": "skills/example/SKILL.md",
            }
        )


def test_skill_folder_rejects_path_traversal():
    with pytest.raises(sync.SkillSyncError, match="지원하지 않는 skillPath"):
        sync.skill_folder({"skillPath": "../outside/SKILL.md"})


def test_repository_vendor_targets_are_supported():
    targets = sync.read_vendor_targets(sync.TARGET_CONFIG_PATH)
    agents = sync.resolve_agents(targets)

    assert agents == [
        "claude-code",
        "codex",
        "github-copilot",
        "antigravity",
        "antigravity-cli",
    ]
