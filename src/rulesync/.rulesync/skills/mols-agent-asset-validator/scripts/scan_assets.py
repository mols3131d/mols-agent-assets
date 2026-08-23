#!/usr/bin/env python3
"""Deterministically inspect agent-facing asset files or ZIP packages.

The scanner uses only the Python standard library. It does not perform model-based
or runtime agent evaluation and never labels semantic behavior as verified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import py_compile
import re
import sys
import tempfile
import tomllib
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


IGNORED_DIRS = {".git", ".hg", ".svn", "__pycache__", ".venv", "node_modules"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".toml", ".ini", ".cfg"}
ASSET_NAMES = {
    "SKILL.md": "skill",
    "AGENTS.md": "instruction",
    "DIRECTIVE.md": "instruction",
}
IDENTITY_ASSET_TYPES = {"skill", "agent", "subagent"}
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
DECLARED_PATH_PATTERN = re.compile(r"`((?:agents|subagents|references|schemas|scripts|evals|templates|docs)/[^`\s]+)`")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+\S")
NORMATIVE_PATTERN = re.compile(r"\b(?:must|should|never|always|required|forbidden)\b|(?:반드시|항상|절대|금지|해야 한다|해야한다|필수)", re.IGNORECASE)
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_ARCHIVE_FILES = 5000
MAX_ARCHIVE_TOTAL_BYTES = 100 * 1024 * 1024
MAX_ARCHIVE_FILE_BYTES = 20 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github-token": re.compile(r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
}


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    path: str
    message: str
    evidence_level: str = "verified"


class ScanError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_safe_zip_member(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts


def extract_zip_safely(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as handle:
        members = handle.infolist()
        if len(members) > MAX_ARCHIVE_FILES:
            raise ScanError(f"ZIP contains too many members: {len(members)}")
        total_size = 0
        for info in members:
            if not is_safe_zip_member(info.filename):
                raise ScanError(f"unsafe ZIP member: {info.filename}")
            mode = info.external_attr >> 16
            if mode and (mode & 0o170000) == 0o120000:
                raise ScanError(f"ZIP symlink is not allowed: {info.filename}")
            if info.file_size > MAX_ARCHIVE_FILE_BYTES:
                raise ScanError(f"ZIP member is too large: {info.filename}")
            total_size += info.file_size
            if total_size > MAX_ARCHIVE_TOTAL_BYTES:
                raise ScanError("ZIP uncompressed size exceeds safety limit")
            if info.file_size and info.compress_size == 0:
                raise ScanError(f"ZIP member has invalid compression metadata: {info.filename}")
            if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                raise ScanError(f"ZIP member compression ratio is suspicious: {info.filename}")
        handle.extractall(destination)


def iter_entries(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        next_dirs: list[str] = []
        for name in sorted(dirs):
            if name in IGNORED_DIRS:
                continue
            path = current_path / name
            if path.is_symlink():
                yield path
            else:
                next_dirs.append(name)
        dirs[:] = next_dirs
        for name in sorted(files):
            yield current_path / name


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def classify(path: Path, root: Path) -> str:
    if path.name in ASSET_NAMES:
        return ASSET_NAMES[path.name]
    parts = {part.lower() for part in path.relative_to(root).parts[:-1]}
    if "subagents" in parts:
        return "subagent"
    if "agents" in parts or path.name.endswith(".agent.md"):
        return "agent"
    if "prompts" in parts or path.name.endswith(".prompt.md"):
        return "prompt"
    if "instructions" in parts or path.name.endswith(".instructions.md"):
        return "instruction"
    if "evals" in parts or "tests" in parts:
        return "eval"
    if "references" in parts:
        return "reference"
    if "templates" in parts:
        return "template"
    if "schemas" in parts:
        return "schema"
    if "scripts" in parts or path.suffix == ".py":
        return "script"
    if path.suffix in {".json", ".yaml", ".yml", ".toml"}:
        return "config"
    return "other"


def read_text(path: Path, findings: list[Finding], root: Path) -> str | None:
    rel = relative(path, root)
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append(Finding("major", "encoding", rel, "text-like file is not valid UTF-8"))
        return None
    except OSError as exc:
        findings.append(Finding("major", "io", rel, f"cannot read file: {exc}"))
        return None


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None
    result: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def normalized_normative_lines(text: str) -> list[str]:
    result: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or len(stripped) < 20 or not NORMATIVE_PATTERN.search(stripped):
            continue
        normalized = re.sub(r"\s+", " ", stripped.lstrip("-*0123456789. ")).casefold()
        if normalized:
            result.append(normalized)
    return result


def heading_depth_jumps(text: str) -> list[tuple[int, int, int]]:
    jumps: list[tuple[int, int, int]] = []
    previous = 0
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_PATTERN.match(raw)
        if not match:
            continue
        current = len(match.group(1))
        if previous and current > previous + 1:
            jumps.append((number, previous, current))
        previous = current
    return jumps


def relation_target(path: Path, raw_target: str, root: Path) -> str | None:
    target = raw_target.strip().split()[0].strip("<>").rstrip(".,;:)")
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "sandbox:", "data:")):
        return None
    target = target.split("#", 1)[0]
    if not target:
        return None
    candidates = [(path.parent / target).resolve(), (root / target).resolve()]
    for candidate in candidates:
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            continue
        if candidate.exists():
            return relative(candidate, root)
    return None


def check_declared_paths(path: Path, text: str, root: Path, findings: list[Finding]) -> None:
    rel = relative(path, root)
    for raw_target in DECLARED_PATH_PATTERN.findall(text):
        target = raw_target.rstrip(".,;:)")
        candidates = [(path.parent / target).resolve(), (root / target).resolve()]
        safe_candidates: list[Path] = []
        for candidate in candidates:
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                continue
            safe_candidates.append(candidate)
        if not safe_candidates:
            findings.append(Finding("major", "reference", rel, f"declared path escapes target root: {raw_target}"))
            continue
        if not any(candidate.exists() for candidate in safe_candidates):
            findings.append(Finding("major", "reference", rel, f"declared asset path does not exist: {raw_target}"))


def check_markdown_links(path: Path, text: str, root: Path, findings: list[Finding]) -> None:
    rel = relative(path, root)
    for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "sandbox:", "data:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            findings.append(Finding("major", "link", rel, f"relative link escapes target root: {raw_target}"))
            continue
        if not resolved.exists():
            findings.append(Finding("major", "link", rel, f"broken relative link: {raw_target}"))


def check_text_file(path: Path, text: str, root: Path, findings: list[Finding]) -> dict[str, object]:
    rel = relative(path, root)
    asset_type = classify(path, root)
    metadata: dict[str, object] = {
        "path": rel,
        "asset_type": asset_type,
        "size": path.stat().st_size,
        "lines": len(text.splitlines()),
    }
    if not text.strip():
        findings.append(Finding("minor", "content", rel, "empty text file"))
    if "\t" in text:
        findings.append(Finding("minor", "format", rel, "tab character found"))
    for number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            findings.append(Finding("minor", "format", rel, f"trailing whitespace at line {number}"))
    if path.suffix == ".md":
        if text.count("```") % 2:
            findings.append(Finding("major", "markdown", rel, "unbalanced fenced code block"))
        check_markdown_links(path, text, root, findings)
        check_declared_paths(path, text, root, findings)
        jumps = heading_depth_jumps(text)
        for number, previous, current in jumps:
            findings.append(Finding("minor", "human-comprehension", rel, f"heading depth jumps from H{previous} to H{current} at line {number}"))
        normative = normalized_normative_lines(text)
        metadata["normative_lines"] = len(normative)
        metadata["normative_density"] = round(len(normative) / max(1, len(text.splitlines())), 4)
        if len(text.splitlines()) > 500 and asset_type in {"skill", "agent", "subagent", "instruction", "prompt"}:
            findings.append(Finding("minor", "context-cost", rel, "agent-facing text exceeds 500 lines; review progressive disclosure and relevance"))
        if len(text.splitlines()) > 100 and metadata["normative_density"] > 0.35:
            findings.append(Finding("note", "instruction-bottleneck", rel, "high normative-line density is a heuristic signal requiring semantic review", evidence_level="inferred"))
        frontmatter = parse_frontmatter(text)
        identity_asset = asset_type in IDENTITY_ASSET_TYPES
        if identity_asset and not frontmatter:
            findings.append(Finding("major", "frontmatter", rel, "agent asset is missing frontmatter"))
        if frontmatter:
            metadata["frontmatter"] = frontmatter
            if identity_asset:
                for key in ("name", "description"):
                    if not frontmatter.get(key):
                        findings.append(Finding("major", "frontmatter", rel, f"frontmatter missing {key}"))
                if asset_type == "skill" and frontmatter.get("name") and not NAME_PATTERN.fullmatch(frontmatter["name"]):
                    findings.append(Finding("major", "identity", rel, "Skill frontmatter name must be kebab-case"))
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding("critical", "secret", rel, f"possible embedded {name}"))
    return metadata


def check_json(path: Path, root: Path, findings: list[Finding]) -> None:
    rel = relative(path, root)
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("major", "json", rel, f"invalid JSON: {exc}"))


def check_toml(path: Path, root: Path, findings: list[Finding]) -> None:
    rel = relative(path, root)
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        findings.append(Finding("major", "toml", rel, f"invalid TOML: {exc}"))


def check_python(path: Path, root: Path, findings: list[Finding]) -> None:
    rel = relative(path, root)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            py_compile.compile(path, cfile=str(Path(temp_dir) / "compiled.pyc"), doraise=True)
    except py_compile.PyCompileError as exc:
        findings.append(Finding("major", "python", rel, f"Python compile failure: {exc.msg}"))


def scan_directory(root: Path) -> dict[str, object]:
    findings: list[Finding] = []
    inventory: list[dict[str, object]] = []
    relationships: list[dict[str, str]] = []
    frontmatter_names: dict[str, list[str]] = {}
    normative_occurrences: dict[str, set[str]] = {}

    if not root.is_dir():
        raise ScanError(f"target is not a directory: {root}")

    entries = list(iter_entries(root))
    if not entries:
        findings.append(Finding("major", "package", ".", "target contains no files"))

    for path in entries:
        rel = relative(path, root)
        if path.is_symlink():
            findings.append(Finding("major", "package", rel, "symlink found; review target and archive semantics"))
            continue
        asset_type = classify(path, root)
        item: dict[str, object] = {
            "path": rel,
            "asset_type": asset_type,
            "size": path.stat().st_size,
            "sha256": sha256(path),
        }
        if path.stat().st_size > 1024 * 1024:
            findings.append(Finding("minor", "size", rel, "file is larger than 1 MiB and may increase context cost"))
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in ASSET_NAMES:
            text = read_text(path, findings, root)
            if text is not None:
                item.update(check_text_file(path, text, root, findings))
                for normalized in normalized_normative_lines(text):
                    normative_occurrences.setdefault(normalized, set()).add(rel)
                if path.suffix.lower() == ".md":
                    for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
                        target = relation_target(path, raw_target, root)
                        if target:
                            relationships.append({"from": rel, "type": "reads", "to": target})
                    for raw_target in DECLARED_PATH_PATTERN.findall(text):
                        target = relation_target(path, raw_target, root)
                        if target:
                            relationships.append({"from": rel, "type": "reads", "to": target})
                frontmatter = item.get("frontmatter")
                if asset_type in IDENTITY_ASSET_TYPES and isinstance(frontmatter, dict) and isinstance(frontmatter.get("name"), str):
                    frontmatter_names.setdefault(frontmatter["name"], []).append(rel)
        if path.suffix.lower() == ".json":
            check_json(path, root, findings)
        if path.suffix.lower() == ".toml":
            check_toml(path, root, findings)
        if path.suffix.lower() == ".py":
            check_python(path, root, findings)
        inventory.append(item)

    for name, paths in sorted(frontmatter_names.items()):
        if len(paths) > 1:
            findings.append(Finding("major", "identity", ", ".join(paths), f"duplicate frontmatter name: {name}"))

    duplicate_normative_groups = 0
    for normalized, paths in sorted(normative_occurrences.items()):
        if len(paths) >= 3:
            duplicate_normative_groups += 1
            rendered_paths = ", ".join(sorted(paths))
            findings.append(Finding("minor", "context-noise", rendered_paths, f"identical normative instruction is repeated across {len(paths)} files: {normalized[:120]}"))

    skill_paths = [item["path"] for item in inventory if item["path"] == "SKILL.md" or str(item["path"]).endswith("/SKILL.md")]
    if len(skill_paths) > 1:
        findings.append(Finding("minor", "package", ".", "multiple SKILL.md files found; validate package roots explicitly"))

    counts: dict[str, int] = {}
    for item in inventory:
        asset_type = str(item["asset_type"])
        counts[asset_type] = counts.get(asset_type, 0) + 1

    severity_order = {"critical": 4, "major": 3, "minor": 2, "note": 1}
    highest = max((severity_order[item.severity] for item in findings), default=0)
    disposition = "revise" if highest >= 3 else "pass"

    text_items = [item for item in inventory if "lines" in item]
    total_lines = sum(int(item.get("lines", 0)) for item in text_items)
    total_text_bytes = sum(int(item.get("size", 0)) for item in text_items)
    total_normative = sum(int(item.get("normative_lines", 0)) for item in text_items)
    longest = max(text_items, key=lambda item: int(item.get("lines", 0)), default=None)

    return {
        "scanner": "mols-agent-asset-validator/scripts/scan_assets.py",
        "evidence_level": "verified",
        "target": str(root),
        "inventory": inventory,
        "relationships": relationships,
        "asset_counts": counts,
        "analysis_signals": {
            "text_files": len(text_items),
            "total_text_bytes": total_text_bytes,
            "total_lines": total_lines,
            "normative_lines": total_normative,
            "normative_density": round(total_normative / max(1, total_lines), 4),
            "duplicate_normative_groups": duplicate_normative_groups,
            "relationship_count": len(relationships),
            "longest_text_file": None if longest is None else {"path": longest["path"], "lines": longest["lines"]}
        },
        "findings": [asdict(item) for item in findings],
        "summary": {
            "files": len(inventory),
            "critical": sum(item.severity == "critical" for item in findings),
            "major": sum(item.severity == "major" for item in findings),
            "minor": sum(item.severity == "minor" for item in findings),
            "note": sum(item.severity == "note" for item in findings),
            "disposition": disposition,
        },
        "limitations": [
            "No model-based semantic, trigger, behavioral, orchestration, stability, or runtime evaluation was performed.",
            "Instruction-bottleneck and context-noise metrics are deterministic signals, not semantic proof.",
            "YAML syntax is not parsed because the scanner intentionally uses only the Python standard library."
        ],
    }


def scan_target(target: Path) -> dict[str, object]:
    if target.is_dir():
        return scan_directory(target.resolve())
    if target.is_file() and target.suffix.lower() == ".zip":
        with tempfile.TemporaryDirectory(prefix="agent-asset-scan-") as temp_dir:
            extracted = Path(temp_dir) / "package"
            extracted.mkdir()
            extract_zip_safely(target, extracted)
            result = scan_directory(extracted)
            result["archive"] = {"path": str(target), "sha256": sha256(target)}
            result["target"] = str(target)
            return result
    raise ScanError("target must be a directory or ZIP archive")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="exit non-zero on any finding")
    args = parser.parse_args()

    try:
        result = scan_target(args.target)
    except (OSError, ScanError, zipfile.BadZipFile) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    summary = result["summary"]
    if args.strict and sum(int(summary[key]) for key in ("critical", "major", "minor", "note")):
        return 1
    if int(summary["critical"]) or int(summary["major"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
