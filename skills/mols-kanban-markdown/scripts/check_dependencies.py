#!/usr/bin/env python3
import importlib.metadata
import re
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None


def check_package_version(req_str):
    # Matches packages like "pyyaml>=6.0.2"
    match = re.match(r"^([a-zA-Z0-9_\-]+)\s*(>=|>|==|<=|<)?\s*(.*)$", req_str)
    if not match:
        return True, ""

    pkg_name, op, req_version = match.groups()
    try:
        inst_version = importlib.metadata.version(pkg_name)
    except importlib.metadata.PackageNotFoundError:
        return False, f"Package '{pkg_name}' is not installed."

    if op and req_version:

        def parse_version(v):
            return tuple(int(x) if x.isdigit() else x for x in re.split(r"\.|\-", v))

        try:
            if op == ">=" and parse_version(inst_version) < parse_version(req_version):
                return (
                    False,
                    f"Package '{pkg_name}' version {inst_version} is lower than required {req_version}.",
                )
            elif op == "==" and parse_version(inst_version) != parse_version(
                req_version
            ):
                return (
                    False,
                    f"Package '{pkg_name}' version {inst_version} does not match required {req_version}.",
                )
        except Exception:
            pass
    return True, ""


def main():
    script_dir = Path(__file__).resolve().parent
    toml_path = script_dir.parent / "pyproject.toml"

    if not toml_path.exists():
        print(f"Error: pyproject.toml not found at {toml_path}", file=sys.stderr)
        sys.exit(1)

    missing = []

    # 1. Parse pyproject.toml
    if tomllib:
        try:
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
            project = data.get("project", {})

            # Python version check
            req_python = project.get("requires-python", "")
            if req_python:
                py_match = re.search(r"([0-9.]+)", req_python)
                if py_match:
                    req_py_ver = tuple(map(int, py_match.group(1).split(".")))
                    if sys.version_info[: len(req_py_ver)] < req_py_ver:
                        missing.append(
                            f"Python version {req_python} required. Current is {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
                        )

            # Python dependencies check
            dependencies = project.get("dependencies", [])
            for dep in dependencies:
                ok, err = check_package_version(dep)
                if not ok:
                    missing.append(err)
        except Exception as e:
            missing.append(f"Failed to parse pyproject.toml: {e}")
    else:
        missing.append("Python version is too old (< 3.11). tomllib is unavailable.")

    # 2. Check for uv
    if not shutil.which("uv"):
        missing.append("Package installer 'uv' not found in PATH.")

    if missing:
        print("Dependency Check Failed for mols-kanban-markdown:", file=sys.stderr)
        for item in missing:
            print(f" - {item}", file=sys.stderr)
        sys.exit(1)

    print("mols-kanban-markdown: All dependencies verified successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
