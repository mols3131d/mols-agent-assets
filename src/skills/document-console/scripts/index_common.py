"""Shared helpers for document index scripts."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence


def split_csv_arg(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def resolve_output_path(base_dir: Path, output: str | None, default_name: str) -> Path:
    raw_path = Path(output or default_name)
    return raw_path.resolve() if raw_path.is_absolute() else base_dir / raw_path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], list(reader)


def read_csv_header(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return next(reader, [])


def write_csv(
    path: Path,
    fields: Sequence[str],
    rows: Sequence[dict[str, str]],
    *,
    extrasaction: str = "ignore",
) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction=extrasaction,
        )
        writer.writeheader()
        writer.writerows(rows)


def sort_rows(
    rows: Sequence[dict[str, str]],
    sort_fields: Sequence[str],
) -> list[dict[str, str]]:
    if not sort_fields:
        return list(rows)

    def key(row: dict[str, str]) -> tuple[tuple[bool, str], ...]:
        return tuple(
            (row.get(field, "") == "", row.get(field, "").casefold())
            for field in sort_fields
        )

    return sorted(rows, key=key)
