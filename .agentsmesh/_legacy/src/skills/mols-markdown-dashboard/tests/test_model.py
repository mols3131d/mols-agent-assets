from __future__ import annotations

import pytest

from mols_dashboard.model import (
    ImplementationStatus,
    VerificationGap,
    VerificationGapState,
    VerificationStatus,
)


@pytest.mark.parametrize(
    ("status", "display"),
    [
        (ImplementationStatus.NOT_STARTED, "⚪ Not Started"),
        (ImplementationStatus.PLANNED, "🔵 Planned"),
        (ImplementationStatus.IN_PROGRESS, "🟡 In Progress"),
        (ImplementationStatus.IMPLEMENTED, "🟢 Implemented"),
        (ImplementationStatus.BLOCKED, "🔴 Blocked"),
        (ImplementationStatus.UNKNOWN, "⚫ Unknown"),
    ],
)
def test_implementation_status_display(
    status: ImplementationStatus,
    display: str,
) -> None:
    assert status.display == display


@pytest.mark.parametrize(
    ("status", "display"),
    [
        (VerificationStatus.UNVERIFIED, "⚪ Unverified"),
        (VerificationStatus.PARTIAL, "🟡 Partial"),
        (VerificationStatus.PASSING, "🟢 Passing"),
        (VerificationStatus.FAILING, "🔴 Failing"),
        (VerificationStatus.BLOCKED, "🟠 Blocked"),
        (VerificationStatus.UNKNOWN, "⚫ Unknown"),
    ],
)
def test_verification_status_display(
    status: VerificationStatus,
    display: str,
) -> None:
    assert status.display == display


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (VerificationGapState.UNVERIFIED, "⚪ Missing evidence"),
        (VerificationGapState.FAILING, "🔴 Missing evidence"),
        (VerificationGapState.BLOCKED, "🟠 Missing evidence"),
        (VerificationGapState.MANUAL, "🟡 Missing evidence"),
    ],
)
def test_verification_gap_display(
    state: VerificationGapState,
    expected: str,
) -> None:
    assert VerificationGap(text="Missing evidence", state=state).display == expected
