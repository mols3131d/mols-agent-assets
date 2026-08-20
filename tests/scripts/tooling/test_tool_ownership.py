from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MISE = ROOT / "mise.toml"
PYPROJECT = ROOT / "pyproject.toml"
PYTHON_VERSION = ROOT / ".python-version"
LEFTHOOK = ROOT / "lefthook.yml"
PACKAGE = ROOT / "package.json"
BIOME = ROOT / "biome.json"


def test_mise_owns_repository_tools_but_not_python() -> None:
    config = MISE.read_text(encoding="utf-8")

    for tool in ["uv", "node", "rumdl", "lefthook", '"npm:@biomejs/biome"']:
        assert f"{tool} =" in config
    assert "python =" not in config


def test_uv_owns_python_and_python_dependencies() -> None:
    pyproject = PYPROJECT.read_text(encoding="utf-8")

    assert PYTHON_VERSION.read_text(encoding="utf-8").strip() == "3.13"
    assert 'requires-python = ">=3.13"' in pyproject
    assert '"ruff>=0.15.15"' in pyproject
    assert "rumdl" not in pyproject
    assert "lefthook" not in pyproject


def test_hooks_preserve_tool_ownership() -> None:
    config = LEFTHOOK.read_text(encoding="utf-8")

    assert "mise exec -- rumdl" in config
    assert "mise exec -- biome" in config
    assert "mise exec -- uv run ruff" in config
    assert "mise exec -- uv run python" in config
    assert "mise exec -- uv run pytest" in config
    assert "uv run rumdl" not in config


def test_node_scripts_route_python_through_uv() -> None:
    package = PACKAGE.read_text(encoding="utf-8")

    assert '"rulesync:doctor": "uv run python ' in package
    assert '"eval:promptfoo:mols-rpi": "uv run python ' in package
    assert '"rulesync:doctor": "python ' not in package


def test_biome_is_repository_configured() -> None:
    config = BIOME.read_text(encoding="utf-8")

    assert '"$schema": "https://biomejs.dev/schemas/2.5.6/schema.json"' in config
    assert '"recommended": true' in config
