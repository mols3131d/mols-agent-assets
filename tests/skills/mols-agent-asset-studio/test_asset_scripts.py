from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/skills/mols-agent-asset-studio"
SCRIPTS = SKILL / "scripts"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_studio_validates() -> None:
    result = run(str(SCRIPTS / "validate_asset.py"), str(SKILL), "--strict")
    assert result.returncode == 0, result.stdout + result.stderr


def test_tuner_validates() -> None:
    tuner = ROOT / "src/skills/mols-agent-asset-tuner"
    result = run(str(SCRIPTS / "validate_asset.py"), str(tuner), "--strict")
    assert result.returncode == 0, result.stdout + result.stderr


def test_inventory_finds_both_skills(tmp_path: Path) -> None:
    output = tmp_path / "inventory.json"
    result = run(
        str(SCRIPTS / "inventory_assets.py"),
        str(ROOT),
        "--format",
        "json",
        "--output",
        str(output),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rows = json.loads(output.read_text(encoding="utf-8"))
    paths = {row["path"] for row in rows}
    assert "src/skills/mols-agent-asset-studio/SKILL.md" in paths
    assert "src/skills/mols-agent-asset-tuner/SKILL.md" in paths


def test_scaffold_is_minimal_and_valid(tmp_path: Path) -> None:
    result = run(
        str(SCRIPTS / "scaffold_asset.py"),
        "skill",
        "sample-skill",
        "--path",
        str(tmp_path),
        "--description",
        "Create sample outputs. Use when testing scaffolding.",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    target = tmp_path / "sample-skill"
    assert sorted(p.name for p in target.iterdir()) == ["SKILL.md"]
    valid = run(str(SCRIPTS / "validate_asset.py"), str(target), "--strict")
    assert valid.returncode == 0, valid.stdout + valid.stderr


def test_eval_sets_validate() -> None:
    for rel in (
        "evals/asset-studio/trigger-cases.json",
        "evals/asset-tuner/trigger-cases.json",
    ):
        result = run(str(SCRIPTS / "validate_eval_set.py"), str(ROOT / rel))
        assert result.returncode == 0, result.stdout + result.stderr


def test_github_agent_scaffold_and_validation(tmp_path: Path) -> None:
    agents = tmp_path / ".github/agents"
    result = run(
        str(SCRIPTS / "scaffold_asset.py"),
        "github-agent",
        "reviewer",
        "--path",
        str(agents),
        "--description",
        "Review agent assets in fresh context.",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    target = agents / "reviewer.md"
    valid = run(
        str(SCRIPTS / "validate_asset.py"), str(target), "--type", "agent", "--strict"
    )
    assert valid.returncode == 0, valid.stdout + valid.stderr


def test_package_excludes_secrets(tmp_path: Path) -> None:
    source = tmp_path / "safe-skill"
    source.mkdir()
    (source / "SKILL.md").write_text(
        "---\nname: safe-skill\n"
        "description: Safe test skill. Use when packaging tests run.\n"
        "---\n\n# Safe\n",
        encoding="utf-8",
    )
    (source / ".env").write_text("SECRET=bad\n", encoding="utf-8")
    output = tmp_path / "safe.zip"
    result = run(
        str(SCRIPTS / "package_skill.py"), str(source), "--output", str(output)
    )
    assert result.returncode == 0, result.stdout + result.stderr
    import zipfile

    with zipfile.ZipFile(output) as zf:
        assert "safe-skill/.env" not in zf.namelist()
        assert "safe-skill/SKILL.md" in zf.namelist()
        assert "safe-skill/MANIFEST.json" in zf.namelist()


def test_scaffold_quotes_hostile_description(tmp_path: Path) -> None:
    description = "Line one\n---\nname: injected"
    result = run(
        str(SCRIPTS / "scaffold_asset.py"),
        "skill",
        "quoted-skill",
        "--path",
        str(tmp_path),
        "--description",
        description,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    valid = run(
        str(SCRIPTS / "validate_asset.py"), str(tmp_path / "quoted-skill"), "--strict"
    )
    assert valid.returncode == 0, valid.stdout + valid.stderr


def test_package_rejects_symlink(tmp_path: Path) -> None:
    source = tmp_path / "linked-skill"
    source.mkdir()
    (source / "SKILL.md").write_text(
        "---\nname: linked-skill\n"
        "description: Linked test. Use when testing links.\n"
        "---\n\n# Linked\n",
        encoding="utf-8",
    )
    external = tmp_path / "external.txt"
    external.write_text("secret", encoding="utf-8")
    (source / "external-link").symlink_to(external)
    output = tmp_path / "linked.zip"
    result = run(
        str(SCRIPTS / "package_skill.py"), str(source), "--output", str(output)
    )
    assert result.returncode != 0
    assert "symlink" in result.stdout.lower()


def test_package_rejects_output_inside_skill(tmp_path: Path) -> None:
    source = tmp_path / "inner-skill"
    source.mkdir()
    (source / "SKILL.md").write_text(
        "---\nname: inner-skill\n"
        "description: Inner test. Use when testing output paths.\n"
        "---\n\n# Inner\n",
        encoding="utf-8",
    )
    result = run(
        str(SCRIPTS / "package_skill.py"),
        str(source),
        "--output",
        str(source / "inner.zip"),
    )
    assert result.returncode != 0


def test_context_audit_passes() -> None:
    result = run(str(SCRIPTS / "audit_context.py"), str(SKILL))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SKILL.md:" in result.stdout
