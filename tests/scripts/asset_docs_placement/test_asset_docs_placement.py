from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME_SKILLS = ROOT / "src" / "skills-chatbot-runtime"
CREATOR = RUNTIME_SKILLS / "mols-skill-creator"
INSPECTOR = RUNTIME_SKILLS / "artifact-consistency-inspector"


def test_runtime_packages_do_not_keep_legacy_docs() -> None:
    legacy = sorted(path for path in RUNTIME_SKILLS.rglob(".docs") if path.is_dir())
    assert legacy == []


def test_migrated_maintainer_docs_exist_outside_packages() -> None:
    expected = [
        ROOT / "docs/skills/artifact-consistency-inspector/customization.md",
        ROOT / "docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md",
        ROOT / "docs/skills/mols-skill-creator/WORKING.md",
        ROOT / "docs/skills/mols-skill-creator/baseline/DIRECTIVE.md",
    ]
    assert all(path.is_file() for path in expected)


def test_creator_initializer_is_minimal(tmp_path: Path) -> None:
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
    files = sorted(path.relative_to(created).as_posix() for path in created.rglob("*") if path.is_file())
    assert files == ["SKILL.md"]
    assert not (created / ".docs").exists()


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


def test_artifact_consistency_inspector_contract_tests_pass() -> None:
    result = subprocess.run(
        [sys.executable, str(INSPECTOR / "tests/run_tests.py")],
        cwd=INSPECTOR,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
