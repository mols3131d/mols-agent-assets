from __future__ import annotations

import argparse
import itertools
import re
from pathlib import Path

from asset_common import load_frontmatter

WORDS = re.compile(r"[a-z0-9가-힣]{2,}")
STOP = {
    "use",
    "when",
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "does",
    "not",
}


def tokens(text: str) -> set[str]:
    return {w for w in WORDS.findall(text.lower()) if w not in STOP}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristically flag overlapping skill descriptions."
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--threshold", type=float, default=0.35)
    args = parser.parse_args()

    skills = []
    for path in args.root.resolve().rglob("SKILL.md"):
        if path.is_symlink() or any(
            part in {".git", ".venv", "__pycache__", "node_modules"}
            for part in path.parts
        ):
            continue
        try:
            fm, _ = load_frontmatter(path)
        except Exception:
            continue
        desc = fm.get("description")
        name = fm.get("name", path.parent.name)
        if isinstance(desc, str):
            skills.append((str(name), path, tokens(desc)))

    found = False
    for (name_a, path_a, a), (name_b, path_b, b) in itertools.combinations(skills, 2):
        union = a | b
        score = len(a & b) / len(union) if union else 0.0
        if score >= args.threshold:
            found = True
            print(f"WARN {score:.2f}: {name_a} <-> {name_b}")
            print(f"  {path_a}")
            print(f"  {path_b}")
    if not found:
        print("PASS: no lexical overlap above threshold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
