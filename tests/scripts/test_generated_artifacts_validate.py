from __future__ import annotations

from scripts import generated_artifacts_sync as sync
from scripts import generated_artifacts_validate as validate


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


def test_select_for_validation_uses_projection_registry():
    selected = validate.select_for_validation({"skills-lock.json"})

    assert [projection.name for projection in selected] == ["repository-routes"]


def test_select_for_validation_limits_unknown_impact_to_local_projections():
    selected = validate.select_for_validation(None, local_only=True)

    assert [projection.name for projection in selected] == [
        "docs-indexes",
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
    assert "mise run generated-sync" in captured.err


def test_validate_noop_when_no_projection_is_affected(capsys):
    assert validate.validate(()) == 0
    assert capsys.readouterr().out == "No generated projections affected.\n"
