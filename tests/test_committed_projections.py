from __future__ import annotations

import json

from scripts import generate_repository_routes as routes
from scripts.generate_docs_indexes import generate_docs_indexes


def _read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_committed_docs_indexes_are_current() -> None:
    assert generate_docs_indexes(check=True) == []


def test_committed_repository_routes_match_lock_and_families() -> None:
    expected_sources = routes.read_rulesync_entries()
    for name, source in routes.read_skills_cli_entries().items():
        assert name not in expected_sources
        expected_sources[name] = source

    all_rows = _read_jsonl(routes.ALL_PATH)
    all_by_name = {row["name"]: row for row in all_rows}
    assert {name: row["source"] for name, row in all_by_name.items()} == expected_sources

    families = routes.read_families()
    categorized = set()
    for family, entry in families.items():
        names = sorted(entry["skills"])
        categorized.update(names)
        assert _read_jsonl(routes.ROUTE_DIR / f"{family}.jsonl") == [
            all_by_name[name] for name in names
        ]

    uncategorized = sorted(set(expected_sources) - categorized)
    assert _read_jsonl(routes.UNCATEGORIZED_PATH) == [
        all_by_name[name] for name in uncategorized
    ]

    expected_route_rows = [
        {
            "name": family,
            "kind": routes.ROUTE_KIND,
            "description": str(families[family]["description"]),
            "source": f"{family}.jsonl",
        }
        for family in sorted(families)
    ]
    expected_route_rows.extend(
        [
            {
                "name": "uncategorized",
                "kind": routes.ROUTE_KIND,
                "description": "아직 family에 배정되지 않은 Skill",
                "source": "uncategorized.jsonl",
            },
            {
                "name": "all",
                "kind": routes.ROUTE_KIND,
                "description": "전체 lock-backed Skill fallback",
                "source": "all.jsonl",
            },
        ]
    )
    assert _read_jsonl(routes.ROUTES_PATH) == expected_route_rows

    expected_paths = {
        routes.ROUTES_PATH,
        routes.ALL_PATH,
        routes.UNCATEGORIZED_PATH,
        *(routes.ROUTE_DIR / f"{family}.jsonl" for family in families),
    }
    assert set(routes.ROUTE_DIR.glob("*.jsonl")) == expected_paths
