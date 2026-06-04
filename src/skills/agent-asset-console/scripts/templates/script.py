from typing import Final

EXAMPLE_SCRIPT: Final[str] = '''#!/usr/bin/env python3
"""예시 스크립트. 실제 로직으로 교체하거나 삭제한다."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence


def build_parser() -> argparse.ArgumentParser:
    """명령행 인자를 정의한다."""
    parser = argparse.ArgumentParser(description="예시 입력을 JSON으로 요약한다.")
    parser.add_argument("value", help="요약할 값")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """명령행 진입점."""
    args = build_parser().parse_args(argv)
    payload: dict[str, Any] = {"value": args.value, "length": len(args.value)}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
