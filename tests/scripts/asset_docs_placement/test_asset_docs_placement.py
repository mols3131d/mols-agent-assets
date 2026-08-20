from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"
CREATOR = SKILLS / "mols-skill-creator"
TARGETED_TESTS = ROOT / ".github" / "workflows" / "targeted-tests.yml"
RESERVED_DOC_NAMESPACES = {"development", "document", "references"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def run_package(skill: Path, output: Path) -> Path:
    result = subprocess.run(
        [
            sys.executable,
            str(CREATOR / "scripts/package_skill.py"),
            str(skill),
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return output / f"{skill.name}.zip"


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


def test_skill_doc_capsules_have_corresponding_skill_source() -> None:
    skill_docs = DOCS / "skills"
    for capsule in skill_docs.iterdir():
        if capsule.is_dir():
            assert (SKILLS / capsule.name / "SKILL.md").is_file(), capsule.name


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
        ROOT / "tests/skills/mols-agent-asset-validator/test_scan_assets.py",
        ROOT / "tests/skills/mols-markdown-dashboard/test_render.py",
        ROOT / "evals/skills/mols-agent-asset-validator",
        ROOT / "evals/skills/mols-skill-creator/cases.json",
    ]
    assert all(path.exists() for path in expected)


def test_migrated_maintainer_docs_exist_outside_packages() -> None:
    expected = [
        ROOT / "docs/skills/artifact-consistency-inspector/customization.md",
        ROOT / "docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md",
        ROOT / "docs/skills/mols-skill-creator/README.md",
        ROOT / "docs/skills/mols-skill-creator/WORKING.md",
        ROOT / "docs/skills/mols-skill-creator/baseline/DIRECTIVE.md",
    ]
    assert all(path.is_file() for path in expected)


def test_creator_initializer_is_minimal_and_self_contained(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(CREATOR / "scripts/init_skill.py"),
            "smoke-skill",
            "--path",
            str(tmp_path),
            "--description",
            "Smoke-test skill description with enough detail for validation.",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout

    created = tmp_path / "smoke-skill"
    files = sorted(
        path.relative_to(created).as_posix()
        for path in created.rglob("*")
        if path.is_file()
    )
    assert files == ["SKILL.md"]


def test_creator_contract_sources_use_repository_eval_surface() -> None:
    cases_path = ROOT / "evals/skills/mols-skill-creator/cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    assertions = "\n".join(
        assertion
        for case in cases["cases"]
        for assertion in case["assertions"]
    )
    assert "both required docs files" not in assertions
    assert "Reads DIRECTIVE before editing" not in assertions
    assert "without mandatory maintainer docs" in assertions

    upstream = (CREATOR / "references/upstream-sources.md").read_text(
        encoding="utf-8"
    )
    quality = (CREATOR / "references/quality-model.md").read_text(
        encoding="utf-8"
    )
    platform = (CREATOR / "references/platform-compatibility.md").read_text(
        encoding="utf-8"
    )
    assert "모든 대상 스킬에 의무화" not in upstream
    assert "`docs/`를 패키지에 포함한다" not in upstream
    assert "필요한 자산과 `docs/`가 포함된다" not in quality
    assert "`WORKING.md`에 현재 지원 범위" not in platform


def test_creator_validator_flags_legacy_docs(tmp_path: Path) -> None:
    skill = tmp_path / "legacy-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: legacy-skill\n"
        "description: A sufficiently detailed legacy skill description for validation.\n"
        "---\n\n"
        "# Legacy Skill\n",
        encoding="utf-8",
    )
    (skill / ".docs").mkdir()

    result = subprocess.run(
        [sys.executable, str(CREATOR / "scripts/validate_skill.py"), str(skill)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert ".docs/ present" in result.stdout
    assert "external maintainer-doc surface" in result.stdout


def test_creator_packager_excludes_non_runtime_surfaces(tmp_path: Path) -> None:
    archive = run_package(CREATOR, tmp_path / "dist")
    with zipfile.ZipFile(archive) as handle:
        names = set(handle.namelist())

    prefix = f"{CREATOR.name}/"
    assert prefix + "SKILL.md" in names
    assert prefix + "agents/openai.yaml" in names
    assert prefix + "references/quality-model.md" in names
    assert not any(
        f"/{part}/" in name
        for name in names
        for part in ("tests", "evals", "scenarios", "results")
    )


def test_pr_gate_covers_repository_tests_and_eval_smoke() -> None:
    workflow = TARGETED_TESTS.read_text(encoding="utf-8")
    assert "name: PR Gate" in workflow
    assert "pytest -q tests" in workflow
    assert "src/rulesync/.rulesync/skills/mols-rpi/*" in workflow
    assert "evals/skills/mols-rpi/*" in workflow
    assert "npm run eval:promptfoo:mols-rpi:smoke" in workflow
