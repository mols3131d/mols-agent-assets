#!/usr/bin/env python3

"""Validate size limits for one or more Markdown files."""

from __future__ import annotations

import argparse
import glob
import json
import logging
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, cast

import pyromark
import yaml

LOGGER = logging.getLogger(__name__)

PARSER_OPTIONS = (
    pyromark.Options.ENABLE_TABLES
    | pyromark.Options.ENABLE_YAML_STYLE_METADATA_BLOCKS
    | pyromark.Options.ENABLE_GFM
)

MARKDOWN_SUFFIXES = frozenset({".md", ".markdown"})
DOCUMENT_CODE_LANGUAGES = frozenset(
    {"", "markdown", "md", "text", "plaintext", "rst", "asciidoc"}
)
CALLOUT_HEADER = re.compile(
    r"^[ \t]{0,3}(?:>[ \t]*)+\[![A-Za-z0-9][A-Za-z0-9_-]*\]"
    r"[+-]?(?:[ \t]+.*)?$",
    re.IGNORECASE,
)
SIZE_PATTERN = re.compile(
    r"^\s*(\d+)\s*(B|KB|MB|KIB|MIB)?\s*$",
    re.IGNORECASE,
)
SIZE_MULTIPLIERS = {
    "B": 1,
    "KB": 1000,
    "MB": 1000**2,
    "KIB": 1024,
    "MIB": 1024**2,
}

Span = tuple[int, int]
PathInput = str | Path


__all__ = (
    "ExclusionPolicy",
    "FrontMatterError",
    "Limits",
    "MarkdownAnalysis",
    "MarkdownParseError",
    "analyze_markdown",
    "check_markdown",
    "inspect_file",
)


class FrontMatterError(ValueError):
    """Raised when YAML front matter is invalid."""


class MarkdownParseError(ValueError):
    """Raised when Markdown events or source ranges are invalid."""


class BlockKind(str, Enum):
    """Supported Markdown block categories."""

    FRONT_MATTER = "front_matter"
    CODE_BLOCKS = "code_blocks"
    TABLES = "tables"
    CALLOUTS = "callouts"


@dataclass(frozen=True, slots=True)
class Limits:
    """Numeric limits applied to each file."""

    max_chars: int = 4000
    max_lines: int = 100
    max_excluded_chars: int = 1500
    max_excluded_lines: int = 40
    max_file_bytes: int = 32768

    def validate(self) -> None:
        """Reject negative limits."""
        invalid = [
            name
            for name in (
                "max_chars",
                "max_lines",
                "max_excluded_chars",
                "max_excluded_lines",
                "max_file_bytes",
            )
            if getattr(self, name) < 0
        ]
        if invalid:
            raise ValueError(f"Limits must be zero or greater: {', '.join(invalid)}")


@dataclass(frozen=True, slots=True)
class ExclusionPolicy:
    """Markdown sections excluded from effective counts."""

    exclude_front_matter: bool = True
    exclude_code_blocks: bool = True
    exclude_tables: bool = True
    exclude_callouts: bool = True
    count_document_code_blocks: bool = True


@dataclass(frozen=True, slots=True)
class ActiveBlock:
    """Open parser block awaiting its end event."""

    kind: BlockKind
    start: int
    data: object


@dataclass(frozen=True, slots=True)
class MarkdownAnalysis:
    """Parsed Markdown spans and effective content."""

    effective_text: str
    excluded_spans: tuple[Span, ...]
    chargeable_spans: tuple[Span, ...]
    category_spans: dict[BlockKind, tuple[Span, ...]]
    category_block_counts: dict[BlockKind, int]

    @property
    def effective_spans(self) -> tuple[Span, ...]:
        """Return excluded spans for backward compatibility."""
        return self.excluded_spans


def validate_front_matter(block: str) -> None:
    """Validate a YAML front matter block."""
    lines = block.splitlines()
    payload = block

    if lines and lines[0].strip() == "---":
        closing = next(
            (
                index
                for index, line in enumerate(lines[1:], start=1)
                if line.strip() in {"---", "..."}
            ),
            None,
        )
        if closing is None:
            raise FrontMatterError("Front matter has no closing delimiter.")
        payload = "\n".join(lines[1:closing])

    try:
        yaml.safe_load(payload)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        location = (
            f" at line {mark.line + 2}, column {mark.column + 1}"
            if mark is not None
            else ""
        )
        problem = getattr(error, "problem", None) or str(error)
        raise FrontMatterError(
            f"Invalid YAML front matter{location}: {problem}"
        ) from error


def is_callout(kind: object, raw_block: str) -> bool:
    """Return whether a block quote is a supported callout."""
    if kind is not None:
        return True

    first_line = next(
        (line for line in raw_block.splitlines() if line.strip()),
        "",
    )
    return CALLOUT_HEADER.fullmatch(first_line) is not None


def as_mapping(value: object) -> dict[str, Any] | None:
    """Narrow unknown objects to string-keyed mappings."""
    if not isinstance(value, dict):
        return None
    return cast(dict[str, Any], value)


def normalize_code_language(code_kind: object) -> str:
    """Extract a normalized fenced-code language."""
    if code_kind == "Indented":
        return ""

    code_kind_map = as_mapping(code_kind)
    if code_kind_map is None:
        return ""

    info = code_kind_map.get("Fenced")
    if not isinstance(info, str):
        return ""

    first_token = info.strip().split(maxsplit=1)[0] if info.strip() else ""
    return first_token.strip("{}.").casefold()


def is_document_code_block(code_kind: object) -> bool:
    """Return whether a code block can conceal document prose."""
    return normalize_code_language(code_kind) in DOCUMENT_CODE_LANGUAGES


def merge_spans(spans: Iterable[Span]) -> list[Span]:
    """Merge overlapping or adjacent byte spans."""
    merged: list[Span] = []

    for start, end in sorted(spans):
        if start == end:
            continue
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
            continue

        previous_start, previous_end = merged[-1]
        merged[-1] = (previous_start, max(previous_end, end))

    return merged


def event_span(source_range: Any, source_size: int) -> Span:
    """Validate and return a pyromark source range."""
    range_map = as_mapping(source_range)
    if range_map is None:
        raise MarkdownParseError("pyromark returned an unknown range format.")

    start = range_map.get("start")
    end = range_map.get("end")
    if not isinstance(start, int) or not isinstance(end, int):
        raise MarkdownParseError("pyromark range boundaries must be integers.")
    if not 0 <= start <= end <= source_size:
        raise MarkdownParseError(f"Invalid pyromark range: {start}..{end}")

    return start, end


def expand_to_full_lines(source: bytes, span: Span) -> Span:
    """Expand a block span to include its source line boundaries."""
    start, end = span
    line_start = source.rfind(b"\n", 0, start) + 1
    line_end = end

    if source[end : end + 2] == b"\r\n":
        line_end += 2
    elif source[end : end + 1] == b"\n":
        line_end += 1

    return line_start, line_end


def target_start(event: object) -> tuple[BlockKind, object] | None:
    """Map a parser start event to a tracked block category."""
    event_map = as_mapping(event)
    if event_map is None:
        return None
    tag = as_mapping(event_map.get("Start"))
    if tag is None:
        return None

    if tag.get("MetadataBlock") == "YamlStyle":
        return BlockKind.FRONT_MATTER, tag["MetadataBlock"]
    if "CodeBlock" in tag:
        return BlockKind.CODE_BLOCKS, tag["CodeBlock"]
    if "Table" in tag:
        return BlockKind.TABLES, tag["Table"]
    if "BlockQuote" in tag:
        return BlockKind.CALLOUTS, tag["BlockQuote"]
    return None


def target_end(event: object) -> BlockKind | None:
    """Map a parser end event to a tracked block category."""
    event_map = as_mapping(event)
    if event_map is None or "End" not in event_map:
        return None

    tag = event_map["End"]
    if tag == "CodeBlock":
        return BlockKind.CODE_BLOCKS
    if tag == "Table":
        return BlockKind.TABLES
    tag_map = as_mapping(tag)
    if tag_map is not None:
        if tag_map.get("MetadataBlock") == "YamlStyle":
            return BlockKind.FRONT_MATTER
        if "BlockQuote" in tag_map:
            return BlockKind.CALLOUTS
    return None


def remove_spans(source: bytes, spans: Iterable[Span]) -> bytes:
    """Remove sorted, merged byte spans from a UTF-8 source buffer."""
    chunks: list[bytes] = []
    cursor = 0

    for start, end in spans:
        chunks.append(source[cursor:start])
        cursor = end

    chunks.append(source[cursor:])
    return b"".join(chunks)


def should_exclude_block(
    block: ActiveBlock,
    raw_block: str,
    policy: ExclusionPolicy,
) -> tuple[bool, bool]:
    """Return exclusion and chargeability decisions for one block."""
    if block.kind is BlockKind.FRONT_MATTER:
        validate_front_matter(raw_block)
        return policy.exclude_front_matter, False

    if block.kind is BlockKind.CODE_BLOCKS:
        excluded = policy.exclude_code_blocks and not (
            policy.count_document_code_blocks and is_document_code_block(block.data)
        )
        return excluded, excluded

    if block.kind is BlockKind.TABLES:
        return policy.exclude_tables, policy.exclude_tables

    if block.kind is BlockKind.CALLOUTS:
        excluded = policy.exclude_callouts and is_callout(block.data, raw_block)
        return excluded, excluded

    return False, False


def _analyze_markdown(text: str, policy: ExclusionPolicy) -> MarkdownAnalysis:
    """Parse Markdown and calculate excluded source spans."""
    source = text.encode("utf-8")
    active: list[ActiveBlock] = []
    category_spans: dict[BlockKind, list[Span]] = {kind: [] for kind in BlockKind}
    effective_spans: list[Span] = []
    chargeable_spans: list[Span] = []

    try:
        events = pyromark.events_with_range(text, options=PARSER_OPTIONS)
    except Exception as error:
        raise MarkdownParseError(str(error)) from error

    for event, source_range in events:
        start, end = event_span(source_range, len(source))
        started = target_start(event)
        if started is not None:
            kind, data = started
            active.append(ActiveBlock(kind=kind, start=start, data=data))
            continue

        ended = target_end(event)
        if ended is None:
            continue
        if not active or active[-1].kind != ended:
            raise MarkdownParseError(
                f"Markdown block events do not match: {ended.value}"
            )

        block = active.pop()
        span = expand_to_full_lines(source, (block.start, end))
        raw_block = source[span[0] : span[1]].decode("utf-8")
        excluded, chargeable = should_exclude_block(block, raw_block, policy)
        if not excluded:
            continue
        category_spans[block.kind].append(span)
        effective_spans.append(span)
        if chargeable:
            chargeable_spans.append(span)

    if active:
        kinds = ", ".join(block.kind.value for block in active)
        raise MarkdownParseError(f"Unclosed Markdown blocks: {kinds}")

    merged_excluded_spans = tuple(merge_spans(effective_spans))
    merged_chargeable_spans = tuple(merge_spans(chargeable_spans))
    merged_category_spans = {
        kind: tuple(merge_spans(spans)) for kind, spans in category_spans.items()
    }
    effective_bytes = remove_spans(source, merged_excluded_spans)
    return MarkdownAnalysis(
        effective_text=effective_bytes.decode("utf-8"),
        excluded_spans=merged_excluded_spans,
        chargeable_spans=merged_chargeable_spans,
        category_spans=merged_category_spans,
        category_block_counts={
            kind: len(spans) for kind, spans in category_spans.items()
        },
    )


def analyze_markdown(
    text: str,
    *,
    exclude_front_matter: bool = True,
    exclude_code_blocks: bool = True,
    exclude_tables: bool = True,
    exclude_callouts: bool = True,
    count_document_code_blocks: bool = True,
) -> MarkdownAnalysis:
    """Analyze one Markdown string using public exclusion options."""
    return _analyze_markdown(
        text,
        ExclusionPolicy(
            exclude_front_matter=exclude_front_matter,
            exclude_code_blocks=exclude_code_blocks,
            exclude_tables=exclude_tables,
            exclude_callouts=exclude_callouts,
            count_document_code_blocks=count_document_code_blocks,
        ),
    )


def count_lines(text: str) -> int:
    """Count logical text lines, returning zero for empty content."""
    if not text:
        return 0
    return text.count("\n") + int(not text.endswith("\n"))


def span_metrics(source: bytes, spans: Iterable[Span]) -> tuple[int, int]:
    """Count Unicode characters and lines across merged byte spans."""
    chars = 0
    lines = 0

    for start, end in spans:
        segment = source[start:end].decode("utf-8")
        chars += len(segment)
        lines += count_lines(segment)

    return chars, lines


def check_result(actual: int, limit: int) -> dict[str, int | bool]:
    """Build one limit-check result."""
    return {
        "passed": actual <= limit,
        "actual": actual,
        "limit": limit,
        "exceeded_by": max(0, actual - limit),
    }


def error_result(path: Path, code: str, message: str) -> dict[str, object]:
    """Build a failed file result for a processing error."""
    return {
        "path": str(path),
        "passed": False,
        "error": {"code": code, "message": message},
        "checks": None,
        "excluded": None,
    }


def _inspect_file(
    path: Path,
    limits: Limits,
    policy: ExclusionPolicy,
) -> dict[str, object]:
    """Inspect one Markdown file."""
    LOGGER.debug("Inspecting %s", path)
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        source = text.encode("utf-8")
        analysis = _analyze_markdown(text, policy)
    except FileNotFoundError:
        return error_result(path, "file_not_found", "File not found.")
    except PermissionError:
        return error_result(path, "permission_denied", "Permission denied.")
    except UnicodeDecodeError as error:
        return error_result(path, "invalid_encoding", f"Not valid UTF-8: {error}")
    except FrontMatterError as error:
        return error_result(path, "invalid_yaml", str(error))
    except MarkdownParseError as error:
        return error_result(path, "markdown_parse_error", str(error))
    except OSError as error:
        return error_result(path, "file_read_error", str(error))

    effective_chars = len(analysis.effective_text)
    effective_lines = count_lines(analysis.effective_text)
    excluded_chars, excluded_lines = span_metrics(source, analysis.chargeable_spans)
    checks = {
        "effective_chars": check_result(effective_chars, limits.max_chars),
        "effective_lines": check_result(effective_lines, limits.max_lines),
        "excluded_chars": check_result(excluded_chars, limits.max_excluded_chars),
        "excluded_lines": check_result(excluded_lines, limits.max_excluded_lines),
        "file_bytes": check_result(len(raw), limits.max_file_bytes),
    }

    excluded: dict[str, dict[str, int]] = {}
    for kind in BlockKind:
        chars, lines = span_metrics(source, analysis.category_spans[kind])
        excluded[kind.value] = {
            "blocks": analysis.category_block_counts[kind],
            "chars": chars,
            "lines": lines,
        }

    passed = all(bool(check["passed"]) for check in checks.values())
    LOGGER.debug(
        "Completed %s; passed=%s, effective_chars=%d, effective_lines=%d, "
        "excluded_chars=%d, excluded_lines=%d, file_bytes=%d",
        path,
        passed,
        effective_chars,
        effective_lines,
        excluded_chars,
        excluded_lines,
        len(raw),
    )
    return {
        "path": str(path),
        "passed": passed,
        "error": None,
        "checks": checks,
        "excluded": excluded,
    }


def inspect_file(
    path: PathInput,
    *,
    max_chars: int = 4000,
    max_lines: int = 100,
    max_excluded_chars: int = 1500,
    max_excluded_lines: int = 40,
    max_file_bytes: int = 32768,
    exclude_front_matter: bool = True,
    exclude_code_blocks: bool = True,
    exclude_tables: bool = True,
    exclude_callouts: bool = True,
    count_document_code_blocks: bool = True,
) -> dict[str, object]:
    """Inspect one Markdown file and return detailed results."""
    limits = Limits(
        max_chars=max_chars,
        max_lines=max_lines,
        max_excluded_chars=max_excluded_chars,
        max_excluded_lines=max_excluded_lines,
        max_file_bytes=max_file_bytes,
    )
    limits.validate()
    return _inspect_file(
        Path(path),
        limits,
        ExclusionPolicy(
            exclude_front_matter=exclude_front_matter,
            exclude_code_blocks=exclude_code_blocks,
            exclude_tables=exclude_tables,
            exclude_callouts=exclude_callouts,
            count_document_code_blocks=count_document_code_blocks,
        ),
    )


def normalize_inputs(paths: PathInput | Iterable[PathInput]) -> list[PathInput]:
    """Normalize a single path or iterable into a list."""
    if isinstance(paths, (str, Path)):
        return [paths]
    return list(paths)


def resolve_markdown_paths(
    paths: PathInput | Iterable[PathInput],
) -> tuple[list[Path], list[dict[str, str]], int]:
    """Expand paths and glob patterns into unique Markdown files."""
    inputs = normalize_inputs(paths)
    resolved: dict[str, Path] = {}
    errors: list[dict[str, str]] = []

    for path_input in inputs:
        pattern = str(Path(path_input).expanduser())
        has_magic = glob.has_magic(pattern)
        matches = glob.glob(pattern, recursive=True) if has_magic else [pattern]
        LOGGER.debug("Resolved input %r to %d candidate(s)", path_input, len(matches))

        if has_magic and not matches:
            errors.append(
                {
                    "input": str(path_input),
                    "code": "glob_no_match",
                    "message": "Glob pattern matched no files.",
                }
            )
            continue

        accepted = 0
        for match in matches:
            candidate = Path(match)
            if not candidate.exists():
                errors.append(
                    {
                        "input": str(path_input),
                        "code": "file_not_found",
                        "message": f"File not found: {candidate}",
                    }
                )
                continue
            if not candidate.is_file():
                if not has_magic:
                    errors.append(
                        {
                            "input": str(path_input),
                            "code": "not_a_file",
                            "message": f"Not a file: {candidate}",
                        }
                    )
                continue
            if candidate.suffix.casefold() not in MARKDOWN_SUFFIXES:
                if not has_magic:
                    errors.append(
                        {
                            "input": str(path_input),
                            "code": "unsupported_extension",
                            "message": (
                                "Unsupported file extension: "
                                f"{candidate.suffix or '<none>'}"
                            ),
                        }
                    )
                continue

            resolved.setdefault(str(candidate.resolve()), candidate)
            accepted += 1

        if has_magic and accepted == 0:
            errors.append(
                {
                    "input": str(path_input),
                    "code": "glob_no_markdown_match",
                    "message": "Glob pattern matched no Markdown files.",
                }
            )

    if not inputs:
        errors.append(
            {
                "input": "",
                "code": "empty_input",
                "message": "No files or glob patterns were provided.",
            }
        )

    files = sorted(resolved.values(), key=lambda path: path.as_posix())
    LOGGER.debug("Selected %d unique Markdown file(s)", len(files))
    return files, errors, len(inputs)


def build_details(
    *,
    limits: Limits,
    input_count: int,
    file_results: list[dict[str, object]],
    input_errors: list[dict[str, str]],
) -> dict[str, object]:
    """Aggregate file results into the public detail structure."""
    passed_file_count = sum(bool(result["passed"]) for result in file_results)
    failed_file_count = len(file_results) - passed_file_count
    error_file_count = sum(result["error"] is not None for result in file_results)
    passed = bool(file_results) and not input_errors and failed_file_count == 0

    return {
        "passed": passed,
        "summary": {
            "input_count": input_count,
            "matched_file_count": len(file_results),
            "passed_file_count": passed_file_count,
            "failed_file_count": failed_file_count,
            "error_file_count": error_file_count,
            "input_error_count": len(input_errors),
        },
        "limits": asdict(limits),
        "files": file_results,
        "errors": input_errors,
    }


def check_markdown(
    paths: PathInput | Iterable[PathInput],
    *,
    max_chars: int = 4000,
    max_lines: int = 100,
    max_excluded_chars: int = 1500,
    max_excluded_lines: int = 40,
    max_file_bytes: int = 32768,
    exclude_front_matter: bool = True,
    exclude_code_blocks: bool = True,
    exclude_tables: bool = True,
    exclude_callouts: bool = True,
    count_document_code_blocks: bool = True,
    return_details: bool = False,
) -> bool | dict[str, object]:
    """Validate Markdown files and return a boolean or detailed dictionary."""
    limits = Limits(
        max_chars=max_chars,
        max_lines=max_lines,
        max_excluded_chars=max_excluded_chars,
        max_excluded_lines=max_excluded_lines,
        max_file_bytes=max_file_bytes,
    )
    limits.validate()
    policy = ExclusionPolicy(
        exclude_front_matter=exclude_front_matter,
        exclude_code_blocks=exclude_code_blocks,
        exclude_tables=exclude_tables,
        exclude_callouts=exclude_callouts,
        count_document_code_blocks=count_document_code_blocks,
    )

    files, input_errors, input_count = resolve_markdown_paths(paths)
    file_results = [_inspect_file(path, limits, policy) for path in files]
    details = build_details(
        limits=limits,
        input_count=input_count,
        file_results=file_results,
        input_errors=input_errors,
    )
    LOGGER.debug(
        "Validation complete; passed=%s, matched=%d, input_errors=%d",
        details["passed"],
        len(file_results),
        len(input_errors),
    )
    return details if return_details else bool(details["passed"])


def parse_size(value: str) -> int:
    """Parse a byte size with optional decimal or binary units."""
    match = SIZE_PATTERN.fullmatch(value)
    if match is None:
        raise argparse.ArgumentTypeError(
            "Size must be an integer with an optional B, KB, MB, KiB, or MiB unit."
        )

    amount = int(match.group(1))
    unit = (match.group(2) or "B").upper()
    return amount * SIZE_MULTIPLIERS[unit]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate size limits for one or more Markdown files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Markdown file paths or glob patterns",
    )
    parser.add_argument("--max-chars", type=int, default=4000)
    parser.add_argument("--max-lines", type=int, default=100)
    parser.add_argument("--max-excluded-chars", type=int, default=1500)
    parser.add_argument("--max-excluded-lines", type=int, default=40)
    parser.add_argument(
        "--max-file-size",
        type=parse_size,
        default=32768,
        dest="max_file_bytes",
        metavar="SIZE",
        help="Maximum source file size, for example 32768, 32KiB, or 1MiB",
    )
    parser.add_argument(
        "--exclude-front-matter",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--exclude-code-blocks",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--exclude-tables",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--exclude-callouts",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--count-document-code-blocks",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Count document-like or unlabelled code blocks as regular content",
    )
    parser.add_argument(
        "--output",
        choices=("text", "table", "boolean", "json"),
        default="text",
        help="Output concise text, one overall boolean, or detailed JSON",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Write debug logs to stderr",
    )
    return parser.parse_args()


def configure_logging(debug: bool) -> None:
    """Enable concise debug logging for CLI execution."""
    if not debug:
        return
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(name)s: %(message)s",
    )


def configuration_error_details(message: str) -> dict[str, object]:
    """Build a JSON-compatible configuration error result."""
    return {
        "passed": False,
        "summary": {
            "input_count": 0,
            "matched_file_count": 0,
            "passed_file_count": 0,
            "failed_file_count": 0,
            "error_file_count": 0,
            "input_error_count": 1,
        },
        "limits": None,
        "files": [],
        "errors": [
            {
                "input": "",
                "code": "invalid_configuration",
                "message": message,
            }
        ],
    }


def format_cli_result(result: dict[str, object]) -> str:
    """Format a concise human-readable validation result."""
    summary = as_mapping(result.get("summary"))
    if summary is None:
        return str(bool(result.get("passed", False)))

    passed = bool(result.get("passed", False))
    matched = int(summary.get("matched_file_count", 0) or 0)
    passed_files = int(summary.get("passed_file_count", 0) or 0)
    failed_files = int(summary.get("failed_file_count", 0) or 0)
    input_errors = int(summary.get("input_error_count", 0) or 0)

    if passed:
        return f"True\t{passed_files}/{matched} files passed"

    summary_parts: list[str] = []
    if matched:
        summary_parts.append(f"{failed_files}/{matched} files failed")
    if input_errors:
        suffix = "error" if input_errors == 1 else "errors"
        summary_parts.append(f"{input_errors} input {suffix}")
    if not summary_parts:
        summary_parts.append("validation failed")

    lines = [f"False\t{'; '.join(summary_parts)}"]

    errors = result.get("errors", [])
    if isinstance(errors, list):
        for error in errors:
            error_map = as_mapping(error)
            if error_map is None:
                continue
            lines.extend(
                [
                    "",
                    str(error_map.get("input") or "<input>"),
                    (
                        f"\t{error_map.get('code', 'input_error')}\t"
                        f"{error_map.get('message', 'Input validation failed.')}"
                    ),
                ]
            )

    files = result.get("files", [])
    if isinstance(files, list):
        for file_result in files:
            file_map = as_mapping(file_result)
            if file_map is None or file_map.get("passed"):
                continue

            lines.extend(["", str(file_map.get("path", "<file>"))])
            error_map = as_mapping(file_map.get("error"))
            if error_map is not None:
                lines.append(
                    f"\t{error_map.get('code', 'file_error')}\t"
                    f"{error_map.get('message', 'File validation failed.')}"
                )
                continue

            checks = as_mapping(file_map.get("checks"))
            if checks is None:
                continue
            for name, check in checks.items():
                check_map = as_mapping(check)
                if check_map is None or check_map.get("passed"):
                    continue
                actual = check_map.get("actual", 0)
                limit = check_map.get("limit", 0)
                exceeded = check_map.get("exceeded_by", 0)
                lines.append(f"\t{name}\t{actual}/{limit}\t+{exceeded}")

    return "\n".join(lines)


def emit_result(result: dict[str, object], output: str) -> None:
    """Print the selected result representation."""
    if output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif output == "boolean":
        print(str(bool(result.get("passed", False))))
    else:
        print(format_cli_result(result))


def exit_code(result: dict[str, object]) -> int:
    """Map a result to the CLI exit code."""
    summary = as_mapping(result["summary"])
    if summary is None:
        return 2
    error_file_count = summary.get("error_file_count", 0)
    has_errors = bool(result["errors"]) or (
        isinstance(error_file_count, int) and error_file_count > 0
    )
    if has_errors:
        return 2
    return 0 if result["passed"] else 1


def main() -> int:
    """Run the command-line validator."""
    args = parse_args()
    configure_logging(args.debug)

    try:
        result = check_markdown(
            args.paths,
            max_chars=args.max_chars,
            max_lines=args.max_lines,
            max_excluded_chars=args.max_excluded_chars,
            max_excluded_lines=args.max_excluded_lines,
            max_file_bytes=args.max_file_bytes,
            exclude_front_matter=args.exclude_front_matter,
            exclude_code_blocks=args.exclude_code_blocks,
            exclude_tables=args.exclude_tables,
            exclude_callouts=args.exclude_callouts,
            count_document_code_blocks=args.count_document_code_blocks,
            return_details=True,
        )
        assert isinstance(result, dict)
    except ValueError as error:
        LOGGER.debug("Invalid configuration", exc_info=True)
        result = configuration_error_details(str(error))

    emit_result(result, args.output)
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
