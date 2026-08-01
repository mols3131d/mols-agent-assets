from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SKIP = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist", "build"}
EXECUTABLE_SUFFIXES = {".py", ".sh", ".bash", ".ps1", ".js", ".ts", ".cmd", ".bat"}
SUSPICIOUS = {
    "prompt-injection": re.compile(
        r"ignore (all|any|the)?\s*(previous|prior)|system prompt|reveal.*secret", re.I
    ),
    "destructive-shell": re.compile(
        r"\brm\s+-rf\b|\bdel\s+/[sq]\b|Remove-Item.+-Recurse", re.I
    ),
    "network-fetch": re.compile(
        r"\bcurl\b|\bwget\b|Invoke-WebRequest|requests\.(get|post)|fetch\(", re.I
    ),
    "process-exec": re.compile(
        r"os\.system|subprocess\.|child_process|Start-Process", re.I
    ),
    "secret-reference": re.compile(
        r"API[_ -]?KEY|TOKEN|PASSWORD|PRIVATE[_ -]?KEY|credentials?", re.I
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidates(source: Path) -> list[tuple[Path, str]]:
    if source.is_symlink():
        return [(source, source.name)]
    if source.is_file():
        return [(source, source.name)]
    rows: list[tuple[Path, str]] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() and not path.is_symlink():
            continue
        rel = path.relative_to(source)
        if any(part in SKIP for part in rel.parts):
            continue
        rows.append((path, rel.as_posix()))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Statically scan imported agent assets without executing them."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-absolute-source", action="store_true")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.exists():
        print(f"ERROR: source not found: {args.source}")
        return 1

    rows = []
    findings = []
    for path, rel in candidates(source):
        if path.is_symlink():
            findings.append({"severity": "High", "kind": "symlink", "path": rel})
            continue
        row = {
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "executable_candidate": path.suffix.lower() in EXECUTABLE_SUFFIXES,
        }
        rows.append(row)
        if path.stat().st_size <= 1_000_000:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for kind, pattern in SUSPICIOUS.items():
                if pattern.search(content):
                    findings.append(
                        {
                            "severity": "Medium",
                            "kind": kind,
                            "path": rel,
                            "note": (
                                "Static signal only; inspect context before judgment."
                            ),
                        }
                    )
    report = {
        "source": str(source) if args.include_absolute_source else source.name,
        "files": rows,
        "findings": findings,
        "executed": False,
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
