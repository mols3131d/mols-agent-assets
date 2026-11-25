from __future__ import annotations

import subprocess

import pytest

from scripts import (
    generated_artifacts_sync as sync,
    generated_artifacts_validate as validate,
)


def test_compare_outputs_reports_missing_outdated_and_stale(tmp_path):
    current = tmp_path / "route" / "current.jsonl"
    outdated = tmp_path / "route" / "outdated.jsonl"
    stale = tmp_path / "route" / "stale.jsonl"
    current.parent.mkdir()
    current.write_text("current\n", encoding="utf-8")
    outdated.write_text("old\n", encoding="utf-8")
    stale.write_text("stale\n", encoding="utf-8")

    expected = {
        current: "current\n",
        outdated: "new\n",
        tmp_path / "route" / "missing.jsonl": "missing\n",
    }

    assert validate.compare_outputs(
        expected,
        lambda path: path.startswith("route/") and path.endswith(".jsonl"),
        tmp_path,
    ) == [
        "missing: route/missing.jsonl",
        "outdated: route/outdated.jsonl",
        "stale: route/stale.jsonl",
    ]


def test_changed_paths_does_not_filter_git_change_types(monkeypatch, tmp_path):
    commands: list[list[str]] = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=b"source.txt\0",
            stderr=b"",
        )

    monkeypatch.setattr(validate.subprocess, "run", fake_run)

    assert validate.changed_paths("base", "head", tmp_path) == {"source.txt"}
    assert not any(argument.startswith("--diff-filter=") for argument in commands[0])


def test_select_for_validation_uses_projection_registry():
    selected = validate.select_for_validation({"skills-lock.json"})

    assert [projection.name for projection in selected] == ["repository-routes"]


@pytest.mark.parametrize(
    "path",
    [
        "scripts/generated_artifacts.py",
        "scripts/generated_artifacts_sync.py",
        "scripts/generated_artifacts_validate.py",
    ],
)
def test_common_validation_source_selects_all_projections(path):
    assert validate.select_for_validation({path}) == sync.PROJECTIONS


def test_common_source_respects_local_only_without_network():
    selected = validate.select_for_validation(
        {"scripts/generated_artifacts_sync.py"}, local_only=True
    )
    assert [projection.name for projection in selected] == [
        "docs-indexes",
        "catalog-indexes",
        "distribution-routes",
    ]


def test_select_for_validation_limits_unknown_impact_to_local_projections():
    selected = validate.select_for_validation(None, local_only=True)

    assert [projection.name for projection in selected] == [
        "docs-indexes",
        "catalog-indexes",
        "distribution-routes",
    ]


def test_select_for_validation_falls_back_to_all_when_impact_is_unknown():
    selected = validate.select_for_validation(None)

    assert selected == sync.PROJECTIONS


def test_validate_reports_drift_and_recovery(capsys):
    projection = sync.Projection(
        name="example",
        source_matches=lambda path: False,
        output_matches=lambda path: False,
        generate=lambda: None,
    )

    result = validate.validate(
        (projection,),
        {"example": lambda: ["outdated: generated.txt"]},
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "FAIL example" in captured.err
    assert "outdated: generated.txt" in captured.err
    assert "mise run generated sync" in captured.err


def test_validate_noop_when_no_projection_is_affected(capsys):
    assert validate.validate(()) == 0
    assert capsys.readouterr().out == "No generated projections affected.\n"


def test_compare_outputs_reports_first_line_difference_when_enabled(tmp_path):
    target = tmp_path / "docs" / "INDEX.tsv"
    target.parent.mkdir(parents=True)
    target.write_text("path\tdescription\na.md\tOld.\n", encoding="utf-8")

    drift = validate.compare_outputs(
        {target: "path\tdescription\na.md\tNew.\n"},
        lambda path: path == "docs/INDEX.tsv",
        tmp_path,
        show_first_difference=True,
    )

    assert drift == [
        "outdated: docs/INDEX.tsv",
        "line 2 current: a.md\tOld.",
        "line 2 expected: a.md\tNew.",
    ]


def test_check_docs_and_catalog_indexes_delegate_with_presets_and_diff(
    monkeypatch,
    tmp_path,
):
    from scripts.indexes_generate import IndexConfig

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "guide.md").write_text(
        "---\ndescription: New.\n---\n", encoding="utf-8"
    )
    (docs_dir / "INDEX.tsv").write_text(
        "path\tdescription\nguide.md\tOld.\n",
        encoding="utf-8",
    )

    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "skills.json").write_text("[]\n", encoding="utf-8")
    stale_catalog = catalog_dir / "obsolete" / "INDEX.tsv"
    stale_catalog.parent.mkdir()
    stale_catalog.write_text("stale\n", encoding="utf-8")

    presets = {
        "docs": IndexConfig(docs_dir, prune=True),
        "catalog": IndexConfig(
            catalog_dir,
            extensions=(".md", ".json"),
            prune=True,
        ),
    }
    monkeypatch.setattr(validate.indexes_generate, "PRESETS", presets)

    real_compare = validate.compare_outputs
    diff_flags: list[bool] = []

    def compare_with_tmp_root(
        expected,
        output_matches,
        root=tmp_path,
        *,
        show_first_difference=False,
    ):
        diff_flags.append(show_first_difference)
        return real_compare(
            expected,
            output_matches,
            tmp_path,
            show_first_difference=show_first_difference,
        )

    monkeypatch.setattr(validate, "compare_outputs", compare_with_tmp_root)

    assert validate.check_docs_indexes() == [
        "outdated: docs/INDEX.tsv",
        "line 2 current: guide.md\tOld.",
        "line 2 expected: guide.md\tNew.",
    ]
    assert validate.check_catalog_indexes() == [
        "missing: catalog/INDEX.tsv",
        "stale: catalog/obsolete/INDEX.tsv",
    ]
    assert diff_flags == [True, True]
