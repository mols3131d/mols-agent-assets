from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_CONFIG = ROOT / "rulesync.jsonc"
REPOSITORY_LOCK = ROOT / "rulesync.lock"
LIBRARY_CONFIG = ROOT / "src" / "rulesync" / "rulesync.jsonc"
LIBRARY_SOURCE = ROOT / "src" / "rulesync" / ".rulesync"
INTERNAL_SKILL_TARGET = "agentsskills"
FORBIDDEN_LIBRARY_GENERATED_SURFACES = (
    ROOT / "src" / "rulesync" / ".github",
    ROOT / "src" / "rulesync" / ".agents",
    ROOT / "src" / "rulesync" / "rulesync.lock",
    ROOT / "src" / "rulesync" / "rulesync-npm.lock.json",
)
VERIFICATION_DIRS = {"tests", "evals", "scenarios", "results"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def directory_names(path: Path) -> set[str]:
    return {entry.name for entry in path.iterdir() if entry.is_dir()}


def load_frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", path
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"missing closing frontmatter delimiter: {path}") from error
    return yaml.safe_load("\n".join(lines[1:end])) or {}


def configured_targets(path: Path) -> set[str]:
    targets = load_json(path)["targets"]
    assert isinstance(targets, list) and targets
    return set(targets)


def test_library_workspace_is_canonical_and_target_scoped() -> None:
    assert LIBRARY_SOURCE == LIBRARY_CONFIG.parent / ".rulesync"
    assert LIBRARY_SOURCE.is_dir()
    assert configured_targets(LIBRARY_CONFIG)

    skills = LIBRARY_SOURCE / "skills"
    assert skills.is_dir()
    for skill_root in skills.iterdir():
        if skill_root.is_dir():
            assert (skill_root / "SKILL.md").is_file(), skill_root


def test_library_assets_declare_explicit_targets() -> None:
    supported = configured_targets(LIBRARY_CONFIG)
    allowed = supported | {INTERNAL_SKILL_TARGET}

    skill_files = sorted((LIBRARY_SOURCE / "skills").glob("*/SKILL.md"))
    subagent_files = sorted((LIBRARY_SOURCE / "subagents").glob("*.md"))
    assert skill_files
    assert subagent_files

    for path in [*skill_files, *subagent_files]:
        targets = load_frontmatter(path).get("targets")
        assert isinstance(targets, list) and targets, path
        assert "*" not in targets, path
        assert not (set(targets) - allowed), path

    for path in subagent_files:
        targets = set(load_frontmatter(path)["targets"])
        assert targets <= supported, path


def test_review_subagents_preserve_target_native_read_only_constraints() -> None:
    supported = configured_targets(LIBRARY_CONFIG)
    source = LIBRARY_SOURCE / "subagents"
    names = ("review-lead", "review-quality", "review-adversarial")
    frontmatter = {name: load_frontmatter(source / f"{name}.md") for name in names}

    for metadata in frontmatter.values():
        assert set(metadata["targets"]) == supported
        assert metadata["claudecode"]["permissionMode"] == "plan"
        assert metadata["codexcli"]["sandbox_mode"] == "read-only"

    assert "Agent" in frontmatter["review-lead"]["claudecode"]["tools"]
    assert "Agent" not in frontmatter["review-quality"]["claudecode"]["tools"]
    assert "Agent" not in frontmatter["review-adversarial"]["claudecode"]["tools"]
    assert "Bash" in frontmatter["review-quality"]["claudecode"]["tools"]
    assert "Bash" not in frontmatter["review-adversarial"]["claudecode"]["tools"]


def test_repository_and_library_workspaces_stay_separate() -> None:
    assert REPOSITORY_CONFIG != LIBRARY_CONFIG
    assert REPOSITORY_CONFIG.is_file()
    assert LIBRARY_SOURCE.is_dir()
    assert LIBRARY_CONFIG.is_file()

    for path in FORBIDDEN_LIBRARY_GENERATED_SURFACES:
        assert not path.exists(), path


def test_repository_workspace_declared_skills_match_lock() -> None:
    config = load_json(REPOSITORY_CONFIG)
    lock = load_json(REPOSITORY_LOCK)

    configured_sources = config.get("sources")
    assert isinstance(configured_sources, list) and configured_sources

    locked_sources = lock.get("sources")
    assert isinstance(locked_sources, dict)

    configured_by_source = {source["source"]: source for source in configured_sources}
    assert len(configured_by_source) == len(configured_sources)
    assert set(locked_sources) == set(configured_by_source)

    for source_name, source in configured_by_source.items():
        locked = locked_sources[source_name]
        if "ref" in source:
            assert locked.get("requestedRef") == source["ref"]
        assert set(locked.get("skills", {})) == set(source.get("skills", []))


def test_deployable_skill_surface_excludes_repository_verification() -> None:
    source = LIBRARY_SOURCE / "skills"

    for skill_root in (path for path in source.iterdir() if path.is_dir()):
        assert directory_names(skill_root).isdisjoint(VERIFICATION_DIRS), (
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
