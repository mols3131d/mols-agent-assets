from __future__ import annotations

import json
import stat
import zipfile
from pathlib import Path
from typing import Any

FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILE_MODE = stat.S_IFREG | 0o644


def _info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = FILE_MODE << 16
    return info


def write_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    archive.writestr(
        _info(name), data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
    )


def write_file(archive: zipfile.ZipFile, name: str, path: Path) -> None:
    write_bytes(archive, name, path.read_bytes())


def canonical_json(data: Any) -> bytes:
    return (
        json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
