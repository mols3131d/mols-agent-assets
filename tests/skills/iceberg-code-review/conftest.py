import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC_SCRIPTS = ROOT / "src" / "skills" / "iceberg-code-review" / "scripts"
RELEASE_SCRIPTS = ROOT / "release" / "skills" / "iceberg-code-review" / "scripts"

if SRC_SCRIPTS.exists():
    sys.path.insert(0, str(SRC_SCRIPTS))
if RELEASE_SCRIPTS.exists():
    sys.path.insert(0, str(RELEASE_SCRIPTS))
