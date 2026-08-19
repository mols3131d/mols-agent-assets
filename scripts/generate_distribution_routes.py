"""Generate the repository-root distribution route, never target-local `.agents/routes/`."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS = ROOT / "src/rulesync/.rulesync/skills"
DISTRIBUTION_ROUTE_DIR = ROOT / "route"
DISTRIBUTION_SKILL_ROUTE = DISTRIBUTION_ROUTE_DIR / "skills.jsonl"
REPOSITORY_LOCAL_ROUTE_DIR = ROOT / ".agents/routes"
RAW_ROOT = (
    "https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main"
)
SKILL_SOURCE_TEMPLATE = (
    f"{RAW_ROOT}/src/rulesync/.rulesync/skills/{{directory}}/SKILL.md"
)
INSTRUCTION = (
    "Before substantive work, select only task-relevant Skills by name and description, "
    "then load every selected source before acting. Select multiple Skills when their "
    "responsibilities independently apply. If no Skill matches, continue without loading "
    "one. Re-evaluate selection when the task materially changes. This file is derived "
    "discovery metadata; the referenced canonical Skill remains authoritative."
)


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"missing front matter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"unclosed front matter: {path}") from exc

    data = yaml.safe_load("\n".join(lines[1:end])) or {}
    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not isinstance(description, str):
        raise ValueError(f"name/description required: {path}")
    return {"name": name, "description": description}


def render_skill_route(
    directory: Path = CANONICAL_SKILLS,
    source_template: str = SKILL_SOURCE_TEMPLATE,
) -> str:
    entries = []
    for path in directory.glob("*/SKILL.md"):
        entry = read_frontmatter(path)
        entry["source"] = source_template.format(directory=path.parent.name)
        entries.append(entry)

    rows = [
        {"_meta": {"kind": "skills", "instructions": INSTRUCTION}},
        *sorted(entries, key=lambda row: row["name"]),
    ]
    return "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in rows
    )


def main() -> None:
    if DISTRIBUTION_ROUTE_DIR == REPOSITORY_LOCAL_ROUTE_DIR:
        raise AssertionError("distribution and repository-local route surfaces must differ")
    DISTRIBUTION_ROUTE_DIR.mkdir(parents=True, exist_ok=True)
    DISTRIBUTION_SKILL_ROUTE.write_text(render_skill_route(), encoding="utf-8")


if __name__ == "__main__":
    main()
