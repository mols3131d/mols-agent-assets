"""mols-markdown-scripts 기능을 asset-studio 코드에 위임하는 adapter."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

MARKDOWN_SCRIPTS_DIR = (
    Path(__file__).resolve().parents[2] / "mols-markdown-scripts" / "scripts"
)


def _require_markdown_scripts() -> None:
    """공통 스크립트 의존성이 있는지 확인한다."""
    if not MARKDOWN_SCRIPTS_DIR.is_dir():
        raise RuntimeError(
            f"mols-markdown-scripts를 찾을 수 없습니다: {MARKDOWN_SCRIPTS_DIR}"
        )


_require_markdown_scripts()
if str(MARKDOWN_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(MARKDOWN_SCRIPTS_DIR))

from frontmatter import read_frontmatter  # noqa: E402
from generate_index import generate_index  # noqa: E402


def read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    """Markdown frontmatter와 본문을 읽는다."""
    parsed = read_frontmatter(path)
    if parsed is None:
        raise ValueError(f"유효한 YAML frontmatter가 없습니다: {path}")
    return parsed


def write_workflow_index(workflows_dir: Path, output_path: Path) -> None:
    """workflow frontmatter에서 name,description CSV를 생성한다."""
    workflows_dir.mkdir(parents=True, exist_ok=True)
    content = generate_index(
        workflows_dir,
        format="csv",
        fields=["name", "description"],
        globs=["*.md"],
        max_depth=0,
        required_fields=["name", "description"],
        unique_fields=["name"],
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        file.write(content)


__all__ = ["MARKDOWN_SCRIPTS_DIR", "read_markdown", "write_workflow_index"]
