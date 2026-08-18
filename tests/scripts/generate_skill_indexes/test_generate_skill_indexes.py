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
        ".agentsmesh/skills/{name}/SKILL.md",
    )
    rows = [json.loads(line) for line in content.splitlines()]

    assert rows[:2] == [
        {
            "metadata": {
                "workspace_path": ".agentsmesh/skills/{name}/SKILL.md",
                "github_url": (
                    "https://github.com/mols3131d/mols-agent-assets/blob/main/"
                    ".agentsmesh/skills/{name}/SKILL.md"
                ),
            }
        },
        {"instruction": generate_skill_indexes.INSTRUCTION},
    ]
    assert [row["name"] for row in rows[2:]] == ["alpha", "beta"]


def test_target_templates_cover_each_skill_profile():
    targets = {
        directory.relative_to(generate_skill_indexes.ROOT).as_posix(): workspace_path
        for directory, (_, workspace_path) in generate_skill_indexes.TARGETS.items()
    }

    assert targets == {
        ".agentsmesh/skills": ".agentsmesh/skills/{name}/SKILL.md",
        "src/skills-chatbot": "src/skills-chatbot/{name}.skill.md",
        "src/skills-chatbot-runtime": "src/skills-chatbot-runtime/{name}/SKILL.md",
    }
