from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from .model import (
    Dashboard,
    DashboardItem,
    ImplementationStatus,
    VerificationGapState,
    VerificationStatus,
)


class DashboardValidationError(ValueError):
    """Raised when a dashboard or rendered Markdown violates core invariants."""


@dataclass(frozen=True, slots=True)
class Heading:
    level: int
    text: str


def validate_dashboard_consistency(dashboard: Dashboard) -> None:
    errors = [
        error
        for item in dashboard.items
        for error in _item_consistency_errors(item)
    ]
    if errors:
        raise DashboardValidationError("\n".join(errors))


def _item_consistency_errors(item: DashboardItem) -> tuple[str, ...]:
    return (
        *_implementation_errors(item),
        *_verification_errors(item),
    )


def _implementation_errors(item: DashboardItem) -> tuple[str, ...]:
    progress = item.implementation_progress
    gaps = item.implementation_gaps
    errors: list[str] = []

    if len(gaps) != progress.remaining:
        errors.append(
            f"{item.name}: implementation gap count must equal remaining requirements "
            f"({len(gaps)} != {progress.remaining})"
        )

    match item.implementation_status:
        case ImplementationStatus.IMPLEMENTED:
            if progress.remaining:
                errors.append(
                    f"{item.name}: implemented requires complete implementation progress"
                )
            if gaps:
                errors.append(
                    f"{item.name}: implemented must not contain implementation gaps"
                )
        case ImplementationStatus.NOT_STARTED | ImplementationStatus.PLANNED:
            if progress.completed:
                errors.append(
                    f"{item.name}: {item.implementation_status.value} requires "
                    "zero completed requirements"
                )
        case ImplementationStatus.IN_PROGRESS:
            if not progress.remaining:
                errors.append(
                    f"{item.name}: in_progress requires incomplete implementation progress"
                )
        case ImplementationStatus.BLOCKED:
            if not progress.remaining:
                errors.append(
                    f"{item.name}: blocked requires at least one remaining requirement"
                )
        case ImplementationStatus.UNKNOWN:
            pass

    return tuple(errors)


def _verification_errors(item: DashboardItem) -> tuple[str, ...]:
    progress = item.verification_progress
    gaps = item.verification_gaps
    errors: list[str] = []
    failing = tuple(gap for gap in gaps if gap.state is VerificationGapState.FAILING)
    blocked = tuple(gap for gap in gaps if gap.state is VerificationGapState.BLOCKED)
    without_results = tuple(gap for gap in gaps if not gap.state.has_current_result)

    if len(without_results) != progress.remaining:
        errors.append(
            f"{item.name}: verification gaps without current results must equal "
            f"remaining targets ({len(without_results)} != {progress.remaining})"
        )

    match item.verification_status:
        case VerificationStatus.PASSING:
            if progress.remaining:
                errors.append(
                    f"{item.name}: passing requires complete verification progress"
                )
            if gaps:
                errors.append(
                    f"{item.name}: passing must not contain verification gaps"
                )
        case VerificationStatus.UNVERIFIED:
            if progress.completed:
                errors.append(
                    f"{item.name}: unverified requires zero verification progress"
                )
            if failing:
                errors.append(
                    f"{item.name}: unverified must not contain failing verification gaps"
                )
            if blocked:
                errors.append(
                    f"{item.name}: unverified must use blocked when a required target is blocked"
                )
        case VerificationStatus.PARTIAL:
            if not progress.completed:
                errors.append(
                    f"{item.name}: partial requires at least one target with a current result"
                )
            if not gaps:
                errors.append(
                    f"{item.name}: partial requires at least one verification gap"
                )
            if failing:
                errors.append(
                    f"{item.name}: partial must use failing when a target currently fails"
                )
            if blocked:
                errors.append(
                    f"{item.name}: partial must use blocked when a required target is blocked"
                )
        case VerificationStatus.FAILING:
            if not failing:
                errors.append(
                    f"{item.name}: failing requires at least one failing verification gap"
                )
        case VerificationStatus.BLOCKED:
            if failing:
                errors.append(
                    f"{item.name}: blocked must use failing when a target currently fails"
                )
            if not blocked:
                errors.append(
                    f"{item.name}: blocked requires at least one blocked verification gap"
                )
        case VerificationStatus.UNKNOWN:
            pass

    return tuple(errors)


def validate_markdown(
    markdown: str,
    *,
    dashboard: Dashboard | None = None,
    event_parser: Callable[[str], Iterable[Any]] | None = None,
) -> None:
    parser = event_parser or _pyromark_events
    try:
        headings = _headings(tuple(parser(markdown)))
    except Exception as exc:  # parser boundary
        raise DashboardValidationError(
            f"pyromark could not parse generated Markdown: {exc}"
        ) from exc

    _validate_heading_structure(headings)

    if dashboard is not None:
        _validate_dashboard_markdown(markdown, headings, dashboard)


def _validate_heading_structure(headings: tuple[Heading, ...]) -> None:
    if not headings or headings[0].level != 1:
        raise DashboardValidationError("Markdown must start with one level-1 title")
    if sum(heading.level == 1 for heading in headings) != 1:
        raise DashboardValidationError("Markdown must contain exactly one level-1 title")

    heading_texts = tuple(heading.text for heading in headings)
    if len(heading_texts) != len(set(heading_texts)):
        raise DashboardValidationError("Markdown contains duplicate headings")
    if "Development Progress" not in heading_texts:
        raise DashboardValidationError(
            "missing required heading: Development Progress"
        )


def _validate_dashboard_markdown(
    markdown: str,
    headings: tuple[Heading, ...],
    dashboard: Dashboard,
) -> None:
    if headings[0].text != dashboard.title:
        raise DashboardValidationError(
            "level-1 title does not match dashboard.title"
        )

    expected_header = (
        f"| {dashboard.level.row_label} | Implementation Status | "
        "Implementation Progress | Verification Status | Verification Progress |"
    )
    if expected_header not in markdown:
        raise DashboardValidationError(
            "development progress table header is missing or changed"
        )

    optional_sections = (
        (
            "Implementation Gaps",
            any(item.implementation_gaps for item in dashboard.items),
        ),
        (
            "Verification Gaps",
            any(item.verification_gaps for item in dashboard.items),
        ),
        ("Risks / Blockers", bool(dashboard.risks)),
        ("References", bool(dashboard.references)),
    )
    heading_texts = {heading.text for heading in headings}
    expected_sections = ["Development Progress"]

    for heading, expected in optional_sections:
        _validate_optional_heading(heading_texts, heading, expected)
        if expected:
            expected_sections.append(heading)

    actual_sections = [
        heading.text
        for heading in headings
        if heading.level == 2 and heading.text in expected_sections
    ]
    if actual_sections != expected_sections:
        raise DashboardValidationError(
            "dashboard sections are missing or out of the canonical order"
        )


def _validate_optional_heading(
    headings: set[str],
    heading: str,
    expected: bool,
) -> None:
    actual = heading in headings
    if actual != expected:
        state = "missing" if expected else "unexpected"
        raise DashboardValidationError(f"{state} optional heading: {heading}")


def _pyromark_events(markdown: str) -> Iterable[Any]:
    try:
        import pyromark
    except ImportError as exc:
        raise DashboardValidationError(
            "pyromark is required for Markdown validation; install project dependencies"
        ) from exc
    return pyromark.events(markdown)


def _headings(events: tuple[Any, ...]) -> tuple[Heading, ...]:
    headings: list[Heading] = []
    active_level: int | None = None
    parts: list[str] = []

    for event in events:
        match event:
            case {"Start": {"Heading": {"level": level}}}:
                active_level = int(level)
                parts = []
            case {"Text": text} | {"Code": text} if active_level is not None:
                parts.append(str(text))
            case {"End": {"Heading": _}} if active_level is not None:
                headings.append(
                    Heading(level=active_level, text="".join(parts).strip())
                )
                active_level = None
                parts = []
            case _:
                continue

    return tuple(headings)
