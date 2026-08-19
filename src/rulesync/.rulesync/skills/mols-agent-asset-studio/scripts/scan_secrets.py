from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tmp",
    "node_modules",
    "dist",
    "build",
}
SECRET_NAMES = {
    "credentials",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
    ".npmrc",
    ".pypirc",
}
SECRET_SUFFIXES = (".key", ".pem", ".p12", ".pfx", ".keystore")
PRIVATE_KEY_MARKER = "-----BEGIN " + "PRIVATE KEY-----"
PATTERNS = [
    ("private-key", re.compile(re.escape(PRIVATE_KEY_MARKER))),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "github-token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
]
ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd|private[_-]?key|secret)"
    r"\s*[:=]\s*['\"]?([^\s'\";,]{8,})"
)
PLACEHOLDER_PREFIXES = (
    "$",
    "${",
    "{",
    "<",
    "YOUR_",
    "EXAMPLE_",
    "DUMMY_",
    "TEST_",
    "REDACTED",
)


@dataclass(frozen=True)
class SecretFinding:
    path: str
    line: int
    kind: str
    redacted: str


def is_secret_filename(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith(".env")
        or name in SECRET_NAMES
        or name.endswith(SECRET_SUFFIXES)
    )


def _looks_placeholder(value: str) -> bool:
    upper = value.upper()
    return (
        value.startswith(PLACEHOLDER_PREFIXES)
        or "SECRETS." in upper
        or "VARS." in upper
    )


def _redact(value: str) -> str:
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}…{value[-2:]}"


def redact_text(text: str) -> str:
    """Redact likely secret values from command output without exposing matches."""
    redacted = text
    for kind, pattern in PATTERNS:
        redacted = pattern.sub(f"[REDACTED:{kind}]", redacted)

    def replace_assignment(match: re.Match[str]) -> str:
        key = match.group(1)
        value = match.group(2)
        if _looks_placeholder(value):
            return match.group(0)
        return f"{key}=[REDACTED]"

    return ASSIGNMENT_RE.sub(replace_assignment, redacted)


def scan_text(text: str, rel: str) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    SecretFinding(rel, number, kind, _redact(match.group(0)))
                )
        for match in ASSIGNMENT_RE.finditer(line):
            value = match.group(2)
            if not _looks_placeholder(value):
                findings.append(
                    SecretFinding(rel, number, "sensitive-assignment", _redact(value))
                )
    return findings


def iter_files(target: Path) -> Iterable[tuple[Path, str]]:
    if target.is_file() or target.is_symlink():
        yield target, target.name
        return
    for path in sorted(target.rglob("*")):
        rel = path.relative_to(target)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file() or path.is_symlink():
            yield path, rel.as_posix()


def scan_target(target: Path) -> tuple[list[SecretFinding], list[str]]:
    findings: list[SecretFinding] = []
    excluded: list[str] = []
    for path, rel in iter_files(target):
        if path.is_symlink():
            continue
        if is_secret_filename(path):
            excluded.append(rel)
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, rel))
    unique = {
        (item.path, item.line, item.kind, item.redacted): item for item in findings
    }
    return list(unique.values()), sorted(set(excluded))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Scan an asset for likely secret content without printing raw values."
        )
    )
    parser.add_argument("target", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    target = args.target.resolve()
    findings, excluded = scan_target(target)
    if args.as_json:
        print(
            json.dumps(
                {
                    "target": target.name,
                    "findings": [asdict(item) for item in findings],
                    "secret_named_files": excluded,
                    "passed": not findings,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for rel in excluded:
            print(f"EXCLUDE: {rel} (secret-like filename)")
        for item in findings:
            print(f"SECRET: {item.path}:{item.line} {item.kind} {item.redacted}")
        if not findings:
            print("PASS: no likely secret content found")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
