#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "skills-lock.json"
TARGET_CONFIG_PATH = ROOT / "src" / "rulesync" / "rulesync.jsonc"

TARGET_TO_AGENT = {
    "claudecode": "claude-code",
    "codexcli": "codex",
    "copilot": "github-copilot",
    "copilotcli": "github-copilot",
    "antigravity-ide": "antigravity",
    "antigravity-cli": "antigravity-cli",
}


class SkillSyncError(RuntimeError):
    pass


def read_vendor_targets(path: Path = TARGET_CONFIG_PATH) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'"targets"\s*:\s*\[(.*?)\]', text, re.DOTALL)
    if not match:
        raise SkillSyncError(f"targets를 찾을 수 없습니다: {path}")

    targets = re.findall(r'"([^"]+)"', match.group(1))
    if not targets:
        raise SkillSyncError(f"targets가 비어 있습니다: {path}")
    return targets


def resolve_agents(targets: list[str]) -> list[str]:
    missing = [target for target in targets if target not in TARGET_TO_AGENT]
    if missing:
        raise SkillSyncError(
            f"skills CLI target mapping이 없습니다: {', '.join(missing)}"
        )

    agents: list[str] = []
    for target in targets:
        agent = TARGET_TO_AGENT[target]
        if agent not in agents:
            agents.append(agent)
    return agents


def read_locked_skills(path: Path = LOCK_PATH) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(data.get("version"), int) or not isinstance(skills, dict):
        raise SkillSyncError(f"지원하지 않는 skills lock 형식입니다: {path}")
    if not all(
        isinstance(name, str) and isinstance(entry, dict)
        for name, entry in skills.items()
    ):
        raise SkillSyncError(f"잘못된 skills lock entry가 있습니다: {path}")
    return skills


def skill_folder(entry: dict[str, Any]) -> str | None:
    value = entry.get("skillPath")
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise SkillSyncError("skillPath가 문자열이 아닙니다.")

    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.name != "SKILL.md":
        raise SkillSyncError(f"지원하지 않는 skillPath입니다: {value}")

    folder = str(path.parent)
    return "" if folder == "." else folder


def build_source(entry: dict[str, Any]) -> str:
    source_type = entry.get("sourceType")
    source_url = entry.get("sourceUrl")
    source = source_url or entry.get("source")

    if source_type in {"git", "gitlab"} and not source_url:
        raise SkillSyncError(f"{source_type} source는 sourceUrl이 필요합니다.")
    if not isinstance(source, str) or not source or source.startswith("-"):
        raise SkillSyncError("설치 가능한 source가 lock entry에 없습니다.")

    folder = skill_folder(entry)
    if folder:
        if source_type == "github":
            if source.startswith(("git@", "ssh://")) or source.endswith(".git"):
                raise SkillSyncError("GitHub skillPath 설치에는 path를 표현할 source가 필요합니다.")
            source = f"{source.rstrip('/')}/{folder}"
        elif source_type == "local":
            source = str(Path(source, *PurePosixPath(folder).parts))
        else:
            raise SkillSyncError(
                f"{source_type or 'unknown'} source의 skillPath 설치는 지원하지 않습니다."
            )

    ref = entry.get("ref")
    return f"{source}#{ref}" if isinstance(ref, str) and ref else source


def build_command(
    skill_name: str,
    entry: dict[str, Any],
    agents: list[str],
) -> list[str]:
    if not skill_name or skill_name.startswith("-"):
        raise SkillSyncError(f"잘못된 Skill 이름입니다: {skill_name!r}")

    return [
        "skills",
        "add",
        build_source(entry),
        "--skill",
        skill_name,
        "--agent",
        *agents,
        "--yes",
    ]


def sync_locked_skills(*, dry_run: bool = False) -> None:
    agents = resolve_agents(read_vendor_targets())
    skills = read_locked_skills()

    if not skills:
        print("[skills-sync] 설치할 project Skill이 없습니다.")
        return
    if not dry_run and shutil.which("skills") is None:
        raise SkillSyncError("skills CLI가 없습니다. 먼저 `mise install`을 실행하세요.")

    env = os.environ.copy()
    env["DISABLE_TELEMETRY"] = "1"
    env["DO_NOT_TRACK"] = "1"

    failures: list[str] = []
    for skill_name, entry in sorted(skills.items()):
        command = build_command(skill_name, entry, agents)
        print(f"[skills-sync] {skill_name} -> {', '.join(agents)}")
        if dry_run:
            print(shlex.join(command))
            continue

        if subprocess.run(command, cwd=ROOT, env=env, check=False).returncode:
            failures.append(skill_name)

    if failures:
        raise SkillSyncError(f"Skill 설치·갱신 실패: {', '.join(failures)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="lock된 Skill을 repository vendor target에 설치·갱신합니다."
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        sync_locked_skills(dry_run=args.dry_run)
    except (OSError, json.JSONDecodeError, SkillSyncError) as error:
        print(f"[skills-sync] error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
