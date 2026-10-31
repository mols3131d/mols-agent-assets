import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from scripts import development_bootstrap as bootstrap


@pytest.fixture
def project(tmp_path, monkeypatch):
    root = tmp_path / "bootstrap project 한글"
    root.mkdir()
    for name in bootstrap.POLICY_FILES:
        (root / name).write_text("original\n", encoding="utf-8")
    (root / "mise.toml").write_text(
        "[tools]\n"
        + "\n".join(f'"{tool}" = "1.2.3"' for tool in bootstrap.TOOL_COMMANDS),
        encoding="utf-8",
    )
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)
    return root


@pytest.fixture
def native(monkeypatch):
    calls = []
    failed = set()
    versions = {}
    paths = {}
    original_which = bootstrap.shutil.which
    monkeypatch.setattr(
        bootstrap.shutil,
        "which",
        lambda name: name if name in {"mise", "git"} else original_which(name),
    )

    def run(args, **kwargs):
        calls.append((args, kwargs))
        output = ""
        code = 0
        if args[1:3] == ["rev-parse", "--show-toplevel"]:
            output = str(kwargs["cwd"])
        elif args[1:3] == ["status", "--porcelain"]:
            output = ""
        elif args[1] == "install":
            target = args[3] if len(args) > 3 and args[2] == "--locked" else args[2]
            code = int(target in failed)
        elif args[1] == "which":
            output = str(Path(kwargs["cwd"]) / "tools" / f"{args[2]}.exe")
            paths[output] = args[2]
        elif args[1] == "where":
            tool = next(t for t in bootstrap.TOOL_COMMANDS if args[2] == f"{t}@1.2.3")
            prefix = (
                Path(kwargs["cwd"]) / "tools" / tool.replace(":", "-").replace("/", "-")
            )
            package = prefix / "node_modules" / tool.removeprefix("npm:")
            package.mkdir(parents=True, exist_ok=True)
            script = package / "cli.js"
            script.write_text("#!/usr/bin/env node\n", encoding="utf-8")
            (package / "package.json").write_text(
                json.dumps(
                    {
                        "name": tool.removeprefix("npm:"),
                        "version": "1.2.3",
                        "bin": "cli.js",
                    }
                ),
                encoding="utf-8",
            )
            output = str(prefix)
        elif args[0] in paths:
            binary = paths[args[0]]
            output = versions.get(binary, "1.2.3")
            if args[1:] == ["lock", "--upgrade", "--no-python-downloads"]:
                (kwargs["cwd"] / "uv.lock").write_text("upgraded\n", encoding="utf-8")
            code = int(tuple(args[1:]) in failed)
        return subprocess.CompletedProcess(
            args, code, output, "sensitive output hidden"
        )

    monkeypatch.setattr(bootstrap.subprocess, "run", run)
    return calls, failed, versions


def commands(native):
    return [args for args, _ in native[0]]


def test_setup_reconciles_exact_pins_without_lock_promotion(project, native, capsys):
    original = {name: (project / name).read_bytes() for name in bootstrap.POLICY_FILES}

    assert bootstrap.main(["setup"], root=project) == 0
    first = len(native[0])
    assert bootstrap.main(["setup"], root=project) == 0

    assert len(native[0]) == 2 * first
    assert original == {
        name: (project / name).read_bytes() for name in bootstrap.POLICY_FILES
    }
    args = commands(native)
    assert ["mise", "install", "--locked", "uv@1.2.3"] in args
    assert not any("--upgrade" in command for command in args)
    assert not any(
        "rulesync" == command[0] or "lefthook" == command[0] for command in args
    )
    assert not any("skills_sync" in " ".join(command) for command in args)
    assert any("--check" in command for command in args)
    output = capsys.readouterr().out
    assert "Result: READY (core toolchain/Python verified;" in output
    assert "optional integrations excluded and not verified" in output
    assert not (project / ".tmp" / "bootstrap.lock").exists()


def test_update_uses_native_bounded_resolution_and_retains_other_policy(
    project, native, capsys
):
    original = {name: (project / name).read_bytes() for name in bootstrap.POLICY_FILES}

    assert bootstrap.main(["update"], root=project) == 0

    args = commands(native)
    resolve = next(i for i, command in enumerate(args) if "--upgrade" in command)
    apply = next(i for i, command in enumerate(args) if "sync" in command)
    assert resolve < apply
    assert args[resolve][1:] == ["lock", "--upgrade", "--no-python-downloads"]
    assert (project / "uv.lock").read_bytes() != original.pop("uv.lock")
    assert original == {name: (project / name).read_bytes() for name in original}
    output = capsys.readouterr().out
    assert "[changed] uv.lock" in output
    assert "[unchanged] mise.lock" in output


@pytest.mark.parametrize("returncode", [0, 1])
def test_update_blocks_mise_lock_mutation_before_sync_without_rollback(
    project, native, monkeypatch, capsys, returncode
):
    original = bootstrap.Bootstrap.command
    before = {name: (project / name).read_bytes() for name in bootstrap.POLICY_FILES}

    def command(self, args, **kwargs):
        result = original(self, args, **kwargs)
        if args[1:] == ["lock", "--upgrade", "--no-python-downloads"]:
            (self.root / "mise.lock").write_text(
                "unexpected mutation\n", encoding="utf-8"
            )
            result.returncode = returncode
        return result

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["update"], root=project) == 1

    assert not any("sync" in args for args in commands(native))
    assert (project / "mise.lock").read_text(
        encoding="utf-8"
    ) == "unexpected mutation\n"
    assert (project / "uv.lock").read_text(encoding="utf-8") == "upgraded\n"
    for name in before.keys() - {"mise.lock", "uv.lock"}:
        assert (project / name).read_bytes() == before[name]
    output = capsys.readouterr()
    assert "Result: BLOCKED" in output.err
    assert "mise.lock changed during bootstrap" in output.err
    assert "Result: READY" not in output.out
    assert not (project / ".tmp" / "bootstrap.lock").exists()


@pytest.mark.parametrize("mode", ["setup", "update"])
def test_plan_does_not_install_resolve_or_create_state(project, native, mode, capsys):
    before = sorted(path.relative_to(project) for path in project.rglob("*"))
    assert bootstrap.main([mode, "--dry-run"], root=project) == 0
    assert sorted(path.relative_to(project) for path in project.rglob("*")) == before
    assert all(
        command[0] == "git" and command[1] in {"rev-parse", "status"}
        for command in commands(native)
    )
    assert "Result: PLAN" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args", [["setup", "--help"], ["update", "--help"], ["--help"]]
)
def test_help_never_runs_a_command(project, native, args):
    with pytest.raises(SystemExit) as error:
        bootstrap.main(args, root=project)
    assert error.value.code == 0
    assert not native[0]
    assert not (project / ".tmp").exists()


@pytest.mark.parametrize("flag", ["--unknown", "--yes", "--force", "--global", "--os"])
def test_unknown_flags_rejected_before_work(project, native, flag):
    with pytest.raises(SystemExit) as error:
        bootstrap.main(["setup", flag], root=project)
    assert error.value.code == 2
    assert not native[0]
    assert not (project / ".tmp").exists()


@pytest.mark.parametrize("relative", [False, True])
def test_external_uv_target_is_blocked_before_native_work(
    project, native, monkeypatch, relative
):
    target = "../foreign-env" if relative else str(project.parent / "foreign-env")
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", target)
    assert bootstrap.main(["setup"], root=project) == 1
    assert not native[0]
    assert not (project.parent / "foreign-env").exists()


def test_project_uv_target_and_active_foreign_env_are_handled(
    project, native, monkeypatch
):
    monkeypatch.delenv("MISE_LOCKED", raising=False)
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", ".venv")
    monkeypatch.setenv("VIRTUAL_ENV", str(project.parent / "other-env"))
    monkeypatch.setenv("UV_PROJECT", str(project.parent))
    assert bootstrap.main(["setup"], root=project) == 0
    for _, kwargs in native[0]:
        assert kwargs["cwd"] == project
        assert kwargs["env"]["UV_PROJECT_ENVIRONMENT"] == str(project / ".venv")
        assert kwargs["env"]["UV_PYTHON_DOWNLOADS"] == "never"
        assert kwargs["env"]["MISE_LOCKFILE"] == "1"
        assert "MISE_LOCKED" not in kwargs["env"]
        assert kwargs["env"]["MISE_AUTO_INSTALL"] == "0"
        assert "VIRTUAL_ENV" not in kwargs["env"]
        assert "UV_PROJECT" not in kwargs["env"]
        assert kwargs["shell"] is False


def test_non_venv_destination_is_not_removed_or_synced(project, native):
    target = project / ".venv"
    target.mkdir()
    marker = target / "user-data"
    marker.write_text("keep")
    assert bootstrap.main(["setup"], root=project) == 1
    assert marker.read_text() == "keep"
    assert not native[0]


def test_linked_venv_is_blocked(project, native, monkeypatch):
    original = bootstrap.linked
    monkeypatch.setattr(bootstrap, "linked", lambda p: p.name == ".venv" or original(p))
    assert bootstrap.main(["setup"], root=project) == 1
    assert not native[0]


def test_real_link_target_is_not_modified(project):
    foreign = project.parent / "foreign"
    foreign.mkdir()
    marker = foreign / "keep"
    marker.write_text("keep")
    target = project / ".venv"
    if os.name == "nt":
        result = subprocess.run(
            [os.environ["COMSPEC"], "/c", "mklink", "/J", str(target), str(foreign)],
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
    else:
        target.symlink_to(foreign, target_is_directory=True)
    try:
        assert bootstrap.main(["setup"], root=project) == 1
        assert marker.read_text() == "keep"
    finally:
        if os.name == "nt":
            target.rmdir()
        else:
            target.unlink()


@pytest.mark.parametrize("value", ["latest", "1", "1.2", ">=1,<2"])
def test_unlocked_tool_ranges_require_a_reviewed_lock_path(project, native, value):
    path = project / "mise.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('"1.2.3"', f'"{value}"'),
        encoding="utf-8",
    )
    assert bootstrap.main(["setup"], root=project) == 1
    assert not native[0]


def test_failed_node_skips_npm_but_continues_python_and_other_tools(
    project, native, capsys
):
    native[1].add("node@1.2.3")
    assert bootstrap.main(["setup"], root=project) == 1
    args = commands(native)
    assert ["mise", "install", "--locked", "rumdl@1.2.3"] in args
    assert not any(
        command[1] == "install" and len(command) > 3 and command[3].startswith("npm:")
        for command in args
    )
    assert any("sync" in command for command in args)
    assert "Result: FAILED" in capsys.readouterr().out


def test_failed_uv_skips_python_but_continues_independent_tools(project, native):
    native[1].add("uv@1.2.3")
    assert bootstrap.main(["setup"], root=project) == 1
    assert ["mise", "install", "--locked", "node@1.2.3"] in commands(native)
    assert not any("sync" in command for command in commands(native))


def test_wrong_binary_version_is_not_used_for_sync(project, native, capsys):
    native[2]["uv"] = "uv 9.9.9"
    assert bootstrap.main(["setup"], root=project) == 1
    assert not any("sync" in command for command in commands(native))
    assert "verify uv" in capsys.readouterr().out


def test_failed_resolution_skips_sync_and_preserves_partial_lock(
    project, native, capsys
):
    native[1].add(("lock", "--upgrade", "--no-python-downloads"))
    assert bootstrap.main(["update"], root=project) == 1
    assert not any("sync" in command for command in commands(native))
    assert (project / "uv.lock").read_text(encoding="utf-8") == "upgraded\n"
    assert "[changed] uv.lock" in capsys.readouterr().out


def test_failed_verification_does_not_report_ready(project, native, capsys):
    native[1].add(
        ("sync", "--check", "--locked", "--all-groups", "--no-python-downloads")
    )
    assert bootstrap.main(["setup"], root=project) == 1
    output = capsys.readouterr().out
    assert "Result: FAILED" in output
    assert "Result: READY" not in output
    assert "sensitive output hidden" not in output


@pytest.mark.parametrize("key", ["GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"])
def test_foreign_git_selection_cannot_hide_dirty_update(
    project, native, monkeypatch, key
):
    monkeypatch.setenv(key, str(project.parent / "another-repository"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(project.parent / "user.gitconfig"))
    original_run = bootstrap.subprocess.run

    def run(args, **kwargs):
        if args[:2] == ["git", "status"]:
            assert key not in kwargs["env"]
            assert kwargs["env"]["GIT_CONFIG_GLOBAL"] == str(
                project.parent / "user.gitconfig"
            )
            return subprocess.CompletedProcess(args, 0, " M uv.lock\n", "")
        return original_run(args, **kwargs)

    monkeypatch.setattr(bootstrap.subprocess, "run", run)
    assert bootstrap.main(["update"], root=project) == 1
    assert not any(args[1] == "install" for args in commands(native))
    assert (project / "uv.lock").read_text(encoding="utf-8") == "original\n"


def test_update_rejects_mismatched_git_worktree(project, native, monkeypatch):
    original_run = bootstrap.subprocess.run

    def run(args, **kwargs):
        if args[:2] == ["git", "rev-parse"]:
            return subprocess.CompletedProcess(args, 0, str(project.parent), "")
        return original_run(args, **kwargs)

    monkeypatch.setattr(bootstrap.subprocess, "run", run)
    assert bootstrap.main(["update"], root=project) == 1
    assert not any(args[1] == "install" for args in commands(native))


@pytest.mark.parametrize("key,value", [("UV_NO_GROUP", "dev"), ("UV_NO_DEV", "1")])
def test_uv_group_exclusions_do_not_change_core_sync(
    project, native, monkeypatch, key, value
):
    monkeypatch.setenv(key, value)
    monkeypatch.setenv("HTTPS_PROXY", "http://example.invalid:3128")
    assert bootstrap.main(["setup"], root=project) == 0
    sync_calls = [
        (args, kwargs)
        for args, kwargs in native[0]
        if len(args) > 1 and args[1] == "sync"
    ]
    assert len(sync_calls) == 2
    for args, kwargs in sync_calls:
        assert key not in kwargs["env"]
        assert kwargs["env"]["HTTPS_PROXY"] == "http://example.invalid:3128"
        assert "--all-groups" in args
    assert any(
        key in kwargs["env"] for args, kwargs in native[0] if args[1] == "install"
    )


@pytest.mark.parametrize("system_packages,expected", [(True, 1), (False, 0)])
def test_existing_venv_system_site_packages_isolated(
    project, native, system_packages, expected
):
    target = project / ".venv"
    target.mkdir()
    config = target / "pyvenv.cfg"
    original = (
        "home = python\ninclude-system-site-packages = "
        + ("true" if system_packages else "false")
        + "\n"
    )
    config.write_text(original, encoding="utf-8")
    assert bootstrap.main(["setup"], root=project) == expected
    assert config.read_text(encoding="utf-8") == original
    if system_packages:
        assert not native[0]


def test_update_allows_unrelated_asset_changes(project, native, monkeypatch):
    assets = ("rulesync.jsonc", "rulesync.lock", "skills-lock.json")
    for name in assets:
        (project / name).write_text("user edit\n", encoding="utf-8")
    original = bootstrap.Bootstrap.command

    def command(self, args, **kwargs):
        if args[1:3] == ["status", "--porcelain"]:
            assert args[args.index("--") + 1 :] == list(bootstrap.UPDATE_INPUTS)
        return original(self, args, **kwargs)

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["update"], root=project) == 0
    assert all(
        (project / name).read_text(encoding="utf-8") == "user edit\n" for name in assets
    )
    assert (project / "uv.lock").read_text(encoding="utf-8") == "upgraded\n"


@pytest.mark.parametrize("name", bootstrap.UPDATE_INPUTS)
def test_update_blocks_dirty_bootstrap_inputs(project, native, monkeypatch, name):
    original = bootstrap.Bootstrap.command

    def command(self, args, **kwargs):
        if args[1:3] == ["status", "--porcelain"]:
            assert name in args[args.index("--") + 1 :]
            return subprocess.CompletedProcess(args, 0, f" M {name}\n", "")
        return original(self, args, **kwargs)

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["update"], root=project) == 1
    assert not any(args[1] == "install" for args in commands(native))
    assert (project / "uv.lock").read_text(encoding="utf-8") == "original\n"


def test_dirty_update_state_is_not_overwritten(project, native, monkeypatch):
    original = bootstrap.Bootstrap.command

    def command(self, args, **kwargs):
        if args[1] == "status":
            return subprocess.CompletedProcess(args, 0, " M uv.lock\n", "")
        return original(self, args, **kwargs)

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["update"], root=project) == 1
    assert not any(args[1] == "install" for args in commands(native))
    assert not (project / ".tmp").exists()


def test_unexpected_policy_mutation_stops_without_rollback(
    project, native, monkeypatch
):
    original = bootstrap.Bootstrap.command

    def command(self, args, **kwargs):
        result = original(self, args, **kwargs)
        if args[1] == "install":
            (self.root / "rulesync.lock").write_text("unexpected mutation")
        return result

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["setup"], root=project) == 1
    assert (project / "rulesync.lock").read_text() == "unexpected mutation"
    assert len(native[0]) == 1
    assert not (project / ".tmp" / "bootstrap.lock").exists()


def test_concurrent_run_is_blocked_without_deleting_existing_lock(project, native):
    directory = project / ".tmp"
    directory.mkdir()
    lock = directory / "bootstrap.lock"
    lock.write_text("pid=existing")
    assert bootstrap.main(["setup"], root=project) == 1
    assert not native[0]
    assert lock.read_text() == "pid=existing"


def test_interruption_releases_only_own_lock(project, native, monkeypatch, capsys):
    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(bootstrap.subprocess, "run", interrupt)
    assert bootstrap.main(["setup"], root=project) == 130
    assert not (project / ".tmp" / "bootstrap.lock").exists()
    assert "partial state preserved" in capsys.readouterr().err


def test_missing_mise_is_reported_without_installer(project, native, monkeypatch):
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: None)
    assert bootstrap.main(["setup"], root=project) == 1
    assert not native[0]


@pytest.mark.parametrize("legacy_layout", [False, True])
def test_npm_bin_uses_package_metadata_and_pinned_node(
    project, monkeypatch, legacy_layout
):
    runner = bootstrap.Bootstrap(project, "setup", {})
    prefix = project / "tools"
    directory = prefix / "lib" if legacy_layout else prefix
    package = directory / "node_modules" / "@example" / "cli"
    package.mkdir(parents=True)
    script = package / "bin.js"
    script.write_text("#!/usr/bin/env node\n", encoding="utf-8")
    (package / "package.json").write_text(
        json.dumps(
            {"name": "@example/cli", "version": "1.2.3", "bin": {"example": "bin.js"}}
        ),
        encoding="utf-8",
    )
    node = str(project / "node.exe")
    runner.binaries["node"] = node
    monkeypatch.setattr(
        runner,
        "command",
        lambda args: subprocess.CompletedProcess(args, 0, str(prefix), ""),
    )
    assert runner.tool_command("mise", "npm:@example/cli", "1.2.3", "example") == [
        node,
        str(script),
    ]


@pytest.mark.parametrize("entry", ["../../../outside.js", "missing.js"])
def test_npm_bin_cannot_escape_prefix_or_be_missing(project, monkeypatch, entry):
    runner = bootstrap.Bootstrap(project, "setup", {})
    prefix = project / "tools"
    package = prefix / "node_modules" / "example"
    package.mkdir(parents=True)
    (project / "outside.js").write_text("not executed")
    (package / "package.json").write_text(
        json.dumps({"name": "example", "version": "1.2.3", "bin": entry}),
        encoding="utf-8",
    )
    runner.binaries["node"] = "node"
    monkeypatch.setattr(
        runner,
        "command",
        lambda args: subprocess.CompletedProcess(args, 0, str(prefix), ""),
    )
    with pytest.raises(bootstrap.BootstrapError, match="outside"):
        runner.tool_command("mise", "npm:example", "1.2.3", "example")


@pytest.mark.parametrize(
    "metadata", [[], {"name": "example", "version": "9.0.0", "bin": "cli.js"}]
)
def test_npm_metadata_must_match_declared_identity(project, monkeypatch, metadata):
    runner = bootstrap.Bootstrap(project, "setup", {})
    prefix = project / "tools"
    package = prefix / "node_modules" / "example"
    package.mkdir(parents=True)
    (package / "package.json").write_text(json.dumps(metadata), encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "command",
        lambda args: subprocess.CompletedProcess(args, 0, str(prefix), ""),
    )
    with pytest.raises(bootstrap.BootstrapError):
        runner.tool_command("mise", "npm:example", "1.2.3", "example")


@pytest.mark.parametrize(
    "folder", ["Lib/site-packages", "lib/python3.13/site-packages", "Scripts"]
)
def test_nested_venv_link_does_not_escape(project, folder):
    target = project / ".venv"
    target.mkdir()
    (target / "pyvenv.cfg").write_text("home = python")
    foreign = project.parent / "foreign-packages"
    foreign.mkdir()
    link = target.joinpath(*folder.split("/"))
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        result = subprocess.run(
            [os.environ["COMSPEC"], "/c", "mklink", "/J", str(link), str(foreign)],
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
    else:
        link.symlink_to(foreign, target_is_directory=True)
    try:
        assert bootstrap.main(["setup"], root=project) == 1
        assert list(foreign.iterdir()) == []
    finally:
        if os.name == "nt":
            link.rmdir()
        else:
            link.unlink()


def test_policy_edit_during_tool_install_blocks_before_resolution(
    project, native, monkeypatch
):
    original = bootstrap.Bootstrap.command

    def command(self, args, **kwargs):
        result = original(self, args, **kwargs)
        if args[1] == "install":
            (self.root / "uv.lock").write_text("concurrent user edit")
        return result

    monkeypatch.setattr(bootstrap.Bootstrap, "command", command)
    assert bootstrap.main(["update"], root=project) == 1
    assert not any("--upgrade" in command for command in commands(native))
    assert (project / "uv.lock").read_text() == "concurrent user edit"


def test_failed_sync_does_not_run_verification(project, native, capsys):
    native[1].add(("sync", "--locked", "--all-groups", "--no-python-downloads"))
    assert bootstrap.main(["setup"], root=project) == 1
    assert not any("--check" in command for command in commands(native))
    assert "Result: FAILED" in capsys.readouterr().out


def test_native_uv_update_respects_upper_bound_and_setup_lock(tmp_path):
    uv = bootstrap.shutil.which("uv")
    if uv is None:
        pytest.skip("uv executable is required for native resolver integration")
    root = tmp_path / "native uv 한글"
    root.mkdir()
    wheels = root / "wheels"
    wheels.mkdir()
    for version in ("1.0.0", "1.1.0", "2.0.0"):
        name = f"bootstrap_fixture-{version}"
        with zipfile.ZipFile(wheels / f"{name}-py3-none-any.whl", "w") as wheel:
            wheel.writestr("bootstrap_fixture.py", f'VERSION = "{version}"\n')
            wheel.writestr(
                f"{name}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: bootstrap-fixture\nVersion: {version}\n",
            )
            wheel.writestr(
                f"{name}.dist-info/WHEEL",
                "Wheel-Version: 1.0\nGenerator: fixture\n"
                "Root-Is-Purelib: true\nTag: py3-none-any\n",
            )
            wheel.writestr(f"{name}.dist-info/RECORD", "")
    manifest = root / "pyproject.toml"
    manifest.write_text(
        '[project]\nname = "bootstrap-integration"\nversion = "0.1.0"\n'
        'requires-python = ">=3.13"\ndependencies = ["bootstrap-fixture>=1,<2"]\n'
        '[tool.uv]\nno-index = true\nfind-links = ["wheels"]\n',
        encoding="utf-8",
    )
    for name in bootstrap.POLICY_FILES:
        path = root / name
        if name not in {"uv.lock", "pyproject.toml", ".python-version"}:
            path.write_text("fixture", encoding="utf-8")
    (root / ".python-version").write_text(sys.executable, encoding="utf-8")
    env = dict(os.environ)
    for key in list(env):
        if key.startswith("UV_"):
            env.pop(key)
    env.update(UV_CACHE_DIR=str(root / "cache"), UV_PYTHON_DOWNLOADS="never")
    initial = subprocess.run(
        [uv, "lock", "--resolution", "lowest-direct", "--no-python-downloads"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert initial.returncode == 0, initial.stderr
    assert 'version = "1.0.0"' in (root / "uv.lock").read_text(encoding="utf-8")
    before = manifest.read_bytes()
    runner = bootstrap.Bootstrap(root, "update", env)
    runner.binaries["uv"] = uv
    with bootstrap.exclusive_run(root):
        runner.python_environment()
    assert not runner.failed
    lock = (root / "uv.lock").read_bytes()
    assert b'version = "1.1.0"' in lock
    assert b'version = "2.0.0"' not in lock
    assert manifest.read_bytes() == before
    setup = bootstrap.Bootstrap(root, "setup", env)
    setup.binaries["uv"] = uv
    with bootstrap.exclusive_run(root):
        setup.python_environment()
    assert not setup.failed
    assert (root / "uv.lock").read_bytes() == lock


def test_mise_lock_included_in_policy_files_and_update_inputs():
    assert "mise.lock" in bootstrap.POLICY_FILES
    assert "mise.lock" in bootstrap.UPDATE_INPUTS


@pytest.mark.parametrize("mode", ["setup", "update"])
def test_mise_lock_mutation_during_step_is_blocked(project, monkeypatch, mode):
    runner = bootstrap.Bootstrap(project, mode, {})

    def mutate(*args, **kwargs):
        (project / "mise.lock").write_text("mutated\n", encoding="utf-8")
        return subprocess.CompletedProcess(args[0], 0, stdout="", stderr="")

    monkeypatch.setattr(runner, "command", mutate)
    with pytest.raises(
        bootstrap.BootstrapError, match="mise.lock changed during bootstrap"
    ):
        runner.step("test step", ["cmd"], "recovery")


def test_locked_install_mode_preserves_lock_on_failure(project, native):
    original_lock = (project / "mise.lock").read_bytes()
    native[1].add("uv@1.2.3")
    assert bootstrap.main(["setup"], root=project) == 1
    assert (project / "mise.lock").read_bytes() == original_lock
    assert any(
        command[:3] == ["mise", "install", "--locked"] for command in commands(native)
    )
