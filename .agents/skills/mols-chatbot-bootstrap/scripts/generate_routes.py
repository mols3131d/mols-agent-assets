#!/usr/bin/env python3
"""Generate baseline .agents route files from local Skills and glob-scoped Rules.

This produces deterministic routing candidates. A maintainer or agent may tune routing
metadata afterward, especially Skill descriptions, without changing source identity or
Rule selector semantics.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def scalar(front: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", front)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {">", ">-", "|", "|-"}:
        block = re.search(
            rf"(?ms)^{re.escape(key)}:\s*[>|]-?\s*\n((?:[ \t]+.*(?:\n|$))*)",
            front,
        )
        if not block:
            return None
        return " ".join(line.strip() for line in block.group(1).splitlines()).strip()
    return value.strip("'\"")


def list_value(front: str, key: str) -> list[str]:
    inline = re.search(rf"(?m)^{re.escape(key)}:\s*\[(.*?)\]\s*$", front)
    if inline:
        return [item.strip().strip("'\"") for item in inline.group(1).split(",") if item.strip()]

    block = re.search(
        rf"(?ms)^{re.escape(key)}:\s*\n((?:[ \t]+-\s+.*(?:\n|$))*)",
        front,
    )
    if block:
        values: list[str] = []
        for line in block.group(1).splitlines():
            item = re.sub(r"^\s*-\s+", "", line).strip().strip("'\"")
            if item:
                values.append(item)
        return values

    value = scalar(front, key)
    if not value:
        return []
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def front_matter(path: Path) -> str:
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def skill_routes(repo: Path) -> list[dict[str, object]]:
    routes: list[dict[str, object]] = []
    for path in sorted((repo / ".agents" / "skills").glob("*/SKILL.md")):
        front = front_matter(path)
        name = scalar(front, "name")
        description = scalar(front, "description")
        if not name or not description:
            continue
        routes.append({"name": name, "description": description, "source": rel(path, repo)})
    return routes


def rule_routes(repo: Path) -> list[dict[str, object]]:
    routes: list[dict[str, object]] = []
    rules_root = repo / ".agents" / "rules"
    if not rules_root.exists():
        return routes

    for path in sorted(rules_root.rglob("*.md")):
        front = front_matter(path)
        globs = list_value(front, "globs") or list_value(front, "applyTo")
        if not globs:
            continue
        routes.append({"source": rel(path, repo), "globs": globs})
    return routes


def write_jsonl(path: Path, meta: dict[str, object], entries: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"_meta": meta}, ensure_ascii=False, separators=(",", ":"))]
    lines.extend(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    routes = repo / ".agents" / "routes"
    write_jsonl(
        routes / "skills.jsonl",
        {
            "kind": "skills",
            "instructions": "Select task-relevant Skills by name and description, then load only the selected source.",
        },
        skill_routes(repo),
    )
    write_jsonl(
        routes / "rules.jsonl",
        {
            "kind": "rules",
            "instructions": "Match known target paths against globs, then load only matching Rule sources.",
        },
        rule_routes(repo),
    )


if __name__ == "__main__":
    main()
