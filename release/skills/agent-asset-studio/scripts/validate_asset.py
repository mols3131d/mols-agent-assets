#!/usr/bin/env python3
"""Agent Skills 및 다양한 에이전트 자산의 구조와 기본 품질 기준을 검증한다."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from core.factory import AssetFactory


def main(argv: Sequence[str]) -> int:
    """명령행 진입점."""
    parser = argparse.ArgumentParser(
        description="에이전트 자산의 구조와 품질 기준을 검증한다."
    )
    parser.add_argument("asset_dir", help="검증할 자산 디렉터리 경로")
    parser.add_argument(
        "--type",
        choices=["skill", "rule", "agent"],
        default="skill",
        help="검증할 자산 유형 (기본값: skill)",
    )

    args = parser.parse_args(argv[1:])
    asset_dir: Path = Path(args.asset_dir).resolve()

    try:
        # 팩토리 패턴을 사용해 자산 객체 로드
        asset = AssetFactory.load_asset(args.type, asset_dir)

        # 자산 검증기 파이프라인(Validation Pipeline) 실행
        results = []
        for validator in asset.get_validators():
            results.extend(validator.validate(asset))

        has_error = any(result.level == "error" for result in results)
        payload = {
            "status": "fail" if has_error else "pass",
            "results": [result.to_dict() for result in results],
        }
    except Exception as exc:
        payload = {
            "status": "error",
            "results": [
                {
                    "level": "error",
                    "code": "runtime_error",
                    "message": str(exc),
                }
            ],
        }
        has_error = True

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
