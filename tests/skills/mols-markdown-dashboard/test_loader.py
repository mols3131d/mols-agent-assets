from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from mols_dashboard.loader import DashboardInputError, parse_dashboard
from mols_dashboard.model import DashboardLevel, VerificationGapState


def valid_raw() -> dict[str, Any]:
    return {
        "version": 1,
        "dashboard": {
            "level": "domain",
            "title": "Demo",
            "snapshot": "2026-08-03",
            "current_focus": "Close gaps",
        },
        "items": [
            {
                "name": "Capability A",
                "implementation": {
                    "status": "in_progress",
                    "progress": "1/2",
                    "gaps": ["Finish A"],
                },
                "verification": {
                    "status": "failing",
                    "progress": {"completed": 1, "total": 2},
                    "gaps": [
                        {"state": "failing", "text": "A fails"},
                        {"state": "unverified", "text": "B is unverified"},
                    ],
                },
            }
        ],
    }


def test_parse_compact_and_mapping_progress() -> None:
    dashboard = parse_dashboard(valid_raw())

    assert dashboard.level is DashboardLevel.DOMAIN
    assert dashboard.level.row_label == "Capability"
    assert dashboard.items[0].implementation_progress.completed == 1
    assert dashboard.items[0].verification_progress.total == 2
    assert dashboard.items[0].verification_gaps[0].state is VerificationGapState.FAILING


def test_rejects_duplicate_item_names_case_insensitively() -> None:
    raw = valid_raw()
    raw["items"].append({**deepcopy(raw["items"][0]), "name": "capability a"})

    with pytest.raises(DashboardInputError, match="unique"):
        parse_dashboard(raw)


def test_rejects_invalid_progress() -> None:
    raw = valid_raw()
    raw["items"][0]["implementation"]["progress"] = "3/2"

    with pytest.raises(DashboardInputError, match="must not exceed"):
        parse_dashboard(raw)


def test_rejects_unknown_root_field() -> None:
    raw = valid_raw()
    raw["unexpected"] = True

    with pytest.raises(DashboardInputError, match="root contains unknown field"):
        parse_dashboard(raw)


def test_rejects_unknown_nested_field_with_path() -> None:
    raw = valid_raw()
    raw["items"][0]["verification"]["coverage"] = "1/2"

    with pytest.raises(
        DashboardInputError,
        match=r"items\[1\]\.verification contains unknown field",
    ):
        parse_dashboard(raw)


def test_rejects_multiline_dashboard_title() -> None:
    raw = valid_raw()
    raw["dashboard"]["title"] = "Line one\nLine two"

    with pytest.raises(DashboardInputError, match="single line"):
        parse_dashboard(raw)


def test_rejects_non_string_text_value() -> None:
    raw = valid_raw()
    raw["dashboard"]["title"] = 123

    with pytest.raises(DashboardInputError, match="dashboard.title must be a string"):
        parse_dashboard(raw)
