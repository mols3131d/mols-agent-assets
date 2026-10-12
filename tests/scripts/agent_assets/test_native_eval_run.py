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

    def fake_promptfoo(
        args: list[str], *, extra_packages: tuple[str, ...] = ()
    ) -> int:
        calls.append(args)
        assert extra_packages == (f"@openai/codex-sdk@{runner.CODEX_SDK_VERSION}",)
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
    assert calls[0][3:5] == ["--repeat", "3"]
    assert calls[0][5:7] == ["--filter-metadata", "suite=native-trigger"]
    assert not staged[0].exists() and not homes[0].exists()


def test_native_runner_uses_explicit_login_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / "mols-loops"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    sibling = package.parent / "mols-agent-asset"
    sibling.mkdir()
    (sibling / "SKILL.md").write_text("# Skill", encoding="utf-8")
    existing_home = tmp_path / "codex-auth"
    existing_home.mkdir()
    monkeypatch.setenv("CODEX_EVAL_HOME", str(existing_home))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("CODEX_API_KEY", raising=False)

    def fake_promptfoo(
        args: list[str], *, extra_packages: tuple[str, ...] = ()
    ) -> int:
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
        lambda args, **kwargs: pytest.fail("should not launch Promptfoo without authentication"),
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
    sibling = package.parent / "mols-agent-asset"
    sibling.mkdir()
    (sibling / "SKILL.md").write_text("# Skill", encoding="utf-8")
    monkeypatch.setenv("CODEX_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:grader-a")
    output = tmp_path / ".tmp" / "evals" / "mols-loops.json"
    config = tmp_path / "evals" / "promptfoo" / "mols-loops-native.yaml"
    config.parent.mkdir(parents=True)
    config.write_text("tests: []\n", encoding="utf-8")
    adapter = tmp_path / "scripts" / "agent_assets" / "skills_promptfoo.py"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# eval adapter\n", encoding="utf-8")
    for skill in ("mols-loops", "mols-agent-asset"):
        fixture = tmp_path / "evals" / "skills" / skill / "cases.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text('{"version": 1, "cases": []}', encoding="utf-8")
    calls: list[list[str]] = []

    def fake_promptfoo(
        args: list[str], *, extra_packages: tuple[str, ...] = ()
    ) -> int:
        calls.append(args)
        Path(args[-1]).write_text("{}", encoding="utf-8")
        return 0

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["mols-loops", "--repeat", "3", "--output", str(output)]) == 0
    assert calls[0][-2:] == ["-o", str(output.resolve())]
    assert output.read_text(encoding="utf-8") == "{}"
    manifest = runner.json.loads(
        output.with_name(output.name + ".manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["profile"] == "mols-loops"
    assert manifest["suite"] == "all"
    assert manifest["repeat"] == 3
    assert manifest["runner_exit_code"] == 0
    assert manifest["auth_mode"] == "api-key"
    assert manifest["git_head"] is None
    assert manifest["codex_sdk_version"] == runner.CODEX_SDK_VERSION
    assert set(manifest["skill_package_sha256"]) == {"mols-loops", "mols-agent-asset"}
    assert set(manifest["fixture_sha256"]) == {"mols-loops", "mols-agent-asset"}
    assert manifest["config_sha256"] == runner.file_sha256(config)
    assert manifest["adapter_sha256"] == runner.file_sha256(adapter)
    assert manifest["grader_provider_sha256"] == runner.hashlib.sha256(
        runner.promptfoo_run.build_env()["PROMPTFOO_GRADER_PROVIDER"].encode("utf-8")
    ).hexdigest()
    assert manifest["result_sha256"] == runner.file_sha256(output)
    assert "test-only-key" not in str(manifest)

    adapter.write_text("# updated adapter\n", encoding="utf-8")
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:grader-b")
    second_output = output.with_name("mols-loops-second.json")
    assert runner.main(["mols-loops", "--output", str(second_output)]) == 0
    second = runner.json.loads(
        second_output.with_name(second_output.name + ".manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert second["adapter_sha256"] != manifest["adapter_sha256"]
    assert second["grader_provider_sha256"] != manifest["grader_provider_sha256"]
    assert "grader-b" not in str(second)


def test_native_runner_filters_behavior_and_trigger_independently(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / "mols-loops"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    sibling = package.parent / "mols-agent-asset"
    sibling.mkdir()
    (sibling / "SKILL.md").write_text("# Skill", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    commands: list[list[str]] = []
    monkeypatch.setattr(
        runner.promptfoo_run, "main", lambda args, **kwargs: commands.append(args) or 0
    )
    assert runner.main(["mols-loops", "--suite", "trigger"]) == 0
    assert runner.main(["mols-loops", "--suite", "behavior"]) == 0
    assert commands[0][-2:] == ["--filter-metadata", "suite=native-trigger"]
    assert commands[1][-2:] == ["--filter-metadata", "suite=behavior"]


def test_native_runner_rejects_missing_profile_suite() -> None:
    with pytest.raises(SystemExit):
        runner.main(["asset-routing", "--suite", "behavior"])


def test_native_runner_fails_when_requested_output_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    for skill in ("mols-loops", "mols-agent-asset"):
        package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / skill
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    monkeypatch.setattr(runner.promptfoo_run, "main", lambda args, **kwargs: 0)
    output = tmp_path / "result.json"
    assert runner.main(["mols-loops", "--output", str(output)]) == 2
    assert not output.with_name(output.name + ".manifest.json").exists()
    assert "requested output was not written or refreshed" in capsys.readouterr().err



def test_native_runner_does_not_manifest_stale_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    for skill in ("mols-loops", "mols-agent-asset"):
        package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / skill
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    monkeypatch.setattr(runner.promptfoo_run, "main", lambda args, **kwargs: 0)
    output = tmp_path / "result.json"
    output.write_text("previous result", encoding="utf-8")
    assert runner.main(["mols-loops", "--output", str(output)]) == 2
    assert output.read_text(encoding="utf-8") == "previous result"
    assert not output.with_name(output.name + ".manifest.json").exists()
    assert "not written or refreshed" in capsys.readouterr().err


def test_native_runner_rejects_mixed_login_and_api_auth(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    login_home = tmp_path / "codex-auth"
    login_home.mkdir()
    monkeypatch.setenv("CODEX_EVAL_HOME", str(login_home))
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_API_KEY", raising=False)
    monkeypatch.setattr(
        runner.promptfoo_run,
        "main",
        lambda args, **kwargs: pytest.fail("ambiguous authentication must not launch Promptfoo"),
    )
    assert runner.main(["mols-loops"]) == 2
    assert "cannot be combined with API keys" in capsys.readouterr().err


def test_native_runner_records_only_executed_suites_and_grader_fingerprint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    for skill in ("mols-agent-asset", "mols-agent-asset-find"):
        package = tmp_path / "src" / "rulesync" / ".rulesync" / "skills" / skill
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text("# Skill", encoding="utf-8")
        fixture = tmp_path / "evals" / "skills" / skill / "cases.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text('{"version": 1, "cases": []}', encoding="utf-8")
    config = tmp_path / "evals" / "promptfoo" / "agent-asset-routing-native.yaml"
    config.parent.mkdir(parents=True)
    config.write_text("tests: []\n", encoding="utf-8")
    adapter = tmp_path / "scripts" / "agent_assets" / "skills_promptfoo.py"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# fixture adapter\n", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    monkeypatch.delenv("CODEX_API_KEY", raising=False)
    monkeypatch.delenv("CODEX_EVAL_HOME", raising=False)
    monkeypatch.setenv("PROMPTFOO_GRADER_PROVIDER", "grader-sensitive-secret-value")
    output = tmp_path / "routing.json"
    commands: list[list[str]] = []

    def fake_promptfoo(
        args: list[str], *, extra_packages: tuple[str, ...] = ()
    ) -> int:
        commands.append(args)
        output.write_text("{}", encoding="utf-8")
        return 0

    monkeypatch.setattr(runner.promptfoo_run, "main", fake_promptfoo)
    assert runner.main(["asset-routing", "--suite", "all", "--output", str(output)]) == 0
    assert ["--filter-metadata", "suite=native-trigger"] == commands[0][5:7]
    manifest = runner.json.loads(
        output.with_name(output.name + ".manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["suite"] == "trigger"
    assert manifest["evidence_scope"] == "skill-file-read-heuristic"
    assert manifest["grader_provider_sha256"] is None
    assert manifest["adapter_sha256"] == runner.file_sha256(adapter)
    assert "grader-sensitive-secret-value" not in str(manifest)
