from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

RUMDL = shutil.which("rumdl")
pytestmark = pytest.mark.skipif(RUMDL is None, reason="rumdl is not installed")


def _run_rumdl(*args: str) -> subprocess.CompletedProcess[str]:
    assert RUMDL is not None
    return subprocess.run(
        [RUMDL, *args],
        capture_output=True,
        check=False,
        text=True,
    )


def test_rumdl_format_contract(tmp_path: Path) -> None:
    target = tmp_path / "format.md"
    target.write_text("# Title\n\nParagraph.\n", encoding="utf-8")

    result = _run_rumdl("fmt", str(target))

    assert result.returncode == 0, result.stderr


def test_rumdl_heading_contract_detects_invalid_structure(tmp_path: Path) -> None:
    target = tmp_path / "heading.md"
    target.write_text("# Title\n\n### Skipped level\n", encoding="utf-8")

    result = _run_rumdl("check", "--enable", "MD001,MD025", str(target))

    assert result.returncode != 0
    assert "MD001" in result.stdout + result.stderr


def test_rumdl_link_contract_detects_missing_fragment(tmp_path: Path) -> None:
    target = tmp_path / "link.md"
    target.write_text("# Target\n\n[Missing](#does-not-exist)\n", encoding="utf-8")

    result = _run_rumdl("check", "--enable", "MD051,MD052", str(target))

    assert result.returncode != 0
    assert "MD051" in result.stdout + result.stderr
