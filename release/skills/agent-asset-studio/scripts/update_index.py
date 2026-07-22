#!/usr/bin/env python3
"""Routing Skill의 semantic route index를 관리한다."""

from __future__ import annotations

import csv
from pathlib import Path

from configs import skill

HEADERS = list(skill.ROUTE_INDEX_FIELDS)


def init_index(path: Path) -> None:
    """INDEX.csv가 없으면 표준 header로 생성한다."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        csv.writer(file).writerow(HEADERS)


def valid_index(path: Path) -> bool:
    """INDEX.csv의 존재와 정확한 schema를 확인한다."""
    if not path.is_file():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            return next(csv.reader(file), None) == HEADERS
    except (csv.Error, OSError):
        return False


def update_index(path: Path, data: dict[str, str]) -> None:
    """Route를 id 기준으로 추가하거나 갱신한다."""
    if not path.exists():
        init_index(path)
    elif not valid_index(path):
        raise ValueError(f"지원하지 않는 INDEX.csv schema입니다: {path}")

    route_id = data.get("id", "").strip()
    if not route_id:
        raise ValueError("route id가 필요합니다.")

    rows: list[dict[str, str]] = []
    updated = False
    with path.open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            if row.get("id") == route_id:
                row.update({key: data[key] for key in HEADERS if key in data})
                updated = True
            rows.append(row)

    if not updated:
        rows.append({key: data.get(key, "") for key in HEADERS})

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
