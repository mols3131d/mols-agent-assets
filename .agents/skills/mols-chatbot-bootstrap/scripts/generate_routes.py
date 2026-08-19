#!/usr/bin/env python3
"""Generate or check baseline routes for common local Skill and Rule layouts.

This is a reference baseline, not a universal workspace parser. Inspect the target asset
layout and metadata contract before use, and adapt the script when they differ.
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


def expand_kinds(kind: str) -> list[str]:
    return ["skills", "rules"] if kind == "both" else [kind]


def generation_kinds(
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

    kinds = expand_kinds(kind)
    roots = {"skills": skills_root, "rules": rules_root}
    missing = [name for name in kinds if not roots[name].is_dir()]
    if missing:
        raise SystemExit(f"requested asset root not found: {', '.join(missing)}")
    return kinds


def check_kinds(
    kind: str,
    output_dir: Path,
    skill_entries: list[dict[str, object]],
    rule_entries: list[dict[str, object]],
) -> list[str]:
    if kind != "auto":
        return expand_kinds(kind)

    available = {
        "skills": bool(skill_entries) or (output_dir / "skills.jsonl").is_file(),
        "rules": bool(rule_entries) or (output_dir / "rules.jsonl").is_file(),
    }
    kinds = [name for name in ("skills", "rules") if available[name]]
    if not kinds:
        raise SystemExit("no route files or routable local Skills/Rules found")
    return kinds


def load_routes(path: Path, kind: str) -> list[dict[str, object]]:
    if not path.is_file():
        raise SystemExit(f"route file not found: {path}")

    rows: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSONL at {path}:{number}: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"route row must be an object at {path}:{number}")
        rows.append(row)

    if not rows:
        raise SystemExit(f"empty route file: {path}")
    meta = rows[0].get("_meta")
    if (
        not isinstance(meta, dict)
        or meta.get("kind") != kind
        or not isinstance(meta.get("instructions"), str)
        or not str(meta["instructions"]).strip()
    ):
        raise SystemExit(f"invalid _meta header for {kind}: {path}")
    return rows[1:]


def validate_source(repo: Path, source: object) -> str:
    if not isinstance(source, str) or not source:
        raise SystemExit("every route entry requires a non-empty source")
    if source.startswith(("https://", "http://")):
        return source

    path = (repo / source).resolve()
    try:
        path.relative_to(repo)
    except ValueError as exc:
        raise SystemExit(f"local route source escapes repository: {source}") from exc
    if not path.is_file():
        raise SystemExit(f"local route source not found: {source}")
    return source


def check_routes(
    repo: Path,
    path: Path,
    kind: str,
    expected: list[dict[str, object]],
) -> None:
    entries = load_routes(path, kind)
    actual: dict[str, dict[str, object]] = {}

    for entry in entries:
        source = validate_source(repo, entry.get("source"))
        if source in actual:
            raise SystemExit(f"duplicate route source in {path}: {source}")
        if kind == "skills":
            name = entry.get("name")
            description = entry.get("description")
            if (
                not isinstance(name, str)
                or not name.strip()
                or not isinstance(description, str)
                or not description.strip()
            ):
                raise SystemExit(f"Skill route requires name and description: {source}")
        else:
            globs = entry.get("globs")
            if not isinstance(globs, list) or not globs or not all(
                isinstance(item, str) and item for item in globs
            ):
                raise SystemExit(f"Rule route requires non-empty globs: {source}")
        actual[source] = entry

    for baseline in expected:
        source = str(baseline["source"])
        entry = actual.get(source)
        if entry is None:
            raise SystemExit(f"missing {kind} route for local source: {source}")
        if kind == "skills" and entry.get("name") != baseline.get("name"):
            raise SystemExit(f"Skill identity drift for source: {source}")
        if kind == "rules" and entry.get("globs") != baseline.get("globs"):
            raise SystemExit(f"Rule selector drift for source: {source}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate/check routes for the bundled common layout. "
            "Inspect/adapt the script first when the target asset spec differs."
        )
    )
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
        help="Route directory. Defaults to .agents/routes relative to repo.",
    )
    parser.add_argument(
        "--kinds",
        choices=("auto", "skills", "rules", "both"),
        default="auto",
        help="Route kinds to generate/check. auto uses local entries or existing routes.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate route invariants without rewriting tuned route metadata.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing route files. Use only when replacing approved tuning intentionally.",
    )
    args = parser.parse_args()

    if args.check and args.force:
        parser.error("--check and --force cannot be used together")

    repo = args.repo.resolve()
    skills_root = resolve_path(repo, args.skills_root, ".agents/skills")
    rules_root = resolve_path(repo, args.rules_root, ".agents/rules")
    output_dir = resolve_path(repo, args.output_dir, ".agents/routes")

    skill_entries = skill_routes(repo, skills_root)
    rule_entries = rule_routes(repo, rules_root)
    baselines = {"skills": skill_entries, "rules": rule_entries}

    if args.check:
        kinds = check_kinds(args.kinds, output_dir, skill_entries, rule_entries)
        for kind in kinds:
            check_routes(repo, output_dir / f"{kind}.jsonl", kind, baselines[kind])
        return

    kinds = generation_kinds(
        args.kinds,
        skills_root,
        rules_root,
        skill_entries,
        rule_entries,
    )
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
