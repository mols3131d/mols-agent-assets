from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


class AssetError(Exception):
    pass


def load_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise AssetError(f"{path}: missing YAML frontmatter")
    if yaml is None:
        raise AssetError("PyYAML is required: install pyyaml")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise AssetError(f"{path}: frontmatter must be a mapping")
    return data, text[match.end() :]


def relative_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    links = []
    for target in LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip()
        if target and "://" not in target and not target.startswith(("mailto:", "#")):
            links.append(target)
    return links


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
