from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "rulesync"
    / ".rulesync"
    / "skills"
    / "mols-agent-asset-validator"
)
sys.path.insert(0, str(ROOT / "scripts"))

from scan_assets import scan_directory  # noqa: E402


def test_canonical_subagent_is_classified_and_validated() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "subagents").mkdir()
        (root / "subagents" / "review.md").write_text(
            "---\nname: review\ndescription: Review.\n---\n\n# Review\n",
            encoding="utf-8",
        )

        result = scan_directory(root)

        assert result["asset_counts"]["subagent"] == 1
        assert not any(
            item["category"] == "frontmatter" for item in result["findings"]
        )


def test_subagent_without_frontmatter_is_major() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "subagents").mkdir()
        (root / "subagents" / "review.md").write_text("# Review\n", encoding="utf-8")

        result = scan_directory(root)

        assert any(
            item["category"] == "frontmatter"
            and item["path"] == "subagents/review.md"
            for item in result["findings"]
        )
        assert result["summary"]["disposition"] == "revise"


def test_classification_ignores_parent_directories_outside_target() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "tests" / "package"
        root.mkdir(parents=True)
        (root / "config.json").write_text("{}\n", encoding="utf-8")

        result = scan_directory(root)

        assert result["asset_counts"] == {"config": 1}


def test_reference_frontmatter_name_does_not_collide_with_skill_identity() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "references").mkdir()
        (root / "SKILL.md").write_text(
            "---\nname: shared\ndescription: Skill.\n---\n\n# Skill\n",
            encoding="utf-8",
        )
        (root / "references" / "note.md").write_text(
            "---\nname: shared\ndescription: Note.\n---\n\n# Note\n",
            encoding="utf-8",
        )

        result = scan_directory(root)

        assert not any(
            item["category"] == "identity"
            and "duplicate frontmatter name" in item["message"]
            for item in result["findings"]
        )


def test_declared_subagent_path_is_tracked_as_relationship() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "subagents").mkdir()
        (root / "subagents" / "review.md").write_text(
            "---\nname: review\ndescription: Review.\n---\n\n# Review\n",
            encoding="utf-8",
        )
        (root / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Example.\n---\n\n"
            "Use `subagents/review.md`.\n",
            encoding="utf-8",
        )

        result = scan_directory(root)

        assert any(
            item["from"] == "SKILL.md"
            and item["type"] == "reads"
            and item["to"] == "subagents/review.md"
            for item in result["relationships"]
        )
