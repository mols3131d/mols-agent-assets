#!/usr/bin/env python3
import importlib.metadata
import re
import shutil
import sys
import tomllib
from pathlib import Path


def main() -> int:
    toml_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    missing = []

    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        project = data.get("project", {})

        req_python = project.get("requires-python", ">=3.13")
        py_ver_match = re.search(r"(\d+\.\d+)", req_python)
        if py_ver_match:
            req_ver = tuple(map(int, py_ver_match.group(1).split(".")))
            if sys.version_info[:2] < req_ver:
                missing.append(
                    f"Python {req_python} required "
                    f"(Current: {sys.version_info[0]}.{sys.version_info[1]})"
                )

        for dep in project.get("dependencies", []):
            pkg_name = re.split(r">=|>|==|<=|<", dep)[0].strip()
            try:
                importlib.metadata.version(pkg_name)
            except importlib.metadata.PackageNotFoundError:
                missing.append(f"Missing dependency: {pkg_name}")
    except Exception as e:
        missing.append(f"Failed to read/parse pyproject.toml: {e}")

    if not (shutil.which("rumdl") or shutil.which("uv")):
        missing.append(
            "Formatting command 'rumdl' not found in PATH, and 'uv' is not "
            "installed to run it via 'uv tool run'."
        )

    if missing:
        print("Dependency Check Failed for mols-markdown-maintenance:", file=sys.stderr)
        for item in missing:
            print(f" - {item}", file=sys.stderr)
        return 1

    print("mols-markdown-maintenance: All dependencies verified successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
