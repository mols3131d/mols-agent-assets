from pathlib import Path

import pytest

from scripts.agent_assets import native_eval_run as runner


def test_native_runner_stages_canonical_packages_and_restores_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for skill in ("mols-agent-asset", "mols-agent-asset-find"):
        package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / skill
        (package / "references").mkdir(parents=True)
        (package / "SKILL.md").write_text(f"# {skill}", encoding="utf-8")
        (package / "references" / "eval.md").write_text(
            "reference", encoding="utf-8"
        )
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_API_KEY", raising=False)
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    monkeypatch.setenv("CODEX_SKILLS_WORKING_DIR", "original")
    staged: list[Path] = []
    homes: list[Path] = []
    calls: list[list[str]] = []

    def fake_promptfoo(args: list[str]) -> int:
        calls.append(args)
        workspace = Path(runner.os.environ["CODEX_SKILLS_WORKING_DIR"])
        home = Path(runner.os.environ["CODEX_EVAL_HOME"])
        staged.append(workspace)
        homes.append(home)
        assert workspace.is_dir() and home.is_dir()
        assert tmp_path not in workspace.parents
        assert home.parent == workspace.parent
        for skill in ("mols-agent-asset", "mols-agent-asset-find"):
            package = workspace / ".agents" / "skills" / skill
            assert (package / "SKILL.md").read_text(encoding="utf-8") == f"# {skill}"
            assert (package / "references" / "eval.md").is_file()
        return 7

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["asset-routing", "--repeat", "3"]) == 7
    assert runner.os.environ["CODEX_SKILLS_WORKING_DIR"] == "original"
    assert "CODEX_EVAL_HOME" not in runner.os.environ
    assert calls[0][-2:] == ["--repeat", "3"]
    assert not staged[0].exists() and not homes[0].exists()


def test_native_runner_uses_explicit_login_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / "mols-loops"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    existing_home = tmp_path / "codex-auth"
    existing_home.mkdir()
    monkeypatch.setenv("CODEX_EVAL_HOME", str(existing_home))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("CODEX_API_KEY", raising=False)

    def fake_promptfoo(args: list[str]) -> int:
        assert runner.os.environ["CODEX_EVAL_HOME"] == str(existing_home)
        return 0

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["mols-loops"]) == 0
    assert runner.os.environ["CODEX_EVAL_HOME"] == str(existing_home)


def test_native_runner_requires_explicit_auth(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    for key in ("CODEX_EVAL_HOME", "OPENAI_API_KEY", "CODEX_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(
        runner.promptfoo_run,
        "main",
        lambda args: pytest.fail("should not launch Promptfoo without authentication"),
    )
    assert runner.main(["mols-loops"]) == 2
    assert "needs OPENAI_API_KEY/CODEX_API_KEY" in capsys.readouterr().err


def test_native_runner_rejects_invalid_repeat() -> None:
    with pytest.raises(SystemExit):
        runner.main(["mols-loops", "--repeat", "0"])


def test_native_stage_fails_on_missing_canonical_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    with pytest.raises(FileNotFoundError, match="canonical Skill missing"):
        runner.stage_skills(tmp_path / "workspace", ("missing",))


def test_native_runner_exports_evidence_outside_ephemeral_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / "mols-loops"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    monkeypatch.setenv("CODEX_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    output = tmp_path / ".tmp" / "evals" / "mols-loops.json"
    calls: list[list[str]] = []

    def fake_promptfoo(args: list[str]) -> int:
        calls.append(args)
        output.write_text("{}", encoding="utf-8")
        return 0

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["mols-loops", "--repeat", "3", "--output", str(output)]) == 0
    assert calls[0][-2:] == ["-o", str(output.resolve())]
    assert output.read_text(encoding="utf-8") == "{}"
