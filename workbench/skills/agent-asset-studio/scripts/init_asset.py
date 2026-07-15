#!/usr/bin/env python3
"""Agent Skills 및 다양한 에이전트 자산 디렉터리를 초기화한다."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from configs import common
from core.base import AssetInitOptions
from core.factory import AssetFactory


def parse_metadata(raw_items: Sequence[str]) -> dict[str, str]:
    """key=value 형식 metadata 인자를 파싱한다."""
    metadata: dict[str, str] = {}
    for item in raw_items:
        if "=" not in item:
            raise ValueError(f"metadata는 key=value 형식이어야 합니다: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"metadata key가 비어 있습니다: {item}")
        metadata[key] = value
    return metadata


def parse_resources_str(raw_resources: str) -> list[str]:
    """쉼표로 구분된 리소스 문자열을 리스트로 파싱한다."""
    if not raw_resources:
        return []
    return [item.strip() for item in raw_resources.split(",") if item.strip()]


def main(argv: Sequence[str] | None = None) -> int:
    """명령행 진입점."""
    parser = argparse.ArgumentParser(
        description=(
            "Agent Skills 표준 규격을 충족하는 에이전트 자산 디렉터리를 초기화한다."
        ),
    )
    parser.add_argument("name", help="생성할 자산 이름. kebab-case로 정규화된다.")
    parser.add_argument(
        "--type",
        choices=["skill", "rule", "agent"],
        default="skill",
        help="생성할 자산 유형 (기본값: skill)",
    )
    parser.add_argument("--path", required=True, help="자산 폴더를 만들 상위 디렉터리")
    parser.add_argument(
        "--description",
        help="frontmatter description 값. 생략하면 자산별 기본 placeholder를 사용한다.",
    )
    parser.add_argument(
        "--resources",
        default="",
        help="생성할 리소스 디렉터리. 예: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="선택한 리소스 디렉터리에 예시 파일을 함께 생성한다.",
    )
    parser.add_argument(
        "--license", dest="license_value", help="frontmatter license 값"
    )
    parser.add_argument("--compatibility", help="frontmatter compatibility 값")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        help="frontmatter metadata 항목. key=value 형식으로 반복 지정 가능",
    )
    parser.add_argument(
        "--allowed-tools", help="frontmatter allowed-tools 값 (스킬 한정)"
    )
    parser.add_argument(
        "--routing-skill",
        action="store_true",
        help=(
            "스킬 생성 시 루트 INDEX.csv와 workflows/를 사용하는 라우팅 "
            "스킬 템플릿을 적용한다."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="파일을 만들지 않고 생성 계획만 JSON으로 출력한다.",
    )

    args = parser.parse_args(argv)

    try:
        resources = parse_resources_str(args.resources)
        metadata = parse_metadata(args.metadata)

        # 팩토리 패턴을 통해 OOP 자산 클래스 인스턴스화
        parent_dir = Path(args.path)
        asset = AssetFactory.create_asset(args.type, args.name, parent_dir)

        # 기본 설명란 설정
        description = (
            args.description if args.description else asset.config.DEFAULT_DESCRIPTION
        )

        # 리소스 적합성 교차 체크
        invalid = sorted({r for r in resources if r not in common.ALLOWED_RESOURCES})
        if invalid:
            allowed = ", ".join(sorted(common.ALLOWED_RESOURCES))
            raise ValueError(
                f"알 수 없는 리소스 유형: {', '.join(invalid)}. 허용값: {allowed}"
            )

        if args.examples and not resources:
            raise ValueError("--examples는 --resources와 함께 사용해야 합니다.")

        if args.routing_skill and args.type != "skill":
            raise ValueError("--routing-skill은 --type skill에서만 사용할 수 있습니다.")

        # 자산별 생성 로직 위임 호출
        options = AssetInitOptions(
            resources=resources,
            include_examples=args.examples,
            description=description,
            license_val=args.license_value,
            compatibility=args.compatibility,
            metadata=metadata,
            allowed_tools=args.allowed_tools,
            dry_run=args.dry_run,
            routing_skill=args.routing_skill,
        )
        payload = asset.initialize(options)

    except (OSError, ValueError) as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
