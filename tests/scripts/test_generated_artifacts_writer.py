from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import zipfile
from pathlib import Path

import pytest
import yaml

from scripts import generated_artifacts_writer as writer

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "generated-writer.yml"
SAMPLE_SHA = "a" * 40
NEWER_SHA = "b" * 40
ARTIFACT_ID = 123


def _artifact_response(**overrides: object) -> dict[str, object]:
    return {
        "total_count": 1,
        "artifacts": [
            {
                "id": ARTIFACT_ID,
                "name": writer.ARTIFACT_NAME,
                "expired": False,
                "size_in_bytes": 128,
                "digest": f"sha256:{'a' * 64}",
                **overrides,
            }
        ],
    }


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
    run_attempt: int | bool | None = 1,
) -> dict[str, object]:
    run_obj: dict[str, object] = {
        "id": run_id,
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
    }
    if run_attempt is not None:
        run_obj["run_attempt"] = run_attempt

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
        "workflow_run": run_obj,
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


def _build_metadata(
    *,
    files: dict[str, bytes] | None = None,
    deleted: list[str] | None = None,
    changed: bool = True,
    branch: str = "feat/example",
    head_sha: str = SAMPLE_SHA,
    repo_id: int = 1167541883,
    repo_name: str = "mols3131d/mols-agent-assets",
    run_id: int = 42,
    run_attempt: int | bool = 1,
) -> dict[str, object]:
    file_entries = []
    if files:
        for rel, content in sorted(files.items()):
            file_entries.append(
                {
                    "path": rel,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size": len(content),
                }
            )
    return {
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
    run_attempt: int | bool = 1,
) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    if files:
        files_root = artifact_dir / "files"
        for rel, content in sorted(files.items()):
            dest = files_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)

    metadata = _build_metadata(
        files=files,
        deleted=deleted,
        changed=changed,
        branch=branch,
        head_sha=head_sha,
        repo_id=repo_id,
        repo_name=repo_name,
        run_id=run_id,
        run_attempt=run_attempt,
    )
    (artifact_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")


def _write_payload_zip(
    zip_path: Path,
    *,
    files: dict[str, bytes] | None = None,
    deleted: list[str] | None = None,
    changed: bool = True,
    branch: str = "feat/example",
    head_sha: str = SAMPLE_SHA,
) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = _build_metadata(
        files=files,
        deleted=deleted,
        changed=changed,
        branch=branch,
        head_sha=head_sha,
    )
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("metadata.json", json.dumps(metadata))
        if files:
            for rel, content in sorted(files.items()):
                zf.writestr(f"files/{rel}", content)


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
        ("docs\\INDEX.tsv", False),
        ("docs//INDEX.tsv", False),
        ("docs/\x00INDEX.tsv", False),
        ("docs/INDEX.tsv/", False),
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
    "branch",
    [
        "main",
        "HEAD",
        "@",
        "refs/heads/feat",
        "-flag",
        "feat..bar",
        "feat@{0}",
        "feat//bar",
        "feat/.hidden",
        "feat/bad.lock",
        "feat with space",
    ],
)
def test_validate_source_branch_rejects_main_and_unsafe_refs(branch: str) -> None:
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

    for allowlist in ("", "*", "feat/*"):
        decision2, _ = writer.verify_workflow_run_event(
            event,
            github_repository="mols3131d/mols-agent-assets",
            github_repository_id="1167541883",
            github_ref="refs/heads/main",
            enabled="true",
            allowed_branches=allowlist,
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
        {"conclusion": "cancelled"},
        {"conclusion": "timed_out"},
        {"status": "in_progress"},
        {"branch": "main"},
        {"head_sha": "not-a-sha"},
        {"run_attempt": 0},
        {"run_attempt": False},
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


def test_verify_workflow_run_event_rejects_bad_repo_id_and_missing_repo_fields() -> (
    None
):
    with pytest.raises(writer.WriterSecurityError):
        writer.verify_workflow_run_event(
            _make_event(),
            github_repository="mols3131d/mols-agent-assets",
            github_repository_id="²",
            github_ref="refs/heads/main",
            enabled="true",
            allowed_branches="*",
        )

    event = _make_event()
    del event["workflow_run"]["head_repository"]  # type: ignore[index]
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
    assert (
        writer.verify_single_artifact(lambda _: (200, _artifact_response()), "o/r", 1)
        == ARTIFACT_ID
    )

    bad_cases = [
        {"total_count": 0, "artifacts": []},
        {**_artifact_response(), "total_count": 2},
        _artifact_response(name="wrong"),
        _artifact_response(expired=True),
        _artifact_response(size_in_bytes=0),
        _artifact_response(size_in_bytes=writer.MAX_ARTIFACT_ARCHIVE_BYTES + 1),
        _artifact_response(digest=None),
        _artifact_response(id=True),
    ]
    for case in bad_cases:
        with pytest.raises(writer.WriterSecurityError):
            writer.verify_single_artifact(lambda _, c=case: (200, c), "o/r", 1)

    with pytest.raises(writer.WriterSecurityError):
        writer.verify_single_artifact(lambda _: (500, {}), "o/r", 1)


def test_github_api_lookup_errors_fail_closed() -> None:
    assert writer.get_branch_head_sha(lambda _: (404, {}), "o/r", "feat/x") is None
    with pytest.raises(writer.WriterSecurityError):
        writer.get_branch_head_sha(lambda _: (500, {}), "o/r", "feat/x")
    with pytest.raises(writer.WriterSecurityError):
        writer.get_branch_head_sha(
            lambda _: (200, {"object": {"type": "tag", "sha": SAMPLE_SHA}}),
            "o/r",
            "feat/x",
        )
    with pytest.raises(writer.WriterSecurityError):
        writer.get_branch_head_sha(
            lambda _: (200, {"object": {"type": "commit", "sha": "bad"}}),
            "o/r",
            "feat/x",
        )

    with pytest.raises(writer.WriterSecurityError):
        writer.get_bot_identity(lambda _: (200, {}), "bad slug!")
    with pytest.raises(writer.WriterSecurityError):
        writer.get_bot_identity(lambda _: (404, {}), "my-app")
    with pytest.raises(writer.WriterSecurityError):
        writer.get_bot_identity(
            lambda _: (200, {"id": 1, "login": "my-app[bot]", "type": "User"}),
            "my-app",
        )
    with pytest.raises(writer.WriterSecurityError):
        writer.get_bot_identity(
            lambda _: (200, {"id": 1, "login": "other[bot]", "type": "Bot"}),
            "my-app",
        )


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


def test_validate_artifact_payload_rejects_tampering_limits_and_symlinks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # 예기치 않은 최상위 파일·빈 디렉터리 거부
    extra_top = tmp_path / "extra_top"
    _write_payload(extra_top, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (extra_top / "evil.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(extra_top, _provenance())

    empty_top_dir = tmp_path / "empty_top_dir"
    _write_payload(empty_top_dir, changed=False)
    (empty_top_dir / "unexpected_dir").mkdir()
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(empty_top_dir, _provenance())

    # metadata 키/타입/boolean coercion 오류 거부
    bad_bool = tmp_path / "bad_bool"
    _write_payload(bad_bool, changed=False, run_attempt=True)
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_bool, _provenance())

    bad_json = tmp_path / "bad_json"
    bad_json.mkdir()
    (bad_json / "metadata.json").write_text("[]", encoding="utf-8")
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_json, _provenance())

    # changed=False 인데 files/ 디렉터리가 남아 있는 경우 거부
    noop_with_files = tmp_path / "noop_with_files"
    _write_payload(noop_with_files, changed=False)
    (noop_with_files / "files").mkdir()
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(noop_with_files, _provenance())

    # changed=True 인데 files와 deleted가 모두 비어 있는 경우 거부
    empty_change = tmp_path / "empty_change"
    _write_payload(empty_change, changed=True)
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(empty_change, _provenance())

    # files/ 내 누락 또는 초과 파일 거부
    extra_file = tmp_path / "extra_file"
    _write_payload(extra_file, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (extra_file / "files" / "catalog").mkdir()
    (extra_file / "files" / "catalog" / "INDEX.tsv").write_text(
        "tamper\n", encoding="utf-8"
    )
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(extra_file, _provenance())

    # SHA-256 불일치 및 비-UTF-8 바이너리 거부
    bad_digest = tmp_path / "bad_digest"
    _write_payload(bad_digest, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    (bad_digest / "files" / "docs" / "INDEX.tsv").write_text(
        "tampered\n", encoding="utf-8"
    )
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_digest, _provenance())

    bad_utf8 = tmp_path / "bad_utf8"
    _write_payload(bad_utf8, files={"docs/INDEX.tsv": b"\xff\xfe\x00"})
    with pytest.raises(writer.WriterSecurityError, match="UTF-8"):
        writer.validate_artifact_payload(bad_utf8, _provenance())

    # 허용되지 않은 경로 및 핵심 출력 삭제·중복 충돌 거부
    bad_path = tmp_path / "bad_path"
    _write_payload(bad_path, files={".github/workflows/pr-gate.yml": b"name: evil\n"})
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_path, _provenance())

    bad_delete = tmp_path / "bad_delete"
    _write_payload(bad_delete, deleted=["docs/INDEX.tsv"])
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(bad_delete, _provenance())

    conflict_dir = tmp_path / "conflict_dir"
    _write_payload(
        conflict_dir,
        files={"docs/sub/INDEX.tsv": b"a\n"},
        deleted=["docs/sub/INDEX.tsv"],
    )
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(conflict_dir, _provenance())

    # 크기 상한 거부
    monkeypatch.setattr(writer, "MAX_FILE_BYTES", 4)
    too_big = tmp_path / "too_big"
    _write_payload(too_big, files={"docs/INDEX.tsv": b"12345"})
    with pytest.raises(writer.WriterSecurityError):
        writer.validate_artifact_payload(too_big, _provenance())
    monkeypatch.undo()

    # Symlink 거부 (OS 권한이 없는 환경에서도 os.lstat 모의로 결정적 검증)
    sym_dir = tmp_path / "sym"
    _write_payload(sym_dir, files={"docs/INDEX.tsv": b"path\tdescription\n"})
    real_lstat = os.lstat
    target_link = sym_dir / "files" / "docs" / "INDEX.tsv"

    class _FakeSymlinkStat:
        st_mode = stat.S_IFLNK | 0o777
        st_size = 0

    monkeypatch.setattr(
        writer.os,
        "lstat",
        lambda p: _FakeSymlinkStat() if Path(p) == target_link else real_lstat(p),
    )
    with pytest.raises(writer.WriterSecurityError, match="symlink"):
        writer.validate_artifact_payload(sym_dir, _provenance())


def test_extract_artifact_zip_prevents_zip_bombs_symlinks_and_traversal(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # 정상 skip-decompress zip 해석
    artifact_holder = tmp_path / "holder"
    zip_file = artifact_holder / f"{writer.ARTIFACT_NAME}.zip"
    _write_payload_zip(
        zip_file,
        files={
            "docs/INDEX.tsv": b"path\tdescription\n",
            ".agents/route/all.jsonl": b"{}\n",
        },
    )
    resolved = writer.resolve_artifact_directory(
        artifact_holder, tmp_path / "extracted"
    )
    validated = writer.validate_artifact_payload(resolved, _provenance())
    assert [f.path for f in validated.files] == [
        ".agents/route/all.jsonl",
        "docs/INDEX.tsv",
    ]

    # Path traversal zip 거부
    bad_trav = tmp_path / "trav.zip"
    with zipfile.ZipFile(bad_trav, "w") as zf:
        zf.writestr("../evil.txt", "pwn")
    with pytest.raises(writer.WriterSecurityError, match="안전하지 않은 zip"):
        writer.extract_artifact_zip(bad_trav, tmp_path / "out_trav")

    # Unix symlink external_attr 거부
    bad_sym = tmp_path / "sym.zip"
    with zipfile.ZipFile(bad_sym, "w") as zf:
        info = zipfile.ZipInfo("files/docs/INDEX.tsv")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        zf.writestr(info, "/etc/passwd")
    with pytest.raises(writer.WriterSecurityError, match="symlink"):
        writer.extract_artifact_zip(bad_sym, tmp_path / "out_sym")

    # Zip bomb (압축 해제 총 크기 초과) 거부
    monkeypatch.setattr(writer, "MAX_TOTAL_PAYLOAD_BYTES", 10)
    monkeypatch.setattr(writer, "MAX_METADATA_BYTES", 1024)
    bomb_zip = tmp_path / "bomb.zip"
    _write_payload_zip(bomb_zip, files={"docs/INDEX.tsv": b"0123456789abcdef"})
    with pytest.raises(writer.WriterSecurityError, match="총 압축 해제 크기"):
        writer.extract_artifact_zip(bomb_zip, tmp_path / "out_bomb")
    assert not (tmp_path / "out_bomb").exists()


def test_extract_accepts_maximum_output_files_across_directories(
    tmp_path: Path,
) -> None:
    files = {
        f"docs/group-{index}/pages/INDEX.tsv": b"path\tdescription\n"
        for index in range(writer.MAX_FILE_COUNT - 1)
    }
    deepest_allowed = "/".join(
        ["docs", *(["deep"] * (writer.MAX_OUTPUT_PATH_DEPTH - 2)), "INDEX.tsv"]
    )
    files[deepest_allowed] = b"path\tdescription\n"
    zip_path = tmp_path / "max-files.zip"
    _write_payload_zip(zip_path, files=files)
    with zipfile.ZipFile(zip_path, "a") as archive:
        dirs = {f"files/{path.rsplit('/', 1)[0]}/" for path in files}
        for directory in sorted(dirs):
            archive.writestr(directory, b"")

    extracted = writer.extract_artifact_zip(zip_path, tmp_path / "extracted")
    payload = writer.validate_artifact_payload(extracted, _provenance())
    assert {file.path for file in payload.files} == files.keys()


def test_extract_checks_path_depth_before_creating_files(tmp_path: Path) -> None:
    deep_path = "/".join(
        ["docs", *(["x"] * (writer.MAX_OUTPUT_PATH_DEPTH - 1)), "INDEX.tsv"]
    )
    assert not writer.is_allowed_generated_output(deep_path)
    files = {"docs/INDEX.tsv": b"header\n", deep_path: b"header\n"}
    zip_path = tmp_path / "deep.zip"
    _write_payload_zip(zip_path, files=files)

    extract_dir = tmp_path / "extracted"
    with pytest.raises(
        writer.WriterSecurityError, match="허용되지 않은 zip 생성 파일 경로"
    ):
        writer.extract_artifact_zip(zip_path, extract_dir)
    assert not extract_dir.exists()


def test_extract_rejects_unsupported_compression_before_writing(tmp_path: Path) -> None:
    zip_path = tmp_path / "unsupported.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("metadata.json", "{}")
        archive.writestr("files/docs/INDEX.tsv", b"header\n", zipfile.ZIP_BZIP2)

    extract_dir = tmp_path / "extracted"
    with pytest.raises(writer.WriterSecurityError, match="지원하지 않는 zip 압축"):
        writer.extract_artifact_zip(zip_path, extract_dir)
    assert not extract_dir.exists()


def test_apply_payload_rejects_dangling_and_live_symlinks_and_dirty_repo(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / "docs").mkdir()
    (repo / "docs" / "INDEX.tsv").write_text("old\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")

    artifact_dir = tmp_path / "artifact"
    _write_payload(artifact_dir, files={"docs/INDEX.tsv": b"new\n"})
    payload = writer.validate_artifact_payload(artifact_dir, _provenance())

    # Dirty checkout 거부 (T15)
    (repo / "untracked.txt").write_text("dirty\n", encoding="utf-8")
    with pytest.raises(writer.WriterSecurityError, match="clean 상태"):
        writer.apply_payload(repo, payload)
    (repo / "untracked.txt").unlink()

    # Dangling symlink 차단 검증 (os.lstat 모의로 권한 비의존)
    target_file = repo / "docs" / "INDEX.tsv"
    real_lstat = os.lstat

    class _DanglingSymlinkStat:
        st_mode = stat.S_IFLNK | 0o777

    monkeypatch.setattr(
        writer.os,
        "lstat",
        lambda p: _DanglingSymlinkStat() if Path(p) == target_file else real_lstat(p),
    )
    with pytest.raises(writer.WriterSecurityError, match="symlink"):
        writer.apply_payload(repo, payload)
    monkeypatch.undo()

    # 실제 OS가 symlink 생성을 허용할 경우 dangling symlink write-through도 직접 검증
    dangling_repo = tmp_path / "dangling_repo"
    dangling_repo.mkdir()
    _git(dangling_repo, "init", "-q")
    _git(dangling_repo, "config", "user.name", "Test")
    _git(dangling_repo, "config", "user.email", "test@example.com")
    (dangling_repo / "docs").mkdir()
    outside = tmp_path / "outside_gitconfig"
    try:
        (dangling_repo / "docs" / "INDEX.tsv").symlink_to(outside)
    except OSError:
        pass
    else:
        _git(dangling_repo, "add", ".")
        _git(dangling_repo, "commit", "-qm", "dangling symlink")
        with pytest.raises(writer.WriterSecurityError, match="symlink"):
            writer._ensure_no_symlink_components(dangling_repo, "docs/INDEX.tsv")
        with pytest.raises(writer.WriterSecurityError, match="symlink|120000"):
            writer.apply_payload(dangling_repo, payload)
        assert not outside.exists()


def test_apply_payload_rejects_type_conflict_and_unexpected_staged_files(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / "docs" / "INDEX.tsv").mkdir(parents=True)
    (repo / "docs" / "INDEX.tsv" / "keep.txt").write_text("dir\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "dir where file expected")

    artifact_dir = tmp_path / "artifact"
    _write_payload(artifact_dir, files={"docs/INDEX.tsv": b"new\n"})
    payload = writer.validate_artifact_payload(artifact_dir, _provenance())

    with pytest.raises(writer.WriterSecurityError, match="일반 파일이 아닙니다"):
        writer.apply_payload(repo, payload)

    # 최상위 일반 파일 이름이 'files'인 변조 zip 거부
    bad_files_zip = tmp_path / "files_reg.zip"
    with zipfile.ZipFile(bad_files_zip, "w") as zf:
        zf.writestr("files", "not a dir")
    with pytest.raises(writer.WriterSecurityError, match="허용되지 않은 최상위"):
        writer.extract_artifact_zip(bad_files_zip, tmp_path / "out_files_reg")

    # staged diff에 T(typechange) 상태가 나타날 경우 거부
    t_repo = tmp_path / "t_repo"
    t_repo.mkdir()
    _git(t_repo, "init", "-q")
    _git(t_repo, "config", "user.name", "Test")
    _git(t_repo, "config", "user.email", "test@example.com")
    _git(t_repo, "config", "core.symlinks", "false")
    # core.symlinks=false 환경에서도 git 120000 -> 100644 typechange를 차단하는지 검증
    (t_repo / "docs").mkdir()
    (t_repo / "docs" / "INDEX.tsv").write_text("target", encoding="utf-8")
    _git(t_repo, "add", "docs/INDEX.tsv")
    blob_sha = _git(t_repo, "rev-parse", ":docs/INDEX.tsv").stdout.strip()
    _git(t_repo, "update-index", "--cacheinfo", f"120000,{blob_sha},docs/INDEX.tsv")
    _git(t_repo, "commit", "-qm", "symlink mode commit")
    _git(t_repo, "checkout", "-f", "--", "docs/INDEX.tsv")
    with pytest.raises(
        writer.WriterSecurityError, match="Git index mode|staged diff 상태"
    ):
        writer.apply_payload(t_repo, payload)


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


def test_apply_payload_rejects_git_attribute_blob_transformation(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / ".gitattributes").write_text("docs/INDEX.tsv ident\n", encoding="utf-8")
    _git(repo, "add", ".gitattributes")
    _git(repo, "commit", "-qm", "set attributes")
    artifact_dir = tmp_path / "artifact"
    _write_payload(artifact_dir, files={"docs/INDEX.tsv": b"$Id: changed bytes $\n"})
    payload = writer.validate_artifact_payload(artifact_dir, _provenance())

    with pytest.raises(writer.WriterSecurityError, match="Staged blobs differ"):
        writer.apply_payload(repo, payload)


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

    # Case 1: API가 sha2를 관측하면 push 없이 stale_head로 종료
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

    # Case 2: 커밋 직전은 sha1이었으나 push 직전 sha2로 이동한 경우 (second stale_head)
    calls = {"ref": 0}

    def race_before_push_api(path: str) -> tuple[int, dict[str, object]]:
        if "users/" in path:
            return 200, {"id": 999001, "login": "test-app[bot]", "type": "Bot"}
        calls["ref"] += 1
        return 200, {
            "object": {"type": "commit", "sha": sha1 if calls["ref"] == 1 else sha2}
        }

    second_stale = writer.commit_and_push(
        target_dir,
        branch="feat/example",
        expected_head_sha=sha1,
        repo_full_name="mols3131d/mols-agent-assets",
        app_token="app-token",
        app_slug="test-app",
        requester=race_before_push_api,
    )
    assert second_stale == writer.Decision(False, "stale_head")

    # Case 3: 원격 HEAD가 이동했는데 API가 구 SHA를 주면 non-fast-forward 거부
    target_dir_3 = tmp_path / "writer-target-3"
    writer.checkout_source_commit(bare.as_uri(), target_dir_3, sha1)
    writer.apply_payload(target_dir_3, payload)
    with pytest.raises(writer.WriterSecurityError, match="Fast-forward push 실패"):
        writer.commit_and_push(
            target_dir_3,
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

    # The API may still report the source SHA when Git sees the ref rewound or deleted.
    for actual_head in (sha1, None):
        _git(bare, "update-ref", "refs/heads/feat/example", sha2)
        target = tmp_path / ("rewound" if actual_head else "deleted")
        writer.checkout_source_commit(bare.as_uri(), target, sha2)
        _git(target, "fetch", "--unshallow", "origin", "refs/heads/feat/example")
        writer.apply_payload(target, payload)
        if actual_head is None:
            _git(bare, "update-ref", "-d", "refs/heads/feat/example")
        else:
            _git(bare, "update-ref", "refs/heads/feat/example", actual_head)

        with pytest.raises(writer.WriterSecurityError, match="remote branch changed"):
            writer.commit_and_push(
                target,
                branch="feat/example",
                expected_head_sha=sha2,
                repo_full_name="mols3131d/mols-agent-assets",
                app_token="app-token",
                app_slug="test-app",
                requester=lambda path: (
                    (200, {"id": 999001, "login": "test-app[bot]", "type": "Bot"})
                    if "users/" in path
                    else (200, {"object": {"type": "commit", "sha": sha2}})
                ),
            )
        remote = _git(
            bare, "for-each-ref", "--format=%(objectname)", "refs/heads/feat/example"
        )
        assert remote.stdout.strip() == (actual_head or "")


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


def test_writer_cli_skips_when_disabled_noop_or_stale_head(
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
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ALLOWED_BRANCHES", "feat/example")

    assert writer.main(["verify-run"]) == 0
    assert "should_continue=false" in out_file.read_text(encoding="utf-8")
    assert "skip_reason=disabled" in out_file.read_text(encoding="utf-8")

    # changed=False no-op CLI 검증 (T01)
    def ok_requester(_token: str, _api_url: str):
        def call(path: str) -> tuple[int, dict[str, object]]:
            if path.endswith("/artifacts"):
                return 200, _artifact_response()
            if "git/ref/heads/" in path:
                return 200, {"object": {"type": "commit", "sha": SAMPLE_SHA}}
            raise AssertionError(path)

        return call

    monkeypatch.setattr(writer, "make_github_api_requester", ok_requester)
    monkeypatch.setenv("GENERATED_SYNC_WRITER_ENABLED", "true")
    assert writer.main(["verify-run"]) == 0
    assert f"artifact_id={ARTIFACT_ID}" in out_file.read_text(encoding="utf-8")
    monkeypatch.setenv("EXPECTED_ARTIFACT_ID", str(ARTIFACT_ID + 1))
    assert writer.main(["verify-run"]) == 1
    monkeypatch.delenv("EXPECTED_ARTIFACT_ID")

    noop_zip_holder = tmp_path / "noop_holder"
    _write_payload_zip(noop_zip_holder / f"{writer.ARTIFACT_NAME}.zip", changed=False)
    out_noop = tmp_path / "noop_out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_noop))
    assert (
        writer.main(
            [
                "prepare-write",
                "--artifact-dir",
                str(noop_zip_holder),
                "--extract-dir",
                str(tmp_path / "noop_extract"),
                "--target-dir",
                str(tmp_path / "noop_repo"),
            ]
        )
        == 0
    )
    noop_txt = out_noop.read_text(encoding="utf-8")
    assert "should_write=false" in noop_txt
    assert "skip_reason=no_op" in noop_txt

    # stale_head (원격 브랜치 404 또는 HEAD 이동) CLI 검증 (T08)
    def deleted_ref(path: str) -> tuple[int, dict[str, object]]:
        assert "/git/ref/heads/" in path
        return 404, {}

    monkeypatch.setattr(writer, "make_github_api_requester", lambda *_: deleted_ref)
    out_stale = tmp_path / "stale_out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_stale))
    assert writer.main(["verify-run"]) == 0
    assert "skip_reason=stale_head" in out_stale.read_text(encoding="utf-8")


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
    _write_payload_zip(
        artifact_dir / f"{writer.ARTIFACT_NAME}.zip",
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
                return 200, _artifact_response()
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
                "--extract-dir",
                str(tmp_path / "extracted"),
                "--target-dir",
                str(target_dir),
                "--state-file",
                str(state_file),
            ]
        )
        == 0
    )
    assert "should_write=true" in out_file.read_text(encoding="utf-8")

    # 손상된 state_file 실패 진단 (T10)
    saved_state = state_file.read_text(encoding="utf-8")
    state_file.write_text("{bad json", encoding="utf-8")
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
        == 1
    )
    state_file.write_text(saved_state, encoding="utf-8")

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


def test_generated_writer_workflow_static_security_invariants() -> None:
    raw_text = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.safe_load(raw_text)
    on_section = workflow.get("on", workflow.get(True))
    assert workflow["permissions"] == {}
    assert "workflow_run" in on_section
    assert on_section["workflow_run"]["workflows"] == [writer.EXPECTED_PRODUCER_NAME]
    assert workflow["concurrency"]["cancel-in-progress"] is False
    assert "workflow_run.id" in workflow["concurrency"]["group"]
    assert "workflow_run.head_sha" in workflow["concurrency"]["group"]

    jobs = workflow["jobs"]
    assert set(jobs.keys()) == {"preflight", "write"}

    for job_name, job in jobs.items():
        perms = job["permissions"]
        assert perms == {"actions": "read", "contents": "read"}, job_name
        assert "write" not in perms.values()
        for step in job["steps"]:
            uses = step.get("uses")
            if uses:
                sha = uses.split("@", 1)[1].split()[0]
                assert writer.HEX_SHA_RE.fullmatch(sha), uses
                if uses.startswith("actions/checkout@"):
                    with_block = step.get("with", {})
                    assert with_block.get("persist-credentials") is False
                    assert "ref" not in with_block
                    assert "repository" not in with_block
                if uses.startswith("astral-sh/setup-uv@"):
                    assert step["with"]["enable-cache"] is False
                if uses.startswith("actions/download-artifact@"):
                    assert step["with"]["skip-decompress"] is True
                    assert (
                        step["with"]["artifact-ids"]
                        == "${{ steps.verify_run.outputs.artifact_id }}"
                    )
                    assert "name" not in step["with"]
            run_cmd = step.get("run", "")
            assert "${{" not in run_cmd, step.get("name")

    preflight = jobs["preflight"]
    assert "environment" not in preflight
    assert "GENERATED_SYNC_WRITER_ENABLED == 'true'" in preflight["if"]
    assert "head_branch != ''" in preflight["if"]
    assert "head_branch != null" in preflight["if"]
    assert "secrets." not in yaml.safe_dump(preflight)

    write_job = jobs["write"]
    assert write_job["environment"] == "generated-writeback"
    assert "needs.preflight.outputs.should_write == 'true'" in write_job["if"]
    assert "GENERATED_SYNC_WRITER_ENABLED == 'true'" in write_job["if"]
    assert "default_branch" in write_job["if"]
    verify_run = next(
        step for step in write_job["steps"] if step.get("id") == "verify_run"
    )
    assert (
        verify_run["env"]["EXPECTED_ARTIFACT_ID"]
        == "${{ needs.preflight.outputs.artifact_id }}"
    )
    secret_steps = [
        step.get("id")
        for step in write_job["steps"]
        if "secrets." in yaml.safe_dump(step)
    ]
    assert secret_steps == ["app_token"]

    jobs_text = raw_text.split("jobs:", 1)[1]
    app_action = (
        "actions/create-github-app-token@64ab729a6294000f5aa4a4bc0b73d1f32bc45510"
    )
    assert "--force" not in raw_text
    assert "+HEAD:" not in raw_text
    assert "github.event.workflow_run.head_branch }}" not in jobs_text
    assert app_action in raw_text
    assert "permission-contents: write" in raw_text
