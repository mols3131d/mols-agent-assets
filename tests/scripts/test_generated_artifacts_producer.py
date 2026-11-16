from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path, PurePosixPath

import pytest
import yaml

from scripts import (
    generated_artifacts_producer as producer,
    generated_artifacts_sync as sync,
)

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "generated-sync.yml"


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", f"core.hooksPath={os.devnull}", *args],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _init_repo(repo: Path) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Author")
    _git(repo, "config", "user.email", "author@example.com")
    _git(repo, "checkout", "-b", "feat/demo")
    (repo / "docs").mkdir()
    (repo / "docs" / "INDEX.tsv").write_text("path\tdescription\n", encoding="utf-8")
    (repo / ".agents" / "route").mkdir(parents=True)
    (repo / ".agents" / "route" / "all.jsonl").write_text("{}\n", encoding="utf-8")
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "initial")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _matches_workflow_path_patterns(path: str, patterns: list[str]) -> bool:
    posix = PurePosixPath(path)
    matched = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw = pattern[1:] if negated else pattern
        if raw.endswith("/**"):
            prefix = raw[:-3]
            hits = path.startswith(f"{prefix}/")
        elif raw == ".agents/route/*.jsonl":
            hits = (
                posix.parent == PurePosixPath(".agents/route")
                and posix.suffix == ".jsonl"
            )
        elif raw == "route/*.jsonl":
            hits = posix.parent == PurePosixPath("route") and posix.suffix == ".jsonl"
        else:
            hits = path == raw
        if hits:
            matched = not negated
    return matched


def test_package_payload_noop_emits_metadata_without_files_dir(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    out = tmp_path / "out"

    metadata = producer.package_payload(
        root=repo,
        output_dir=out,
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=head_sha,
        producer_run_id=456,
    )
    assert metadata["changed"] is False
    assert metadata["files"] == []
    assert metadata["deleted"] == []
    assert (out / "metadata.json").is_file()
    assert not (out / "files").exists()


def test_package_payload_collects_added_modified_and_deleted_outputs(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    (repo / "docs" / "sub").mkdir()
    stale = repo / "docs" / "sub" / "INDEX.tsv"
    stale.write_text("stale\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "with sub index")
    head_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # sync 결과를 모의해 docs/INDEX.tsv 수정, docs/sub/INDEX.tsv 삭제, route 추가를 검증
    (repo / "docs" / "INDEX.tsv").write_text(
        "path\tdescription\ndocs/a.md\ta\n", encoding="utf-8"
    )
    stale.unlink()
    (repo / "route").mkdir()
    (repo / "route" / "skills.jsonl").write_text('{"name":"demo"}\n', encoding="utf-8")

    out = tmp_path / "out"
    metadata = producer.package_payload(
        root=repo,
        output_dir=out,
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=head_sha,
        producer_run_id=789,
    )
    assert metadata["changed"] is True
    assert metadata["deleted"] == ["docs/sub/INDEX.tsv"]
    paths = [item["path"] for item in metadata["files"]]
    assert paths == ["docs/INDEX.tsv", "route/skills.jsonl"]

    for item in metadata["files"]:
        staged_file = out / "files" / item["path"]
        assert staged_file.is_file()
        raw = staged_file.read_bytes()
        assert len(raw) == item["size"]
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]


def test_package_payload_rejects_non_generated_changes_and_core_deletions(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    (repo / "README.md").write_text("oops\n", encoding="utf-8")

    with pytest.raises(producer.ProducerError, match="허용된 생성 출력 외"):
        producer.package_payload(
            root=repo,
            output_dir=tmp_path / "out1",
            repository_id=123,
            repository_full_name="mols3131d/mols-agent-assets",
            branch="feat/demo",
            head_sha=head_sha,
            producer_run_id=1,
        )

    _git(repo, "checkout", "--", "README.md")
    (repo / "docs" / "INDEX.tsv").unlink()
    with pytest.raises(producer.ProducerError, match="핵심 생성 출력"):
        producer.package_payload(
            root=repo,
            output_dir=tmp_path / "out2",
            repository_id=123,
            repository_full_name="mols3131d/mols-agent-assets",
            branch="feat/demo",
            head_sha=head_sha,
            producer_run_id=1,
        )


def test_producer_cli_end_to_end_via_env(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    (repo / ".agents" / "route" / "all.jsonl").write_text(
        '{"name":"updated"}\n', encoding="utf-8"
    )

    event_file = tmp_path / "event.json"
    event_file.write_text(
        json.dumps(
            {"repository": {"id": 555, "full_name": "mols3131d/mols-agent-assets"}}
        ),
        encoding="utf-8",
    )
    github_output = tmp_path / "github_output.txt"
    out_dir = tmp_path / "artifact"

    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "mols3131d/mols-agent-assets")
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "555")
    monkeypatch.setenv("GITHUB_REF", "refs/heads/feat/demo")
    monkeypatch.setenv("GITHUB_SHA", head_sha)
    monkeypatch.setenv("GITHUB_RUN_ID", "901")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output))

    rc = producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
    assert rc == 0
    assert github_output.read_text(encoding="utf-8").strip() == "changed=true"
    assert (out_dir / "files" / ".agents" / "route" / "all.jsonl").is_file()


def test_generated_sync_workflow_is_read_only_and_covers_projection_inputs() -> None:
    raw = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.safe_load(raw)
    on_section = workflow.get("on", workflow.get(True))

    assert workflow["name"] == "Sync Generated Artifacts"
    assert workflow["permissions"] == {"contents": "read"}
    assert "workflow_dispatch" not in on_section
    assert "main" in on_section["push"]["branches-ignore"]
    assert "git push" not in raw
    assert "gh auth setup-git" not in raw
    assert "secrets." not in raw
    assert "include-hidden-files: true" in raw

    patterns = on_section["push"]["paths"]
    assert _matches_workflow_path_patterns("scripts/generated_artifacts.py", patterns)
    canonical_paths = [
        "docs/guide.md",
        "docs/INDEX.tsv",
        "docs/development/INDEX.tsv",
        "catalog/skills.json",
        "catalog/patterns/example.md",
        "catalog/INDEX.tsv",
        "src/rulesync/.rulesync/skills/example/SKILL.md",
        "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/generate_index.py",
        "src/rulesync/.rulesync/subagents/review.md",
        "scripts/agent_assets/routes_distribution_generate.py",
        "scripts/agent_assets/routes_repository_generate.py",
        "rulesync.lock",
        "rulesync.jsonc",
        "skills-lock.json",
        ".agents/route/families.json",
        ".agents/route/all.jsonl",
        "route/skills.jsonl",
    ]
    for path in canonical_paths:
        assert _matches_workflow_path_patterns(path, patterns), path
        assert sync.select_projections({path}), path


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/INDEX.tsv", True),
        ("docs/development/INDEX.tsv", True),
        ("catalog/INDEX.tsv", True),
        ("route/skills.jsonl", True),
        (".agents/route/all.jsonl", True),
        (".agents/route/nested/all.jsonl", False),
        ("route/nested/skills.jsonl", False),
        ("../docs/INDEX.tsv", False),
        (".github/workflows/generated-sync.yml", False),
        ("docs/guide.md", False),
    ],
)
def test_producer_allowed_generated_output_allowlist(path: str, expected: bool) -> None:
    assert producer.is_allowed_generated_output(path) is expected


def test_package_payload_recovers_output_only_deletion_then_becomes_noop(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)

    # API 커밋으로 생성 파일이 삭제된 상태를 만든다 (T05)
    (repo / "route").mkdir()
    (repo / "route" / "skills.jsonl").write_text(
        '{"name":"canonical"}\n', encoding="utf-8"
    )
    _git(repo, "add", "route/skills.jsonl")
    _git(repo, "commit", "-qm", "with route")

    (repo / "route" / "skills.jsonl").unlink()
    _git(repo, "add", "route/skills.jsonl")
    _git(repo, "commit", "-qm", "api deleted generated file")
    corrupt_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # Producer sync restores route/skills.jsonl -> packaged as changed=True
    (repo / "route" / "skills.jsonl").write_text(
        '{"name":"canonical"}\n', encoding="utf-8"
    )
    first_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out1",
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=corrupt_sha,
        producer_run_id=10,
    )
    assert first_meta["changed"] is True
    assert [entry["path"] for entry in first_meta["files"]] == ["route/skills.jsonl"]

    # 복구 커밋 후 재진입 실행은 changed=False no-op 이어야 한다 (T11)
    _git(repo, "add", "route/skills.jsonl")
    _git(repo, "commit", "-qm", "chore(generated): sync indexes and routes")
    bot_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    second_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out2",
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=bot_sha,
        producer_run_id=11,
    )
    assert second_meta["changed"] is False
    assert second_meta["files"] == []
    assert second_meta["deleted"] == []
    assert head_sha != bot_sha
