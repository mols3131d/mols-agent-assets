#!/usr/bin/env python3
"""Generate deterministic baseline route files for local Skills and glob-scoped Rules.

Generation handles factual baseline metadata only. Route descriptions may be tuned later,
so existing output is preserved unless --force is explicitly supplied.
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
    entries: list[dict[str, object]] = []
    for path in sorted((repo / ".agents" / "skills").glob("*/SKILL.md")):
        front = front_matter(path)
        name = scalar(front, "name")
        description = scalar(front, "description")
        if name and description:
            entries.append(
                {"name": name, "description": description, "source": rel(path, repo)}
            )
    return entries


def rule_routes(repo: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    rules_root = repo / ".agents" / "rules"
    if not rules_root.exists():
        return entries

    for path in sorted(rules_root.rglob("*.md")):
        front = front_matter(path)
        globs = list_value(front, "globs") or list_value(front, "applyTo")
        if globs:
            entries.append({"source": rel(path, repo), "globs": globs})
    return entries


def render_jsonl(meta: dict[str, object], entries: list[dict[str, object]]) -> str:
    lines = [json.dumps({"_meta": meta}, ensure_ascii=False, separators=(",", ":"))]
    lines.extend(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries)
    return "\n".join(lines) + "\n"


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing route: {path} (use --force)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to <repo>/.agents/routes.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing route files. Use only when replacing approved tuning intentionally.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo / ".agents" / "routes"
    )

    write(
        output_dir / "skills.jsonl",
        render_jsonl(
            {
                "kind": "skills",
                "instructions": "Select task-relevant Skills by name and description, then load only the selected source.",
            },
            skill_routes(repo),
        ),
        args.force,
    )
    write(
        output_dir / "rules.jsonl",
        render_jsonl(
            {
                "kind": "rules",
                "instructions": "Match known target paths against globs, then load only matching Rule sources.",
            },
            rule_routes(repo),
        ),
        args.force,
    )


if __name__ == "__main__":
    main()
