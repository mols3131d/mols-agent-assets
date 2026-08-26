import json

from scripts import generate_distribution_routes


def write_asset(path, name, description):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n",
        encoding="utf-8",
    )


def test_render_skill_route_uses_meta_sorted_entries_and_canonical_sources(tmp_path):
    write_asset(tmp_path / "beta-dir" / "SKILL.md", "beta", "Beta skill")
    write_asset(tmp_path / "alpha-dir" / "SKILL.md", "alpha", "Alpha skill")

    content = generate_distribution_routes.render_skill_route(
        tmp_path,
        "https://example.test/{directory}/SKILL.md",
    )
    rows = [json.loads(line) for line in content.splitlines()]

    assert rows[0] == {
        "_meta": {
            "kind": "skills",
            "instructions": generate_distribution_routes.SKILL_INSTRUCTION,
        }
    }
    assert rows[1:] == [
        {
            "name": "alpha",
            "description": "Alpha skill",
            "source": "https://example.test/alpha-dir/SKILL.md",
        },
        {
            "name": "beta",
            "description": "Beta skill",
            "source": "https://example.test/beta-dir/SKILL.md",
        },
    ]


def test_render_subagent_route_uses_meta_sorted_entries_and_canonical_sources(tmp_path):
    write_asset(tmp_path / "review-z.md", "review-z", "Review Z")
    write_asset(tmp_path / "review-a.md", "review-a", "Review A")

    content = generate_distribution_routes.render_subagent_route(
        tmp_path,
        "https://example.test/{filename}",
    )
    rows = [json.loads(line) for line in content.splitlines()]

    assert rows[0] == {
        "_meta": {
            "kind": "subagents",
            "instructions": generate_distribution_routes.SUBAGENT_INSTRUCTION,
        }
    }
    assert rows[1:] == [
        {
            "name": "review-a",
            "description": "Review A",
            "source": "https://example.test/review-a.md",
        },
        {
            "name": "review-z",
            "description": "Review Z",
            "source": "https://example.test/review-z.md",
        },
    ]


def test_render_routes_indexes_provided_agent_asset_kinds():
    rows = [
        json.loads(line)
        for line in generate_distribution_routes.render_routes().splitlines()
    ]

    assert rows[0] == {
        "_meta": {
            "kind": "routes",
            "instructions": generate_distribution_routes.ROUTE_INSTRUCTION,
        }
    }
    assert rows[1:] == [
        {
            "name": "skills",
            "description": "이 repository가 제공하는 reusable Skill",
            "source": f"{generate_distribution_routes.RAW_ROOT}/route/skills.jsonl",
        },
        {
            "name": "subagents",
            "description": "이 repository가 제공하는 reusable Subagent",
            "source": f"{generate_distribution_routes.RAW_ROOT}/route/subagents.jsonl",
        },
    ]


def test_distribution_and_repository_local_route_surfaces_are_distinct():
    root = generate_distribution_routes.ROOT
    assert generate_distribution_routes.CANONICAL_ASSET_ROOT.relative_to(
        root
    ).as_posix() == "src/rulesync/.rulesync"
    assert generate_distribution_routes.DISTRIBUTION_ROUTES_PATH.relative_to(
        root
    ).as_posix() == "route/routes.jsonl"
    assert generate_distribution_routes.REPOSITORY_LOCAL_ROUTE_DIR.relative_to(
        root
    ).as_posix() == ".agents/route"
    assert (
        generate_distribution_routes.DISTRIBUTION_ROUTE_DIR
        != generate_distribution_routes.REPOSITORY_LOCAL_ROUTE_DIR
    )


def test_route_entrypoint_targets_distribution_route_index():
    entrypoint = (
        generate_distribution_routes.DISTRIBUTION_ROUTE_DIR / "ROUTE.md"
    ).read_text(encoding="utf-8")
    expected_url = f"{generate_distribution_routes.RAW_ROOT}/route/routes.jsonl"
    assert expected_url in entrypoint


def test_committed_distribution_routes_are_current():
    expected = {
        generate_distribution_routes.DISTRIBUTION_ROUTES_PATH:
            generate_distribution_routes.render_routes(),
        generate_distribution_routes.DISTRIBUTION_SKILL_ROUTE:
            generate_distribution_routes.render_skill_route(),
        generate_distribution_routes.DISTRIBUTION_SUBAGENT_ROUTE:
            generate_distribution_routes.render_subagent_route(),
    }
    for path, content in expected.items():
        assert path.read_text(encoding="utf-8") == content


def test_canonical_skill_directory_contains_no_route_index():
    assert not (generate_distribution_routes.CANONICAL_SKILLS / "INDEX.jsonl").exists()
