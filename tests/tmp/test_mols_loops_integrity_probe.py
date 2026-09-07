from __future__ import annotations

import hashlib
from pathlib import Path


def test_mols_loops_integrity_probe() -> None:
    path = Path("src/rulesync/.rulesync/skills/mols-loops/SKILL.md")
    content = path.read_text(encoding="utf-8")
    digest = hashlib.sha256()
    digest.update(b"SKILL.md")
    digest.update(b"\0")
    digest.update(content.encode())
    digest.update(b"\0")
    raise AssertionError(f"sha256-{digest.hexdigest()}")
