from __future__ import annotations

import subprocess

import pytest

from scripts.generation import sync_generated_artifacts as sync


def _run_git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/guide.md", True),
        ("docs/references/README.md", True),
        ("docs/references/index.md", True),
        ("docs/AGENTS.md", False),
        ("docs/references/.private.md", False),
        ("docs/references/__system__.md", False),
        ("docs/references/INDEX.md", False),
        ("scripts/generation/generate_docs_indexes.py", True),
        (
            "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
            "scripts/generate_index.py",
            True,
        ),
        ("README.md", False),
    ],
)
def test_docs_index_source_matching(path, expected):
    assert sync._is_docs_index_source(path) is expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("src/rulesync/.rulesync/skills/example/SKILL.md", True),
        ("src/rulesync/.rulesync/skills/example/references/guide.md", False),
        ("src/rulesync/.rulesync/subagents/review.md", True),
        ("src/rulesync/.rulesync/subagents/references/guide.md", False),
        ("scripts/generation/generate_distribution_routes.py", True),
        ("rulesync.lock", False),
    ],
)
def test_distribution_route_source_matching(path, expected):
    assert sync._is_distribution_route_source(path) is expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("rulesync.lock", True),
        ("rulesync.jsonc", True),
        ("skills-lock.json", True),
        (".agents/route/families.json", True),
        ("scripts/generation/generate_repository_routes.py", True),
        ("src/rulesync/.rulesync/skills/example/SKILL.md", False),
    ],
)
def test_repository_route_source_matching(path, expected):
    assert sync._is_repository_route_source(path) is expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/guide.md", ["docs-indexes"]),
        (
            "src/rulesync/.rulesync/skills/example/SKILL.md",
            ["distribution-routes"],
        ),
        (
            "src/rulesync/.rulesync/subagents/review.md",
            ["distribution-routes"],
        ),
        ("skills-lock.json", ["repository-routes"]),
    ],
)
def test_source_path_selects_only_its_projection_owner(path, expected):
    assert [projection.name for projection in sync.select_projections({path})] == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/INDEX.tsv", ["docs-indexes"]),
        ("route/routes.jsonl", ["distribution-routes"]),
        ("route/skills.jsonl", ["distribution-routes"]),
        ("route/subagents.jsonl", ["distribution-routes"]),
        (".agents/route/routes.jsonl", ["repository-routes"]),
    ],
)
def test_generated_output_selects_its_projection_owner(path, expected):
    assert [projection.name for projection in sync.select_projections({path})] == expected


def test_sync_staged_is_noop_when_no_projection_is_affected(monkeypatch, tmp_path):
    monkeypatch.setattr(sync, "staged_paths", lambda root: {"README.md"})

    def fail_if_called(root):
        raise AssertionError("dirty state should not be inspected for an irrelevant commit")

    monkeypatch.setattr(sync, "dirty_worktree_paths", fail_if_called)

    assert sync.sync_staged(tmp_path) == ()


def test_conflicting_paths_are_scoped_to_affected_projection():
    affected = sync.select_projections({"docs/guide.md"})

    assert sync.conflicting_paths(
        {"docs/other.md", "src/rulesync/.rulesync/skills/foo/SKILL.md"},
        affected,
    ) == {"docs-indexes": ["docs/other.md"]}


def test_sync_staged_generates_then_stages_affected_projection(
    monkeypatch,
    tmp_path,
):
    events = []
    projection = sync.Projection(
        name="example",
        source_matches=lambda path: path == "source.md",
        output_matches=lambda path: path == "generated.txt",
        generate=lambda: events.append("generate"),
    )
    monkeypatch.setattr(sync, "staged_paths", lambda root: {"source.md"})
    monkeypatch.setattr(sync, "dirty_worktree_paths", lambda root: set())
    monkeypatch.setattr(
        sync,
        "_stage_projection_outputs",
        lambda projection, root: events.append(f"stage:{projection.name}"),
    )

    assert sync.sync_staged(tmp_path, (projection,)) == ("example",)
    assert events == ["generate", "stage:example"]


def test_sync_staged_delays_staging_until_all_generators_succeed(
    monkeypatch,
    tmp_path,
):
    events = []

    def fail():
        events.append("generate:second")
        raise RuntimeError("boom")

    projections = (
        sync.Projection(
            name="first",
            source_matches=lambda path: path == "first.md",
            output_matches=lambda path: path == "first.txt",
            generate=lambda: events.append("generate:first"),
        ),
        sync.Projection(
            name="second",
            source_matches=lambda path: path == "second.md",
            output_matches=lambda path: path == "second.txt",
            generate=fail,
        ),
    )
    monkeypatch.setattr(
        sync,
        "staged_paths",
        lambda root: {"first.md", "second.md"},
    )
    monkeypatch.setattr(sync, "dirty_worktree_paths", lambda root: set())
    monkeypatch.setattr(
        sync,
        "_stage_projection_outputs",
        lambda projection, root: events.append(f"stage:{projection.name}"),
    )

    with pytest.raises(RuntimeError, match="boom"):
        sync.sync_staged(tmp_path, projections)

    assert events == ["generate:first", "generate:second"]


def test_sync_staged_refuses_related_unstaged_changes_before_generation(
    monkeypatch,
    tmp_path,
):
    events = []
    projection = sync.Projection(
        name="example",
        source_matches=lambda path: path.endswith(".md"),
        output_matches=lambda path: path == "generated.txt",
        generate=lambda: events.append("generate"),
    )
    monkeypatch.setattr(sync, "staged_paths", lambda root: {"source.md"})
    monkeypatch.setattr(
        sync,
        "dirty_worktree_paths",
        lambda root: {"other.md"},
    )

    with pytest.raises(sync.GeneratedArtifactSyncError, match="other.md"):
        sync.sync_staged(tmp_path, (projection,))

    assert events == []


def test_git_state_detects_partial_staging_and_untracked_sources(tmp_path):
    _run_git(tmp_path, "init", "-q")
    _run_git(tmp_path, "config", "user.name", "Test")
    _run_git(tmp_path, "config", "user.email", "test@example.com")

    docs = tmp_path / "docs"
    docs.mkdir()
    guide = docs / "guide.md"
    guide.write_text("initial\n", encoding="utf-8")
    _run_git(tmp_path, "add", "docs/guide.md")
    _run_git(tmp_path, "commit", "-qm", "initial")

    guide.write_text("staged\n", encoding="utf-8")
    _run_git(tmp_path, "add", "docs/guide.md")
    guide.write_text("unstaged\n", encoding="utf-8")
    (docs / "new.md").write_text("new\n", encoding="utf-8")

    assert sync.staged_paths(tmp_path) == {"docs/guide.md"}
    assert sync.dirty_worktree_paths(tmp_path) == {
        "docs/guide.md",
        "docs/new.md",
    }


def test_stage_projection_outputs_handles_new_modified_and_deleted_outputs(
    tmp_path,
):
    _run_git(tmp_path, "init", "-q")
    _run_git(tmp_path, "config", "user.name", "Test")
    _run_git(tmp_path, "config", "user.email", "test@example.com")

    docs = tmp_path / "docs"
    stale = docs / "stale" / "INDEX.tsv"
    stale.parent.mkdir(parents=True)
    index = docs / "INDEX.tsv"
    index.write_text("old\n", encoding="utf-8")
    stale.write_text("stale\n", encoding="utf-8")
    note = tmp_path / "note.txt"
    note.write_text("old\n", encoding="utf-8")
    _run_git(tmp_path, "add", ".")
    _run_git(tmp_path, "commit", "-qm", "initial")

    index.write_text("new\n", encoding="utf-8")
    stale.unlink()
    new_index = docs / "new" / "INDEX.tsv"
    new_index.parent.mkdir()
    new_index.write_text("new\n", encoding="utf-8")
    note.write_text("new\n", encoding="utf-8")

    projection = sync.Projection(
        name="docs-indexes",
        source_matches=lambda path: False,
        output_matches=sync._is_docs_index_output,
        generate=lambda: None,
    )
    sync._stage_projection_outputs(projection, tmp_path)

    staged = _run_git(
        tmp_path,
        "diff",
        "--cached",
        "--name-only",
    ).stdout.splitlines()
    assert staged == [
        "docs/INDEX.tsv",
        "docs/new/INDEX.tsv",
        "docs/stale/INDEX.tsv",
    ]
