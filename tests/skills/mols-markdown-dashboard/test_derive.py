from __future__ import annotations

from typing import Any

from mols_dashboard.derive import aggregate_dashboard, progress_bar
from mols_dashboard.loader import parse_dashboard
from mols_dashboard.model import Progress, VerificationStatus


def _base_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": 1,
        "dashboard": {
            "level": "project",
            "title": "Demo",
            "snapshot": "v1",
            "current_focus": "Focus",
        },
        "items": items,
    }


def test_progress_bar_is_conservative_and_exact() -> None:
    assert progress_bar(Progress(3, 4)) == "███████░░░ 3/4"
    assert progress_bar(Progress(4, 4)) == "██████████ 4/4"


def test_aggregate_sums_counts_instead_of_averaging_percentages() -> None:
    dashboard = parse_dashboard(
        _base_dashboard(
            [
                {
                    "name": "Small",
                    "implementation": {
                        "status": "in_progress",
                        "progress": "1/2",
                        "gaps": ["x"],
                    },
                    "verification": {
                        "status": "partial",
                        "progress": "1/2",
                        "gaps": ["x"],
                    },
                },
                {
                    "name": "Large",
                    "implementation": {
                        "status": "implemented",
                        "progress": "8/8",
                    },
                    "verification": {
                        "status": "failing",
                        "progress": "8/8",
                        "gaps": [{"state": "failing", "text": "x"}],
                    },
                },
            ]
        )
    )

    total = aggregate_dashboard(dashboard)

    assert total.implementation_progress == Progress(9, 10)
    assert total.verification_progress == Progress(9, 10)
    assert total.verification_status is VerificationStatus.FAILING


def test_failing_aggregate_outranks_blocked() -> None:
    dashboard = parse_dashboard(
        _base_dashboard(
            [
                {
                    "name": "Failing",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "failing",
                        "progress": "1/1",
                        "gaps": [{"state": "failing", "text": "failure"}],
                    },
                },
                {
                    "name": "Blocked",
                    "implementation": {
                        "status": "implemented",
                        "progress": "1/1",
                    },
                    "verification": {
                        "status": "blocked",
                        "progress": "0/1",
                        "gaps": [{"state": "blocked", "text": "blocked"}],
                    },
                },
            ]
        )
    )

    assert aggregate_dashboard(dashboard).verification_status is VerificationStatus.FAILING
