#!/usr/bin/env python3
"""Reconcile exact-pinned tools and a project-local Python environment."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tomllib
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATE_INPUTS = (
    "mise.toml",
    "pyproject.toml",
    ".python-version",
    "uv.lock",
    "mise.lock",
)
POLICY_FILES = (*UPDATE_INPUTS, "rulesync.jsonc", "rulesync.lock", "skills-lock.json")
TOOL_COMMANDS = {
    "uv": ("uv", "--version"),
    "node": ("node", "--version"),
    "rumdl": ("rumdl", "--version"),
    "lefthook": ("lefthook", "version"),
    "npm:@biomejs/biome": ("biome", "--version"),
    "npm:rulesync": ("rulesync", "--version"),
    "npm:skills": ("skills", "--version"),
}
EXACT_VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?")


class BootstrapError(RuntimeError):
    pass


def linked(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def check_environment(root: Path, env: dict[str, str]) -> None:
    target = root / ".venv"
    requested = env.get("UV_PROJECT_ENVIRONMENT")
    if requested:
        path = Path(requested).expanduser()
        if not path.is_absolute():
            path = root / path
        if path.resolve() != target.resolve():
            raise BootstrapError(
                "UV_PROJECT_ENVIRONMENT must refer to this repository's .venv; "
                "unset it and rerun."
            )
    if linked(target):
        raise BootstrapError(
            ".venv is a link or junction; use a project-owned directory."
        )
    if target.exists():
        config = target / "pyvenv.cfg"
        if not config.is_file() or linked(config):
            raise BootstrapError(
                "Existing .venv is not an ordinary virtual environment."
            )
        for line in config.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.partition("=")
            if (
                sep
                and name.strip().lower() == "include-system-site-packages"
                and value.strip().lower() == "true"
            ):
                raise BootstrapError(
                    "Existing .venv exposes system site-packages; "
                    "inspect it before replacing or recreating."
                )
        for directory in (
            target / "Lib",
            target / "lib",
            target / "lib64",
            target / "Scripts",
            target / "bin",
        ):
            paths = [
                directory,
                directory / "site-packages",
                *directory.glob("python*/site-packages"),
            ]
            for path in paths:
                if not path.resolve().is_relative_to(target.resolve()):
                    raise BootstrapError(
                        ".venv package directory points outside .venv."
                    )
    for name in POLICY_FILES:
        path = root / name
        if not path.is_file() or linked(path):
            raise BootstrapError(f"{name} must be a regular project file.")
    if linked(root / ".tmp"):
        raise BootstrapError(
            ".tmp is a link or junction; bootstrap will not write there."
        )


def read_tools(root: Path) -> dict[str, str]:
    config = tomllib.loads((root / "mise.toml").read_text(encoding="utf-8"))
    tools = config.get("tools", {})
    if not tools or set(tools) != set(TOOL_COMMANDS):
        raise BootstrapError(
            "Tool ownership changed; review the bootstrap tool mapping."
        )
    if any(
        not isinstance(version, str) or not EXACT_VERSION.fullmatch(version)
        for version in tools.values()
    ):
        raise BootstrapError("Bootstrap currently requires exact tool pins.")
    return tools


@contextmanager
def exclusive_run(root: Path):
    directory = root / ".tmp"
    directory.mkdir(exist_ok=True)
    path = directory / "bootstrap.lock"
    try:
        handle = path.open("x", encoding="utf-8")
    except FileExistsError:
        raise BootstrapError(
            "Another bootstrap started; rerun after it finishes."
        ) from None
    try:
        with handle:
            handle.write(f"pid={os.getpid()}\n")
        yield
    finally:
        path.unlink()


class Bootstrap:
    def __init__(self, root: Path, mode: str, env: dict[str, str]):
        self.root = root
        self.mode = mode
        self.env = {
            **env,
            "UV_PROJECT_ENVIRONMENT": str(root / ".venv"),
            "UV_PYTHON_DOWNLOADS": "never",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "MISE_AUTO_INSTALL": "0",
            "MISE_LOCKFILE": "1",
        }
        for key in (
            "VIRTUAL_ENV",
            "UV_PROJECT",
            "UV_WORKING_DIR",
            "UV_CONFIG_FILE",
            "UV_PYTHON",
            "UV_FROZEN",
        ):
            self.env.pop(key, None)
        self.original = {name: (root / name).read_bytes() for name in POLICY_FILES}
        self.failed = False
        self.binaries: dict[str, str] = {}

    def command(
        self, args: list[str], *, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=self.root,
            env=self.env if env is None else env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            shell=False,
        )

    def check_update_state(self) -> None:
        git = shutil.which("git")
        if git is None:
            raise BootstrapError(
                "update requires Git to protect uncommitted policy/locks."
            )
        git_env = self.env.copy()
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            git_env.pop(key, None)
        top = self.command([git, "rev-parse", "--show-toplevel"], env=git_env)
        if top.returncode or Path(top.stdout.strip()).resolve() != self.root:
            raise BootstrapError(
                "update requires the intended Git worktree; inspect Git "
                "environment and repository location first."
            )
        result = self.command(
            [
                git,
                "status",
                "--porcelain",
                "--untracked-files=all",
                "--",
                *UPDATE_INPUTS,
            ],
            env=git_env,
        )
        if result.returncode or result.stdout.strip():
            raise BootstrapError(
                "update requires clean bootstrap inputs/lock; inspect Git status "
                "and preserve or commit your work first."
            )

    def unchanged_policy(self) -> None:
        for name, content in self.original.items():
            if name == "uv.lock" and self.mode == "update":
                continue
            path = self.root / name
            if linked(path) or not path.is_file() or path.read_bytes() != content:
                raise BootstrapError(
                    f"{name} changed during bootstrap; stopped without rollback. "
                    "Inspect the diff before retrying."
                )

    def step(
        self,
        name: str,
        args: list[str],
        recovery: str,
        *,
        env: dict[str, str] | None = None,
    ) -> bool:
        self.unchanged_policy()
        print(f"[run] {name}", flush=True)
        try:
            result = self.command(args) if env is None else self.command(args, env=env)
        except OSError:
            detail = "could not start the native command"
        else:
            if result.returncode == 0:
                self.unchanged_policy()
                print(f"[pass] {name}")
                return True
            detail = f"native command exited {result.returncode}"
        self.failed = True
        print(f"[fail] {name}: {detail}. Next: {recovery}")
        return False

    def tool_command(
        self, mise: str, tool: str, version: str, binary: str
    ) -> list[str]:
        request = f"{tool}@{version}"
        if tool.startswith("npm:"):
            resolved = self.command([mise, "where", request])
            prefix = Path(resolved.stdout.strip())
            if resolved.returncode or not prefix.is_absolute() or not prefix.is_dir():
                raise BootstrapError("mise could not locate the installed npm package")
            package = tool.removeprefix("npm:")
            for modules in (prefix / "node_modules", prefix / "lib" / "node_modules"):
                directory = modules / package
                manifest = directory / "package.json"
                if not manifest.is_file():
                    continue
                if not manifest.resolve().is_relative_to(prefix.resolve()):
                    raise BootstrapError("installed npm metadata is outside its prefix")
                data = json.loads(manifest.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    raise BootstrapError("installed npm package metadata is invalid")
                if data.get("name") != package or data.get("version") != version:
                    raise BootstrapError("installed npm package identity differs")
                bins = data.get("bin")
                entry = bins.get(binary) if isinstance(bins, dict) else bins
                if not isinstance(entry, str):
                    raise BootstrapError("installed npm package has no matching bin")
                script = (directory / entry).resolve()
                if not script.is_relative_to(prefix.resolve()) or not script.is_file():
                    raise BootstrapError(
                        "installed npm bin is outside its managed prefix"
                    )
                return [self.binaries["node"], str(script)]
            raise BootstrapError("installed npm package metadata is missing")
        resolved = self.command([mise, "which", binary, f"--tool={request}"])
        path = resolved.stdout.strip()
        if resolved.returncode or not path or not Path(path).is_absolute():
            raise BootstrapError("mise could not locate the configured binary")
        if os.name == "nt" and Path(path).suffix.lower() != ".exe":
            raise BootstrapError("native tool must resolve to a Windows executable")
        return [path]

    def install_tools(self, tools: dict[str, str], mise: str) -> None:
        ordered = sorted(tools, key=lambda name: name.startswith("npm:"))
        for tool in ordered:
            version = tools[tool]
            binary, flag = TOOL_COMMANDS[tool]
            if tool.startswith("npm:") and "node" not in self.binaries:
                self.failed = True
                print(
                    f"[blocked] {tool}: Node prerequisite failed; "
                    "repair Node and rerun."
                )
                continue
            request = f"{tool}@{version}"
            recovery = (
                f"inspect `mise install --locked {request}` and rerun {self.mode}"
            )
            if not self.step(
                f"tool {request}", [mise, "install", "--locked", request], recovery
            ):
                continue
            try:
                command = self.tool_command(mise, tool, version, binary)
                result = self.command([*command, flag])
                actual = re.search(
                    r"(?<![\w.])v?(\d+\.\d+\.\d+(?:-[\w.-]+)?)", result.stdout
                )
                if result.returncode or actual is None or actual.group(1) != version:
                    raise BootstrapError(
                        "configured binary version verification failed"
                    )
            except (OSError, ValueError, BootstrapError):
                self.failed = True
                print(f"[fail] verify {tool}: {recovery}")
                continue
            self.binaries[tool] = command[0]
            if tool == "node":
                self.env["PATH"] = (
                    str(Path(command[0]).parent) + os.pathsep + self.env.get("PATH", "")
                )
            print(f"[pass] verify {tool} {version}")

    def python_environment(self) -> None:
        uv = self.binaries.get("uv")
        if uv is None:
            self.failed = True
            print(
                "[blocked] Python environment: uv prerequisite failed; "
                "repair uv and rerun."
            )
            return
        if self.mode == "update":
            check_environment(self.root, self.env)
            if (self.root / "uv.lock").read_bytes() != self.original["uv.lock"]:
                raise BootstrapError(
                    "uv.lock changed after preflight; inspect before retry."
                )
            if not self.step(
                "resolve Python dependencies within pyproject constraints",
                [uv, "lock", "--upgrade", "--no-python-downloads"],
                "inspect `uv lock --upgrade --no-python-downloads`; "
                "review any partial lock diff",
            ):
                return
        check_environment(self.root, self.env)
        uv_env = self.env.copy()
        for key in ("UV_NO_GROUP", "UV_NO_DEV"):
            uv_env.pop(key, None)
        if self.step(
            "locked Python sync",
            [uv, "sync", "--locked", "--all-groups", "--no-python-downloads"],
            "inspect `uv sync --locked --all-groups --no-python-downloads`; "
            "rerun setup",
            env=uv_env,
        ):
            self.step(
                "verify Python environment",
                [
                    uv,
                    "sync",
                    "--check",
                    "--locked",
                    "--all-groups",
                    "--no-python-downloads",
                ],
                "repair the project .venv and rerun setup; "
                "do not delete user environments",
                env=uv_env,
            )

    def report(self) -> int:
        self.unchanged_policy()
        uv_changed = (self.root / "uv.lock").read_bytes() != self.original["uv.lock"]
        if self.mode == "update":
            print(
                f"[{'changed' if uv_changed else 'unchanged'}] uv.lock; "
                "review before committing."
            )
            print("[unchanged] mise.lock; exact CLI lock retained.")
            print(
                "[unchanged] Exact CLI pins and external Agent Asset revisions "
                "are retained."
            )
        print(
            "[skipped] Agent Asset installation/projection: "
            "review `rulesync install --frozen` "
            "and `rulesync generate --dry-run` before explicit generation."
        )
        print(
            "[skipped] User-home Skills: review native installer effects, "
            "then explicitly "
            "run `mise run skills-sync` if authorized."
        )
        print(
            "[skipped] Git hooks: inspect shared core.hooksPath and existing hooks "
            "before "
            "explicit `lefthook install`."
        )
        if self.failed:
            print(
                "Result: FAILED (required preparation incomplete; "
                "partial state preserved)."
            )
            return 1
        print(
            "Result: READY (core toolchain/Python verified; "
            "optional integrations excluded and not verified)."
        )
        return 0


def main(argv: list[str] | None = None, *, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile exact-pinned managed tools and project .venv; "
            "never install host/global integrations."
        ),
        epilog=(
            "Requires installed mise, uv and the declared Python. "
            "--dry-run is a read-only plan, not a resolver preview."
        ),
    )
    parser.add_argument("mode", choices=("setup", "update"))
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect safety gates and show the plan without installing or resolving",
    )
    args = parser.parse_args(argv)
    root = root.resolve()
    try:
        env = dict(os.environ)
        check_environment(root, env)
        tools = read_tools(root)
        bootstrap = Bootstrap(root, args.mode, env)
        if args.mode == "update":
            bootstrap.check_update_state()
        print(f"Preflight: {platform.system()} / {platform.machine()} / {args.mode}")
        print(
            "Scope: exact-pinned mise-managed tools/cache and project .venv; "
            "no host installer, profile, HOME Agent or hook writes."
        )
        if args.dry_run:
            for tool, version in tools.items():
                print(f"[plan] install/verify {tool}@{version} in mise-managed storage")
            if args.mode == "update":
                print(
                    "[plan] uv lock --upgrade within existing pyproject constraints; "
                    "external refs unchanged"
                )
            print("[plan] uv sync --locked --all-groups, then uv sync --check")
            print(
                "[skipped] Agent projections, user-home Skills and Git hooks "
                "require separate review."
            )
            print(
                "Result: PLAN (no resolver or installer executed; "
                "readiness not verified)."
            )
            return 0
        mise = shutil.which("mise")
        if mise is None:
            raise BootstrapError(
                "mise is required; install it using the official instructions."
            )
        with exclusive_run(root):
            bootstrap.install_tools(tools, mise)
            bootstrap.python_environment()
            return bootstrap.report()
    except KeyboardInterrupt:
        print(
            "Result: FAILED (interrupted; partial state preserved). "
            "Rerun setup after inspection.",
            file=sys.stderr,
        )
        return 130
    except (BootstrapError, OSError, ValueError) as error:
        detail = (
            str(error)
            if isinstance(error, BootstrapError)
            else "Could not read project policy/state."
        )
        print(f"Result: BLOCKED. {detail}", file=sys.stderr)
        print(
            "Partial state is preserved; inspect policy/lock diffs before retrying. "
            "No automatic rollback was attempted.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
