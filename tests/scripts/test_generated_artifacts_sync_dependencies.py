from __future__ import annotations

import pytest

from scripts import generated_artifacts_sync as sync


@pytest.mark.parametrize(
    "path",
    [
        (
            "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
            "scripts/generate_index.py"
        ),
        (
            "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
            "scripts/frontmatter.py"
        ),
        (
            "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
            "scripts/future_helper.py"
        ),
    ],
)
def test_docs_index_sync_tracks_generator_python_implementation(path: str) -> None:
    assert sync._is_docs_index_source(path)


def test_docs_index_sync_does_not_track_non_python_skill_support_files() -> None:
    path = (
        "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
        "scripts/README.md"
    )
    assert not sync._is_docs_index_source(path)


@pytest.mark.parametrize(
    "path",
    [
        "scripts/catalog_indexes_generate.py",
        "scripts/docs_indexes_generate.py",
        (
            "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
            "scripts/generate_index.py"
        ),
    ],
)
def test_catalog_index_tracks_all_implementation_dependencies(path: str) -> None:
    assert sync._is_catalog_index_source(path)
