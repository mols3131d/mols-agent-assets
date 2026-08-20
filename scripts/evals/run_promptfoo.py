from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTFOO_VERSION = "0.122.0"
MIN_NODE_VERSION = (22, 22, 0)


def build_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base is None else base)
    env.setdefault("PROMPTFOO_DISABLE_TELEMETRY", "1")
    env.setdefault("PROMPTFOO_DISABLE_UPDATE", "1")
    env.setdefault("PROMPTFOO_DISABLE_REMOTE_GENERATION", "true")
    env.setdefault("PROMPTFOO_DISABLE_SHARING", "1")
    env.setdefault("PROMPTFOO_CONFIG_DIR", str(ROOT / ".tmp" / "promptfoo"))
    env.setdefault("PROMPTFOO_PYTHON", sys.executable)
    env.setdefault("PROMPTFOO_RUNTIME_MODEL", "qwen2.5")
    env.setdefault("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:qwen2.5")
    return env


def parse_node_version(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", value.strip())
    if match is None:
        raise ValueError(f"unsupported Node.js version string: {value!r}")
    return tuple(int(part) for part in match.groups())


def resolve_npx(env: dict[str, str]) -> str:
    path = env.get("PATH")
    node = shutil.which("node", path=path)
    npx = shutil.which("npx", path=path)
    if node is None or npx is None:
        raise RuntimeError("Promptfoo eval requires Node.js and npx on PATH")

    result = subprocess.run(
        [node, "--version"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    version = parse_node_version(result.stdout)
    if version < MIN_NODE_VERSION:
        required = ".".join(str(part) for part in MIN_NODE_VERSION)
        actual = ".".join(str(part) for part in version)
        raise RuntimeError(f"Promptfoo {PROMPTFOO_VERSION} requires Node.js >= {required}; found {actual}")
    return npx


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        args = ["--help"]

    env = build_env()
    Path(env["PROMPTFOO_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)

    try:
        npx = resolve_npx(env)
    except (OSError, subprocess.SubprocessError, ValueError, RuntimeError) as error:
        print(f"promptfoo runner: {error}", file=sys.stderr)
        return 2

    command = [npx, "--yes", f"promptfoo@{PROMPTFOO_VERSION}", *args]
    return subprocess.run(command, check=False, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
