from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals/regression/agentsmesh-source-isolation.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def directory_names(path: Path) -> set[str]:
    return {entry.name for entry in path.iterdir() if entry.is_dir()}


def test_agentsmesh_source_matches_regression_contract() -> None:
    contract = load_contract()["canonical"]
    source = ROOT / contract["root"]
    config = yaml.safe_load((ROOT / contract["config"]).read_text(encoding="utf-8"))

    assert config["version"] == 1
    assert config["targets"] == contract["targets"]
    assert config["features"] == contract["features"]

    rules = source / "rules"
    assert {path.name for path in rules.glob("*.md")} == set(contract["rules"])

    skills = source / "skills"
    assert directory_names(skills) == set(contract["skills"])
    for name in contract["skills"]:
        assert (skills / name / "SKILL.md").is_file()

    agents = source / "agents"
    assert {path.stem for path in agents.glob("*.md")} == set(contract["agents"])


def test_distribution_assets_are_not_repository_runtime_configuration() -> None:
    contract = load_contract()

    for path in contract["forbidden_repository_runtime_surfaces"]:
        assert not (ROOT / path).exists(), path

    for path in contract["repository_local_exceptions"]:
        assert (ROOT / path).exists(), path


def test_deployable_skill_surface_excludes_repository_verification() -> None:
    contract = load_contract()
    source = ROOT / contract["canonical"]["root"] / "skills"
    surface = contract["package_surface"]
    forbidden_top_level = set(surface["forbid_top_level_dirs"])

    assert surface["forbid_dot_paths"] is True
    for skill_root in (path for path in source.iterdir() if path.is_dir()):
        assert directory_names(skill_root).isdisjoint(forbidden_top_level), (
            f"repository verification leaked into deployable Skill surface: "
            f"{skill_root.relative_to(ROOT)}"
        )
        for path in skill_root.rglob("*"):
            relative = path.relative_to(skill_root)
            assert not any(part.startswith(".") for part in relative.parts), (
                f"non-runtime dot path leaked into deployable Skill surface: "
                f"{skill_root.relative_to(ROOT)}/{relative}"
            )


def test_retired_legacy_surfaces_do_not_return() -> None:
    for path in load_contract()["retired"]:
        assert not (ROOT / path).exists(), path


def test_agentsmesh_toolchain_stays_pinned() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["devDependencies"]["agentsmesh"] == "0.32.0"
