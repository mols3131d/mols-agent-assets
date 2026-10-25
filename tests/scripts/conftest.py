import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def isolate_git_user_configuration(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.hooksPath")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", os.devnull)
