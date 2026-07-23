import subprocess
import sys
import tempfile
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))


def test_initialize_kanban():
    # Find script path
    repo_root = Path(__file__).resolve().parents[3]
    script_path = (
        repo_root
        / "src"
        / "skills"
        / "mols-kanban-markdown"
        / "scripts"
        / "initialize.py"
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "test-kanban"

        # Execute the script using subprocess
        # Pass the source assets directory by resolving it inside the script
        result = subprocess.run(
            [sys.executable, str(script_path), str(tmp_path)],
            capture_output=True,
            text=True,
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        assert result.returncode == 0

        # Verify directories created
        assert (tmp_path).exists()
        assert (tmp_path / ".configs").exists()
        assert (tmp_path / "backlog").exists()
        assert (tmp_path / "active").exists()
        assert (tmp_path / "archive").exists()

        # Verify files copied
        assert (tmp_path / ".configs" / "config.jsonc").exists()
        assert (tmp_path / ".configs" / "template.md").exists()
        assert (tmp_path / "AGENTS.md").exists()
        assert (tmp_path / "README.md").exists()
