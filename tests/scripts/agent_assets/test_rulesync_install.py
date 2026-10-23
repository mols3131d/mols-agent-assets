"""Rulesync installation must retain caller Git configuration."""

from __future__ import annotations

import os
import subprocess

import pytest

from scripts.agent_assets import rulesync_install


def test_git_lf_environment_without_inherited_config() -> None:
    parent = {"OTHER": "preserve"}
    result = rulesync_install.git_lf_environment(parent)
    assert result == {
        "OTHER": "preserve",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.autocrlf",
        "GIT_CONFIG_VALUE_0": "false",
    }
    assert parent == {"OTHER": "preserve"}


def test_git_lf_environment_preserves_credentials_and_overrides_autocrlf() -> None:
    parent = {
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
        "GIT_CONFIG_VALUE_0": "AUTHORIZATION: example",
        "GIT_CONFIG_KEY_1": "core.autocrlf",
        "GIT_CONFIG_VALUE_1": "true",
    }
    result = rulesync_install.git_lf_environment(parent)
    assert result["GIT_CONFIG_COUNT"] == "3"
    for key, value in parent.items():
        if key != "GIT_CONFIG_COUNT":
            assert result[key] == value
    assert result["GIT_CONFIG_KEY_2"] == "core.autocrlf"
    assert result["GIT_CONFIG_VALUE_2"] == "false"
    for key, expected in (
        ("http.https://github.com/.extraheader", "AUTHORIZATION: example"),
        ("core.autocrlf", "false"),
    ):
        process = subprocess.run(
            ["git", "config", "--get", key],
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, **result},
        )
        assert process.stdout.strip() == expected


def test_git_lf_environment_rejects_negative_count() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        rulesync_install.git_lf_environment({"GIT_CONFIG_COUNT": "-1"})


def test_rulesync_install_scopes_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> None:
        observed["command"] = command
        observed.update(kwargs)

    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "http.https://github.com/.extraheader")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "AUTHORIZATION: example")
    monkeypatch.setattr(rulesync_install.shutil, "which", lambda _: "/path/to/rulesync")
    monkeypatch.setattr(rulesync_install.subprocess, "run", fake_run)
    rulesync_install.main()

    assert observed["command"] == ["/path/to/rulesync", "install", "--frozen"]
    assert observed["cwd"] == rulesync_install.ROOT
    assert observed["check"] is True
    environment = observed["env"]
    assert isinstance(environment, dict)
    assert environment["GIT_CONFIG_COUNT"] == "2"
    assert environment["GIT_CONFIG_KEY_0"] == "http.https://github.com/.extraheader"
    assert environment["GIT_CONFIG_KEY_1"] == "core.autocrlf"
    assert environment["GIT_CONFIG_VALUE_1"] == "false"
    assert os.environ["GIT_CONFIG_COUNT"] == "1"
