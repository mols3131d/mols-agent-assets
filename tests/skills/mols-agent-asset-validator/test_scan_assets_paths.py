from __future__ import annotations

import json
import sys
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

from scan_assets import output_mutates_target, scan_directory, scan_target  # noqa: E402


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_canonical_subagent_is_classified_and_validated(tmp_path: Path) -> None:
    write(
        tmp_path / "subagents/review.md",
        "---\nname: review\ndescription: Review.\n---\n\n# Review\n",
    )

    result = scan_directory(tmp_path)

    assert result["asset_counts"]["subagent"] == 1
    assert not any(item["category"] == "frontmatter" for item in result["findings"])


def test_subagent_without_frontmatter_is_major(tmp_path: Path) -> None:
    write(tmp_path / "subagents/review.md", "# Review\n")

    result = scan_directory(tmp_path)

    assert any(
        item["category"] == "frontmatter" and item["path"] == "subagents/review.md"
        for item in result["findings"]
    )
    assert result["summary"]["disposition"] == "revise"


def test_classification_ignores_parent_directories_outside_target(tmp_path: Path) -> None:
    root = tmp_path / "tests/package"
    write(root / "config.json", "{}\n")

    result = scan_directory(root)

    assert result["asset_counts"] == {"config": 1}


def test_reference_frontmatter_name_does_not_collide_with_skill_identity(tmp_path: Path) -> None:
    write(tmp_path / "SKILL.md", "---\nname: shared\ndescription: Skill.\n---\n\n# Skill\n")
    write(
        tmp_path / "references/note.md",
        "---\nname: shared\ndescription: Note.\n---\n\n# Note\n",
    )

    result = scan_directory(tmp_path)

    assert not any(
        item["category"] == "identity" and "duplicate" in item["message"]
        for item in result["findings"]
    )


def test_identity_names_are_scoped_by_asset_type(tmp_path: Path) -> None:
    write(tmp_path / "SKILL.md", "---\nname: shared\ndescription: Skill.\n---\n\n# Skill\n")
    write(
        tmp_path / "subagents/shared.md",
        "---\nname: shared\ndescription: Subagent.\n---\n\n# Subagent\n",
    )

    result = scan_directory(tmp_path)

    assert not any(item["category"] == "identity" for item in result["findings"])


def test_agent_directory_document_is_not_forced_to_be_agent_identity(tmp_path: Path) -> None:
    write(tmp_path / "agents/README.md", "# Agents\n")

    result = scan_directory(tmp_path)

    assert not any(item["category"] == "frontmatter" for item in result["findings"])


def test_declared_subagent_path_is_tracked_as_relationship(tmp_path: Path) -> None:
    write(
        tmp_path / "subagents/review.md",
        "---\nname: review\ndescription: Review.\n---\n\n# Review\n",
    )
    write(
        tmp_path / "SKILL.md",
        "---\nname: example-skill\ndescription: Example.\n---\n\nUse `subagents/review.md`.\n",
    )

    result = scan_directory(tmp_path)

    assert any(
        item == {"from": "SKILL.md", "type": "reads", "to": "subagents/review.md"}
        for item in result["relationships"]
    )


def test_detected_secret_is_redacted_from_result(tmp_path: Path) -> None:
    token = "sk-" + "abcdefghijklmnopqrstuvwx"
    write(
        tmp_path / "SKILL.md",
        f"---\nname: secret-skill\ndescription: {token}\n---\n\n# Secret\n",
    )

    result = scan_directory(tmp_path)
    rendered = json.dumps(result)

    assert result["summary"]["critical"] == 1
    assert token not in rendered
    assert "[REDACTED]" in rendered


def test_single_file_target_is_scanned(tmp_path: Path) -> None:
    target = tmp_path / "SKILL.md"
    write(target, "---\nname: single-skill\ndescription: Single.\n---\n\n# Single\n")

    result = scan_target(target)

    assert result["summary"]["files"] == 1
    assert result["asset_counts"] == {"skill": 1}
    assert result["target"] == str(target)


def test_output_path_cannot_mutate_scanned_directory(tmp_path: Path) -> None:
    root = tmp_path / "package"
    root.mkdir()

    assert output_mutates_target(root / "scan.json", root)
    assert not output_mutates_target(tmp_path / "scan.json", root)


def test_output_path_cannot_overwrite_scanned_file(tmp_path: Path) -> None:
    target = tmp_path / "asset.zip"
    target.write_bytes(b"placeholder")

    assert output_mutates_target(target, target)
    assert not output_mutates_target(tmp_path / "scan.json", target)
