from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import floor

from .model import Dashboard, ImplementationStatus, Progress, VerificationStatus

_BAR_WIDTH = 10


@dataclass(frozen=True, slots=True)
class Aggregate:
    implementation_status: ImplementationStatus
    implementation_progress: Progress
    verification_status: VerificationStatus
    verification_progress: Progress


@dataclass(frozen=True, slots=True)
class GapRow:
    name: str
    number: int
    text: str


def progress_bar(progress: Progress, width: int = _BAR_WIDTH) -> str:
    """Render a conservative bar without visually overstating partial progress."""
    filled = width if progress.completed == progress.total else floor(progress.ratio * width)
    return f"{'█' * filled}{'░' * (width - filled)} {progress.completed}/{progress.total}"


def aggregate_dashboard(dashboard: Dashboard) -> Aggregate:
    implementation = _sum_progress(
        item.implementation_progress for item in dashboard.items
    )
    verification = _sum_progress(item.verification_progress for item in dashboard.items)
    return Aggregate(
        implementation_status=_aggregate_implementation_status(
            tuple(item.implementation_status for item in dashboard.items)
        ),
        implementation_progress=implementation,
        verification_status=_aggregate_verification_status(
            tuple(item.verification_status for item in dashboard.items)
        ),
        verification_progress=verification,
    )


def implementation_gap_rows(dashboard: Dashboard) -> tuple[GapRow, ...]:
    return tuple(
        GapRow(name=item.name, number=number, text=gap)
        for item in dashboard.items
        for number, gap in enumerate(item.implementation_gaps, start=1)
    )


def verification_gap_rows(dashboard: Dashboard) -> tuple[GapRow, ...]:
    return tuple(
        GapRow(name=item.name, number=number, text=gap.display)
        for item in dashboard.items
        for number, gap in enumerate(item.verification_gaps, start=1)
    )


def _sum_progress(progresses: Iterable[Progress]) -> Progress:
    values = tuple(progresses)
    return Progress(
        completed=sum(progress.completed for progress in values),
        total=sum(progress.total for progress in values),
    )


def _aggregate_implementation_status(
    statuses: tuple[ImplementationStatus, ...],
) -> ImplementationStatus:
    if ImplementationStatus.BLOCKED in statuses:
        return ImplementationStatus.BLOCKED
    if ImplementationStatus.UNKNOWN in statuses:
        return ImplementationStatus.UNKNOWN
    if all(status is ImplementationStatus.IMPLEMENTED for status in statuses):
        return ImplementationStatus.IMPLEMENTED
    if all(status is ImplementationStatus.NOT_STARTED for status in statuses):
        return ImplementationStatus.NOT_STARTED
    if all(
        status in {ImplementationStatus.NOT_STARTED, ImplementationStatus.PLANNED}
        for status in statuses
    ):
        return ImplementationStatus.PLANNED
    return ImplementationStatus.IN_PROGRESS


def _aggregate_verification_status(
    statuses: tuple[VerificationStatus, ...],
) -> VerificationStatus:
    if VerificationStatus.FAILING in statuses:
        return VerificationStatus.FAILING
    if VerificationStatus.BLOCKED in statuses:
        return VerificationStatus.BLOCKED
    if VerificationStatus.UNKNOWN in statuses:
        return VerificationStatus.UNKNOWN
    if all(status is VerificationStatus.PASSING for status in statuses):
        return VerificationStatus.PASSING
    if all(status is VerificationStatus.UNVERIFIED for status in statuses):
        return VerificationStatus.UNVERIFIED
    return VerificationStatus.PARTIAL
