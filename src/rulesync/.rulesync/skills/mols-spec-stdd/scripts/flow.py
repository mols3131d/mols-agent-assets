#!/usr/bin/env python3
"""Read-only validation and review routing for the bundled spec workflow."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKFLOW = PACKAGE_ROOT / "assets" / "workflows" / "default.json"
ARTIFACT_REGISTRY = PACKAGE_ROOT / "assets" / "artifacts.json"
IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class ContractError(ValueError):
    """Invalid input contract; never treat an unverified input as successful."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"unable to read JSON from {path}: {exc}") from exc


def require_text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{where} must be a nonempty string")
    return value.strip()


def require_ref_list(value: Any, where: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ContractError(f"{where} must be {'a nonempty' if nonempty else 'a'} list")
    refs = [require_text(entry, f"{where}[{index}]") for index, entry in enumerate(value)]
    if len(refs) != len(set(refs)):
        raise ContractError(f"{where} has duplicate entries")
    return refs


def load_artifacts() -> dict[str, dict[str, str]]:
    data = read_json(ARTIFACT_REGISTRY)
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ContractError("artifact registry must have version 1")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ContractError("artifact registry needs an artifacts mapping")
    for name, artifact in artifacts.items():
        if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
            raise ContractError(f"invalid artifact ID: {name!r}")
        if not isinstance(artifact, dict) or artifact.get("kind") not in {"document", "code"}:
            raise ContractError(f"artifact {name}: kind must be document or code")
        if artifact["kind"] == "document":
            filename = require_text(artifact.get("default_file"), f"artifact {name}.default_file")
            path = Path(filename)
            if path.is_absolute() or ".." in path.parts or path.suffix != ".md":
                raise ContractError(f"artifact {name}: unsafe default_file")
            template = require_text(artifact.get("template"), f"artifact {name}.template")
            template_path = Path(template)
            if template_path.is_absolute() or ".." in template_path.parts or template_path.suffix != ".md":
                raise ContractError(f"artifact {name}: unsafe template")
            if not (PACKAGE_ROOT / "assets" / template_path).is_file():
                raise ContractError(f"artifact {name}: missing template {template}")
    return artifacts


def load_workflow(path: Path) -> dict[str, Any]:
    artifacts = load_artifacts()
    data = read_json(path)
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ContractError("workflow must have version 1")
    require_text(data.get("name"), "workflow.name")
    steps = data.get("steps")
    if not isinstance(steps, list) or len(steps) < 2:
        raise ContractError("workflow.steps must have at least two steps")

    seen: set[str] = set()
    produced: set[str] = set()
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise ContractError(f"steps[{index}] must be an object")
        name = require_text(step.get("id"), f"steps[{index}].id")
        if not IDENTIFIER.fullmatch(name) or name in seen:
            raise ContractError(f"invalid or duplicate step ID: {name}")
        after = require_ref_list(step.get("after"), f"step {name}.after")
        missing = [ref for ref in after if ref not in seen]
        if missing:
            raise ContractError(f"step {name}: dependency not earlier in workflow: {missing}")
        targets = require_ref_list(step.get("artifacts"), f"step {name}.artifacts")
        unknown = [ref for ref in targets if ref not in artifacts]
        if unknown:
            raise ContractError(f"step {name}: unknown artifacts: {unknown}")
        if name == "review":
            if index != len(steps) - 1 or targets:
                raise ContractError("review must be last and must not produce artifacts")
        elif index == len(steps) - 1:
            raise ContractError("review must be the last step")
        produced.update(targets)
        seen.add(name)
    if "specification" not in produced:
        raise ContractError("workflow must include the specification artifact")
    return data


def route_review(workflow: dict[str, Any], report: Any) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ContractError("review report must be an object")
    result = report.get("result")
    if result == "pass":
        evidence = require_ref_list(report.get("evidence"), "review.evidence", nonempty=True)
        if report.get("findings"):
            raise ContractError("pass review cannot contain findings")
        return {
            "status": "candidate_complete",
            "evidence_refs": evidence,
            "warning": "Evidence references are not validated or executed by this script",
        }
    if result == "blocked":
        return {"status": "blocked", "reason": require_text(report.get("reason"), "review.reason")}
    if result != "rework":
        raise ContractError("review.result must be pass, rework, or blocked")

    findings = report.get("findings")
    if not isinstance(findings, list) or not findings:
        raise ContractError("rework requires nonempty findings")
    steps = workflow["steps"]
    order = [step["id"] for step in steps]
    children: dict[str, set[str]] = {name: set() for name in order}
    for step in steps:
        for dependency in step["after"]:
            children[dependency].add(step["id"])
    targets = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ContractError(f"findings[{index}] must be an object")
        target = require_text(finding.get("target"), f"findings[{index}].target")
        if target not in children or target == "review":
            raise ContractError(f"findings[{index}]: unknown or invalid target {target}")
        require_text(finding.get("issue"), f"findings[{index}].issue")
        require_ref_list(finding.get("evidence"), f"findings[{index}].evidence", nonempty=True)
        targets.add(target)

    pending = list(targets)
    recheck = set(targets)
    while pending:
        current = pending.pop()
        for dependent in children[current] - recheck:
            recheck.add(dependent)
            pending.append(dependent)
    recheck.add("review")
    return {
        "status": "rework",
        "return_to": next(name for name in order if name in targets),
        "recheck_steps": [name for name in order if name in recheck],
        "warning": "Recheck means inspect impact, not automatically rewrite every artifact",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check artifact registry and workflow structure")
    route = commands.add_parser("route", help="route a review report without changing files")
    route.add_argument("--review", required=True, type=Path, help="review JSON file")
    args = parser.parse_args(argv)
    try:
        workflow = load_workflow(args.workflow)
        if args.command == "validate":
            result = {"valid": True, "workflow": workflow["name"], "steps": [s["id"] for s in workflow["steps"]]}
        else:
            result = route_review(workflow, read_json(args.review))
    except ContractError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
