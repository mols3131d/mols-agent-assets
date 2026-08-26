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
    route_rows = [
        {
            "name": "skills",
            "description": "작업 수행 방법을 선택·보강하는 reusable Skill",
            "source": f"{generate_distribution_routes.RAW_ROOT}/route/skills.jsonl",
        },
        {
            "name": "subagents",
            "description": "전문 역할로 위임하거나 독립 검토할 때 사용하는 reusable Subagent",
            "source": f"{generate_distribution_routes.RAW_ROOT}/route/subagents.jsonl",
        },
    ]
    rows = [
        json.loads(line)
        for line in generate_distribution_routes.render_routes(route_rows).splitlines()
    ]

    assert rows[0] == {
        "_meta": {
            "kind": "routes",
            "instructions": generate_distribution_routes.ROUTE_INSTRUCTION,
        }
    }
    assert rows[1:] == route_rows


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


def test_generate_returns_all_distribution_routes():
    assert set(generate_distribution_routes.generate()) == {
        generate_distribution_routes.DISTRIBUTION_ROUTES_PATH,
        generate_distribution_routes.DISTRIBUTION_SKILL_ROUTE,
        generate_distribution_routes.DISTRIBUTION_SUBAGENT_ROUTE,
    }


def test_generate_omits_empty_asset_kind_route(tmp_path, monkeypatch):
    skills = tmp_path / "skills"
    subagents = tmp_path / "subagents"
    subagents.mkdir()
    write_asset(skills / "alpha" / "SKILL.md", "alpha", "Alpha skill")
    monkeypatch.setattr(generate_distribution_routes, "CANONICAL_SKILLS", skills)
    monkeypatch.setattr(generate_distribution_routes, "CANONICAL_SUBAGENTS", subagents)

    outputs = generate_distribution_routes.generate()
    route_rows = [
        json.loads(line)
        for line in outputs[generate_distribution_routes.DISTRIBUTION_ROUTES_PATH].splitlines()
    ]

    assert set(outputs) == {
        generate_distribution_routes.DISTRIBUTION_ROUTES_PATH,
        generate_distribution_routes.DISTRIBUTION_SKILL_ROUTE,
    }
    assert [row["name"] for row in route_rows[1:]] == ["skills"]


def test_generate_keeps_only_route_index_when_no_asset_kind_exists(tmp_path, monkeypatch):
    skills = tmp_path / "skills"
    subagents = tmp_path / "subagents"
    skills.mkdir()
    subagents.mkdir()
    monkeypatch.setattr(generate_distribution_routes, "CANONICAL_SKILLS", skills)
    monkeypatch.setattr(generate_distribution_routes, "CANONICAL_SUBAGENTS", subagents)

    outputs = generate_distribution_routes.generate()
    rows = [
        json.loads(line)
        for line in outputs[generate_distribution_routes.DISTRIBUTION_ROUTES_PATH].splitlines()
    ]

    assert set(outputs) == {generate_distribution_routes.DISTRIBUTION_ROUTES_PATH}
    assert rows == [
        {
            "_meta": {
                "kind": "routes",
                "instructions": generate_distribution_routes.ROUTE_INSTRUCTION,
            }
        }
    ]


def test_write_outputs_removes_retired_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_distribution_routes, "DISTRIBUTION_ROUTE_DIR", tmp_path)
    stale = tmp_path / "retired.jsonl"
    stale.write_text("stale\n", encoding="utf-8")
    readme = tmp_path / "README.md"
    readme.write_text("keep\n", encoding="utf-8")
    current = tmp_path / "current.jsonl"

    generate_distribution_routes.write_outputs({current: "current\n"})

    assert current.read_text(encoding="utf-8") == "current\n"
    assert not stale.exists()
    assert readme.exists()


def test_committed_distribution_routes_are_current():
    for path, content in generate_distribution_routes.generate().items():
        assert path.read_text(encoding="utf-8") == content


def test_canonical_skill_directory_contains_no_route_index():
    assert not (generate_distribution_routes.CANONICAL_SKILLS / "INDEX.jsonl").exists()
