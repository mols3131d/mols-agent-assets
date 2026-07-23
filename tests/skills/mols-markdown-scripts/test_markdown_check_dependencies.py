import subprocess
import sys
from pathlib import Path

def test_check_dependencies():
    repo_root = Path(__file__).resolve().parents[3]
    script_path = (
        repo_root
        / "src"
        / "skills"
        / "mols-markdown-scripts"
        / "scripts"
        / "check_dependencies.py"
    )
    
    # Run the dependency check script
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )
    
    # Since we are running in tests inside a configured python environment,
    # it should pass successfully or fail gracefully based on system requirements.
    # We assert that we get a structured exit code (0 or 1) and output is printed.
    assert result.returncode in (0, 1)
    if result.returncode == 0:
        assert "verified successfully" in result.stdout
    else:
        assert "Dependency Check Failed" in result.stderr
