#!/usr/bin/env python3
"""workbench 자산 하나를 동일한 상대 경로의 src로 승격한다.

기존 src는 ``.tmp/src``로 이동하고 새 자산으로 완전히 교체한다. workbench 원본은
유지하며, 성공 결과 또는 오류를 JSON으로 출력한다.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]


def resolve_paths(source_arg: str, repo_root: Path) -> tuple[Path, Path, Path]:
    """입력 경로를 검증하고 source, src destination, archive 경로를 반환한다.

    source는 workbench 내부의 파일 또는 디렉터리여야 한다.
    """
    root = repo_root.resolve()
    workbench = (root / "workbench").resolve()
    src = (root / "src").resolve()
    archive_root = (root / ".tmp" / "src").resolve()
    raw_source = Path(source_arg)

    if raw_source.is_absolute():
        source = raw_source.resolve()
    elif raw_source.parts and raw_source.parts[0] == "workbench":
        source = (root / raw_source).resolve()
    else:
        source = (workbench / raw_source).resolve()

    try:
        relative = source.relative_to(workbench)
    except ValueError as exc:
        raise ValueError(f"source는 workbench 내부여야 합니다: {source}") from exc

    if relative == Path("."):
        raise ValueError("workbench 전체는 승격할 수 없습니다. 하위 경로를 지정하세요.")
    if not source.exists():
        raise FileNotFoundError(f"source가 없습니다: {source}")
    if not source.is_file() and not source.is_dir():
        raise ValueError(f"source는 파일 또는 디렉터리여야 합니다: {source}")

    destination = (src / relative).resolve()
    archive = (archive_root / relative).resolve()
    for path, parent, label in (
        (destination, src, "destination"),
        (archive, archive_root, "archive"),
    ):
        try:
            path.relative_to(parent)
        except ValueError as exc:
            raise ValueError(f"{label} 경로가 허용 범위를 벗어납니다: {path}") from exc
    return source, destination, archive


def copy_to_staging(source: Path, staging: Path) -> None:
    """기존 src를 변경하기 전에 source 전체를 staging에 복사한다."""
    if source.is_dir():
        shutil.copytree(source, staging)
    else:
        shutil.copy2(source, staging)


def remove_path(path: Path) -> None:
    """파일·링크를 삭제하거나 디렉터리를 재귀적으로 삭제한다."""
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def promote(
    source_arg: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """기존 src를 archive로 이동하고 workbench 자산으로 완전히 교체한다.

    최종 교체 실패 시 가능한 경우 기존 src를 복구하고, 결과를 dict로 반환한다.
    """
    source, destination, archive = resolve_paths(source_arg, repo_root)
    archived = destination.exists()

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{destination.name}.promote-", dir=destination.parent
    ) as temp_dir:
        staging = Path(temp_dir) / destination.name
        copy_to_staging(source, staging)

        if archived:
            archive.parent.mkdir(parents=True, exist_ok=True)
            if archive.exists() or archive.is_symlink():
                remove_path(archive)
            shutil.move(str(destination), str(archive))

        try:
            staging.replace(destination)
        except OSError:
            if archived and archive.exists() and not destination.exists():
                shutil.move(str(archive), str(destination))
            raise

    return {
        "status": "copied",
        "source": str(source),
        "destination": str(destination),
        "archive": str(archive) if archived else None,
    }


def build_parser() -> argparse.ArgumentParser:
    """필수 source 인자를 받는 CLI 파서를 생성한다."""
    parser = argparse.ArgumentParser(
        description=(
            "기존 src/<path>를 .tmp/src/<path>로 이동한 뒤 "
            "workbench/<path>를 src/<path>로 복사합니다."
        )
    )
    parser.add_argument(
        "source",
        help="workbench 기준 상대 경로 또는 workbench 내부 경로",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """승격 결과를 JSON으로 출력하고 성공 시 0, 오류 시 1을 반환한다."""
    args = build_parser().parse_args(argv)
    try:
        result = promote(args.source)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
