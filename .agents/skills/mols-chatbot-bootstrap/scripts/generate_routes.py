#!/usr/bin/env python3
"""Generate deterministic baseline routes for a common local Skill/Rule layout.

This is a reference implementation, not a universal asset parser. Inspect the target
workspace's asset roots, package shape, frontmatter, and Rule selector semantics before
using it. Configure or adapt the script when those contracts differ.

Defaults follow the common .agents layout, but roots and output are configurable. Existing
route files are preserved unless --force is explicitly supplied.
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


def resolve_path(repo: Path, value: Path | None, default: str) -> Path:
    path = Path(default) if value is None else value
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def rel(path: Path, repo: Path) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError as exc:
        raise SystemExit(f"local asset must be inside repo: {path}") from exc


def skill_routes(repo: Path, root: Path) -> list[dict[str, object]]:
    if not root.is_dir():
        return []

    entries: list[dict[str, object]] = []
    for path in sorted(root.glob("*/SKILL.md")):
        front = front_matter(path)
        name = scalar(front, "name")
        description = scalar(front, "description")
        if name and description:
            entries.append(
                {"name": name, "description": description, "source": rel(path, repo)}
            )
    return entries


def rule_routes(repo: Path, root: Path) -> list[dict[str, object]]:
    if not root.is_dir():
        return []

    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*.md")):
        front = front_matter(path)
        globs = list_value(front, "globs") or list_value(front, "applyTo")
        if globs:
            entries.append({"source": rel(path, repo), "globs": globs})
    return entries


def render_jsonl(meta: dict[str, object], entries: list[dict[str, object]]) -> str:
    lines = [json.dumps({"_meta": meta}, ensure_ascii=False, separators=(",", ":"))]
    lines.extend(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries)
    return "\n".join(lines) + "\n"


def resolve_kinds(
    kind: str,
    skills_root: Path,
    rules_root: Path,
    skill_entries: list[dict[str, object]],
    rule_entries: list[dict[str, object]],
) -> list[str]:
    if kind == "auto":
        kinds = []
        if skill_entries:
            kinds.append("skills")
        if rule_entries:
            kinds.append("rules")
        if not kinds:
            raise SystemExit("no routable local Skills or Rules found")
        return kinds

    kinds = ["skills", "rules"] if kind == "both" else [kind]
    roots = {"skills": skills_root, "rules": rules_root}
    missing = [name for name in kinds if not roots[name].is_dir()]
    if missing:
        raise SystemExit(f"requested asset root not found: {', '.join(missing)}")
    return kinds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--skills-root",
        type=Path,
        help="Local Skill root. Defaults to .agents/skills relative to repo.",
    )
    parser.add_argument(
        "--rules-root",
        type=Path,
        help="Local Rule root. Defaults to .agents/rules relative to repo.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to .agents/routes relative to repo.",
    )
    parser.add_argument(
        "--kinds",
        choices=("auto", "skills", "rules", "both"),
        default="auto",
        help="Route kinds to generate. auto emits only kinds with routable local entries.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing route files. Use only when replacing approved tuning intentionally.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    skills_root = resolve_path(repo, args.skills_root, ".agents/skills")
    rules_root = resolve_path(repo, args.rules_root, ".agents/rules")
    output_dir = resolve_path(repo, args.output_dir, ".agents/routes")

    skill_entries = skill_routes(repo, skills_root)
    rule_entries = rule_routes(repo, rules_root)
    kinds = resolve_kinds(args.kinds, skills_root, rules_root, skill_entries, rule_entries)

    outputs: dict[Path, str] = {}
    if "skills" in kinds:
        outputs[output_dir / "skills.jsonl"] = render_jsonl(
            {
                "kind": "skills",
                "instructions": "Select task-relevant Skills by name and description, then load only the selected source.",
            },
            skill_entries,
        )
    if "rules" in kinds:
        outputs[output_dir / "rules.jsonl"] = render_jsonl(
            {
                "kind": "rules",
                "instructions": "Match known target paths against globs, then load only matching Rule sources.",
            },
            rule_entries,
        )

    if not args.force:
        existing = [path for path in outputs if path.exists()]
        if existing:
            joined = ", ".join(str(path) for path in existing)
            raise SystemExit(f"refusing to overwrite existing routes: {joined} (use --force)")

    output_dir.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
