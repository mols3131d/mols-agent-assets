from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = (
    Path(__file__).resolve().parents[3]
    / ".agentsmesh"
    / "skills"
    / "mols-markdown-dashboard"
)
sys.path.insert(0, str(SKILL_ROOT / "src"))
