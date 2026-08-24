"""Generate repository-local Skill discovery routes from lock-backed dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse
from urllib.request import urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROUTE_DIR = ROOT / ".agents/route"
FAMILIES_PATH = ROUTE_DIR / "families.json"
RULESYNC_LOCK = ROOT / "rulesync.lock"
RULESYNC_CONFIG = ROOT / "rulesync.jsonc"
SKILLS_LOCK = ROOT / "skills-lock.json"
ROUTES_PATH = ROUTE_DIR / "routes.jsonl"
ALL_PATH = ROUTE_DIR / "all.jsonl"
UNCATEGORIZED_PATH = ROUTE_DIR / "uncategorized.jsonl"
FAMILY_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class RouteGenerationError(RuntimeError):
    pass


def strip_jsonc_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and next_char == "*":
            index += 2
            while index < len(text):
                if text[index] == "*" and index + 1 < len(text) and text[index + 1] == "/":
                    index += 2
                    break
                if text[index] in "\r\n":
                    result.append(text[index])
                index += 1
            else:
                raise RouteGenerationError("닫히지 않은 JSONC block comment가 있습니다.")
            continue
        result.append(char)
        index += 1
    return "".join(result)


def parse_frontmatter(text: str, source: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise RouteGenerationError(f"frontmatter가 없습니다: {source}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise RouteGenerationError(f"frontmatter가 닫히지 않았습니다: {source}") from exc
    data = yaml.safe_load("\n".join(lines[1:end])) or {}
    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not isinstance(description, str):
        raise RouteGenerationError(f"name/description이 필요합니다: {source}")
    return name, description


def fetch_text(url: str) -> str:
    with urlopen(url, timeout=30) as response:  # noqa: S310
        return response.read().decode("utf-8")


def normalize_github_source(source: str) -> str:
    shorthand = source.removesuffix(".git")
    if re.fullmatch(r"[^/]+/[^/]+", shorthand):
        return shorthand
    parsed = urlparse(source)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme == "https" and parsed.hostname == "github.com" and len(parts) == 2:
        return f"{parts[0]}/{parts[1].removesuffix('.git')}"
    raise RouteGenerationError(f"지원하지 않는 GitHub source입니다: {source}")


def github_raw_url(source: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{normalize_github_source(source)}/{ref}/{path.lstrip('/')}"


def read_rulesync_entries() -> dict[str, str]:
    lock = json.loads(RULESYNC_LOCK.read_text(encoding="utf-8"))
    config = json.loads(strip_jsonc_comments(RULESYNC_CONFIG.read_text(encoding="utf-8")))
    config_sources = {
        item["source"]: item
        for item in config.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("source"), str)
    }
    result: dict[str, str] = {}
    for source, locked in lock.get("sources", {}).items():
        if not isinstance(locked, dict):
            raise RouteGenerationError(f"잘못된 rulesync lock source입니다: {source}")
        resolved_ref = locked.get("resolvedRef")
        skills = locked.get("skills")
        config_source = config_sources.get(source)
        if not isinstance(resolved_ref, str) or not isinstance(skills, dict):
            raise RouteGenerationError(f"불완전한 rulesync lock source입니다: {source}")
        if not isinstance(config_source, dict) or not isinstance(config_source.get("path"), str):
            raise RouteGenerationError(f"rulesync source path를 찾을 수 없습니다: {source}")
        base_path = config_source["path"].rstrip("/")
        for skill_name in skills:
            if not isinstance(skill_name, str):
                raise RouteGenerationError(f"잘못된 rulesync Skill 이름입니다: {skill_name!r}")
            result[skill_name] = github_raw_url(source, resolved_ref, f"{base_path}/{skill_name}/SKILL.md")
    return result


def read_skills_cli_entries() -> dict[str, str]:
    lock = json.loads(SKILLS_LOCK.read_text(encoding="utf-8"))
    skills = lock.get("skills")
    if not isinstance(skills, dict):
        raise RouteGenerationError("skills-lock.json의 skills가 올바르지 않습니다.")
    result: dict[str, str] = {}
    for skill_name, entry in skills.items():
        if not isinstance(skill_name, str) or not isinstance(entry, dict):
            raise RouteGenerationError("잘못된 skills CLI lock entry가 있습니다.")
        source = entry.get("sourceUrl") or entry.get("source")
        ref = entry.get("ref")
        path = entry.get("skillPath")
        if entry.get("sourceType") != "github":
            raise RouteGenerationError(f"repository route는 github Skill dependency만 지원합니다: {skill_name}")
        if not all(isinstance(value, str) and value for value in (source, ref, path)):
            raise RouteGenerationError(f"불완전한 skills CLI lock entry입니다: {skill_name}")
        result[skill_name] = github_raw_url(source, ref, path)
    return result


def read_families() -> dict[str, dict[str, object]]:
    data = json.loads(FAMILIES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RouteGenerationError("families.json은 object여야 합니다.")
    for family, entry in data.items():
        if not isinstance(family, str) or not FAMILY_NAME_RE.fullmatch(family):
            raise RouteGenerationError(f"잘못된 family 이름입니다: {family!r}")
        if not isinstance(entry, dict):
            raise RouteGenerationError(f"잘못된 family entry입니다: {family}")
        if not isinstance(entry.get("description"), str) or not entry["description"]:
            raise RouteGenerationError(f"family description이 필요합니다: {family}")
        skills = entry.get("skills")
        if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
            raise RouteGenerationError(f"family skills가 올바르지 않습니다: {family}")
    return data


def load_skill_rows(sources: dict[str, str], loader: Callable[[str], str] = fetch_text) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for locked_name, source in sorted(sources.items()):
        actual_name, description = parse_frontmatter(loader(source), source)
        if actual_name != locked_name:
            raise RouteGenerationError(f"lock 이름과 Skill 이름이 다릅니다: {locked_name} != {actual_name}")
        rows[locked_name] = {"name": locked_name, "description": description, "source": source}
    return rows


def render_jsonl(rows: list[dict[str, str]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)


def build_outputs(skill_rows: dict[str, dict[str, str]], families: dict[str, dict[str, object]]) -> dict[Path, str]:
    all_names = set(skill_rows)
    categorized: set[str] = set()
    outputs: dict[Path, str] = {}
    route_rows: list[dict[str, str]] = []
    for family in sorted(families):
        entry = families[family]
        skill_names = set(entry["skills"])
        unknown = skill_names - all_names
        if unknown:
            raise RouteGenerationError(f"lock에 없는 Skill이 family에 있습니다: {family}: {sorted(unknown)}")
        categorized.update(skill_names)
        outputs[ROUTE_DIR / f"{family}.jsonl"] = render_jsonl([skill_rows[name] for name in sorted(skill_names)])
        route_rows.append({"name": family, "description": str(entry["description"]), "source": f"{family}.jsonl"})
    outputs[UNCATEGORIZED_PATH] = render_jsonl([skill_rows[name] for name in sorted(all_names - categorized)])
    outputs[ALL_PATH] = render_jsonl([skill_rows[name] for name in sorted(all_names)])
    route_rows.extend([
        {"name": "uncategorized", "description": "아직 family에 배정되지 않은 Skill", "source": "uncategorized.jsonl"},
        {"name": "all", "description": "전체 lock-backed Skill fallback", "source": "all.jsonl"},
    ])
    outputs[ROUTES_PATH] = render_jsonl(route_rows)
    return outputs


def generate(loader: Callable[[str], str] = fetch_text) -> dict[Path, str]:
    sources = read_rulesync_entries()
    for name, source in read_skills_cli_entries().items():
        if name in sources:
            raise RouteGenerationError(f"Skill dependency가 두 lock에 중복됩니다: {name}")
        sources[name] = source
    return build_outputs(load_skill_rows(sources, loader), read_families())


def write_outputs(outputs: dict[Path, str]) -> None:
    ROUTE_DIR.mkdir(parents=True, exist_ok=True)
    generated_paths = set(outputs)
    for path in ROUTE_DIR.glob("*.jsonl"):
        if path not in generated_paths:
            path.unlink()
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    write_outputs(generate())


if __name__ == "__main__":
    main()
