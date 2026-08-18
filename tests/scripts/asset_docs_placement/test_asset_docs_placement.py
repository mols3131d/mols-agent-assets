from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME_SKILLS = ROOT / "src" / "skills-chatbot-runtime"
CREATOR = RUNTIME_SKILLS / "mols-skill-creator"
INSPECTOR = RUNTIME_SKILLS / "artifact-consistency-inspector"
TARGETED_TESTS = ROOT / ".github" / "workflows" / "targeted-tests.yml"


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


def test_runtime_packages_do_not_keep_legacy_docs() -> None:
    legacy = sorted(
        path for path in RUNTIME_SKILLS.rglob(".docs") if path.is_dir()
    )
    assert legacy == []


def test_migrated_maintainer_docs_exist_outside_packages() -> None:
    expected = [
        ROOT / "docs/skills/artifact-consistency-inspector/customization.md",
        ROOT / "docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md",
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
    assert not (created / ".docs").exists()

    skill_text = (created / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/DIRECTIVE.md" not in skill_text
    assert "docs/WORKING.md" not in skill_text
    assert "maintainer-only documentation" in skill_text


def test_creator_contract_sources_use_optional_maintainer_docs() -> None:
    cases = json.loads((CREATOR / "evals/cases.json").read_text(encoding="utf-8"))
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


def test_creator_packager_excludes_explicit_non_runtime_surfaces(
    tmp_path: Path,
) -> None:
    archive = run_package(CREATOR, tmp_path / "dist")
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())

    prefix = f"{CREATOR.name}/"
    assert prefix + "SKILL.md" in names
    assert prefix + "agents/openai.yaml" in names
    assert prefix + "references/quality-model.md" in names
    assert prefix + "evals/cases.json" not in names
    assert not any("/.docs/" in name or "/.evals/" in name for name in names)


def test_creator_packager_does_not_treat_every_dot_dir_as_non_runtime(
    tmp_path: Path,
) -> None:
    skill = tmp_path / "dot-runtime"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: dot-runtime\n"
        "description: Package a target-owned dot runtime resource for testing.\n"
        "---\n\n"
        "# Dot Runtime\n",
        encoding="utf-8",
    )
    (skill / ".runtime").mkdir()
    (skill / ".runtime/config.json").write_text("{}\n", encoding="utf-8")
    (skill / "evals").mkdir()
    (skill / "evals/case.json").write_text("{}\n", encoding="utf-8")

    archive = run_package(skill, tmp_path / "dist")
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())

    assert "dot-runtime/.runtime/config.json" in names
    assert "dot-runtime/evals/case.json" not in names


def test_targeted_workflow_routes_asset_doc_contract_changes() -> None:
    workflow = TARGETED_TESTS.read_text(encoding="utf-8")
    assert '"src/skills-chatbot-runtime/**"' in workflow
    assert '"docs/skills/**"' in workflow
    assert "src/skills-chatbot-runtime/*|docs/skills/*" in workflow
    assert ".github/workflows/targeted-tests.yml)" in workflow
    assert 'root_targets["tests/scripts/asset_docs_placement"]=1' in workflow


def test_artifact_consistency_inspector_contract_tests_pass() -> None:
    result = subprocess.run(
        [sys.executable, str(INSPECTOR / "tests/run_tests.py")],
        cwd=INSPECTOR,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
