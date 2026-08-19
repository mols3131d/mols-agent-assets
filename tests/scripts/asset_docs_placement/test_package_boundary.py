from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CREATOR = (
    ROOT
    / "src"
    / "rulesync"
    / ".rulesync"
    / "skills"
    / "mols-skill-creator"
)


def test_packager_excludes_repository_verification_directories(tmp_path: Path) -> None:
    skill = tmp_path / "package-boundary"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: package-boundary\n"
        "description: Exercise runtime and repository verification package boundaries.\n"
        "---\n\n"
        "# Package Boundary\n",
        encoding="utf-8",
    )
    (skill / "references").mkdir()
    (skill / "references/runtime.md").write_text("# Runtime\n", encoding="utf-8")

    for part in ("tests", "evals", "scenarios", "results"):
        directory = skill / part
        directory.mkdir()
        (directory / "fixture.txt").write_text("fixture\n", encoding="utf-8")

    output = tmp_path / "dist"
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

    archive = output / "package-boundary.zip"
    with zipfile.ZipFile(archive) as handle:
        names = set(handle.namelist())

    assert "package-boundary/SKILL.md" in names
    assert "package-boundary/references/runtime.md" in names
    assert not any(
        f"/{part}/" in name
        for name in names
        for part in ("tests", "evals", "scenarios", "results")
    )
