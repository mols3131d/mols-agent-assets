from __future__ import annotations

import pytest

from scripts import generated_artifacts as cli
from scripts import generated_artifacts_sync as sync
from scripts import generated_artifacts_validate as validation


def test_sync_generates_selected_outputs(monkeypatch, capsys):
    monkeypatch.setattr(sync, "sync_all", lambda: ("docs-indexes",))
    assert cli.main(["sync"]) == 0
    assert capsys.readouterr().out == "generated: docs-indexes\n"


def test_sync_staged_is_explicit(monkeypatch):
    calls: list[str] = []
    monkeypatch.setattr(sync, "sync_staged", lambda: calls.append("staged") or ())
    assert cli.main(["sync", "--staged"]) == 0
    assert calls == ["staged"]


def test_sync_reports_conflict_without_staging(monkeypatch, capsys):
    def reject():
        raise sync.GeneratedArtifactSyncError("unstaged source")

    monkeypatch.setattr(sync, "sync_staged", reject)
    assert cli.main(["sync", "--staged"]) == 1
    assert "unstaged source" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("args", "local_only"),
    [
        (["validate"], False),
        (["validate", "--all"], False),
        (["validate", "--local-only", "--all"], True),
    ],
)
def test_validate_scope(monkeypatch, args, local_only):
    selected = []

    def select(paths, *, local_only=False):
        selected.append((paths, local_only))
        return ()

    monkeypatch.setattr(validation, "select_for_validation", select)
    monkeypatch.setattr(validation, "validate", lambda _: 0)
    assert cli.main(args) == 0
    assert selected == [(None, local_only)]


def test_validate_changed_from_and_exit_code(monkeypatch):
    seen = []

    def select(paths, *, local_only=False):
        seen.append((paths, local_only))
        return ()

    monkeypatch.setattr(validation, "changed_paths", lambda rev: {"docs/a.md"})
    monkeypatch.setattr(validation, "select_for_validation", select)
    monkeypatch.setattr(validation, "validate", lambda _: 1)
    assert cli.main(["validate", "--changed-from", "HEAD~1"]) == 1
    assert seen == [({"docs/a.md"}, False)]


def test_validate_unknown_impact_falls_back_to_all(monkeypatch, capsys):
    selection = []
    monkeypatch.setattr(validation, "changed_paths", lambda rev: None)

    def select(paths, *, local_only=False):
        selection.append(paths)
        return ()

    monkeypatch.setattr(validation, "select_for_validation", select)
    monkeypatch.setattr(validation, "validate", lambda _: 0)
    assert cli.main(["validate", "--changed-from", "missing"]) == 0
    assert selection == [None]
    assert "validating all projections" in capsys.readouterr().err


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["sync", "--all"],
        ["validate", "--staged"],
        ["validate", "--all", "--changed-from", "HEAD~1"],
    ],
)
def test_invalid_arguments_are_rejected(args):
    with pytest.raises(SystemExit) as error:
        cli.main(args)
    assert error.value.code == 2
