#!/usr/bin/env python3
"""Rulesync로 재사용 Agent Asset을 결정론적으로 검증한다.

``src/rulesync``를 대상으로 read-only 검증을 실행해 Rulesync 설정, 이 repository가
설정한 projection, 각 asset이 선언한 ``targets``에 따라 선택되는 projection을 확인한다.
생성 검증은 모두 ``--dry-run``을 사용한다. ``--targets '*'``는 Rulesync가 고려하는
대상 범위를 넓히지만 각 asset이 직접 선언한 target을 덮어쓰지 않는다.

Rulesync의 JSON 결과가 성공이 아니거나 warning이 하나라도 있으면 검증 실패로 본다.
schema parsing, source loading, target adapter semantics는 여기서 다시 구현하지 않고
Rulesync가 소유한다. 이 검증기는 semantic quality, routing quality, runtime behavior를
검증한다고 간주하지 않는다.
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
    """Rulesync 검증 결과가 repository의 통과 조건을 만족하지 않을 때 발생한다."""


def rulesync_command() -> str:
    rulesync = shutil.which("rulesync")
    if rulesync is None:
        raise RuntimeError("Rulesync가 필요합니다. mise로 repository 도구를 설치하세요.")
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
        raise ValidationFailure("Rulesync가 JSON 출력을 반환하지 않았습니다.")
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValidationFailure("Rulesync가 유효하지 않은 JSON을 반환했습니다.") from exc
    if not isinstance(payload, dict):
        raise ValidationFailure("Rulesync JSON 출력은 object여야 합니다.")
    return payload


def warnings_from(payload: dict[str, Any]) -> list[str]:
    warnings = payload.get("warnings", [])
    if warnings is None:
        return []
    if not isinstance(warnings, list) or not all(isinstance(item, str) for item in warnings):
        raise ValidationFailure("Rulesync JSON의 warnings는 string array여야 합니다.")
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
    return "Rulesync 명령이 실패했습니다."


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
        raise ValidationFailure(f"Rulesync가 warning을 보고했습니다:\n{rendered}")

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
