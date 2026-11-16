from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import generated_artifacts_writer as writer

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "generated-writer.yml"
SAMPLE_SHA = "a" * 40
NEWER_SHA = "b" * 40


def _git(
    cwd: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        ["git", "-c", f"core.hooksPath={os.devnull}", *args],
        cwd=cwd,
        env=merged_env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _make_event(
    *,
    repo_id: int = 1167541883,
    repo_name: str = "mols3131d/mols-agent-assets",
    head_repo_id: int | None = None,
    head_repo_name: str | None = None,
    branch: str = "feat/example",
    head_sha: str = SAMPLE_SHA,
    workflow_name: str = writer.EXPECTED_PRODUCER_NAME,
    workflow_path: str = writer.EXPECTED_PRODUCER_PATH,
    event_name: str = "push",
    status: str = "completed",
    conclusion: str = "success",
    run_id: int = 42,
    run_attempt: int = 1,
) -> dict[str, object]:
    return {
        "repository": {
            "id": repo_id,
            "full_name": repo_name,
            "default_branch": "main",
        },
        "workflow": {
            "name": workflow_name,
            "path": workflow_path,
        },
        "workflow_run": {
            "id": run_id,
            "run_attempt": run_attempt,
            "name": workflow_name,
            "path": workflow_path,
            "event": event_name,
            "status": status,
            "conclusion": conclusion,
            "head_branch": branch,
            "head_sha": head_sha,
            "repository": {
                "id": repo_id,
                "full_name": repo_name,
            },
            "head_repository": {
                "id": repo_id if head_repo_id is None else head_repo_id,
                "full_name": repo_name if head_repo_name is None else head_repo_name,
            },
        },
    }


def _provenance(
    *, branch: str = "feat/example", head_sha: str = SAMPLE_SHA
) -> writer.Provenance:
    return writer.Provenance(
        repository_id=1167541883,
        repository_full_name="mols3131d/mols-agent-assets",
        default_branch="main",
        branch=branch,
        head_sha=head_sha,
        run_id=42,
        run_attempt=1,
    )


def _write_payload(
    artifact_dir: Path,
    *,
    files: dict[str, bytes] | None = None,
    deleted: list[str] | None = None,
    changed: bool = True,
    branch: str = "feat/example",
    head_sha: str = SAMPLE_SHA,
    repo_id: int = 1167541883,
    repo_name: str = "mols3131d/mols-agent-assets",
    run_id: int = 42,
    run_attempt: int = 1,
) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    file_entries = []
    if files:
        files_root = artifact_dir / "files"
        for rel, content in sorted(files.items()):
            dest = files_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            file_entries.append(
                {
                    "path": rel,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size": len(content),
                }
            )

    metadata = {
        "schema_version": 1,
        "repository_id": repo_id,
        "repository_full_name": repo_name,
        "branch": branch,
        "head_sha": head_sha,
        "producer_run_id": run_id,
        "producer_run_attempt": run_attempt,
        "changed": changed,
        "files": file_entries,
        "deleted": deleted or [],
    }
    (artifact_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/INDEX.tsv", True),
        ("docs/development/INDEX.tsv", True),
        ("catalog/INDEX.tsv", True),
        ("catalog/patterns/INDEX.tsv", True),
        ("route/routes.jsonl", True),
        ("route/skills.jsonl", True),
        (".agents/route/routes.jsonl", True),
        (".agents/route/all.jsonl", True),
        (".agents/route/nested/all.jsonl", False),
        ("route/nested/skills.jsonl", False),
        ("docs/evilINDEX.tsv", False),
        ("../docs/INDEX.tsv", False),
        ("docs/../README.md", False),
        (".github/workflows/pr-gate.yml", False),
        (".git/config", False),
        ("scripts/generated_artifacts_writer.py", False),
        ("docs/guide.md", False),
    ],
)
def test_is_allowed_generated_output_enforces_strict_allowlist(
    path: str, expected: bool
) -> None:
    assert writer.is_allowed_generated_output(path) is expected


@pytest.mark.parametrize(
    ("branch", "allowed"),
    [
        ("main", False),
        ("HEAD", False),
        ("refs/heads/feat", False),
        ("-flag", False),
        ("feat..bar", False),
        ("feat@{0}", False),
        ("feat//bar", False),
        ("feat/.hidden", False),
        ("feat/bad.lock", False),
        ("feat with space", False),
    ],
)
def test_validate_source_branch_rejects_main_and_unsafe_refs(
    branch: str, allowed: bool
) -> None:
    assert allowed is False
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_source_branch(branch, default_branch="main")


def test_verify_workflow_run_event_is_fail_closed_when_disabled_or_unlisted() -> None:
    event = _make_event()
    decision, provenance = writer.verify_workflow_run_event(
        event,
        github_repository="mols3131d/mols-agent-assets",
        github_repository_id="1167541883",
        github_ref="refs/heads/main",
        enabled="",
        allowed_branches="*",
    )
    assert decision == writer.Decision(False, "disabled")
    assert provenance is None

    decision2, _ = writer.verify_workflow_run_event(
        event,
        github_repository="mols3131d/mols-agent-assets",
        github_repository_id="1167541883",
        github_ref="refs/heads/main",
        enabled="true",
        allowed_branches="",
    )
    assert decision2 == writer.Decision(False, "branch_not_allowed")

    decision3, _ = writer.verify_workflow_run_event(
        event,
        github_repository="mols3131d/mols-agent-assets",
        github_repository_id="1167541883",
        github_ref="refs/heads/main",
        enabled="true",
        allowed_branches="other-branch, feat/example",
    )
    assert decision3 == writer.Decision(True, "ok")


@pytest.mark.parametrize(
    "overrides",
    [
        {"head_repo_id": 999, "head_repo_name": "attacker/mols-agent-assets"},
        {"repo_id": 999, "repo_name": "attacker/mols-agent-assets"},
        {"workflow_name": "Evil Workflow"},
        {"workflow_path": ".github/workflows/evil.yml"},
        {"event_name": "pull_request"},
        {"conclusion": "failure"},
        {"status": "in_progress"},
        {"branch": "main"},
        {"head_sha": "not-a-sha"},
    ],
)
def test_verify_workflow_run_event_rejects_untrusted_provenance(
    overrides: dict[str, object],
) -> None:
    event = _make_event(**overrides)  # type: ignore[arg-type]
    with pytest.raises(writer.WriterSecurityError):
        writer.verify_workflow_run_event(
            event,
            github_repository="mols3131d/mols-agent-assets",
            github_repository_id="1167541883",
            github_ref="refs/heads/main",
            enabled="true",
            allowed_branches="*",
        )


def test_verify_workflow_run_event_rejects_non_default_execution_ref() -> None:
    with pytest.raises(writer.WriterSecurityError):
        writer.verify_workflow_run_event(
            _make_event(),
            github_repository="mols3131d/mols-agent-assets",
            github_repository_id="1167541883",
            github_ref="refs/heads/feat/example",
            enabled="true",
            allowed_branches="*",
        )


def test_verify_single_artifact_enforces_exact_single_expected_artifact() -> None:
    ok_payload = {
        "total_count": 1,
        "artifacts": [
            {
                "name": writer.EXPECTED_ARTIFACT_NAME,
                "expired": False,
                "size_in_bytes": 128,
            }
        ],
    }
    assert (
        writer.verify_single_artifact(lambda _: (200, ok_payload), "o/r", 1)["name"]
        == writer.EXPECTED_ARTIFACT_NAME
    )

    bad_cases = [
        {"total_count": 0, "artifacts": []},
        {
            "total_count": 2,
            "artifacts": [
                {
                    "name": writer.EXPECTED_ARTIFACT_NAME,
                    "expired": False,
                    "size_in_bytes": 128,
                },
                {"name": "extra", "expired": False, "size_in_bytes": 128},
            ],
        },
        {
            "total_count": 1,
            "artifacts": [{"name": "wrong", "expired": False, "size_in_bytes": 128}],
        },
        {
            "total_count": 1,
            "artifacts": [
                {
                    "name": writer.EXPECTED_ARTIFACT_NAME,
                    "expired": True,
                    "size_in_bytes": 128,
                }
            ],
        },
        {
            "total_count": 1,
            "artifacts": [
                {
                    "name": writer.EXPECTED_ARTIFACT_NAME,
                    "expired": False,
                    "size_in_bytes": 0,
                }
            ],
        },
    ]
    for case in bad_cases:
        with pytest.raises(writer.WriterSecurityError):
            writer.verify_single_artifact(lambda _, c=case: (200, c), "o/r", 1)


def test_validate_artifact_payload_accepts_noop_and_valid_changes(
    tmp_path: Path,
) -> None:
    noop_dir = tmp_path / "noop"
    _write_payload(noop_dir, changed=False)
    noop = writer.validate_artifact_payload(noop_dir, _provenance())
    assert noop.changed is False
    assert noop.files == ()

    valid_dir = tmp_path / "valid"
    _write_payload(
        valid_dir,
        files={
            "docs/INDEX.tsv": b"path\tdescription\n",
            ".agents/route/all.jsonl": b"{}\n",
        },
        deleted=["docs/old/INDEX.tsv"],
        changed=True,
    )
    valid = writer.validate_artifact_payload(valid_dir, _provenance())
    assert valid.changed is True
    assert [f.path for f in valid.files] == [
        ".agents/route/all.jsonl",
        "docs/INDEX.tsv",
    ]
    assert valid.deleted == ("docs/old/INDEX.tsv",)


def test_validate_artifact_payload_rejects_tampering_and_symlinks(
    tmp_path: Path,
) -> None:
    # Unexpected top-level file
    extra_top = tmp_path / "extra_top"
    _write_payload(extra_top, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (extra_top / "evil.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(extra_top, _provenance())

    # Unexpected extra file under files/
    extra_file = tmp_path / "extra_file"
    _write_payload(extra_file, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (extra_file / "files" / "catalog").mkdir()
    (extra_file / "files" / "catalog" / "INDEX.tsv").write_text(
        "tamper\n", encoding="utf-8"
    )
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(extra_file, _provenance())

    # SHA-256 mismatch
    bad_digest = tmp_path / "bad_digest"
    _write_payload(bad_digest, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (bad_digest / "files" / "docs" / "INDEX.tsv").write_text(
        "tampered\n", encoding="utf-8"
    )
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_digest, _provenance())

    # Disallowed path
    bad_path = tmp_path / "bad_path"
    _write_payload(bad_path, files={".github/workflows/pr-gate.yml": b"name: evil\n"})
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_path, _provenance())

    # Protected core output deletion
    bad_delete = tmp_path / "bad_delete"
    _write_payload(bad_delete, deleted=["docs/INDEX.tsv"])
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_delete, _provenance())

    # Symlink rejection (skip only if OS denies symlink creation without admin)
    sym_dir = tmp_path / "sym"
    _write_payload(sym_dir, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    target = tmp_path / "outside.txt"
    target.write_text("secret", encoding="utf-8")
    link = sym_dir / "files" / "docs" / "link.tsv"
    try:
        link.symlink_to(target)
    except OSError:
        pass
    else:
        with pytest.raises(writer.WriterSecurityError):
            writer.validate_artifact_payload(sym_dir, _provenance())


def test_apply_payload_and_commit_and_push_end_to_end_with_local_bare_repo(
    tmp_path: Path,
) -> None:
    bare = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "-q", str(bare))

    seed = tmp_path / "seed"
    _git(tmp_path, "clone", "-q", bare.as_uri(), str(seed))
    _git(seed, "config", "user.name", "Author")
    _git(seed, "config", "user.email", "author@example.com")
    _git(seed, "checkout", "-b", "feat/example")

    (seed / "docs" / "old").mkdir(parents=True)
    (seed / "docs" / "INDEX.tsv").write_text("path\tdescription\n", encoding="utf-8")
    (seed / "docs" / "old" / "INDEX.tsv").write_text(
        "path\tdescription\n", encoding="utf-8"
    )
    (seed / "README.md").write_text("hello\n", encoding="utf-8")
    _git(seed, "add", ".")
    _git(seed, "commit", "-qm", "initial")
    _git(seed, "push", "-q", "origin", "feat/example")
    head_sha = _git(seed, "rev-parse", "HEAD").stdout.strip()

    artifact_dir = tmp_path / "artifact"
    _write_payload(
        artifact_dir,
        files={
            "docs/INDEX.tsv": b"path\tdescription\ndocs/guide.md\tguide\n",
            ".agents/route/all.jsonl": b'{"name":"demo"}\n',
        },
        deleted=["docs/old/INDEX.tsv"],
        branch="feat/example",
        head_sha=head_sha,
    )
    payload = writer.validate_artifact_payload(
        artifact_dir, _provenance(head_sha=head_sha)
    )

    target_dir = tmp_path / "writer-target"
    writer.checkout_source_commit(bare.as_uri(), target_dir, head_sha)
    staged = writer.apply_payload(target_dir, payload)
    assert staged == [".agents/route/all.jsonl", "docs/INDEX.tsv", "docs/old/INDEX.tsv"]

    def fake_api(path: str) -> tuple[int, dict[str, object]]:
        if path == "users/test-app%5Bbot%5D":
            return 200, {"id": 999001, "login": "test-app[bot]", "type": "Bot"}
        if path == "repos/mols3131d/mols-agent-assets/git/ref/heads/feat%2Fexample":
            return 200, {"object": {"type": "commit", "sha": head_sha}}
        raise AssertionError(f"unexpected API call: {path}")

    decision = writer.commit_and_push(
        target_dir,
        branch="feat/example",
        expected_head_sha=head_sha,
        repo_full_name="mols3131d/mols-agent-assets",
        app_token="app-token-value",
        app_slug="test-app",
        requester=fake_api,
        github_token="gh-token-value",
    )
    assert decision == writer.Decision(True, "pushed")

    new_remote_head = _git(
        seed, "ls-remote", bare.as_uri(), "refs/heads/feat/example"
    ).stdout.split()[0]
    assert new_remote_head != head_sha
    _git(seed, "pull", "-q", "origin", "feat/example")
    expected_log = (
        "test-app[bot]|"
        "999001+test-app[bot]@users.noreply.github.com|"
        "chore(generated): sync indexes and routes"
    )
    assert _git(seed, "log", "-1", "--format=%an|%ae|%s").stdout.strip() == expected_log
    changed_in_bot_commit = _git(
        seed, "diff", "--name-only", f"{head_sha}..{new_remote_head}"
    ).stdout.splitlines()
    assert sorted(changed_in_bot_commit) == [
        ".agents/route/all.jsonl",
        "docs/INDEX.tsv",
        "docs/old/INDEX.tsv",
    ]


def test_commit_and_push_discards_stale_head_and_rejects_non_fast_forward(
    tmp_path: Path,
) -> None:
    bare = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "-q", str(bare))

    seed = tmp_path / "seed"
    _git(tmp_path, "clone", "-q", bare.as_uri(), str(seed))
    _git(seed, "config", "user.name", "Author")
    _git(seed, "config", "user.email", "author@example.com")
    _git(seed, "checkout", "-b", "feat/example")
    (seed / "docs").mkdir()
    (seed / "docs" / "INDEX.tsv").write_text("old\n", encoding="utf-8")
    _git(seed, "add", ".")
    _git(seed, "commit", "-qm", "c1")
    _git(seed, "push", "-q", "origin", "feat/example")
    sha1 = _git(seed, "rev-parse", "HEAD").stdout.strip()

    # Advance remote branch with c2
    (seed / "README.md").write_text("concurrent edit\n", encoding="utf-8")
    _git(seed, "add", "README.md")
    _git(seed, "commit", "-qm", "c2")
    _git(seed, "push", "-q", "origin", "feat/example")
    sha2 = _git(seed, "rev-parse", "HEAD").stdout.strip()

    artifact_dir = tmp_path / "artifact"
    _write_payload(artifact_dir, files={"docs/INDEX.tsv": b"new\n"}, head_sha=sha1)
    payload = writer.validate_artifact_payload(artifact_dir, _provenance(head_sha=sha1))

    target_dir = tmp_path / "writer-target"
    writer.checkout_source_commit(bare.as_uri(), target_dir, sha1)
    writer.apply_payload(target_dir, payload)

    # Case 1: API observes sha2 != sha1 -> clean stale_head skip without push
    stale_decision = writer.commit_and_push(
        target_dir,
        branch="feat/example",
        expected_head_sha=sha1,
        repo_full_name="mols3131d/mols-agent-assets",
        app_token="app-token",
        app_slug="test-app",
        requester=lambda path: (
            (200, {"id": 999001, "login": "test-app[bot]", "type": "Bot"})
            if "users/" in path
            else (200, {"object": {"type": "commit", "sha": sha2}})
        ),
    )
    assert stale_decision == writer.Decision(False, "stale_head")

    # Case 2: API races (sha1) so git push hits non-fast-forward without force push
    with pytest.raises(writer.WriterSecurityError, match="Fast-forward push 실패"):
        writer.commit_and_push(
            target_dir,
            branch="feat/example",
            expected_head_sha=sha1,
            repo_full_name="mols3131d/mols-agent-assets",
            app_token="app-token",
            app_slug="test-app",
            requester=lambda path: (
                (200, {"id": 999001, "login": "test-app[bot]", "type": "Bot"})
                if "users/" in path
                else (200, {"object": {"type": "commit", "sha": sha1}})
            ),
        )
    assert (
        _git(
            seed, "ls-remote", bare.as_uri(), "refs/heads/feat/example"
        ).stdout.split()[0]
        == sha2
    )


def test_commit_and_push_rejects_empty_or_github_token_fallback(tmp_path: Path) -> None:
    with pytest.raises(writer.WriterSecurityError):
        writer.commit_and_push(
            tmp_path,
            branch="feat/example",
            expected_head_sha=SAMPLE_SHA,
            repo_full_name="mols3131d/mols-agent-assets",
            app_token="",
            app_slug="test-app",
            requester=lambda _: (200, {}),
        )
    with pytest.raises(writer.WriterSecurityError):
        writer.commit_and_push(
            tmp_path,
            branch="feat/example",
            expected_head_sha=SAMPLE_SHA,
            repo_full_name="mols3131d/mols-agent-assets",
            app_token="same-token",
            app_slug="test-app",
            requester=lambda _: (200, {}),
            github_token="same-token",
        )


def test_apply_payload_rejects_deleting_nonexistent_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / "README.md").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-qm", "init")

    artifact_dir = tmp_path / "artifact"
    _write_payload(artifact_dir, deleted=["docs/missing/INDEX.tsv"])
    payload = writer.validate_artifact_payload(artifact_dir, _provenance())

    with pytest.raises(writer.WriterSecurityError, match="삭제 요청은 거부"):
        writer.apply_payload(repo, payload)


def test_git_askpass_env_answers_username_and_token_prompts(tmp_path: Path) -> None:
    env = writer._git_askpass_env("secret-app-token", tmp_path)
    askpass = env["GIT_ASKPASS"]

    user_out = subprocess.run(
        [askpass, "Username for 'https://github.com':"],
        env={**os.environ, **env},
        check=True,
        capture_output=True,
        text=True,
    )
    pass_out = subprocess.run(
        [askpass, "Password for 'https://x-access-token@github.com':"],
        env={**os.environ, **env},
        check=True,
        capture_output=True,
        text=True,
    )
    assert user_out.stdout.strip() == "x-access-token"
    assert pass_out.stdout.strip() == "secret-app-token"


def test_writer_cli_preflight_disabled_and_noop_skip_cleanly(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    event_file = tmp_path / "event.json"
    event_file.write_text(json.dumps(_make_event()), encoding="utf-8")
    out_file = tmp_path / "github_output.txt"

    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "mols3131d/mols-agent-assets")
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "1167541883")
    monkeypatch.setenv("GITHUB_REF", "refs/heads/main")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ENABLED", "false")
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ALLOWED_BRANCHES", "*")

    assert writer.main(["verify-run"]) == 0
    assert "should_continue=false" in out_file.read_text(encoding="utf-8")
    assert "skip_reason=disabled" in out_file.read_text(encoding="utf-8")


def test_generated_writer_workflow_static_security_invariants() -> None:
    raw_text = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.safe_load(raw_text)
    on_section = workflow.get("on", workflow.get(True))
    assert workflow["permissions"] == {}
    assert "workflow_run" in on_section
    assert on_section["workflow_run"]["workflows"] == [writer.EXPECTED_PRODUCER_NAME]
    assert workflow["concurrency"]["cancel-in-progress"] is False

    jobs = workflow["jobs"]
    assert set(jobs.keys()) == {"preflight", "write"}

    for job_name, job in jobs.items():
        perms = job["permissions"]
        assert perms == {"actions": "read", "contents": "read"}, job_name
        assert "write" not in perms.values()

    write_job = jobs["write"]
    assert write_job["environment"] == "generated-writeback"
    assert "needs.preflight.outputs.should_write == 'true'" in write_job["if"]
    assert "GENERATED_SYNC_WRITER_ENABLED == 'true'" in jobs["preflight"]["if"]

    # Ensure SHA-pinned actions and no untrusted branch checkout ref
    jobs_text = raw_text.split("jobs:", 1)[1]
    app_action = (
        "actions/create-github-app-token@64ab729a6294000f5aa4a4bc0b73d1f32bc45510"
    )
    assert "persist-credentials: false" in raw_text
    assert "--force" not in raw_text
    assert "github.event.workflow_run.head_branch }}" not in jobs_text
    assert app_action in raw_text
    assert "permission-contents: write" in raw_text


def test_writer_cli_prepare_write_and_commit_and_push_end_to_end(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    bare = tmp_path / "mols3131d" / "mols-agent-assets.git"
    bare.parent.mkdir(parents=True)
    _git(tmp_path, "init", "--bare", "-q", str(bare))

    seed = tmp_path / "seed"
    _git(tmp_path, "clone", "-q", bare.as_uri(), str(seed))
    _git(seed, "config", "user.name", "Author")
    _git(seed, "config", "user.email", "author@example.com")
    _git(seed, "checkout", "-b", "feat/e2e-cli")
    (seed / "docs").mkdir()
    (seed / "docs" / "INDEX.tsv").write_text("old\n", encoding="utf-8")
    _git(seed, "add", ".")
    _git(seed, "commit", "-qm", "source commit")
    _git(seed, "push", "-q", "origin", "feat/e2e-cli")
    head_sha = _git(seed, "rev-parse", "HEAD").stdout.strip()

    artifact_dir = tmp_path / "artifact"
    _write_payload(
        artifact_dir,
        files={"docs/INDEX.tsv": b"path\tdescription\ndocs/a.md\ta\n"},
        branch="feat/e2e-cli",
        head_sha=head_sha,
    )

    event_file = tmp_path / "event.json"
    event_file.write_text(
        json.dumps(_make_event(branch="feat/e2e-cli", head_sha=head_sha)),
        encoding="utf-8",
    )
    out_file = tmp_path / "github_output.txt"
    target_dir = tmp_path / "target-repo"
    state_file = tmp_path / "state.json"

    def fake_requester(_token: str, _api_url: str):
        def call(path: str) -> tuple[int, dict[str, object]]:
            if path.endswith("/artifacts"):
                return 200, {
                    "total_count": 1,
                    "artifacts": [
                        {
                            "name": writer.EXPECTED_ARTIFACT_NAME,
                            "expired": False,
                            "size_in_bytes": 256,
                        }
                    ],
                }
            if "git/ref/heads/" in path:
                return 200, {"object": {"type": "commit", "sha": head_sha}}
            if path == "users/mols-sync%5Bbot%5D":
                return 200, {"id": 888111, "login": "mols-sync[bot]", "type": "Bot"}
            raise AssertionError(f"unexpected path: {path}")

        return call

    monkeypatch.setattr(writer, "make_github_api_requester", fake_requester)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "mols3131d/mols-agent-assets")
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "1167541883")
    monkeypatch.setenv("GITHUB_REF", "refs/heads/main")
    monkeypatch.setenv("GITHUB_SERVER_URL", tmp_path.as_uri())
    monkeypatch.setenv("GITHUB_TOKEN", "")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ENABLED", "true")
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ALLOWED_BRANCHES", "feat/e2e-cli")

    assert (
        writer.main(
            [
                "prepare-write",
                "--artifact-dir",
                str(artifact_dir),
                "--target-dir",
                str(target_dir),
                "--state-file",
                str(state_file),
            ]
        )
        == 0
    )
    assert "should_write=true" in out_file.read_text(encoding="utf-8")

    monkeypatch.setenv("APP_TOKEN", "ephemeral-app-token")
    monkeypatch.setenv("APP_SLUG", "mols-sync")
    monkeypatch.setenv("GITHUB_TOKEN", "gh-read-token")
    assert (
        writer.main(
            [
                "commit-and-push",
                "--target-dir",
                str(target_dir),
                "--state-file",
                str(state_file),
            ]
        )
        == 0
    )
    pushed_sha = _git(
        seed, "ls-remote", bare.as_uri(), "refs/heads/feat/e2e-cli"
    ).stdout.split()[0]
    assert pushed_sha != head_sha
