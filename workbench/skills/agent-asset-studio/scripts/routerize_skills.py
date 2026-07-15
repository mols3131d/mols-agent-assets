#!/usr/bin/env python3
"""여러 Skill을 하나의 shallow Routing Skill로 이동한다."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import update_index
from core.validators import parse_frontmatter

ROUTER_TEMPLATE = """---
name: {skill_name}
description: >
  Route requests across the {skill_title} workflow set. Use when a request
  matches one or more indexed workflows. Replace this with domain-specific intent.
---

# {skill_title}

## Routing

1. Read `INDEX.csv` once.
2. Eliminate routes matching `avoid_when`.
3. Select the smallest route set matching `use_when`.
4. Read only the selected `entrypoint` files.
5. Load additional resources only when a workflow requires them.

Route by semantic intent, not keyword overlap. Do not scan `workflows/`.

## Ambiguity

- Select one route when it fully covers the request.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when routes imply materially different actions.
- State that the skill does not cover the request when no route matches.
"""


def title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-") if part)


def read_source_skill(path: Path) -> tuple[str, str]:
    """Source SKILL.md에서 description과 body를 읽는다."""
    skill_path = path / "SKILL.md"
    if not skill_path.is_file():
        raise ValueError(f"SKILL.md가 없습니다: {path}")
    frontmatter, body = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    return frontmatter.get("description", "").strip(), body.lstrip()


def setup_target(target: Path) -> None:
    """Routing Skill root와 필수 파일을 초기화한다."""
    target.mkdir(parents=True, exist_ok=True)
    (target / "workflows").mkdir(exist_ok=True)

    skill_path = target / "SKILL.md"
    if not skill_path.exists():
        skill_path.write_text(
            ROUTER_TEMPLATE.format(
                skill_name=target.name,
                skill_title=title_case(target.name),
            ),
            encoding="utf-8",
        )
    update_index.init_index(target / "INDEX.csv")


def add_route(
    target: Path,
    route_id: str,
    description: str,
    entrypoint: str,
) -> None:
    """Migrated workflow의 초기 route를 기록한다."""
    update_index.update_index(
        target / "INDEX.csv",
        {
            "id": route_id,
            "use_when": description or f"Requests covered by {route_id}",
            "avoid_when": "Requests outside this workflow's original scope",
            "entrypoint": entrypoint,
        },
    )


def process_lite(target: Path, source_paths: list[Path]) -> None:
    """Source directory를 isolated workflow directory로 이동한다."""
    for source in source_paths:
        if not source.is_dir():
            print(f"Warning: directory가 아닙니다: {source}", file=sys.stderr)
            continue

        route_id = source.name
        destination = target / "workflows" / route_id
        if destination.exists():
            print(
                f"Warning: destination이 이미 있습니다: {destination}", file=sys.stderr
            )
            continue

        try:
            description, body = read_source_skill(source)
        except ValueError as exc:
            print(f"Warning: {exc}", file=sys.stderr)
            continue

        shutil.move(str(source), str(destination))
        old_entrypoint = destination / "SKILL.md"
        entrypoint = destination / "WORKFLOW.md"
        old_entrypoint.unlink()
        entrypoint.write_text(body, encoding="utf-8")

        relative_entrypoint = entrypoint.relative_to(target).as_posix()
        add_route(target, route_id, description, relative_entrypoint)
        print(f"Routerized (lite): {route_id}")


def process_full(target: Path, source_paths: list[Path]) -> None:
    """Source SKILL.md를 flat workflow로 이동하고 resource를 병합한다."""
    resource_dirs = ("assets", "scripts", "references", "prompts")

    for source in source_paths:
        if not source.is_dir():
            print(f"Warning: directory가 아닙니다: {source}", file=sys.stderr)
            continue

        route_id = source.name
        entrypoint = target / "workflows" / f"{route_id}.md"
        if entrypoint.exists():
            print(f"Warning: entrypoint가 이미 있습니다: {entrypoint}", file=sys.stderr)
            continue

        try:
            description, body = read_source_skill(source)
        except ValueError as exc:
            print(f"Warning: {exc}", file=sys.stderr)
            continue

        path_replacements: dict[str, str] = {}
        for resource_name in resource_dirs:
            source_dir = source / resource_name
            if not source_dir.is_dir():
                continue

            target_dir = target / resource_name
            target_dir.mkdir(exist_ok=True)
            for item in source_dir.iterdir():
                if not item.is_file():
                    continue
                destination = target_dir / item.name
                if destination.exists():
                    destination = target_dir / f"{item.stem}-{route_id}{item.suffix}"
                shutil.move(str(item), str(destination))
                path_replacements[f"{resource_name}/{item.name}"] = (
                    f"../{resource_name}/{destination.name}"
                )

        for old_path, new_path in path_replacements.items():
            body = body.replace(old_path, new_path)

        entrypoint.write_text(body, encoding="utf-8")
        shutil.rmtree(source)

        relative_entrypoint = entrypoint.relative_to(target).as_posix()
        add_route(target, route_id, description, relative_entrypoint)
        print(f"Routerized (full): {route_id}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="기존 Skill을 shallow Routing Skill로 이동합니다."
    )
    parser.add_argument("--mode", choices=("lite", "full"), default="lite")
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("skills", nargs="+", type=Path)
    args = parser.parse_args()

    target = args.target.resolve()
    sources = [path.resolve() for path in args.skills]
    if target in sources:
        parser.error("target은 source skill과 달라야 합니다.")

    setup_target(target)
    if args.mode == "lite":
        process_lite(target, sources)
    else:
        process_full(target, sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
