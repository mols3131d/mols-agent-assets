import json

import pytest

from scripts import generate_repository_routes as routes


def skill_row(name: str) -> dict[str, str]:
    return {"name": name, "description": f"{name} description", "source": f"https://example.test/{name}/SKILL.md"}


def parse_jsonl(content: str) -> list[dict[str, str]]:
    return [json.loads(line) for line in content.splitlines()]


def patch_route_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(routes, "ROUTE_DIR", tmp_path)
    monkeypatch.setattr(routes, "ROUTES_PATH", tmp_path / "routes.jsonl")
    monkeypatch.setattr(routes, "ALL_PATH", tmp_path / "all.jsonl")
    monkeypatch.setattr(routes, "UNCATEGORIZED_PATH", tmp_path / "uncategorized.jsonl")


def test_build_outputs_creates_narrow_routes_all_and_uncategorized(tmp_path, monkeypatch):
    patch_route_paths(tmp_path, monkeypatch)
    rows = {name: skill_row(name) for name in ("alpha", "beta", "gamma")}
    families = {"first": {"description": "First family", "skills": ["alpha", "beta"]}, "overlap": {"description": "Overlap family", "skills": ["beta"]}}
    outputs = routes.build_outputs(rows, families)
    assert parse_jsonl(outputs[tmp_path / "first.jsonl"]) == [rows["alpha"], rows["beta"]]
    assert parse_jsonl(outputs[tmp_path / "overlap.jsonl"]) == [rows["beta"]]
    assert parse_jsonl(outputs[tmp_path / "all.jsonl"]) == [rows["alpha"], rows["beta"], rows["gamma"]]
    assert parse_jsonl(outputs[tmp_path / "uncategorized.jsonl"]) == [rows["gamma"]]


def test_generated_jsonl_contains_data_not_routing_instructions(tmp_path, monkeypatch):
    patch_route_paths(tmp_path, monkeypatch)
    outputs = routes.build_outputs({"alpha": skill_row("alpha")}, {"first": {"description": "First family", "skills": ["alpha"]}})
    for content in outputs.values():
        assert '"instructions"' not in content
        assert '"_meta"' not in content


def test_empty_uncategorized_route_is_empty_file(tmp_path, monkeypatch):
    patch_route_paths(tmp_path, monkeypatch)
    outputs = routes.build_outputs({"alpha": skill_row("alpha")}, {"first": {"description": "First family", "skills": ["alpha"]}})
    assert outputs[tmp_path / "uncategorized.jsonl"] == ""


def test_unknown_family_skill_is_rejected(tmp_path, monkeypatch):
    patch_route_paths(tmp_path, monkeypatch)
    with pytest.raises(routes.RouteGenerationError, match="lock에 없는 Skill"):
        routes.build_outputs({"alpha": skill_row("alpha")}, {"first": {"description": "First family", "skills": ["missing"]}})


def test_reserved_family_name_is_rejected(tmp_path, monkeypatch):
    families = tmp_path / "families.json"
    families.write_text('{"all":{"description":"reserved","skills":[]}}', encoding="utf-8")
    monkeypatch.setattr(routes, "FAMILIES_PATH", families)

    with pytest.raises(routes.RouteGenerationError, match="예약된 route 이름"):
        routes.read_families()


def test_load_skill_rows_rejects_name_drift():
    text = "---\nname: beta\ndescription: Beta description\n---\n"
    with pytest.raises(routes.RouteGenerationError, match="lock 이름과 Skill 이름"):
        routes.load_skill_rows({"alpha": "https://example.test/SKILL.md"}, lambda _: text)


def test_strip_jsonc_comments_preserves_comment_like_strings():
    raw = '{\n  // line\n  "url": "https://example.test/a//b",\n  /* block */\n  "value": 1\n}\n'
    assert json.loads(routes.strip_jsonc_comments(raw)) == {"url": "https://example.test/a//b", "value": 1}


def test_github_source_accepts_shorthand_and_https():
    expected = "https://raw.githubusercontent.com/owner/repo/v1/path/SKILL.md"
    assert routes.github_raw_url("owner/repo", "v1", "path/SKILL.md") == expected
    assert routes.github_raw_url("https://github.com/owner/repo.git", "v1", "path/SKILL.md") == expected


def test_write_outputs_removes_stale_generated_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(routes, "ROUTE_DIR", tmp_path)
    stale = tmp_path / "stale.jsonl"
    stale.write_text("stale\n", encoding="utf-8")
    manual = tmp_path / "families.json"
    manual.write_text("{}\n", encoding="utf-8")
    expected = tmp_path / "all.jsonl"
    routes.write_outputs({expected: ""})
    assert expected.exists()
    assert not stale.exists()
    assert manual.exists()
