from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from project_profile import discover_profile
from scan_secrets import redact_text

NETWORK_COMMANDS = {"curl", "wget", "invoke-webrequest"}
PACKAGE_PATTERNS = {
    ("pip", "install"),
    ("pip3", "install"),
    ("uv", "add"),
    ("uv", "pip"),
    ("npm", "install"),
    ("pnpm", "add"),
    ("yarn", "add"),
    ("cargo", "install"),
}


def _blocked(argv: list[str], policy: dict) -> str | None:
    command = Path(argv[0]).name.lower()
    lowered = [item.lower() for item in argv]
    if command in NETWORK_COMMANDS and not policy.get("allow_network", False):
        return "network command blocked by policy.allow_network=false"
    if (
        len(lowered) >= 2
        and (command, lowered[1]) in PACKAGE_PATTERNS
        and not policy.get("allow_package_install", False)
    ):
        return "package installation blocked by policy.allow_package_install=false"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute validated project-owned local checks without a shell."
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--allow-execution", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        source, path, profile = discover_profile(root, args.profile)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    commands = profile.get("validation", {}).get("local_commands", [])
    legacy = [item for item in commands if isinstance(item, str)]
    executable = [item for item in commands if isinstance(item, dict)]
    report = {
        "profile_source": source,
        "execution": "Executed" if args.allow_execution else "Deferred",
        "legacy_shell_strings": legacy,
        "checks": [],
    }
    if legacy:
        report["checks"].append(
            {
                "id": "legacy-shell-strings",
                "status": "Blocked",
                "reason": "convert to argv mappings",
            }
        )
    if not args.allow_execution:
        for item in executable:
            report["checks"].append(
                {
                    "id": item.get("id"),
                    "argv": [redact_text(arg) for arg in item.get("argv", [])],
                    "status": "Not run",
                }
            )
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 2

    policy = profile.get("policy", {})
    failed_required = False
    for item in executable:
        argv = item["argv"]
        check_id = item["id"]
        required = item.get("required", True)
        reason = _blocked(argv, policy)
        if reason:
            report["checks"].append(
                {
                    "id": check_id,
                    "argv": [redact_text(arg) for arg in argv],
                    "status": "Blocked",
                    "required": required,
                    "reason": reason,
                }
            )
            failed_required = failed_required or required
            continue
        cwd = (root / item.get("cwd", ".")).resolve()
        try:
            cwd.relative_to(root)
        except ValueError:
            report["checks"].append(
                {
                    "id": check_id,
                    "argv": [redact_text(arg) for arg in argv],
                    "status": "Blocked",
                    "required": required,
                    "reason": "cwd escapes project root",
                }
            )
            failed_required = failed_required or required
            continue
        if not cwd.is_dir():
            report["checks"].append(
                {
                    "id": check_id,
                    "argv": [redact_text(arg) for arg in argv],
                    "status": "Blocked",
                    "required": required,
                    "reason": "cwd does not exist",
                }
            )
            failed_required = failed_required or required
            continue
        try:
            process = subprocess.run(
                argv,
                cwd=cwd,
                shell=False,
                text=True,
                capture_output=True,
                timeout=item.get("timeout_sec", 120),
                check=False,
            )
            status = "Passed" if process.returncode == 0 else "Failed"
            failed_required = failed_required or (required and process.returncode != 0)
            report["checks"].append(
                {
                    "id": check_id,
                    "argv": [redact_text(arg) for arg in argv],
                    "status": status,
                    "required": required,
                    "returncode": process.returncode,
                    "stdout": redact_text(process.stdout[-20000:]),
                    "stderr": redact_text(process.stderr[-20000:]),
                }
            )
        except subprocess.TimeoutExpired:
            report["checks"].append(
                {
                    "id": check_id,
                    "argv": [redact_text(arg) for arg in argv],
                    "status": "Failed",
                    "required": required,
                    "reason": "timeout",
                }
            )
            failed_required = failed_required or required
    report["result"] = "Fail" if failed_required or legacy else "Pass"
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if failed_required or legacy else 0


if __name__ == "__main__":
    raise SystemExit(main())
