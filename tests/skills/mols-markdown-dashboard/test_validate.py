from __future__ import annotations

import sys
from collections.abc import Iterator
from types import SimpleNamespace
from typing import Any

import pytest

from mols_dashboard.loader import parse_dashboard
from mols_dashboard.validate import (
    DashboardValidationError,
    validate_dashboard_consistency,
    validate_markdown,
)


def heading_events(markdown: str) -> Iterator[dict[str, object]]:
    for line in markdown.splitlines():
        if line.startswith("# "):
            yield {"Start": {"Heading": {"level": 1}}}
            yield {"Text": line[2:]}
            yield {"End": {"Heading": 1}}
        elif line.startswith("## "):
            yield {"Start": {"Heading": {"level": 2}}}
            yield {"Text": line[3:]}
            yield {"End": {"Heading": 2}}


def _dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": 1,
        "dashboard": {
            "level": "domain",
            "title": "Demo",
            "snapshot": "v1",
            "current_focus": "Focus",
        },
        "items": items,
    }


def _progress_table() -> str:
    return (
        "| Capability | Implementation Status | Implementation Progress | "
        "Verification Status | Verification Progress |\n"
        "| --- | --- | --- | --- | --- |"
    )


def test_consistency_rejects_implemented_with_gap() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                        "gaps": ["still open"],
                    },
                    "verification": {
                        "status": "passing",
                        "progress": "1/1",
                    },
                }
            ]
        )
    )

    with pytest.raises(DashboardValidationError, match="must not contain"):
        validate_dashboard_consistency(dashboard)


def test_markdown_structure_validation() -> None:
    markdown = f"# Demo\n\n## Development Progress\n\n{_progress_table()}\n"

    validate_markdown(markdown, event_parser=heading_events)


def test_default_pyromark_boundary_uses_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "pyromark", SimpleNamespace(events=heading_events))
    markdown = f"# Demo\n\n## Development Progress\n\n{_progress_table()}\n"

    validate_markdown(markdown)


def test_failing_target_can_have_complete_progress_but_remain_a_gap() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "failing",
                        "progress": "2/2",
                        "gaps": [
                            {"state": "failing", "text": "Integration fails"}
                        ],
                    },
                }
            ]
        )
    )

    validate_dashboard_consistency(dashboard)


def test_unverified_gap_count_matches_targets_without_results() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "partial",
                        "progress": "1/3",
                        "gaps": ["Missing A"],
                    },
                }
            ]
        )
    )

    with pytest.raises(
        DashboardValidationError,
        match="gaps without current results",
    ):
        validate_dashboard_consistency(dashboard)


def test_partial_status_rejects_failing_gap() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "partial",
                        "progress": "1/1",
                        "gaps": [{"state": "failing", "text": "Currently fails"}],
                    },
                }
            ]
        )
    )

    with pytest.raises(DashboardValidationError, match="must use failing"):
        validate_dashboard_consistency(dashboard)


def test_blocked_status_rejects_failing_gap() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "blocked",
                        "progress": "1/2",
                        "gaps": [
                            {"state": "failing", "text": "Currently fails"},
                            {"state": "blocked", "text": "Cannot run B"},
                        ],
                    },
                }
            ]
        )
    )

    with pytest.raises(DashboardValidationError, match="must use failing"):
        validate_dashboard_consistency(dashboard)


def test_markdown_rejects_wrong_section_order() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "in_progress",
                        "progress": "0/1",
                        "gaps": ["missing"],
                    },
                    "verification": {
                        "status": "unverified",
                        "progress": "0/1",
                        "gaps": ["missing"],
                    },
                }
            ]
        )
    )
    markdown = (
        "# Demo\n\n"
        "## Verification Gaps\n\n"
        "## Development Progress\n\n"
        f"{_progress_table()}\n\n"
        "## Implementation Gaps\n"
    )

    with pytest.raises(DashboardValidationError, match="canonical order"):
        validate_markdown(markdown, dashboard=dashboard, event_parser=heading_events)


def test_unverified_status_rejects_blocked_gap() -> None:
    dashboard = parse_dashboard(
        _dashboard(
            [
                {
                    "name": "A",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "unverified",
                        "progress": "0/1",
                        "gaps": [{"state": "blocked", "text": "Cannot run"}],
                    },
                }
            ]
        )
    )

    with pytest.raises(DashboardValidationError, match="must use blocked"):
        validate_dashboard_consistency(dashboard)
