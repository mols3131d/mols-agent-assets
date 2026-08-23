#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "skills-lock.json"


class SkillSyncError(RuntimeError):
    pass


@dataclass(frozen=True)
class LockedSkill:
    name: str
    source: str
    ref: str
    source_type: str


@dataclass(frozen=True)
class NativeAdapter:
    name: str
    supported_skills: frozenset[str]
    install_script: str


@dataclass(frozen=True)
class SyncPlan:
    source: str
    ref: str
    skills: tuple[str, ...]
    adapter: NativeAdapter


NATIVE_ADAPTERS = {
    "epoko77-ai/im-not-ai": NativeAdapter(
        name="im-not-ai",
        supported_skills=frozenset({"humanize-korean"}),
        install_script="install.sh",
    ),
}


def default_cache_root() -> Path:
    base = os.environ.get("XDG_CACHE_HOME")
    root = Path(base).expanduser() if base else Path.home() / ".cache"
    return root / "mols-agent-assets" / "skill-sources"


def normalize_github_source(source: str) -> str:
    shorthand = re.fullmatch(r"([^/:]+)/([^/]+)", source)
    if shorthand:
        owner, repo = shorthand.groups()
        repo = repo.removesuffix(".git")
    elif source.startswith(("http://", "https://")):
        parsed = urlparse(source)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.hostname != "github.com" or len(parts) != 2:
            raise SkillSyncError(
                f"public GitHub owner/repo source만 지원합니다: {source}"
            )
        owner, repo = parts[0], parts[1].removesuffix(".git")
    else:
        raise SkillSyncError(f"public GitHub source 형식이 아닙니다: {source}")

    if not owner or not repo or owner.startswith("-") or repo.startswith("-"):
        raise SkillSyncError(f"잘못된 GitHub source입니다: {source}")
    return f"{owner}/{repo}"


def validate_ref(ref: Any, skill_name: str) -> str:
    if not isinstance(ref, str) or not ref:
        raise SkillSyncError(
            f"native Skill 동기화에는 고정된 ref가 필요합니다: {skill_name}"
        )
    if ref.startswith("-") or any(char in ref for char in ("\0", "\n", "\r")):
        raise SkillSyncError(f"지원하지 않는 ref입니다: {ref!r}")
    return ref


def read_locked_skills(path: Path = LOCK_PATH) -> list[LockedSkill]:
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(data.get("version"), int) or not isinstance(skills, dict):
        raise SkillSyncError(f"지원하지 않는 skills lock 형식입니다: {path}")

    locked: list[LockedSkill] = []
    for name, entry in sorted(skills.items()):
        if not isinstance(name, str) or not isinstance(entry, dict):
            raise SkillSyncError(f"잘못된 skills lock entry가 있습니다: {path}")

        source_type = entry.get("sourceType")
        source = entry.get("sourceUrl") or entry.get("source")
        if not isinstance(source_type, str) or not isinstance(source, str):
            raise SkillSyncError(f"source metadata가 불완전합니다: {name}")

        locked.append(
            LockedSkill(
                name=name,
                source=source,
                ref=validate_ref(entry.get("ref"), name),
                source_type=source_type,
            )
        )
    return locked


def build_sync_plans(skills: list[LockedSkill]) -> list[SyncPlan]:
    grouped: dict[str, dict[str, Any]] = {}

    for skill in skills:
        if skill.source_type != "github":
            raise SkillSyncError(
                f"native adapter가 지원하지 않는 sourceType입니다: {skill.source_type!r}"
            )

        source = normalize_github_source(skill.source)
        adapter = NATIVE_ADAPTERS.get(source)
        if adapter is None:
            raise SkillSyncError(
                f"native installer adapter가 없는 dependency입니다: {source}"
            )
        if skill.name not in adapter.supported_skills:
            raise SkillSyncError(
                f"{adapter.name} adapter가 지원하지 않는 Skill입니다: {skill.name}"
            )

        current = grouped.setdefault(
            source,
            {"ref": skill.ref, "skills": [], "adapter": adapter},
        )
        if current["ref"] != skill.ref:
            raise SkillSyncError(
                f"같은 source에 서로 다른 ref를 사용할 수 없습니다: {source}"
            )
        current["skills"].append(skill.name)

    return [
        SyncPlan(
            source=source,
            ref=values["ref"],
            skills=tuple(sorted(values["skills"])),
            adapter=values["adapter"],
        )
        for source, values in sorted(grouped.items())
    ]


def checkout_path(source: str, cache_root: Path) -> Path:
    repo = source.rsplit("/", 1)[-1]
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
    return cache_root / f"{repo}-{digest}"


def run_checked(command: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(
        command,
        cwd=cwd,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        check=True,
    )


def ensure_checkout(plan: SyncPlan, cache_root: Path) -> Path:
    if shutil.which("git") is None:
        raise SkillSyncError("git이 없습니다.")

    checkout = checkout_path(plan.source, cache_root)
    git_dir = checkout / ".git"
    source_url = f"https://github.com/{plan.source}.git"
    cache_root.mkdir(parents=True, exist_ok=True)

    if checkout.exists() and not git_dir.is_dir():
        raise SkillSyncError(f"관리되지 않는 cache path가 이미 존재합니다: {checkout}")

    if not checkout.exists():
        run_checked(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                source_url,
                str(checkout),
            ]
        )

    run_checked(
        ["git", "-C", str(checkout), "remote", "set-url", "origin", source_url]
    )
    run_checked(
        [
            "git",
            "-C",
            str(checkout),
            "fetch",
            "--depth",
            "1",
            "--force",
            "origin",
            plan.ref,
        ]
    )
    run_checked(
        ["git", "-C", str(checkout), "checkout", "--detach", "--force", "FETCH_HEAD"]
    )
    run_checked(["git", "-C", str(checkout), "clean", "-fdx"])
    return checkout


def run_native_installer(plan: SyncPlan, checkout: Path) -> None:
    if shutil.which("bash") is None:
        raise SkillSyncError(
            f"{plan.adapter.name} native installer는 bash가 필요합니다."
        )

    installer = checkout / plan.adapter.install_script
    if not installer.is_file():
        raise SkillSyncError(f"native installer를 찾을 수 없습니다: {installer}")

    run_checked(["bash", plan.adapter.install_script], cwd=checkout)


def sync_locked_skills(
    *,
    dry_run: bool = False,
    lock_path: Path = LOCK_PATH,
    cache_root: Path | None = None,
) -> None:
    plans = build_sync_plans(read_locked_skills(lock_path))
    if not plans:
        print("[skills-sync] 설치할 project Skill dependency가 없습니다.")
        return

    resolved_cache = cache_root or default_cache_root()
    for plan in plans:
        names = ", ".join(plan.skills)
        print(
            f"[skills-sync] {names}: {plan.source}@{plan.ref} "
            f"-> native:{plan.adapter.name}"
        )
        if dry_run:
            continue

        checkout = ensure_checkout(plan, resolved_cache)
        run_native_installer(plan, checkout)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "lock된 외부 Skill dependency를 source-native installer로 설치·갱신합니다."
        )
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        sync_locked_skills(dry_run=args.dry_run)
    except (
        OSError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
        SkillSyncError,
    ) as error:
        print(f"[skills-sync] error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
