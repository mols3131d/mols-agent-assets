from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace

import pytest

from mols_dashboard.cli import main

SKILL_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "rulesync"
    / ".rulesync"
    / "skills"
    / "mols-markdown-dashboard"
)


def heading_events(markdown: str) -> Iterator[dict[str, object]]:
    for line in markdown.splitlines():
        if line.startswith("# "):
            yield {"Start": {"Heading": {"level": 1}}}
            yield {"Text": line[2:]}
            yield {"End": {"Heading": 1}}
        elif line.startswith("## "):
            yield {"Start": {"Heading": {"level": 2}}}
            yield {"Text": line[3:]}
            yield {"End": {"Heading": 2}}


def test_render_cli_checks_markdown_and_writes_atomically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "pyromark", SimpleNamespace(events=heading_events))
    output = tmp_path / "dashboard.md"

    result = main(
        [
            "render",
            str(SKILL_ROOT / "examples/domain-dashboard.yml"),
            "-o",
            str(output),
        ]
    )

    assert result == 0
    assert output.read_text(encoding="utf-8").startswith("# HMDA Data")
    assert not list(tmp_path.glob("*.tmp"))


def test_render_cli_supports_stdout(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setitem(sys.modules, "pyromark", SimpleNamespace(events=heading_events))

    result = main(
        [
            "render",
            str(SKILL_ROOT / "examples/project-dashboard.yml"),
            "-o",
            "-",
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.startswith("# Project Pivot")


def test_validate_cli_accepts_current_render(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "pyromark", SimpleNamespace(events=heading_events))

    result = main(
        [
            "validate",
            str(SKILL_ROOT / "examples/project-dashboard.yml"),
            "--markdown",
            str(SKILL_ROOT / "examples/project-dashboard.md"),
        ]
    )

    assert result == 0


def test_validate_cli_rejects_stale_rendered_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setitem(sys.modules, "pyromark", SimpleNamespace(events=heading_events))
    expected = (SKILL_ROOT / "examples/project-dashboard.md").read_text(encoding="utf-8")
    stale = expected.replace("8/10", "7/10", 1)
    markdown = tmp_path / "dashboard.md"
    markdown.write_text(stale, encoding="utf-8")

    result = main(
        [
            "validate",
            str(SKILL_ROOT / "examples/project-dashboard.yml"),
            "--markdown",
            str(markdown),
        ]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert "does not match current YAML render" in captured.err
