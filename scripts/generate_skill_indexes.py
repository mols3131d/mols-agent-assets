from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    ROOT / "src/skills": "*/SKILL.md",
    ROOT / "src/skills-chatbot": "*.skill.md",
    ROOT / "src/skills-chatbot-runtime": "*/SKILL.md",
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


def main() -> None:
    for directory, pattern in TARGETS.items():
        rows = sorted(
            (read_frontmatter(path) for path in directory.glob(pattern)),
            key=lambda row: row["name"],
        )
        content = "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        )
        (directory / "INDEX.jsonl").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
