"""Commit되는 projection을 재생성하고 pre-commit에서 영향받는 output을 stage한다."""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from scripts import indexes_generate

ROOT = Path(__file__).resolve().parents[1]

_DOCS_INDEX_TOOL_SOURCES = {"scripts/indexes_generate.py"}
_DOCS_INDEX_TOOL_PREFIX = (
    "src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/"
)


class GeneratedArtifactSyncError(RuntimeError):
    """Generated projection을 안전하게 동기화할 수 없을 때 사용한다."""


@dataclass(frozen=True)
class Projection:
    """하나의 committed projection과 이를 소유하는 source surface를 묶는다."""

    name: str
    source_matches: Callable[[str], bool]
    output_matches: Callable[[str], bool]
    generate: Callable[[], None]

    def is_relevant(self, path: str) -> bool:
        return self.source_matches(path) or self.output_matches(path)


def _is_docs_index_source(path: str) -> bool:
    if path in _DOCS_INDEX_TOOL_SOURCES:
        return True
    if path.startswith(_DOCS_INDEX_TOOL_PREFIX) and path.endswith(".py"):
        return True
    if not path.startswith("docs/") or not path.endswith(".md"):
        return False

    name = PurePosixPath(path).name
    if name in {"README.md", "index.md"}:
        return True
    if name == "AGENTS.md" or name.startswith("."):
        return False
    if name.startswith("INDEX") or name.startswith("__index__"):
        return False
    if name.startswith("__") and name.endswith("__.md"):
        return False
    return True


def _is_docs_index_output(path: str) -> bool:
    return path == "docs/INDEX.tsv" or (
        path.startswith("docs/") and path.endswith("/INDEX.tsv")
    )


def _is_catalog_index_source(path: str) -> bool:
    if path == "scripts/indexes_generate.py":
        return True
    if path.startswith(_DOCS_INDEX_TOOL_PREFIX) and path.endswith(".py"):
        return True
    if not path.startswith("catalog/") or not path.endswith((".md", ".json")):
        return False

    name = PurePosixPath(path).name
    if name == "README.md":
        return True
    if name == "AGENTS.md" or (name.startswith(".") and name.endswith(".md")):
        return False
    if name.startswith("INDEX") or name.startswith("__index__"):
        return False
    if name.startswith("__") and name.endswith("__.md"):
        return False
    return True


def _is_catalog_index_output(path: str) -> bool:
    return path == "catalog/INDEX.tsv" or (
        path.startswith("catalog/") and path.endswith("/INDEX.tsv")
    )


def _generate_docs_indexes() -> None:
    indexes_generate.sync_indexes(indexes_generate.PRESETS["docs"])


def _generate_catalog_index() -> None:
    indexes_generate.sync_indexes(indexes_generate.PRESETS["catalog"])


PROJECTIONS = (
    Projection(
        name="docs-indexes",
        source_matches=_is_docs_index_source,
        output_matches=_is_docs_index_output,
        generate=_generate_docs_indexes,
    ),
    Projection(
        name="catalog-indexes",
        source_matches=_is_catalog_index_source,
        output_matches=_is_catalog_index_output,
        generate=_generate_catalog_index,
    ),

)


def _git_paths(*args: str, root: Path = ROOT) -> set[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    return {
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    }


def staged_paths(root: Path = ROOT) -> set[str]:
    return _git_paths(
        "diff",
        "--cached",
        "--name-only",
        "--no-renames",
        "--diff-filter=ACMRD",
        "-z",
        "--",
        root=root,
    )


def dirty_worktree_paths(root: Path = ROOT) -> set[str]:
    tracked = _git_paths(
        "diff",
        "--name-only",
        "--no-renames",
        "--diff-filter=ACMRD",
        "-z",
        "--",
        root=root,
    )
    untracked = _git_paths(
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        root=root,
    )
    return tracked | untracked


def select_projections(
    paths: Iterable[str],
    projections: tuple[Projection, ...] = PROJECTIONS,
) -> tuple[Projection, ...]:
    path_set = set(paths)
    return tuple(
        projection
        for projection in projections
        if any(projection.is_relevant(path) for path in path_set)
    )


def conflicting_paths(
    dirty_paths: Iterable[str],
    projections: Iterable[Projection],
) -> dict[str, list[str]]:
    dirty = set(dirty_paths)
    conflicts: dict[str, list[str]] = {}
    for projection in projections:
        paths = sorted(path for path in dirty if projection.is_relevant(path))
        if paths:
            conflicts[projection.name] = paths
    return conflicts


def _stage_projection_outputs(
    projection: Projection,
    root: Path = ROOT,
) -> None:
    candidates = _git_paths(
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        root=root,
    )
    outputs = sorted(path for path in candidates if projection.output_matches(path))
    if not outputs:
        return

    subprocess.run(
        ["git", "add", "-A", "--", *outputs],
        cwd=root,
        check=True,
    )


def sync_staged(
    root: Path = ROOT,
    projections: tuple[Projection, ...] = PROJECTIONS,
) -> tuple[str, ...]:
    affected = select_projections(staged_paths(root), projections)
    if not affected:
        return ()

    conflicts = conflicting_paths(dirty_worktree_paths(root), affected)
    if conflicts:
        details = "\n".join(
            f"- {name}: {', '.join(paths)}" for name, paths in conflicts.items()
        )
        raise GeneratedArtifactSyncError(
            "관련 source 또는 generated output에 unstaged/untracked 변경이 있어 "
            "자동 동기화를 중단합니다.\n"
            f"{details}\n"
            "해당 변경을 stage하거나 분리한 뒤 다시 commit하세요."
        )

    for projection in affected:
        projection.generate()
    for projection in affected:
        _stage_projection_outputs(projection, root)

    return tuple(projection.name for projection in affected)


def sync_all(
    projections: tuple[Projection, ...] = PROJECTIONS,
) -> tuple[str, ...]:
    for projection in projections:
        projection.generate()
    return tuple(projection.name for projection in projections)
