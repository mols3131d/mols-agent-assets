"""Generate cross-runtime discovery routes for Agent Assets provided by this repository."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ASSET_ROOT = ROOT / "src/rulesync/.rulesync"
CANONICAL_SKILLS = CANONICAL_ASSET_ROOT / "skills"
CANONICAL_SUBAGENTS = CANONICAL_ASSET_ROOT / "subagents"
DISTRIBUTION_ROUTE_DIR = ROOT / "route"
DISTRIBUTION_ROUTES_PATH = DISTRIBUTION_ROUTE_DIR / "routes.jsonl"
DISTRIBUTION_SKILL_ROUTE = DISTRIBUTION_ROUTE_DIR / "skills.jsonl"
DISTRIBUTION_SUBAGENT_ROUTE = DISTRIBUTION_ROUTE_DIR / "subagents.jsonl"
REPOSITORY_LOCAL_ROUTE_DIR = ROOT / ".agents/route"
RAW_ROOT = (
    "https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main"
)
SKILL_SOURCE_TEMPLATE = (
    f"{RAW_ROOT}/src/rulesync/.rulesync/skills/{{directory}}/SKILL.md"
)
SUBAGENT_SOURCE_TEMPLATE = (
    f"{RAW_ROOT}/src/rulesync/.rulesync/subagents/{{filename}}"
)
ROUTE_INSTRUCTION = (
    "Select only task-relevant Agent Asset routes by name and description, then load every "
    "selected source before continuing discovery. Follow each selected route's own "
    "instructions. If no route matches, continue without loading one. Re-evaluate route "
    "selection when the task materially changes."
)
SKILL_INSTRUCTION = (
    "When this Skill route is loaded for a task, select only task-relevant Skills by name "
    "and description, then load every selected source before continuing the task. Select "
    "multiple Skills when their responsibilities independently apply. If no Skill matches, "
    "continue without loading one. Re-evaluate selection when the task materially changes. "
    "This file is derived discovery metadata; the referenced canonical Skill remains "
    "authoritative."
)
SUBAGENT_INSTRUCTION = (
    "When this Subagent route is loaded for a task, select only task-relevant Subagents by "
    "name and description, then load every selected source before using or adapting that "
    "Subagent. If no Subagent matches, continue without loading one. Re-evaluate selection "
    "when the task materially changes. This file is derived discovery metadata; the "
    "referenced canonical Subagent remains authoritative."
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


def render_asset_route(
    paths: Iterable[Path],
    source_for: Callable[[Path], str],
    *,
    kind: str,
    instructions: str,
) -> str:
    entries = []
    for path in paths:
        entry = read_frontmatter(path)
        entry["source"] = source_for(path)
        entries.append(entry)

    rows = [
        {"_meta": {"kind": kind, "instructions": instructions}},
        *sorted(entries, key=lambda row: row["name"]),
    ]
    return "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in rows
    )


def render_skill_route(
    directory: Path = CANONICAL_SKILLS,
    source_template: str = SKILL_SOURCE_TEMPLATE,
) -> str:
    return render_asset_route(
        directory.glob("*/SKILL.md"),
        lambda path: source_template.format(directory=path.parent.name),
        kind="skills",
        instructions=SKILL_INSTRUCTION,
    )


def render_subagent_route(
    directory: Path = CANONICAL_SUBAGENTS,
    source_template: str = SUBAGENT_SOURCE_TEMPLATE,
) -> str:
    return render_asset_route(
        directory.glob("*.md"),
        lambda path: source_template.format(filename=path.name),
        kind="subagents",
        instructions=SUBAGENT_INSTRUCTION,
    )


def render_routes(route_rows: Iterable[dict[str, str]]) -> str:
    rows = [
        {"_meta": {"kind": "routes", "instructions": ROUTE_INSTRUCTION}},
        *route_rows,
    ]
    return "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in rows
    )


def generate() -> dict[Path, str]:
    route_rows: list[dict[str, str]] = []
    asset_outputs: dict[Path, str] = {}

    if next(CANONICAL_SKILLS.glob("*/SKILL.md"), None) is not None:
        route_rows.append(
            {
                "name": "skills",
                "description": "이 repository가 제공하는 reusable Skill",
                "source": f"{RAW_ROOT}/route/skills.jsonl",
            }
        )
        asset_outputs[DISTRIBUTION_SKILL_ROUTE] = render_skill_route()

    if next(CANONICAL_SUBAGENTS.glob("*.md"), None) is not None:
        route_rows.append(
            {
                "name": "subagents",
                "description": "이 repository가 제공하는 reusable Subagent",
                "source": f"{RAW_ROOT}/route/subagents.jsonl",
            }
        )
        asset_outputs[DISTRIBUTION_SUBAGENT_ROUTE] = render_subagent_route()

    return {
        DISTRIBUTION_ROUTES_PATH: render_routes(route_rows),
        **asset_outputs,
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    DISTRIBUTION_ROUTE_DIR.mkdir(parents=True, exist_ok=True)
    generated_paths = set(outputs)
    for path in DISTRIBUTION_ROUTE_DIR.glob("*.jsonl"):
        if path not in generated_paths:
            path.unlink()
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    if DISTRIBUTION_ROUTE_DIR == REPOSITORY_LOCAL_ROUTE_DIR:
        raise AssertionError("distribution and repository-local route surfaces must differ")
    write_outputs(generate())


if __name__ == "__main__":
    main()
