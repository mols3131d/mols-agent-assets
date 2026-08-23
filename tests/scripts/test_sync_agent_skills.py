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


def test_build_source_normalizes_public_github_url_before_subpath():
    assert sync.build_source(
        {
            "source": "https://github.com/epoko77-ai/im-not-ai",
            "ref": "v2.3.0",
            "sourceType": "github",
            "skillPath": "codex/skills/humanize-korean/SKILL.md",
        }
    ) == "epoko77-ai/im-not-ai/codex/skills/humanize-korean#v2.3.0"


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


def test_build_source_rejects_unsupported_source_type():
    with pytest.raises(sync.SkillSyncError, match="지원하지 않는 sourceType"):
        sync.build_source(
            {
                "source": "example-package",
                "sourceType": "node_modules",
            }
        )


def test_github_shorthand_rejects_non_public_github_source():
    with pytest.raises(sync.SkillSyncError, match="public GitHub owner/repo"):
        sync.github_shorthand("https://ghe.example.com/owner/repo")


def test_skill_folder_rejects_path_traversal():
    with pytest.raises(sync.SkillSyncError, match="지원하지 않는 skillPath"):
        sync.skill_folder({"skillPath": "../outside/SKILL.md"})


def test_build_env_pins_public_github_and_disables_telemetry(monkeypatch):
    monkeypatch.setenv("GH_HOST", "ghe.example.com")

    env = sync.build_env({"sourceType": "github"})

    assert env["GH_HOST"] == "github.com"
    assert env["DISABLE_TELEMETRY"] == "1"
    assert env["DO_NOT_TRACK"] == "1"


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
