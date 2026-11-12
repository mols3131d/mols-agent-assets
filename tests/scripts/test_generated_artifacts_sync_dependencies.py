from __future__ import annotations

import pytest

from scripts import generated_artifacts_sync as sync


@pytest.mark.parametrize(
    "path",
    [
        "scripts/indexes_generate.py",
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
def test_shared_index_source_selects_both_projections(path: str) -> None:
    assert sync._is_docs_index_source(path)
    assert sync._is_catalog_index_source(path)


def test_index_sync_does_not_track_non_python_skill_support_files() -> None:
    path = (
        "src/rulesync/.rulesync/skills/mols-markdown-maintenance/"
        "scripts/README.md"
    )
    assert not sync._is_docs_index_source(path)
    assert not sync._is_catalog_index_source(path)
