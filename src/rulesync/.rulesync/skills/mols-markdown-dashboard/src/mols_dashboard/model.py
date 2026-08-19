from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DashboardLevel(StrEnum):
    PROJECT = "project"
    DOMAIN = "domain"

    @property
    def row_label(self) -> str:
        return "Domain" if self is DashboardLevel.PROJECT else "Capability"


class ImplementationStatus(StrEnum):
    NOT_STARTED = "not_started"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"

    @property
    def display(self) -> str:
        match self:
            case ImplementationStatus.NOT_STARTED:
                return "⚪ Not Started"
            case ImplementationStatus.PLANNED:
                return "🔵 Planned"
            case ImplementationStatus.IN_PROGRESS:
                return "🟡 In Progress"
            case ImplementationStatus.IMPLEMENTED:
                return "🟢 Implemented"
            case ImplementationStatus.BLOCKED:
                return "🔴 Blocked"
            case ImplementationStatus.UNKNOWN:
                return "⚫ Unknown"
        raise AssertionError(f"unsupported implementation status: {self!r}")


class VerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    PARTIAL = "partial"
    PASSING = "passing"
    FAILING = "failing"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"

    @property
    def display(self) -> str:
        match self:
            case VerificationStatus.UNVERIFIED:
                return "⚪ Unverified"
            case VerificationStatus.PARTIAL:
                return "🟡 Partial"
            case VerificationStatus.PASSING:
                return "🟢 Passing"
            case VerificationStatus.FAILING:
                return "🔴 Failing"
            case VerificationStatus.BLOCKED:
                return "🟠 Blocked"
            case VerificationStatus.UNKNOWN:
                return "⚫ Unknown"
        raise AssertionError(f"unsupported verification status: {self!r}")


class VerificationGapState(StrEnum):
    UNVERIFIED = "unverified"
    FAILING = "failing"
    BLOCKED = "blocked"
    MANUAL = "manual"

    @property
    def emoji(self) -> str:
        match self:
            case VerificationGapState.UNVERIFIED:
                return "⚪"
            case VerificationGapState.FAILING:
                return "🔴"
            case VerificationGapState.BLOCKED:
                return "🟠"
            case VerificationGapState.MANUAL:
                return "🟡"
        raise AssertionError(f"unsupported verification gap state: {self!r}")

    @property
    def has_current_result(self) -> bool:
        return self is VerificationGapState.FAILING


@dataclass(frozen=True, slots=True)
class Progress:
    completed: int
    total: int

    def __post_init__(self) -> None:
        if self.completed < 0:
            raise ValueError("progress.completed must be >= 0")
        if self.total <= 0:
            raise ValueError("progress.total must be > 0")
        if self.completed > self.total:
            raise ValueError("progress.completed must not exceed progress.total")

    @property
    def ratio(self) -> float:
        return self.completed / self.total

    @property
    def remaining(self) -> int:
        return self.total - self.completed


@dataclass(frozen=True, slots=True)
class VerificationGap:
    text: str
    state: VerificationGapState = VerificationGapState.UNVERIFIED

    def __post_init__(self) -> None:
        _require_text(self.text, "verification gap text")

    @property
    def display(self) -> str:
        return f"{self.state.emoji} {self.text}"


@dataclass(frozen=True, slots=True)
class DashboardItem:
    name: str
    implementation_status: ImplementationStatus
    implementation_progress: Progress
    verification_status: VerificationStatus
    verification_progress: Progress
    implementation_gaps: tuple[str, ...] = ()
    verification_gaps: tuple[VerificationGap, ...] = ()

    def __post_init__(self) -> None:
        _require_single_line(self.name, "item name")
        for gap in self.implementation_gaps:
            _require_text(gap, "implementation gap text")


@dataclass(frozen=True, slots=True)
class Risk:
    area: str
    text: str
    impact: str

    def __post_init__(self) -> None:
        _require_single_line(self.area, "risk area")
        _require_text(self.text, "risk text")
        _require_text(self.impact, "risk impact")


@dataclass(frozen=True, slots=True)
class Dashboard:
    level: DashboardLevel
    title: str
    snapshot: str
    current_focus: str
    items: tuple[DashboardItem, ...]
    include_total: bool = True
    risks: tuple[Risk, ...] = ()
    references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_single_line(self.title, "dashboard.title")
        _require_single_line(self.snapshot, "dashboard.snapshot")
        _require_single_line(self.current_focus, "dashboard.current_focus")
        if not self.items:
            raise ValueError("dashboard must contain at least one item")

        names = [item.name.casefold() for item in self.items]
        if len(names) != len(set(names)):
            raise ValueError("item names must be unique within a dashboard")

        for reference in self.references:
            _require_single_line(reference, "reference text")


def _require_text(value: str, label: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be empty")


def _require_single_line(value: str, label: str) -> None:
    _require_text(value, label)
    if "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be a single line")
