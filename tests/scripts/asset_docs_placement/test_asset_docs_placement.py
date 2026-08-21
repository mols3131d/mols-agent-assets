from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"
TARGETED_TESTS = ROOT / ".github" / "workflows" / "targeted-tests.yml"
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


def test_skill_doc_capsules_have_skill_or_family_owner() -> None:
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
        assert any(name in body for name in skill_names), (
            f"family docs must name at least one current Skill: {capsule.name}"
        )


def test_skill_packages_exclude_repository_verification_surfaces() -> None:
    forbidden = {"tests", "evals", "scenarios", "results"}
    for skill in SKILLS.iterdir():
        if not skill.is_dir():
            continue
        assert {path.name for path in skill.iterdir() if path.is_dir()}.isdisjoint(
            forbidden
        ), skill.name


def test_skill_verification_assets_live_outside_packages() -> None:
    expected = [
        ROOT / "tests/skills/artifact-consistency-inspector/test_contract.py",
        ROOT / "tests/skills/artifact-consistency-inspector/scenarios",
        ROOT / "tests/skills/mols-agent-asset/test_contract.py",
        ROOT / "tests/skills/mols-agent-asset-validator/test_scan_assets.py",
        ROOT / "tests/skills/mols-markdown-dashboard/test_render.py",
        ROOT / "evals/skills/mols-agent-asset/cases.json",
        ROOT / "evals/skills/mols-agent-asset-validator",
    ]
    assert all(path.exists() for path in expected)


def test_migrated_maintainer_docs_exist_outside_packages() -> None:
    expected = [
        ROOT / "docs/skills/artifact-consistency-inspector/customization.md",
        ROOT / "docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md",
    ]
    assert all(path.is_file() for path in expected)


def test_pr_gate_covers_repository_tests_and_eval_smoke() -> None:
    workflow = TARGETED_TESTS.read_text(encoding="utf-8")
    assert "name: PR Gate" in workflow
    assert "pytest -q tests" in workflow
    assert "src/rulesync/.rulesync/skills/mols-rpi/*" in workflow
    assert "evals/skills/mols-rpi/*" in workflow
    assert "npm run eval:promptfoo:mols-rpi:smoke" in workflow
