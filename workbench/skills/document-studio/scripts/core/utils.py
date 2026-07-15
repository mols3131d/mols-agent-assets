from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def normalize_kebab_case(s: str) -> str:
    """문자열을 kebab-case 형태로 정규화한다."""
    s = s.strip().lower()
    s = re.sub(r"[\s_.]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def title_case_name(name: str) -> str:
    """kebab-case 명칭을 가독성 높은 제목으로 변환한다."""
    return " ".join(part.capitalize() for part in name.split("-") if part)


def format_yaml_list(items: list[str]) -> str:
    """리스트를 YAML 배열 형식으로 포맷한다."""
    return json.dumps(items, ensure_ascii=False)


def write_if_not_exists(file_path: Path, content: str) -> bool:
    """파일이 존재하지 않을 경우에만 생성한다."""
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def unquote(value: str) -> str:
    """양 끝의 따옴표를 제거한다."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_yaml_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """프론트매터 딕셔너리와 본문 텍스트를 읽어온다."""
    if not content.startswith("---\n"):
        return {}, content

    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content

    fm_text = content[4:end]
    body = content[end + 5 :]

    data: dict[str, Any] = {}
    current_key: str | None = None
    list_items: list[str] = []

    for raw_line in fm_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        if current_key and stripped.startswith("- "):
            list_items.append(unquote(stripped[2:]))
            continue

        if current_key:
            data[current_key] = list_items
            current_key = None
            list_items = []

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if value == "":
            current_key = key
            list_items = []
        elif value == "[]":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [
                unquote(item) for item in value[1:-1].split(",") if item.strip()
            ]
        else:
            data[key] = unquote(value)

    if current_key:
        data[current_key] = list_items

    return data, body
