from pathlib import Path

import pytest

from src.scripts.sync_github_files import (
    filename_from_url,
    github_blob_to_raw,
    resolve_dest_path,
)


def test_github_blob_to_raw():
    url = "https://github.com/owner/repo/blob/main/src/rules/antigravity.md"

    assert github_blob_to_raw(url) == (
        "https://raw.githubusercontent.com/owner/repo/main/src/rules/antigravity.md"
    )


def test_non_github_url_is_returned_as_is():
    url = "https://example.com/files/sample.md"

    assert github_blob_to_raw(url) == url


def test_filename_from_url():
    url = "https://github.com/owner/repo/blob/main/src/rules/antigravity.md"

    assert filename_from_url(url) == "antigravity.md"


def test_filename_from_url_without_filename_raises():
    with pytest.raises(ValueError):
        filename_from_url("https://github.com/owner/repo/blob/main/src/rules/")


def test_resolve_dest_path_directory():
    source_url = "https://github.com/owner/repo/blob/main/src/rules/antigravity.md"

    assert resolve_dest_path(source_url, ".agents/rules/") == Path(
        ".agents/rules/antigravity.md"
    )


def test_resolve_dest_path_file_rename():
    source_url = "https://github.com/owner/repo/blob/main/src/rules/antigravity.md"

    assert resolve_dest_path(source_url, ".agents/rules/custom.md") == Path(
        ".agents/rules/custom.md"
    )
