from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from dataclasses import replace
from pathlib import Path, PurePosixPath

import pytest
import yaml

from scripts import (
    generated_artifacts_producer as producer,
    generated_artifacts_sync as sync,
    generated_artifacts_writeback as writeback,
    indexes_generate,
)
from scripts.agent_assets import (
    routes_distribution_generate as dist_routes,
    routes_repository_generate as repo_routes,
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


def _run_real_index_generators(repo: Path) -> None:
    for name in ("docs", "catalog"):
        indexes_generate.sync_indexes(
            replace(indexes_generate.PRESETS[name], root=repo / name)
        )


def _matches_workflow_path_patterns(path: str, patterns: list[str]) -> bool:
    posix = PurePosixPath(path)
    matched = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw = pattern[1:] if negated else pattern
        if posix.full_match(raw):
            matched = not negated
    return matched


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
        ("docs\\INDEX.tsv", False),
        ("docs//INDEX.tsv", False),
        ("docs/\x00INDEX.tsv", False),
        ("docs/\udc80INDEX.tsv", False),
        ("route/.jsonl", False),
        ("docs/INDEX.tsv/", False),
        (".git/config", False),
        (".github/workflows/generated-sync.yml", False),
        ("docs/guide.md", False),
    ],
)
def test_producer_allowed_generated_output_allowlist(path: str, expected: bool) -> None:
    assert writeback.is_allowed_generated_output(path) is expected


def test_package_payload_noop_and_cleanup_when_changed_becomes_false(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    out = tmp_path / "out"
    (out / "files" / "docs").mkdir(parents=True)
    (out / "files" / "docs" / "stale.txt").write_text("old", encoding="utf-8")

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


def test_package_payload_collects_non_ascii_and_deletions_without_files_dir(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    (repo / "docs" / "안내").mkdir(parents=True)
    sub_index = repo / "docs" / "안내" / "INDEX.tsv"
    sub_index.write_text("path\tdescription\n", encoding="utf-8")
    (repo / "route").mkdir()
    extra_route = repo / "route" / "skills.jsonl"
    extra_route.write_text('{"name":"demo"}\n', encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "with sub index and route")
    head_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # 비핵심 생성 파일 삭제만 발생한 경우 files/ 없이 deleted만 패키징한다
    extra_route.unlink()
    out_del = tmp_path / "out_del"
    del_meta = producer.package_payload(
        root=repo,
        output_dir=out_del,
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=head_sha,
        producer_run_id=700,
    )
    assert del_meta["changed"] is True
    assert del_meta["files"] == []
    assert del_meta["deleted"] == ["route/skills.jsonl"]
    assert not (out_del / "files").exists()

    # 한글 경로 수정 + 삭제 동시 검증
    _git(repo, "checkout", "--", "route/skills.jsonl")
    sub_index.write_text("path\tdescription\ndocs/a.md\t설명\n", encoding="utf-8")
    extra_route.unlink()
    out = tmp_path / "out"
    meta = producer.package_payload(
        root=repo,
        output_dir=out,
        repository_id=123,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/demo",
        head_sha=head_sha,
        producer_run_id=789,
    )
    assert meta["changed"] is True
    assert meta["deleted"] == ["route/skills.jsonl"]
    assert [item["path"] for item in meta["files"]] == ["docs/안내/INDEX.tsv"]
    staged_file = out / "files" / "docs" / "안내" / "INDEX.tsv"
    raw = staged_file.read_bytes()
    assert len(raw) == meta["files"][0]["size"]
    assert hashlib.sha256(raw).hexdigest() == meta["files"][0]["sha256"]


def test_collect_rejects_ignored_new_output_from_canonical_generator(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    (repo / ".gitignore").write_text(
        "/docs/development/INDEX.tsv\n/.venv/\n", encoding="utf-8"
    )
    development = repo / "docs" / "development"
    development.mkdir()
    (development / "guide.md").write_text(
        "---\ndescription: Guide\n---\n\n# Guide\n", encoding="utf-8"
    )
    _git(repo, "add", ".gitignore", "docs/development/guide.md")
    _git(repo, "commit", "-qm", "add documentation source")

    unrelated = repo / ".venv" / "docs" / "INDEX.tsv"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("ignored tool state\n", encoding="utf-8")
    assert producer.collect_generated_changes(repo) == ([], [])

    config = replace(indexes_generate.PRESETS["docs"], root=repo / "docs")
    indexes_generate.sync_indexes(config)
    assert (development / "INDEX.tsv").is_file()

    with pytest.raises(producer.ProducerError, match="docs/development/INDEX.tsv"):
        producer.collect_generated_changes(repo)


def test_real_generators_and_package_cover_t02_t03_t04_t05_and_t11(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Author")
    _git(repo, "config", "user.email", "author@example.com")
    _git(repo, "checkout", "-b", "feat/real-sync")

    # T02(docs) + T03(catalog) + T04(distribution & repository routes) 입력 구성
    (repo / "docs").mkdir()
    (repo / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")
    (repo / "docs" / "guide.md").write_text(
        "---\ndescription: 가이드 문서\n---\n\n# Guide\n", encoding="utf-8"
    )
    (repo / "catalog").mkdir()
    (repo / "catalog" / "README.md").write_text("# Catalog\n", encoding="utf-8")
    (repo / "catalog" / "skills.json").write_text("[]\n", encoding="utf-8")

    skills_dir = repo / "src" / "rulesync" / ".rulesync" / "skills" / "demo-skill"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text(
        "---\nname: demo-skill\ndescription: 데모 스킬\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    subagents_dir = repo / "src" / "rulesync" / ".rulesync" / "subagents"
    subagents_dir.mkdir(parents=True)
    (subagents_dir / "reviewer.md").write_text(
        "---\nname: reviewer\ndescription: 리뷰어\n---\n\n# Reviewer\n",
        encoding="utf-8",
    )

    _run_real_index_generators(repo)
    route_dir = repo / "route"
    route_dir.mkdir()
    (route_dir / "skills.jsonl").write_text(
        dist_routes.render_skill_route(skills_dir.parent), encoding="utf-8"
    )
    (route_dir / "subagents.jsonl").write_text(
        dist_routes.render_subagent_route(subagents_dir), encoding="utf-8"
    )
    (route_dir / "routes.jsonl").write_text(
        dist_routes.render_routes(
            [
                {
                    "name": "skills",
                    "description": "skills",
                    "source": "https://example.com/skills.jsonl",
                }
            ]
        ),
        encoding="utf-8",
    )
    local_route_outputs = repo_routes.build_outputs(
        repo_routes.load_skill_rows(
            {"demo-skill": "https://example.com/SKILL.md"},
            loader=lambda _: "---\nname: demo-skill\ndescription: 데모\n---\n",
        ),
        {},
    )
    agents_route_dir = repo / ".agents" / "route"
    agents_route_dir.mkdir(parents=True)
    for orig_path, content in local_route_outputs.items():
        (agents_route_dir / orig_path.name).write_text(content, encoding="utf-8")

    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "canonical baseline")
    baseline_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # T01: 변경 없는 상태 재실행 시 changed=False
    _run_real_index_generators(repo)
    noop_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out_noop",
        repository_id=1,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/real-sync",
        head_sha=baseline_sha,
        producer_run_id=100,
    )
    assert noop_meta["changed"] is False

    # T02 + T03 + T04: docs/catalog/skill 추가 커밋 후 생성기 -> package 검증
    (repo / "docs" / "new-guide.md").write_text(
        "---\ndescription: 신규 가이드\n---\n", encoding="utf-8"
    )
    (repo / "catalog" / "plugins.json").write_text("[]\n", encoding="utf-8")
    new_skill = repo / "src" / "rulesync" / ".rulesync" / "skills" / "extra"
    new_skill.mkdir()
    (new_skill / "SKILL.md").write_text(
        "---\nname: extra\ndescription: 추가 스킬\n---\n", encoding="utf-8"
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "source updates")
    source_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _run_real_index_generators(repo)
    (route_dir / "skills.jsonl").write_text(
        dist_routes.render_skill_route(skills_dir.parent), encoding="utf-8"
    )
    update_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out_update",
        repository_id=1,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/real-sync",
        head_sha=source_sha,
        producer_run_id=101,
    )
    assert update_meta["changed"] is True
    assert [f["path"] for f in update_meta["files"]] == [
        "catalog/INDEX.tsv",
        "docs/INDEX.tsv",
        "route/skills.jsonl",
    ]

    # T11: 봇 커밋 반영 후 재진입 실행은 changed=False no-op
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "chore(generated): sync indexes and routes")
    bot_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _run_real_index_generators(repo)
    (route_dir / "skills.jsonl").write_text(
        dist_routes.render_skill_route(skills_dir.parent), encoding="utf-8"
    )
    reentry_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out_reentry",
        repository_id=1,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/real-sync",
        head_sha=bot_sha,
        producer_run_id=102,
    )
    assert reentry_meta["changed"] is False

    # T05: API 커밋으로 docs/INDEX.tsv 삭제 + catalog/INDEX.tsv 훼손 시 복구 검증
    (repo / "docs" / "INDEX.tsv").unlink()
    (repo / "catalog" / "INDEX.tsv").write_text("corrupted\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "api corrupt outputs")
    corrupt_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _run_real_index_generators(repo)
    recover_meta = producer.package_payload(
        root=repo,
        output_dir=tmp_path / "out_recover",
        repository_id=1,
        repository_full_name="mols3131d/mols-agent-assets",
        branch="feat/real-sync",
        head_sha=corrupt_sha,
        producer_run_id=103,
    )
    assert recover_meta["changed"] is True
    assert [f["path"] for f in recover_meta["files"]] == [
        "catalog/INDEX.tsv",
        "docs/INDEX.tsv",
    ]


def test_package_payload_rejects_bad_changes_symlinks_and_bad_args(
    monkeypatch: pytest.MonkeyPatch,
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

    _git(repo, "checkout", "--", "docs/INDEX.tsv")

    # boolean/잘못된 repository/head_sha 불일치 거부
    with pytest.raises(producer.ProducerError):
        producer.package_payload(
            root=repo,
            output_dir=tmp_path / "out_bool",
            repository_id=True,
            repository_full_name="mols3131d/mols-agent-assets",
            branch="feat/demo",
            head_sha=head_sha,
            producer_run_id=1,
        )
    with pytest.raises(producer.ProducerError):
        producer.package_payload(
            root=repo,
            output_dir=tmp_path / "out_repo",
            repository_id=123,
            repository_full_name="invalid/",
            branch="feat/demo",
            head_sha=head_sha,
            producer_run_id=1,
        )
    with pytest.raises(producer.ProducerError, match="기대 SHA"):
        producer.package_payload(
            root=repo,
            output_dir=tmp_path / "out_sha",
            repository_id=123,
            repository_full_name="mols3131d/mols-agent-assets",
            branch="feat/demo",
            head_sha="0" * 40,
            producer_run_id=1,
        )

    # 생성 출력 symlink 거부
    (repo / "docs" / "INDEX.tsv").write_text("changed\n", encoding="utf-8")
    real_lstat = Path.lstat
    target = repo / "docs" / "INDEX.tsv"

    class _FakeSymlinkStat:
        st_mode = stat.S_IFLNK | 0o777

    monkeypatch.setattr(
        Path,
        "lstat",
        lambda path: _FakeSymlinkStat() if path == target else real_lstat(path),
    )
    with pytest.raises(producer.ProducerError, match="일반 파일이 아닙니다"):
        producer.collect_generated_changes(repo)


def test_producer_cli_and_env_provenance_validation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    (repo / ".agents" / "route" / "all.jsonl").write_text(
        '{"name":"updated"}\n', encoding="utf-8"
    )

    event_file = tmp_path / "event.json"
    event = {
        "deleted": False,
        "ref": "refs/heads/feat/demo",
        "after": head_sha,
        "repository": {"id": 555, "full_name": "mols3131d/mols-agent-assets"},
    }
    event_file.write_text(json.dumps(event), encoding="utf-8")
    out_dir = tmp_path / "artifact"

    monkeypatch.setenv("GITHUB_EVENT_NAME", "push")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_file))
    monkeypatch.setenv("GITHUB_REPOSITORY", "mols3131d/mols-agent-assets")
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "555")
    monkeypatch.setenv("GITHUB_REF", "refs/heads/feat/demo")
    monkeypatch.setenv("GITHUB_SHA", head_sha)
    monkeypatch.setenv("GITHUB_RUN_ID", "901")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")

    rc = producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
    assert rc == 0
    assert json.loads((out_dir / "metadata.json").read_text(encoding="utf-8"))[
        "changed"
    ]
    assert (out_dir / "files" / ".agents" / "route" / "all.jsonl").is_file()

    # 잘못된 GITHUB_REPOSITORY_ID가 조용히 fallback되지 않고 실패해야 한다
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "invalid")
    assert (
        producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
        == 1
    )
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "999")
    assert (
        producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
        == 1
    )

    # deleted=true 또는 malformed event JSON도 실패해야 한다
    monkeypatch.setenv("GITHUB_REPOSITORY_ID", "555")
    event_file.write_text(json.dumps({"deleted": True}), encoding="utf-8")
    assert (
        producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
        == 1
    )

    for event_update in (
        {"repository": {"id": 555.0, "full_name": "mols3131d/mols-agent-assets"}},
        {"ref": None},
        {"after": None},
    ):
        event_file.write_text(json.dumps(event | event_update), encoding="utf-8")
        assert (
            producer.main(
                ["package", "--root", str(repo), "--output-dir", str(out_dir)]
            )
            == 1
        )
    event_file.write_text("{bad json", encoding="utf-8")
    assert (
        producer.main(["package", "--root", str(repo), "--output-dir", str(out_dir)])
        == 1
    )


def test_package_rejects_source_tree_output_and_oversized_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "repo"
    head_sha = _init_repo(repo)
    source = repo / "docs" / "INDEX.tsv"
    source.write_bytes(b"updated")

    options = {
        "root": repo,
        "repository_id": 123,
        "repository_full_name": "mols3131d/mols-agent-assets",
        "branch": "feat/demo",
        "head_sha": head_sha,
        "producer_run_id": 1,
    }
    with pytest.raises(producer.ProducerError, match="별도 디렉터리"):
        producer.package_payload(output_dir=tmp_path, **options)
    assert source.read_bytes() == b"updated"

    monkeypatch.setattr(writeback, "MAX_FILE_BYTES", 3)
    with pytest.raises(producer.ProducerError, match="크기가 artifact 제한"):
        producer.package_payload(output_dir=tmp_path / "payload", **options)


def test_collect_rejects_linked_generated_parent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    (repo / "docs" / "INDEX.tsv").write_bytes(b"updated")
    real_lstat = Path.lstat
    linked_dir = repo / "docs"

    def lstat(path: Path):
        if path == linked_dir:
            return os.stat_result((stat.S_IFLNK, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        return real_lstat(path)

    monkeypatch.setattr(Path, "lstat", lstat)
    with pytest.raises(producer.ProducerError, match="상위 경로가 일반 디렉터리"):
        producer.collect_generated_changes(repo)


def test_generated_sync_workflow_is_read_only_and_covers_projection_inputs() -> None:
    raw = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.safe_load(raw)
    on_section = workflow.get("on", workflow.get(True))

    assert workflow["name"] == "Sync Generated Artifacts"
    assert workflow["permissions"] == {"contents": "read"}
    assert "workflow_dispatch" not in on_section
    assert "main" in on_section["push"]["branches-ignore"]

    sync_job = workflow["jobs"]["sync"]
    assert "permissions" not in sync_job
    assert "environment" not in sync_job
    assert "secrets." not in yaml.safe_dump(workflow)
    assert "git push" not in raw
    assert "gh auth setup-git" not in raw

    steps = sync_job["steps"]
    for step in steps:
        uses = step.get("uses")
        if uses:
            sha = uses.split("@", 1)[1].split()[0]
            assert writeback.HEX_SHA_RE.fullmatch(sha), uses
            if uses.startswith("actions/checkout@"):
                assert step["with"]["persist-credentials"] is False
            if uses.startswith("actions/upload-artifact@"):
                assert step["with"]["name"] == writeback.ARTIFACT_NAME
                assert step["with"]["include-hidden-files"] is True
                assert step["with"]["if-no-files-found"] == "error"
                assert step["with"]["overwrite"] is True
        run_cmd = step.get("run", "")
        assert "${{" not in run_cmd, step.get("name")

    run_commands = [step.get("run", "") for step in steps]
    assert any("scripts.generated_artifacts sync" in cmd for cmd in run_commands)
    assert any(
        "scripts.generated_artifacts validate --all" in cmd for cmd in run_commands
    )
    assert any(
        "scripts.generated_artifacts_producer package" in cmd for cmd in run_commands
    )

    patterns = on_section["push"]["paths"]
    for input_path in (
        ".github/workflows/generated-sync.yml",
        "pyproject.toml",
        "uv.lock",
        "scripts/generated_artifacts.py",
    ):
        assert _matches_workflow_path_patterns(input_path, patterns), input_path
    maintenance_script = (
        "src/rulesync/.rulesync/skills/"
        "mols-markdown-maintenance/scripts/generate_index.py"
    )
    canonical_paths = [
        "docs/guide.md",
        "docs/INDEX.tsv",
        "docs/development/INDEX.tsv",
        "catalog/skills.json",
        "catalog/patterns/example.md",
        "catalog/INDEX.tsv",
        "src/rulesync/.rulesync/skills/example/SKILL.md",
        maintenance_script,
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
