from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"
RESERVED_DOC_NAMESPACES = {"development", "document", "references"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def iter_asset_capsules() -> list[Path]:
    capsules: list[Path] = []
    for asset_type in DOCS.iterdir():
        if not asset_type.is_dir() or asset_type.name in RESERVED_DOC_NAMESPACES:
            continue
        capsules.extend(path for path in asset_type.iterdir() if path.is_dir())
    return sorted(capsules)


def test_asset_capsules_keep_relative_links_inside_capsule() -> None:
    for capsule in iter_asset_capsules():
        root = capsule.resolve()
        for document in capsule.rglob("*.md"):
            for raw_target in MARKDOWN_LINK.findall(
                document.read_text(encoding="utf-8")
            ):
                target = raw_target.split("#", 1)[0].strip()
                if (
                    not target
                    or "://" in target
                    or target.startswith(("mailto:", "data:"))
                ):
                    continue
                resolved = (document.parent / target).resolve()
                assert resolved.is_relative_to(root), (
                    f"{document.relative_to(ROOT)} links outside its capsule: {raw_target}"
                )


def test_skill_doc_capsules_have_skill_or_documented_family_owner() -> None:
    skill_docs = DOCS / "skills"
    skill_names = {
        path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()
    }

    for capsule in skill_docs.iterdir():
        if not capsule.is_dir() or (SKILLS / capsule.name / "SKILL.md").is_file():
            continue

        readme = capsule / "README.md"
        assert readme.is_file(), f"family docs require README.md: {capsule.name}"
        body = readme.read_text(encoding="utf-8")
        assert "## Members" in body, f"family docs require Members: {capsule.name}"
        members = body.split("## Members", 1)[1].split("\n## ", 1)[0]
        assert any(f"`{name}`" in members for name in skill_names), (
            f"family Members must name at least one current Skill: {capsule.name}"
        )
