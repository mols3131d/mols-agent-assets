#!/usr/bin/env python3
"""Deterministically validate reusable Agent Assets through Rulesync.

Run read-only checks against ``src/rulesync`` to verify the Rulesync
configuration, the repository's configured projections, and the projections
selected by each asset's declared targets. Generation checks use ``--dry-run``;
``--targets '*'`` broadens the target surface considered by Rulesync but does
not override an asset's own target declaration.

Treat every non-success JSON result and every Rulesync warning as a validation
failure. Schema parsing, source loading, and target-adapter semantics remain
owned by Rulesync rather than being reimplemented here. This validator does not
claim to assess semantic quality, routing quality, or runtime behavior.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "src" / "rulesync"


@dataclass(frozen=True)
class Check:
    name: str
    args: tuple[str, ...]


CHECKS = (
    Check("config", ("doctor", "--strict")),
    Check("configured-projection", ("generate", "--dry-run")),
    Check("declared-targets", ("generate", "--dry-run", "--targets", "*")),
)

Runner = Callable[[tuple[str, ...]], subprocess.CompletedProcess[str]]


class ValidationFailure(RuntimeError):
    """Raised when a Rulesync validation check is not clean."""


def rulesync_command() -> str:
    rulesync = shutil.which("rulesync")
    if rulesync is None:
        raise RuntimeError("rulesync is required; install repository tools with mise")
    return rulesync


def run_rulesync(args: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [rulesync_command(), "--json", *args],
        cwd=WORKSPACE,
        check=False,
        capture_output=True,
        text=True,
    )


def parse_payload(stdout: str) -> dict[str, Any]:
    if not stdout.strip():
        raise ValidationFailure("Rulesync returned no JSON output")
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValidationFailure("Rulesync returned invalid JSON output") from exc
    if not isinstance(payload, dict):
        raise ValidationFailure("Rulesync JSON output must be an object")
    return payload


def warnings_from(payload: dict[str, Any]) -> list[str]:
    warnings = payload.get("warnings", [])
    if warnings is None:
        return []
    if not isinstance(warnings, list) or not all(isinstance(item, str) for item in warnings):
        raise ValidationFailure("Rulesync JSON warnings must be a string array")
    return warnings


def failure_message(payload: dict[str, Any], stderr: str) -> str:
    error = payload.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if isinstance(message, str) and message:
            return message
        code = error.get("code")
        if isinstance(code, str) and code:
            return code
    if isinstance(error, str) and error:
        return error
    if stderr.strip():
        return stderr.strip()
    return "Rulesync command failed"


def validate_result(result: subprocess.CompletedProcess[str]) -> None:
    try:
        payload = parse_payload(result.stdout)
    except ValidationFailure:
        if result.returncode != 0 and result.stderr.strip():
            raise ValidationFailure(result.stderr.strip()) from None
        raise

    if result.returncode != 0:
        raise ValidationFailure(failure_message(payload, result.stderr))

    warnings = warnings_from(payload)
    if warnings:
        rendered = "\n".join(f"  - {warning}" for warning in warnings)
        raise ValidationFailure(f"Rulesync reported warnings:\n{rendered}")

    if payload.get("success") is not True:
        raise ValidationFailure(failure_message(payload, result.stderr))


def validate(runner: Runner = run_rulesync) -> int:
    failed = False
    for check in CHECKS:
        try:
            validate_result(runner(check.args))
        except (OSError, RuntimeError, ValidationFailure) as exc:
            failed = True
            print(f"FAIL {check.name}: {exc}", file=sys.stderr)
        else:
            print(f"PASS {check.name}")
    return 1 if failed else 0


def main() -> int:
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
