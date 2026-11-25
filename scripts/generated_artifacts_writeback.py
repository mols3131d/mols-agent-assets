"""Payload contract shared by the generated artifacts Producer and Writer."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from scripts import generated_artifacts_sync as sync

ARTIFACT_NAME = "generated-sync-payload"
SCHEMA_VERSION = 1
MAX_METADATA_BYTES = 1024 * 1024
MAX_FILE_COUNT = 500
MAX_OUTPUT_PATH_DEPTH = 16
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_PAYLOAD_BYTES = 20 * 1024 * 1024
HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PROTECTED_CORE_OUTPUTS = frozenset(
    {
        "docs/INDEX.tsv",
        "catalog/INDEX.tsv",
        "route/routes.jsonl",
        ".agents/route/routes.jsonl",
        ".agents/route/all.jsonl",
        ".agents/route/uncategorized.jsonl",
    }
)


def is_safe_relative_posix_path(path: str) -> bool:
    """Accept only relative POSIX paths with no traversal or Git metadata."""
    if "\\" in path or any(
        ord(ch) < 32 or ord(ch) == 127 or 0xD800 <= ord(ch) <= 0xDFFF for ch in path
    ):
        return False
    return all(
        part and part.lower() not in {".", "..", ".git"} for part in path.split("/")
    )


def is_allowed_generated_output(path: str) -> bool:
    """Restrict writeback to generated indexes and direct route JSONL files."""
    if path.count("/") >= MAX_OUTPUT_PATH_DEPTH or not is_safe_relative_posix_path(
        path
    ):
        return False
    if not any(projection.output_matches(path) for projection in sync.PROJECTIONS):
        return False

    output = PurePosixPath(path)
    if path.startswith(("docs/", "catalog/")):
        return output.name == "INDEX.tsv"
    return output.suffix == ".jsonl" and output.parent.as_posix() in {
        "route",
        ".agents/route",
    }
