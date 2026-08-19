from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evals/regression/rulesync-source-isolation.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def directory_names(path: Path) -> set[str]:
    return {entry.name for entry in path.iterdir() if entry.is_dir()}


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    end = text.find("\n---\n", 4)
    assert end >= 0, path
    data = yaml.safe_load(text[4:end])
    assert isinstance(data, dict), path
    return data


def test_rulesync_source_matches_regression_contract() -> None:
    contract = load_contract()["canonical"]
    workspace = ROOT / contract["workspace"]
    source = ROOT / contract["asset_root"]
    config = json.loads((ROOT / contract["config"]).read_text(encoding="utf-8"))

    assert source == workspace / ".rulesync"
    assert config["targets"] == contract["targets"]
    assert config["features"] == contract["features"]

    rules = source / "rules"
    assert {path.name for path in rules.glob("*.md")} == set(contract["rules"])

    skills = source / "skills"
    assert directory_names(skills) == set(contract["skills"])
    for name in contract["skills"]:
        assert (skills / name / "SKILL.md").is_file()

    subagents = source / "subagents"
    assert {path.stem for path in subagents.glob("*.md")} == set(contract["subagents"])


def test_antigravity_subagents_use_native_tool_ids() -> None:
    subagents = ROOT / load_contract()["canonical"]["asset_root"] / "subagents"
    expected = {
        "review-adversarial": {"view_file", "grep_search"},
        "review-lead": {
            "view_file",
            "grep_search",
            "invoke_subagent",
            "replace_file_content",
        },
        "review-quality": {"run_command", "view_file", "grep_search"},
    }

    for name, tools in expected.items():
        frontmatter = load_frontmatter(subagents / f"{name}.md")
        section = frontmatter["antigravity-ide"]
        assert isinstance(section, dict)
        assert set(section["tools"]) == tools


def test_antigravity_reviewers_preserve_native_roles() -> None:
    subagents = ROOT / load_contract()["canonical"]["asset_root"] / "subagents"

    for name in ("review-adversarial", "review-quality"):
        frontmatter = load_frontmatter(subagents / f"{name}.md")
        section = frontmatter["antigravity-ide"]
        assert isinstance(section, dict)
        assert section["mainAgent"] is False
        assert section["subagent"] is True

    lead = load_frontmatter(subagents / "review-lead.md")["antigravity-ide"]
    assert isinstance(lead, dict)
    assert "mainAgent" not in lead
    assert "subagent" not in lead


def test_distribution_assets_are_not_repository_runtime_configuration() -> None:
    contract = load_contract()

    for path in contract["forbidden_repository_runtime_surfaces"]:
        assert not (ROOT / path).exists(), path

    for path in contract["forbidden_workspace_generated_surfaces"]:
        assert not (ROOT / path).exists(), path

    for path in contract["repository_local_exceptions"]:
        assert (ROOT / path).exists(), path


def test_deployable_skill_surface_excludes_repository_verification() -> None:
    contract = load_contract()
    source = ROOT / contract["canonical"]["asset_root"] / "skills"
    surface = contract["package_surface"]
    forbidden_top_level = set(surface["forbid_top_level_dirs"])

    assert surface["forbid_dot_paths"] is True
    for skill_root in (path for path in source.iterdir() if path.is_dir()):
        assert directory_names(skill_root).isdisjoint(forbidden_top_level), (
            f"repository verification leaked into deployable Skill surface: "
            f"{skill_root.relative_to(ROOT)}"
        )
        nested_entrypoints = [
            path.relative_to(skill_root)
            for path in skill_root.rglob("SKILL.md")
            if path != skill_root / "SKILL.md"
        ]
        assert not nested_entrypoints, (
            "Rulesync treats every basename SKILL.md as a Skill entrypoint and omits "
            f"nested copies from projection: {skill_root.relative_to(ROOT)} "
            f"{nested_entrypoints}"
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


def test_rulesync_toolchain_tracks_latest() -> None:
    runner = (ROOT / "scripts/run_rulesync.py").read_text(encoding="utf-8")
    assert '"rulesync@latest"' in runner
    assert "RULESYNC_VERSION" not in runner
    assert not (ROOT / "package-lock.json").exists()


def test_repository_rulesync_commands_keep_write_validation_isolated() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package["scripts"]

    assert set(scripts) == {
        "rulesync:doctor",
        "rulesync:preview",
        "rulesync:validate",
    }
    assert scripts["rulesync:doctor"].endswith(" doctor")
    assert scripts["rulesync:preview"].endswith(" preview")
    assert scripts["rulesync:validate"].endswith(" validate")

    workflow = (ROOT / ".github/workflows/rulesync.yml").read_text(encoding="utf-8")
    assert "npm run rulesync:doctor" in workflow
    assert "npm run rulesync:validate" in workflow
    assert "rulesync generate" not in workflow
