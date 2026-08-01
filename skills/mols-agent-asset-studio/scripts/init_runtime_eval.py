from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a fillable runtime evaluation result file."
    )
    parser.add_argument("cases", type=Path)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--runtime-version")
    parser.add_argument(
        "--configuration", choices=("candidate", "legacy", "baseline"), required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.cases.read_text(encoding="utf-8"))
    output = {
        "schema_version": 1,
        "runtime": args.runtime,
        "runtime_version": args.runtime_version,
        "configuration": args.configuration,
        "executed_at": None,
        "cases": [
            {
                "id": item["id"],
                "activated": None,
                "completed": None,
                "route": None,
                "evidence": None,
                "duration_ms": None,
                "total_tokens": None,
            }
            for item in data
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
