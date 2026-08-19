from __future__ import annotations

from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    file = Path(path)
    text = file.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text not found: {path}")
    file.write_text(text.replace(old, new, 1), encoding="utf-8")


replace(
    ".agentsmesh/skills/artifact-consistency-inspector/SKILL.md",
    'metadata:\n  - target:\n    - "OpenAI ChatGPT"\n  - version: 2026.08.05.0   # YYYY.MM.DD.REVISION\n',
    'metadata:\n  target: "OpenAI ChatGPT"\n  version: "2026.08.05.0"\n',
)
replace(
    ".agentsmesh/skills/mols-agent-asset-validator/SKILL.md",
    'metadata:\n  - target:\n    - "OpenAI ChatGPT"\n',
    'metadata:\n  target: "OpenAI ChatGPT"\n',
)
replace(
    ".agentsmesh/skills/writing/SKILL.md",
    'metadata:\n  - version: "1.0.0"\n  - target:\n    - "OpenAI ChatGPT"\n',
    'metadata:\n  version: "1.0.0"\n  target: "OpenAI ChatGPT"\n',
)
replace(
    ".agentsmesh/skills/text-humanize-korean/SKILL.md",
    'metadata:\n  version: "0.0.1"\n  target: ["OpenAI ChatGPT"]\n  license: "MIT"\n  references:\n  - epoko77-ai/im-not-ai\n',
    'license: MIT\nmetadata:\n  target: "OpenAI ChatGPT"\n  version: "0.0.1"\n  references: "epoko77-ai/im-not-ai"\n',
)
replace(
    ".agentsmesh/skills/mols-skill-find/SKILL.md",
    'metadata:\n  references:\n    - vercel-labs/skills:skills/find-skills/SKILL.md\n',
    'metadata:\n  references: "vercel-labs/skills:skills/find-skills/SKILL.md"\n',
)

for path in [
    ".agentsmesh/skills/artifact-consistency-inspector/README.md",
    ".agentsmesh/skills/writing/README.md",
]:
    file = Path(path)
    if file.exists():
        file.unlink()

contract_test = Path("tests/skills/artifact-consistency-inspector/test_contract.py")
text = contract_test.read_text(encoding="utf-8")
text = text.replace('    "README.md",\n', "", 1)
text = text.replace('        assert f"{SKILL.name}/README.md" in names\n', "", 1)
contract_test.write_text(text, encoding="utf-8")

validator = Path(".agentsmesh/skills/mols-skill-creator/scripts/validate_skill.py")
text = validator.read_text(encoding="utf-8")
start = text.index("def parse_frontmatter")
end = text.index("\ndef validate", start)
parser = '''def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    """Read only the top-level fields this lightweight validator needs.

    Full Agent Skills YAML conformance is repository/test or reference-validator
    responsibility; this dependency-free helper must not reject valid block scalars
    or nested optional metadata merely because it does not fully parse YAML.
    """
    if not text.startswith("---\\n"):
        return {}, "SKILL.md must start with YAML frontmatter"
    end = text.find("\\n---\\n", 4)
    if end < 0:
        return {}, "frontmatter closing delimiter not found"

    lines = text[4:end].splitlines()
    fields: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            i += 1
            continue
        if ":" not in line:
            return {}, f"unsupported top-level frontmatter line: {line}"

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            style = value[0]
            i += 1
            parts: list[str] = []
            while i < len(lines):
                child = lines[i]
                if child.strip() and not child[:1].isspace():
                    break
                if child.strip():
                    parts.append(child.strip())
                elif style == "|":
                    parts.append("")
                i += 1
            fields[key] = " ".join(parts) if style == ">" else "\\n".join(parts).strip()
            continue

        fields[key] = value.strip('"\\'')
        i += 1

    return fields, None

'''
validator.write_text(text[:start] + parser + text[end + 1 :], encoding="utf-8")

spec = Path("docs/references/skills/agent-skills-io/agent-skills-io-specification.md")
text = spec.read_text(encoding="utf-8")
old = """- repository-local target profile
- flat chatbot token budget
- dot-prefixed maintainer surface
- `.docs/baseline/`
- repository-local naming convention"""
new = """- repository-local package shape and target boundary
- single-file-by-default authoring convention
- deployable package와 repository verification surface boundary
- optional maintainer documentation convention
- repository-local naming convention"""
if old not in text:
    raise SystemExit("stale Tier 1 boundary list not found")
spec.write_text(text.replace(old, new, 1), encoding="utf-8")

guide = Path("docs/references/skills/agent-skills-guide.md")
text = guide.read_text(encoding="utf-8")
old = """- Target profile / package surface →
  [Skill Target Profiles](agent-assets-skills-target-profiles.md)"""
new = """- Package shape / target boundary →
  [Skill Package and Target Boundaries](agent-assets-skills-target-profiles.md)"""
if old not in text:
    raise SystemExit("stale Skill Target Profiles label not found")
guide.write_text(text.replace(old, new, 1), encoding="utf-8")

Path("tests/scripts/asset_docs_placement/test_skill_frontmatter_contract.py").write_text(
    '''from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / ".agentsmesh" / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\\n"):
        raise AssertionError("missing frontmatter")
    end = text.find("\\n---\\n", 4)
    if end < 0:
        raise AssertionError("unclosed frontmatter")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise AssertionError("frontmatter must be a mapping")
    return data


def test_canonical_skill_frontmatter_matches_portable_contract() -> None:
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

        license_value = data.get("license")
        if license_value is not None and (not isinstance(license_value, str) or not license_value):
            problems.append(f"{label}: license must be a non-empty string")

        compatibility = data.get("compatibility")
        if compatibility is not None and (
            not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500
        ):
            problems.append(f"{label}: compatibility must be a string of 1-500 chars")

        metadata = data.get("metadata")
        if metadata is not None:
            if not isinstance(metadata, dict):
                problems.append(f"{label}: metadata must be a mapping")
            else:
                bad = [
                    str(key)
                    for key, value in metadata.items()
                    if not isinstance(key, str) or not isinstance(value, str)
                ]
                if bad:
                    problems.append(f"{label}: metadata values must be strings: {', '.join(bad)}")

        allowed_tools = data.get("allowed-tools")
        if allowed_tools is not None and not isinstance(allowed_tools, str):
            problems.append(f"{label}: allowed-tools must be a string")

    assert not problems, "\\n" + "\\n".join(problems)
''',
    encoding="utf-8",
)
