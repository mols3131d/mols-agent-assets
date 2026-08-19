from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GITHUB_BLOB_ROOT = "https://github.com/mols3131d/mols-agent-assets/blob/main"
INSTRUCTION = (
    "Before substantive work, use each entry's name and description to select only "
    "applicable Skills; select multiple when their responsibilities independently apply. "
    "For each match, substitute its name for {name} in metadata, use workspace_path when "
    "the repository is directly accessible and otherwise use github_url, then read the "
    "Skill before acting. If neither source is accessible, do not claim the Skill was "
    "loaded. If no Skill matches, continue without loading one. Re-evaluate selection "
    "when the task materially changes. Do not treat currently visible Skill, tool, or "
    "plugin inventories as substitutes for this repository index."
)
TARGETS = {
    ROOT / "src/agentsmesh/skills": (
        "*/SKILL.md",
        "src/agentsmesh/skills/{name}/SKILL.md",
    ),
}


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"missing front matter: {path.relative_to(ROOT)}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"unclosed front matter: {path.relative_to(ROOT)}") from exc
    data = yaml.safe_load("\n".join(lines[1:end])) or {}
    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not isinstance(description, str):
        raise ValueError(f"name/description required: {path.relative_to(ROOT)}")
    return {"name": name, "description": description}


def render_index(directory: Path, pattern: str, workspace_path: str) -> str:
    rows = [
        {
            "metadata": {
                "workspace_path": workspace_path,
                "github_url": f"{GITHUB_BLOB_ROOT}/{workspace_path}",
            }
        },
        {"instruction": INSTRUCTION},
        *sorted(
            (read_frontmatter(path) for path in directory.glob(pattern)),
            key=lambda row: row["name"],
        ),
    ]
    return "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in rows
    )


def main() -> None:
    for directory, (pattern, workspace_path) in TARGETS.items():
        content = render_index(directory, pattern, workspace_path)
        (directory / "INDEX.jsonl").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
