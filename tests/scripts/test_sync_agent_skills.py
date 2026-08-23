import json
from pathlib import Path

import pytest

from scripts import sync_agent_skills as sync


def locked_skill(
    *,
    name: str = "humanize-korean",
    source: str = "epoko77-ai/im-not-ai",
    ref: str = "v2.3.0",
    source_type: str = "github",
) -> sync.LockedSkill:
    return sync.LockedSkill(
        name=name,
        source=source,
        ref=ref,
        source_type=source_type,
    )


def test_normalize_github_source_accepts_shorthand_and_url():
    assert sync.normalize_github_source("epoko77-ai/im-not-ai") == "epoko77-ai/im-not-ai"
    assert (
        sync.normalize_github_source("https://github.com/epoko77-ai/im-not-ai.git")
        == "epoko77-ai/im-not-ai"
    )


def test_normalize_github_source_rejects_non_public_repo_source():
    with pytest.raises(sync.SkillSyncError, match="public GitHub owner/repo"):
        sync.normalize_github_source("https://ghe.example.com/owner/repo")


def test_build_sync_plan_uses_locked_source_and_ref():
    plans = sync.build_sync_plans([locked_skill()])

    assert plans == [
        sync.SyncPlan(
            source="epoko77-ai/im-not-ai",
            ref="v2.3.0",
            skills=("humanize-korean",),
            adapter=sync.NATIVE_ADAPTERS["epoko77-ai/im-not-ai"],
        )
    ]


def test_build_sync_plan_rejects_non_github_source():
    with pytest.raises(sync.SkillSyncError, match="sourceType"):
        sync.build_sync_plans([locked_skill(source_type="gitlab")])


def test_build_sync_plan_rejects_dependency_without_native_adapter():
    with pytest.raises(sync.SkillSyncError, match="adapter가 없는"):
        sync.build_sync_plans([locked_skill(source="example/repo")])


def test_build_sync_plan_rejects_skill_not_owned_by_adapter():
    with pytest.raises(sync.SkillSyncError, match="지원하지 않는 Skill"):
        sync.build_sync_plans([locked_skill(name="another-skill")])


def test_build_sync_plan_rejects_mixed_refs_for_same_source():
    with pytest.raises(sync.SkillSyncError, match="서로 다른 ref"):
        sync.build_sync_plans(
            [
                locked_skill(name="humanize-korean", ref="v2.3.0"),
                locked_skill(name="humanize-korean", ref="main"),
            ]
        )


def test_read_locked_skills_requires_ref(tmp_path: Path):
    lock = tmp_path / "skills-lock.json"
    lock.write_text(
        json.dumps(
            {
                "version": 1,
                "skills": {
                    "humanize-korean": {
                        "source": "epoko77-ai/im-not-ai",
                        "sourceType": "github",
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(sync.SkillSyncError, match="고정된 ref"):
        sync.read_locked_skills(lock)


def test_checkout_path_is_stable_and_source_scoped(tmp_path: Path):
    first = sync.checkout_path("epoko77-ai/im-not-ai", tmp_path)
    second = sync.checkout_path("epoko77-ai/im-not-ai", tmp_path)
    other = sync.checkout_path("example/im-not-ai", tmp_path)

    assert first == second
    assert first != other
    assert first.parent == tmp_path


def test_dry_run_is_lock_read_only(tmp_path: Path, monkeypatch, capsys):
    lock = tmp_path / "skills-lock.json"
    original = json.dumps(
        {
            "version": 1,
            "skills": {
                "humanize-korean": {
                    "source": "epoko77-ai/im-not-ai",
                    "ref": "v2.3.0",
                    "sourceType": "github",
                    "skillPath": "codex/skills/humanize-korean/SKILL.md",
                    "computedHash": "deadbeef",
                }
            },
        },
        indent=2,
    )
    lock.write_text(original, encoding="utf-8")

    monkeypatch.setattr(
        sync,
        "ensure_checkout",
        lambda *_args, **_kwargs: pytest.fail("dry-run must not checkout"),
    )
    monkeypatch.setattr(
        sync,
        "run_native_installer",
        lambda *_args, **_kwargs: pytest.fail("dry-run must not install"),
    )

    sync.sync_locked_skills(
        dry_run=True,
        lock_path=lock,
        cache_root=tmp_path / "cache",
    )

    assert lock.read_text(encoding="utf-8") == original
    assert "native:im-not-ai" in capsys.readouterr().out


def test_ensure_checkout_fetches_exact_locked_ref(tmp_path: Path, monkeypatch):
    plan = sync.build_sync_plans([locked_skill()])[0]
    calls: list[tuple[list[str], Path | None]] = []

    monkeypatch.setattr(sync.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(
        sync,
        "run_checked",
        lambda command, cwd=None: calls.append((command, cwd)),
    )

    checkout = sync.ensure_checkout(plan, tmp_path)

    assert checkout == sync.checkout_path(plan.source, tmp_path)
    assert calls[0][0][:3] == ["git", "clone", "--filter=blob:none"]
    assert [
        "git",
        "-C",
        str(checkout),
        "fetch",
        "--depth",
        "1",
        "--force",
        "origin",
        "v2.3.0",
    ] in [command for command, _cwd in calls]


def test_native_installer_delegates_vendor_detection_to_upstream(
    tmp_path: Path, monkeypatch
):
    plan = sync.build_sync_plans([locked_skill()])[0]
    (tmp_path / "install.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    calls: list[tuple[list[str], Path | None]] = []

    monkeypatch.setattr(sync.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(
        sync,
        "run_checked",
        lambda command, cwd=None: calls.append((command, cwd)),
    )

    sync.run_native_installer(plan, tmp_path)

    assert calls == [(["bash", "install.sh"], tmp_path)]
