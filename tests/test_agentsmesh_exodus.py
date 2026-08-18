from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals/regression/agentsmesh-exodus.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def directory_names(path: Path) -> set[str]:
    return {entry.name for entry in path.iterdir() if entry.is_dir()}


def skill_roots() -> list[Path]:
    contract = load_contract()
    names = contract["canonical"]["skills"]
    roots = [ROOT / ".agentsmesh/skills" / name for name in names]
    for projection in contract["projections"].values():
        roots.extend(ROOT / projection["skills"] / name for name in names)
    return roots


def test_agentsmesh_config_matches_regression_contract() -> None:
    contract = load_contract()["canonical"]
    config = yaml.safe_load((ROOT / "agentsmesh.yaml").read_text(encoding="utf-8"))

    assert config["version"] == 1
    assert config["targets"] == contract["targets"]
    assert config["features"] == contract["features"]


def test_canonical_rules_skills_and_agents_match_regression_contract() -> None:
    contract = load_contract()["canonical"]

    rules = ROOT / ".agentsmesh/rules"
    assert {path.name for path in rules.glob("*.md")} == set(contract["rules"])

    skills = ROOT / ".agentsmesh/skills"
    assert directory_names(skills) == set(contract["skills"])
    for name in contract["skills"]:
        assert (skills / name / "SKILL.md").is_file()

    agents = ROOT / ".agentsmesh/agents"
    assert {path.stem for path in agents.glob("*.md")} == set(contract["agents"])


def test_active_target_projections_cover_supported_canonical_assets() -> None:
    contract = load_contract()
    expected_skills = set(contract["canonical"]["skills"])
    expected_agents = set(contract["canonical"]["agents"])

    for projection in contract["projections"].values():
        assert (ROOT / projection["root_rule"]).is_file()

        projected_skill_names = directory_names(ROOT / projection["skills"])
        agent_mode = projection.get("agent_mode")

        if agent_mode == "embedded-skill":
            prefix = projection["agent_prefix"]
            expected_embedded_agents = {f"{prefix}{name}" for name in expected_agents}
            assert projected_skill_names == expected_skills | expected_embedded_agents
            for name in expected_embedded_agents:
                assert (ROOT / projection["skills"] / name / "SKILL.md").is_file()
        else:
            assert projected_skill_names == expected_skills

        if agent_mode == "native":
            projected_agents = ROOT / projection["agents"]
            assert {
                path.name.removesuffix(".agent.md")
                for path in projected_agents.glob("*.agent.md")
            } == expected_agents


def test_deployable_skill_surface_excludes_repository_verification() -> None:
    surface = load_contract()["package_surface"]
    assert surface["forbid_dot_paths"] is True
    forbidden_top_level = set(surface["forbid_top_level_dirs"])

    for skill_root in skill_roots():
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


def test_declared_exceptions_remain_explicit() -> None:
    for path in load_contract()["exceptions"]:
        assert (ROOT / path).exists(), path


def test_retired_legacy_surfaces_do_not_return() -> None:
    for path in load_contract()["retired"]:
        assert not (ROOT / path).exists(), path


def test_pinned_agentsmesh_version_matches_generated_lock() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    lock = yaml.safe_load((ROOT / ".agentsmesh/.lock").read_text(encoding="utf-8"))

    assert package["devDependencies"]["agentsmesh"] == "0.32.0"
    assert lock["lib_version"] == "0.32.0"
