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
    assert text.startswith("---\\n"), path
    end = text.find("\\n---\\n", 4)
    assert end >= 0, path
    data = yaml.safe_load(text[4:end]) or {}
    assert isinstance(data, dict), path
    return data


def test_canonical_skill_frontmatter_matches_portable_contract() -> None:
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    assert skills

    for path in skills:
        data = load_frontmatter(path)
        name = data.get("name")
        description = data.get("description")

        assert isinstance(name, str) and NAME_RE.fullmatch(name), path
        assert 1 <= len(name) <= 64, path
        assert name == path.parent.name, path
        assert isinstance(description, str) and 1 <= len(description) <= 1024, path

        license_value = data.get("license")
        if license_value is not None:
            assert isinstance(license_value, str) and license_value, path

        compatibility = data.get("compatibility")
        if compatibility is not None:
            assert isinstance(compatibility, str), path
            assert 1 <= len(compatibility) <= 500, path

        metadata = data.get("metadata")
        if metadata is not None:
            assert isinstance(metadata, dict), path
            assert all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in metadata.items()
            ), path

        allowed_tools = data.get("allowed-tools")
        if allowed_tools is not None:
            assert isinstance(allowed_tools, str), path
''',
    encoding="utf-8",
)
