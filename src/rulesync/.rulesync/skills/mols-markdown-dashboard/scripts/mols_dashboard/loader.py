from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from enum import StrEnum
from pathlib import Path
from typing import Any, TypeVar

import yaml

from .model import (
    Dashboard,
    DashboardItem,
    DashboardLevel,
    ImplementationStatus,
    Progress,
    Risk,
    VerificationGap,
    VerificationGapState,
    VerificationStatus,
)

EnumT = TypeVar("EnumT", bound=StrEnum)
_PROGRESS_PATTERN = re.compile(r"^(?P<completed>\d+)\s*/\s*(?P<total>\d+)$")


class DashboardInputError(ValueError):
    """Raised when dashboard YAML is structurally or semantically invalid."""


def load_dashboard(path: Path) -> Dashboard:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise DashboardInputError(f"cannot read YAML: {path}") from exc
    except yaml.YAMLError as exc:
        raise DashboardInputError(f"invalid YAML: {exc}") from exc

    if not isinstance(raw, Mapping):
        raise DashboardInputError("YAML root must be a mapping")

    return parse_dashboard(raw)


def parse_dashboard(raw: Mapping[str, Any]) -> Dashboard:
    _reject_unknown_keys(
        raw,
        {"version", "dashboard", "items", "risks", "references"},
        "root",
    )

    version = raw.get("version", 1)
    if version != 1:
        raise DashboardInputError(f"unsupported schema version: {version!r}")

    dashboard_raw = _mapping(raw, "dashboard")
    _reject_unknown_keys(
        dashboard_raw,
        {"level", "title", "snapshot", "current_focus", "include_total"},
        "dashboard",
    )
    items_raw = _sequence(raw, "items")
    risks_raw = _optional_sequence(raw.get("risks", ()), "risks")
    references_raw = _optional_sequence(raw.get("references", ()), "references")

    level = _enum(DashboardLevel, dashboard_raw.get("level"), "dashboard.level")
    title = _text(dashboard_raw.get("title"), "dashboard.title")
    snapshot = _text(dashboard_raw.get("snapshot"), "dashboard.snapshot")
    current_focus = _text(
        dashboard_raw.get("current_focus"),
        "dashboard.current_focus",
    )
    include_total = _boolean(
        dashboard_raw.get("include_total", True),
        "dashboard.include_total",
    )
    items = tuple(
        _parse_item(item, index)
        for index, item in enumerate(items_raw, start=1)
    )
    risks = tuple(
        _parse_risk(item, index)
        for index, item in enumerate(risks_raw, start=1)
    )
    references = tuple(
        _text(value, f"references[{index}]")
        for index, value in enumerate(references_raw, start=1)
    )

    try:
        return Dashboard(
            level=level,
            title=title,
            snapshot=snapshot,
            current_focus=current_focus,
            include_total=include_total,
            items=items,
            risks=risks,
            references=references,
        )
    except ValueError as exc:
        raise DashboardInputError(str(exc)) from exc


def _parse_item(raw: Any, index: int) -> DashboardItem:
    path = f"items[{index}]"
    item = _as_mapping(raw, path)
    _reject_unknown_keys(item, {"name", "implementation", "verification"}, path)

    implementation = _mapping(item, "implementation", parent=path)
    verification = _mapping(item, "verification", parent=path)
    _reject_unknown_keys(
        implementation,
        {"status", "progress", "gaps"},
        f"{path}.implementation",
    )
    _reject_unknown_keys(
        verification,
        {"status", "progress", "gaps"},
        f"{path}.verification",
    )

    implementation_gaps_raw = _optional_sequence(
        implementation.get("gaps", ()),
        f"{path}.implementation.gaps",
    )
    verification_gaps_raw = _optional_sequence(
        verification.get("gaps", ()),
        f"{path}.verification.gaps",
    )

    name = _text(item.get("name"), f"{path}.name")
    implementation_status = _enum(
        ImplementationStatus,
        implementation.get("status"),
        f"{path}.implementation.status",
    )
    implementation_progress = _progress(
        implementation.get("progress"),
        f"{path}.implementation.progress",
    )
    implementation_gaps = tuple(
        _text(value, f"{path}.implementation.gaps[{gap_index}]")
        for gap_index, value in enumerate(implementation_gaps_raw, start=1)
    )
    verification_status = _enum(
        VerificationStatus,
        verification.get("status"),
        f"{path}.verification.status",
    )
    verification_progress = _progress(
        verification.get("progress"),
        f"{path}.verification.progress",
    )
    verification_gaps = tuple(
        _parse_verification_gap(
            value,
            f"{path}.verification.gaps[{gap_index}]",
        )
        for gap_index, value in enumerate(verification_gaps_raw, start=1)
    )

    try:
        return DashboardItem(
            name=name,
            implementation_status=implementation_status,
            implementation_progress=implementation_progress,
            implementation_gaps=implementation_gaps,
            verification_status=verification_status,
            verification_progress=verification_progress,
            verification_gaps=verification_gaps,
        )
    except ValueError as exc:
        raise DashboardInputError(f"{path}: {exc}") from exc


def _parse_verification_gap(raw: Any, path: str) -> VerificationGap:
    if isinstance(raw, str):
        return VerificationGap(text=_text(raw, path))

    item = _as_mapping(raw, path)
    _reject_unknown_keys(item, {"state", "text"}, path)
    return VerificationGap(
        text=_text(item.get("text"), f"{path}.text"),
        state=_enum(
            VerificationGapState,
            item.get("state", VerificationGapState.UNVERIFIED.value),
            f"{path}.state",
        ),
    )


def _parse_risk(raw: Any, index: int) -> Risk:
    path = f"risks[{index}]"
    item = _as_mapping(raw, path)
    _reject_unknown_keys(item, {"area", "text", "impact"}, path)
    area = _text(item.get("area"), f"{path}.area")
    text = _text(item.get("text"), f"{path}.text")
    impact = _text(item.get("impact"), f"{path}.impact")

    try:
        return Risk(area=area, text=text, impact=impact)
    except ValueError as exc:
        raise DashboardInputError(f"{path}: {exc}") from exc


def _progress(raw: Any, path: str) -> Progress:
    if isinstance(raw, str):
        match = _PROGRESS_PATTERN.fullmatch(raw.strip())
        if not match:
            raise DashboardInputError(f"{path} must use 'completed/total', got {raw!r}")
        completed = int(match.group("completed"))
        total = int(match.group("total"))
    elif isinstance(raw, Mapping):
        _reject_unknown_keys(raw, {"completed", "total"}, path)
        completed = _integer(raw.get("completed"), f"{path}.completed")
        total = _integer(raw.get("total"), f"{path}.total")
    else:
        raise DashboardInputError(f"{path} must be a string or mapping")

    try:
        return Progress(completed=completed, total=total)
    except ValueError as exc:
        raise DashboardInputError(f"{path}: {exc}") from exc


def _mapping(
    raw: Mapping[str, Any],
    key: str,
    *,
    parent: str | None = None,
) -> Mapping[str, Any]:
    path = f"{parent}.{key}" if parent else key
    return _as_mapping(raw.get(key), path)


def _as_mapping(raw: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(raw, Mapping):
        raise DashboardInputError(f"{path} must be a mapping")
    return raw


def _sequence(raw: Mapping[str, Any], key: str) -> Sequence[Any]:
    return _optional_sequence(raw.get(key), key)


def _optional_sequence(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise DashboardInputError(f"{path} must be a sequence")
    return value


def _text(raw: Any, path: str) -> str:
    if raw is None:
        raise DashboardInputError(f"{path} is required")
    if not isinstance(raw, str):
        raise DashboardInputError(f"{path} must be a string")
    value = raw.strip()
    if not value:
        raise DashboardInputError(f"{path} must not be empty")
    return value


def _integer(raw: Any, path: str) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise DashboardInputError(f"{path} must be an integer")
    return raw


def _boolean(raw: Any, path: str) -> bool:
    if not isinstance(raw, bool):
        raise DashboardInputError(f"{path} must be a boolean")
    return raw


def _enum(enum_type: type[EnumT], raw: Any, path: str) -> EnumT:
    try:
        return enum_type(raw)
    except (TypeError, ValueError) as exc:
        allowed = ", ".join(member.value for member in enum_type)
        raise DashboardInputError(f"{path} must be one of: {allowed}") from exc


def _reject_unknown_keys(
    raw: Mapping[str, Any],
    allowed: set[str],
    path: str,
) -> None:
    unknown = sorted(str(key) for key in raw if key not in allowed)
    if unknown:
        joined = ", ".join(unknown)
        raise DashboardInputError(f"{path} contains unknown field(s): {joined}")
