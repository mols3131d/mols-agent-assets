import json

from scripts import generate_skill_indexes


def write_skill(path, name, description):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n",
        encoding="utf-8",
    )


def test_render_index_prepends_metadata_and_instruction(tmp_path):
    write_skill(tmp_path / "beta" / "SKILL.md", "beta", "Beta skill")
    write_skill(tmp_path / "alpha" / "SKILL.md", "alpha", "Alpha skill")

    content = generate_skill_indexes.render_index(
        tmp_path,
        "*/SKILL.md",
        "src/agentsmesh/skills/{name}/SKILL.md",
    )
    rows = [json.loads(line) for line in content.splitlines()]

    assert rows[:2] == [
        {
            "metadata": {
                "workspace_path": "src/agentsmesh/skills/{name}/SKILL.md",
                "github_url": (
                    "https://github.com/mols3131d/mols-agent-assets/blob/main/"
                    "src/agentsmesh/skills/{name}/SKILL.md"
                ),
            }
        },
        {"instruction": generate_skill_indexes.INSTRUCTION},
    ]
    assert [row["name"] for row in rows[2:]] == ["alpha", "beta"]


def test_target_template_uses_isolated_canonical_skill_surface():
    targets = {
        directory.relative_to(generate_skill_indexes.ROOT).as_posix(): workspace_path
        for directory, (_, workspace_path) in generate_skill_indexes.TARGETS.items()
    }

    assert targets == {
        "src/agentsmesh/skills": "src/agentsmesh/skills/{name}/SKILL.md",
    }


def test_committed_canonical_skill_index_is_current():
    for directory, (pattern, workspace_path) in generate_skill_indexes.TARGETS.items():
        expected = generate_skill_indexes.render_index(directory, pattern, workspace_path)
        actual = (directory / "INDEX.jsonl").read_text(encoding="utf-8")
        assert actual == expected, (
            f"stale Skill index: {directory.relative_to(generate_skill_indexes.ROOT)}/INDEX.jsonl"
        )
