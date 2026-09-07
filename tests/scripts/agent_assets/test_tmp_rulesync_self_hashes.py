from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = (
    "artifact-consistency-inspector",
    "github-context",
    "mols-agent-asset",
    "mols-agent-asset-find",
    "mols-chatbot-bootstrap",
    "mols-markdown-for-human",
    "mols-markdown-maintenance",
    "mols-mermaid-chart",
    "mols-mermaid-diagram",
    "mols-loops",
)


def _integrity(skill: str) -> str:
    root = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / skill
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256-{digest.hexdigest()}"


def test_emit_rulesync_self_source_integrities() -> None:
    hashes = {skill: _integrity(skill) for skill in SKILLS}
    raise AssertionError(json.dumps(hashes, sort_keys=True))
