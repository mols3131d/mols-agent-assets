import json

from scripts import generate_distribution_routes


def write_skill(path, name, description):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n",
        encoding="utf-8",
    )


def test_render_skill_route_uses_meta_sorted_entries_and_sources(tmp_path):
    write_skill(tmp_path / "beta" / "SKILL.md", "beta", "Beta skill")
    write_skill(tmp_path / "alpha" / "SKILL.md", "alpha", "Alpha skill")

    content = generate_distribution_routes.render_skill_route(
        tmp_path,
        "https://example.test/{name}/SKILL.md",
    )
    rows = [json.loads(line) for line in content.splitlines()]

    assert rows[0] == {
        "_meta": {
            "kind": "skills",
            "instructions": generate_distribution_routes.INSTRUCTION,
        }
    }
    assert rows[1:] == [
        {
            "name": "alpha",
            "description": "Alpha skill",
            "source": "https://example.test/alpha/SKILL.md",
        },
        {
            "name": "beta",
            "description": "Beta skill",
            "source": "https://example.test/beta/SKILL.md",
        },
    ]


def test_distribution_and_repository_local_route_surfaces_are_distinct():
    root = generate_distribution_routes.ROOT
    assert generate_distribution_routes.CANONICAL_SKILLS.relative_to(root).as_posix() == (
        "src/rulesync/.rulesync/skills"
    )
    assert generate_distribution_routes.DISTRIBUTION_SKILL_ROUTE.relative_to(
        root
    ).as_posix() == "route/skills.jsonl"
    assert generate_distribution_routes.REPOSITORY_LOCAL_ROUTE_DIR.relative_to(
        root
    ).as_posix() == ".agents/routes"
    assert (
        generate_distribution_routes.DISTRIBUTION_ROUTE_DIR
        != generate_distribution_routes.REPOSITORY_LOCAL_ROUTE_DIR
    )


def test_committed_distribution_skill_route_is_current():
    expected = generate_distribution_routes.render_skill_route()
    actual = generate_distribution_routes.DISTRIBUTION_SKILL_ROUTE.read_text(
        encoding="utf-8"
    )
    assert actual == expected


def test_canonical_skill_directory_contains_no_route_index():
    assert not (generate_distribution_routes.CANONICAL_SKILLS / "INDEX.jsonl").exists()
