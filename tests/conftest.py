"""Keep temporary Git repositories independent of the invoking Git hook."""

from __future__ import annotations

import subprocess
from collections.abc import Iterator

import pytest


@pytest.fixture(scope="session", autouse=True)
def isolate_git_hook_environment() -> Iterator[None]:
    result = subprocess.run(
        ["git", "rev-parse", "--local-env-vars"],
        check=True,
        capture_output=True,
        text=True,
    )
    with pytest.MonkeyPatch.context() as environment:
        for name in result.stdout.splitlines():
            # Keep mise's counted Git config so LF behavior remains under test.
            if name != "GIT_CONFIG_COUNT":
                environment.delenv(name, raising=False)
        yield
