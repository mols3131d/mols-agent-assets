from __future__ import annotations

import argparse
import json
from pathlib import Path


def metrics(path: Path) -> dict[str, int | str]:
    text = path.read_text(encoding="utf-8")
    return {
        "path": path.as_posix(),
        "bytes": len(text.encode("utf-8")),
        "lines": text.count("\n") + 1,
        "words": len(text.split()),
    }


def markdown_resources(root: Path, directory: str) -> list[dict[str, int | str]]:
    target = root / directory
    if not target.is_dir():
        return []
    return [metrics(path) for path in sorted(target.glob("*.md"))]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report Agent Skill context-loading size."
    )
    parser.add_argument("skill_root", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-entry-lines", type=int, default=500)
    args = parser.parse_args()
    root = args.skill_root.resolve()
    skill = root / "SKILL.md"
    if not skill.is_file():
        print("ERROR: missing SKILL.md")
        return 1

    entry = metrics(skill)
    workflows = markdown_resources(root, "workflows")
    references = markdown_resources(root, "references")
    report = {
        "entry": {**entry, "path": "SKILL.md"},
        "workflows": [
            {**item, "path": Path(str(item["path"])).name} for item in workflows
        ],
        "references": [
            {**item, "path": Path(str(item["path"])).name} for item in references
        ],
        "warnings": [],
    }
    if int(entry["lines"]) > args.max_entry_lines:
        report["warnings"].append(f"SKILL.md exceeds {args.max_entry_lines} lines")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"SKILL.md: {entry['lines']} lines, {entry['words']} words, "
            f"{entry['bytes']} bytes"
        )
        for group in ("workflows", "references"):
            for item in sorted(
                report[group], key=lambda row: int(row["bytes"]), reverse=True
            ):
                label = "workflow" if group == "workflows" else "reference"
                print(
                    f"{label} {item['path']}: {item['lines']} lines, "
                    f"{item['bytes']} bytes"
                )
        for warning in report["warnings"]:
            print(f"WARN: {warning}")
    return 0 if not report["warnings"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
