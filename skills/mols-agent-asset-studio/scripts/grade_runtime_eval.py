from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def grade(
    cases: list[dict[str, Any]], results: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    expected = {item["id"]: item for item in cases}
    observed = {
        item.get("id"): item
        for item in results.get("cases", [])
        if isinstance(item, dict)
    }
    missing: list[str] = []
    tp = tn = fp = fn = 0
    for case_id, case in expected.items():
        item = observed.get(case_id)
        if item is None or not isinstance(item.get("activated"), bool):
            missing.append(case_id)
            continue
        actual = item["activated"]
        wanted = case["should_trigger"]
        if actual and wanted:
            tp += 1
        elif actual and not wanted:
            fp += 1
        elif not actual and wanted:
            fn += 1
        else:
            tn += 1
    evaluated = tp + tn + fp + fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / evaluated if evaluated else 0.0
    return {
        "runtime": results.get("runtime"),
        "runtime_version": results.get("runtime_version"),
        "configuration": results.get("configuration"),
        "total_cases": len(cases),
        "evaluated_cases": evaluated,
        "missing_cases": missing,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
    }, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Grade observed runtime activation results and compare a baseline."
    )
    parser.add_argument("cases", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = load(args.cases)
    candidate, candidate_missing = grade(cases, load(args.candidate))
    report: dict[str, Any] = {
        "candidate": candidate,
        "status": "Pass" if not candidate_missing else "Deferred",
    }
    if args.baseline:
        baseline, baseline_missing = grade(cases, load(args.baseline))
        report["baseline"] = baseline
        report["delta"] = {
            metric: round(candidate[metric] - baseline[metric], 4)
            for metric in ("precision", "recall", "f1", "accuracy")
        }
        if baseline_missing:
            report["status"] = "Deferred"
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if report["status"] == "Deferred":
        print("DEFERRED: runtime results are incomplete")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
