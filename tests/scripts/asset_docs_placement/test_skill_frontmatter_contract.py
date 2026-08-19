from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src" / "rulesync" / ".rulesync" / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AGENT_SKILLS_FIELDS = {"license", "compatibility", "metadata", "allowed-tools"}


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("unclosed frontmatter")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise AssertionError("frontmatter must be a mapping")
    return data


def test_canonical_skill_frontmatter_matches_rulesync_contract() -> None:
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    assert skills
    problems: list[str] = []

    for path in skills:
        label = path.parent.name
        try:
            data = load_frontmatter(path)
        except Exception as error:
            problems.append(f"{label}: {error}")
            continue

        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            problems.append(f"{label}: invalid name")
        elif not 1 <= len(name) <= 64 or name != label:
            problems.append(f"{label}: name must be 1-64 chars and match directory")

        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            problems.append(f"{label}: description must be a non-empty string <=1024 chars")

        misplaced = sorted(AGENT_SKILLS_FIELDS.intersection(data))
        if misplaced:
            problems.append(
                f"{label}: Agent Skills fields belong under agentsskills: {', '.join(misplaced)}"
            )

        agentsskills = data.get("agentsskills")
        if agentsskills is None:
            continue
        if not isinstance(agentsskills, dict):
            problems.append(f"{label}: agentsskills must be a mapping")
            continue

        unknown = sorted(set(agentsskills) - AGENT_SKILLS_FIELDS)
        if unknown:
            problems.append(f"{label}: unsupported agentsskills fields: {', '.join(unknown)}")

        license_value = agentsskills.get("license")
        if license_value is not None and (
            not isinstance(license_value, str) or not license_value
        ):
            problems.append(f"{label}: agentsskills.license must be a non-empty string")

        compatibility = agentsskills.get("compatibility")
        if compatibility is not None and not isinstance(compatibility, (str, dict)):
            problems.append(f"{label}: agentsskills.compatibility must be a string or mapping")

        metadata = agentsskills.get("metadata")
        if metadata is not None and not isinstance(metadata, dict):
            problems.append(f"{label}: agentsskills.metadata must be a mapping")

        allowed_tools = agentsskills.get("allowed-tools")
        if allowed_tools is not None and not isinstance(allowed_tools, (str, list)):
            problems.append(f"{label}: agentsskills.allowed-tools must be a string or list")

    assert not problems, "\n" + "\n".join(problems)
