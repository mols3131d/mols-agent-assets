from __future__ import annotations

import argparse
import itertools
import json
import re
from pathlib import Path

from asset_common import load_frontmatter

WORD_RE = re.compile(r"[a-z0-9가-힣]{2,}")
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
    return {word for word in WORD_RE.findall(text.lower()) if word not in STOP}


def domain_prefix(name: str) -> str:
    return name.split("-", 1)[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate review candidates for skill consolidation."
    )
    parser.add_argument("skills_root", type=Path)
    parser.add_argument("--threshold", type=float, default=0.20)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = []
    for path in sorted(args.skills_root.resolve().rglob("SKILL.md")):
        if path.is_symlink() or any(
            part in {".git", "__pycache__", ".venv", "node_modules"}
            for part in path.parts
        ):
            continue
        try:
            fm, _ = load_frontmatter(path)
        except Exception:
            continue
        name = fm.get("name")
        description = fm.get("description")
        if isinstance(name, str) and isinstance(description, str):
            rows.append(
                {
                    "name": name,
                    "path": path.parent.as_posix(),
                    "tokens": tokens(description),
                }
            )

    candidates = []
    for left, right in itertools.combinations(rows, 2):
        union = left["tokens"] | right["tokens"]
        lexical = len(left["tokens"] & right["tokens"]) / len(union) if union else 0.0
        same_domain = domain_prefix(left["name"]) == domain_prefix(right["name"])
        score = lexical + (0.15 if same_domain else 0.0)
        if score < args.threshold:
            continue
        candidates.append(
            {
                "left": left["name"],
                "right": right["name"],
                "lexical_score": round(lexical, 3),
                "same_domain_prefix": same_domain,
                "review_score": round(score, 3),
                "decision": (
                    "Review: Merge | Compose | Route | Keep separate | Deprecate"
                ),
                "required_evidence": [
                    "authority",
                    "owner",
                    "runtime",
                    "safety",
                    "release_lifecycle",
                    "behavior_cases",
                ],
            }
        )
    candidates.sort(key=lambda row: (-row["review_score"], row["left"], row["right"]))

    if args.format == "json":
        output = (
            json.dumps(
                {"candidates": candidates, "automatic_merge": False},
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
    else:
        lines = [
            "| Left | Right | Lexical | Domain | Review score | Decision |",
            "|---|---|---:|:---:|---:|---|",
        ]
        lines.extend(
            f"| `{row['left']}` | `{row['right']}` | {row['lexical_score']:.3f} | "
            f"{'yes' if row['same_domain_prefix'] else 'no'} | "
            f"{row['review_score']:.3f} | Review required |"
            for row in candidates
        )
        if not candidates:
            lines.append("| — | — | — | — | — | No candidates above threshold |")
        output = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
