from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals/regression/rulesync-source-isolation.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def directory_names(path: Path) -> set[str]:
    return {entry.name for entry in path.iterdir() if entry.is_dir()}


def test_library_workspace_is_canonical_and_target_neutral() -> None:
    contract = load_contract()["library_workspace"]
    source = ROOT / contract["asset_root"]
    config_path = ROOT / contract["config"]
    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert source == config_path.parent / ".rulesync"
    assert source.is_dir()
    assert config["targets"] == []
    assert contract["target_neutral"] is True

    skills = source / "skills"
    assert skills.is_dir()
    for skill_root in skills.iterdir():
        if skill_root.is_dir():
            assert (skill_root / "SKILL.md").is_file(), skill_root


def test_repository_and_library_workspaces_stay_separate() -> None:
    contract = load_contract()
    repository = contract["repository_workspace"]
    library = contract["library_workspace"]

    repository_source = ROOT / repository["asset_root"]
    repository_config = ROOT / repository["config"]
    library_source = ROOT / library["asset_root"]
    library_config = ROOT / library["config"]

    assert repository_source != library_source
    assert repository_config != library_config
    assert library_source.is_dir()
    assert library_config.is_file()

    if repository_source.exists() or repository_config.exists():
        assert repository_source.is_dir()
        assert repository_config.is_file()

    for path in contract["forbidden_library_generated_surfaces"]:
        assert not (ROOT / path).exists(), path


def test_deployable_skill_surface_excludes_repository_verification() -> None:
    source = ROOT / load_contract()["library_workspace"]["asset_root"] / "skills"
    forbidden = set(load_contract()["verification_dirs"])

    for skill_root in (path for path in source.iterdir() if path.is_dir()):
        assert directory_names(skill_root).isdisjoint(forbidden), (
            f"repository verification leaked into deployable Skill surface: "
            f"{skill_root.relative_to(ROOT)}"
        )

        nested_entrypoints = [
            path.relative_to(skill_root)
            for path in skill_root.rglob("SKILL.md")
            if path != skill_root / "SKILL.md"
        ]
        assert not nested_entrypoints, (
            "Rulesync treats every basename SKILL.md as a Skill entrypoint: "
            f"{skill_root.relative_to(ROOT)} {nested_entrypoints}"
        )


def test_rulesync_toolchain_is_reproducibly_pinned() -> None:
    mise = tomllib.loads((ROOT / "mise.toml").read_text(encoding="utf-8"))
    runner = (ROOT / "scripts/run_rulesync.py").read_text(encoding="utf-8")
    version = mise["tools"]["npm:rulesync"]

    parts = version.split(".")
    assert len(parts) == 3 and all(part.isdigit() for part in parts)
    assert 'shutil.which("rulesync")' in runner
    assert "rulesync@latest" not in runner
    assert not (ROOT / "package-lock.json").exists()


def test_repository_rulesync_commands_delegate_projection_to_rulesync() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package["scripts"]

    assert scripts["rulesync:doctor"].endswith(" doctor")
    assert scripts["rulesync:preview"].endswith(" preview")
    assert scripts["rulesync:validate"].endswith(" validate")

    runner = (ROOT / "scripts/run_rulesync.py").read_text(encoding="utf-8")
    assert "TemporaryDirectory" in runner
    assert "assert_projection" not in runner

    workflow = (ROOT / ".github/workflows/rulesync.yml").read_text(encoding="utf-8")
    assert "npm run rulesync:doctor" in workflow
    assert "rulesync generate" not in workflow
    assert "--targets" not in workflow
