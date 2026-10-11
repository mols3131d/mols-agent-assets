from pathlib import Path

import pytest

from scripts.agent_assets import native_eval_run as runner


def test_native_runner_stages_canonical_packages_and_restores_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for skill in ("mols-agent-asset", "mols-agent-asset-find"):
        package = (
            tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / skill
        )
        (package / "references").mkdir(parents=True)
        (package / "SKILL.md").write_text(f"# {skill}", encoding="utf-8")
        (package / "references" / "eval.md").write_text("reference", encoding="utf-8")
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setenv("CODEX_SKILLS_WORKING_DIR", "original")
    calls: list[list[str]] = []

    def fake_promptfoo(args: list[str]) -> int:
        calls.append(args)
        workspace = Path(runner.os.environ["CODEX_SKILLS_WORKING_DIR"])
        assert workspace.is_dir()
        for skill in ("mols-agent-asset", "mols-agent-asset-find"):
            package = workspace / ".agents" / "skills" / skill
            assert (package / "SKILL.md").read_text(encoding="utf-8") == f"# {skill}"
            assert (package / "references" / "eval.md").is_file()
        return 7

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["asset-routing", "--repeat", "3"]) == 7
    assert runner.os.environ["CODEX_SKILLS_WORKING_DIR"] == "original"
    assert calls[0][-2:] == ["--repeat", "3"]
    assert not any((tmp_path / ".tmp" / "native-agent-eval").iterdir())


def test_native_runner_rejects_invalid_repeat() -> None:
    with pytest.raises(SystemExit):
        runner.main(["mols-loops", "--repeat", "0"])


def test_native_stage_fails_on_missing_canonical_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    with pytest.raises(FileNotFoundError, match="canonical Skill missing"):
        runner.stage_skills(tmp_path / "workspace", ("missing",))
