#!/usr/bin/env python3
"""Unified Kanban board and card manager script."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

# Add current scripts directory to sys.path to allow importing update_index
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


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


def parse_yaml(text: str) -> dict[str, any]:
    """간단한 YAML 프론트매터 파서."""
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in {'"', "'"}:
            val = val[1:-1]
        if val == "[]":
            data[key] = []
        elif val.startswith("[") and val.endswith("]"):
            data[key] = [item.strip().strip('"').strip("'") for item in val[1:-1].split(",") if item.strip()]
        else:
            data[key] = val
    return data


def format_yaml_list(items: list[str]) -> str:
    """리스트를 YAML 배열 형식으로 포맷한다."""
    return json.dumps(items, ensure_ascii=False)


def get_next_id(base_dir: Path) -> str:
    """모든 폴더를 스캔하여 다음 kbn ID(예: 001)를 결정한다."""
    max_id = 0
    folders = [base_dir, base_dir / "backlog", base_dir / "archive"]
    for folder in folders:
        if not folder.exists():
            continue
        for file_path in folder.glob("kbn-*.md"):
            name = file_path.name
            prefix = "kbn-"
            if not name.startswith(prefix):
                continue
            rest = name[len(prefix):]
            parts = rest.split(".", 1)[0].split("-", 1)
            num_str = parts[0]
            if num_str.isdigit():
                val = int(num_str)
                if val > max_id:
                    max_id = val
    return f"{max_id + 1:03d}"


def locate_card(base_dir: Path, ident: str) -> Path | None:
    """ID, 파일명 또는 경로로 카드를 검색하여 Path 객체를 반환한다."""
    # 1. 직접 경로 체크
    paths = [
        base_dir / ident,
        base_dir / "backlog" / ident,
        base_dir / "archive" / ident
    ]
    for p in paths:
        if p.is_file():
            return p

    # 2. 식별자 정규화
    card_id = ident.strip()
    if card_id.isdigit():
        card_id = f"kbn-{int(card_id):03d}"

    # 3. 디렉터리 스캔
    for folder in [base_dir, base_dir / "backlog", base_dir / "archive"]:
        if not folder.exists():
            continue
        for p in folder.glob("kbn-*.md"):
            name = p.name
            parts = name.split(".", 1)[0].split("-", 2)
            if len(parts) >= 2:
                current_id = f"{parts[0]}-{parts[1]}"
                if current_id.lower() == card_id.lower():
                    return p
    return None


def read_frontmatter(file_path: Path) -> tuple[dict[str, any], str]:
    """파일에서 프론트매터 딕셔너리와 본문 텍스트를 읽어온다."""
    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}, content
    
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content
        
    fm_text = content[4:end]
    body = content[end + 5:]
    return parse_yaml(fm_text), body


def write_card_file(file_path: Path, fm: dict[str, any], body: str) -> None:
    """프론트매터와 본문을 카드 파일에 쓴다."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}: {format_yaml_list(v)}")
        elif isinstance(v, (int, float, bool)):
            lines.append(f"{k}: {v}")
        else:
            # 특수문자나 쉼표가 있을 수 있으므로 따옴표 처리
            val_str = str(v)
            if '"' in val_str:
                lines.append(f"{k}: '{val_str}'")
            else:
                lines.append(f"{k}: \"{val_str}\"")
    lines.append("---")
    lines.append(body.lstrip())
    
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("\n".join(lines), encoding="utf-8")


def update_folder_index(folder: Path) -> None:
    """지정된 폴더의 INDEX.csv를 update_index.py 규칙에 따라 업데이트한다."""
    if not folder.exists():
        return
    import contextlib
    import io

    from update_index import main as update_index_main

    f_io = io.StringIO()
    with contextlib.redirect_stdout(f_io):
        try:
            update_index_main([
                str(folder),
                "--fields", "file,id,title,status,priority,assignee,tags",
                "--sort", "status,id,file"
            ])
        except Exception:
            pass


def get_status_folder(base_dir: Path, status: str) -> Path:
    """상태값에 따른 카드 저장 폴더를 반환한다."""
    if status in ("backlog", "todo"):
        return base_dir / "backlog"
    elif status in ("in-progress", "review"):
        return base_dir
    else:
        return base_dir / "archive"


def cmd_init(args: argparse.Namespace) -> int:
    """칸반 보드 디렉터리를 생성하고 메인 보드 README.md를 초기화한다."""
    base_dir = Path(args.path).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / "backlog").mkdir(exist_ok=True)
    (base_dir / "archive").mkdir(exist_ok=True)

    readme_path = base_dir / "README.md"
    initial_readme = """# Kanban Board

Goal: show work state at glance.

## Use When

- User needs board, not plain checklist.
- Items move through states.
- Status matters more than detailed prose.

## Board

| Backlog | Todo | In-Progress | Review | Done |
| :--- | :--- | :--- | :--- | :--- |

## Rules

- One card = one markdown file.
- Each card markdown file contains Frontmatter.
- Keep card text short.
- Link detailed docs, do not embed.
- Archive done items when board noisy.
"""
    if not readme_path.exists():
        readme_path.write_text(initial_readme, encoding="utf-8")

    # INDEX.csv 초기화
    update_folder_index(base_dir)
    update_folder_index(base_dir / "backlog")
    update_folder_index(base_dir / "archive")

    payload = {
        "status": "initialized",
        "path": str(base_dir),
        "created": [
            "README.md",
            "INDEX.csv",
            "backlog/INDEX.csv",
            "archive/INDEX.csv"
        ]
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    """새로운 칸반 카드 파일을 생성한다."""
    base_dir = Path(args.path).resolve()
    if not base_dir.exists():
        raise FileNotFoundError(f"칸반 디렉터리가 존재하지 않습니다. 먼저 init을 실행하세요: {base_dir}")

    id_num = get_next_id(base_dir)
    card_id = f"kbn-{id_num}"
    doc_name = normalize_kebab_case(args.name)
    filename = f"{card_id}-{doc_name}.md"
    
    # 신규 카드는 backlog 폴더에 저장됨
    dest_path = base_dir / "backlog" / filename

    if dest_path.exists():
        raise FileExistsError(f"카드 파일이 이미 존재합니다: {dest_path}")

    title = title_case_name(doc_name)
    tags_list = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    fm = {
        "id": card_id,
        "title": title,
        "status": "backlog",
        "priority": args.priority,
        "description": args.description or "",
        "assignee": args.assignee or "",
        "tags": tags_list
    }
    body = f"# {card_id}: {title}\n\n카드 설명을 입력하세요.\n"

    if not args.dry_run:
        write_card_file(dest_path, fm, body)
        # 보드 업데이트 및 인덱스 동기화
        cmd_update(args)

    payload = {
        "status": "created",
        "card_id": card_id,
        "filename": filename,
        "path": str(dest_path)
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    """카드의 상태를 변경하고 해당하는 디렉터리로 이동시킨다."""
    base_dir = Path(args.path).resolve()
    card_path = locate_card(base_dir, args.card)
    if not card_path:
        raise FileNotFoundError(f"지정된 카드를 찾을 수 없습니다: {args.card}")

    fm, body = read_frontmatter(card_path)
    if not fm:
        raise ValueError(f"카드 파일의 프론트매터를 파싱할 수 없습니다: {card_path}")

    old_status = fm.get("status", "backlog")
    new_status = args.status

    # 프론트매터 업데이트
    fm["status"] = new_status
    if args.assignee is not None:
        fm["assignee"] = args.assignee
    if args.priority is not None:
        fm["priority"] = args.priority

    # 신규 경로 확인
    dest_folder = get_status_folder(base_dir, new_status)
    dest_path = dest_folder / card_path.name

    if not args.dry_run:
        # 기존 파일 삭제 및 신규 경로에 저장
        if card_path != dest_path:
            if dest_path.exists():
                raise FileExistsError(f"이동하려는 위치에 파일이 이미 존재합니다: {dest_path}")
            card_path.unlink()
        
        write_card_file(dest_path, fm, body)
        # 전체 보드 업데이트 및 인덱스 업데이트
        cmd_update(args)

    payload = {
        "status": "moved",
        "card_id": fm.get("id"),
        "old_status": old_status,
        "new_status": new_status,
        "old_path": str(card_path),
        "new_path": str(dest_path)
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """전체 인덱스 갱신 및 README.md 내 보드 테이블 렌더링을 처리한다."""
    base_dir = Path(args.path).resolve()
    
    # 1. 인덱스 업데이트
    update_folder_index(base_dir)
    update_folder_index(base_dir / "backlog")
    update_folder_index(base_dir / "archive")

    # 2. 모든 카드 수집
    cards_by_status: dict[str, list[dict[str, any]]] = {
        "backlog": [],
        "todo": [],
        "in-progress": [],
        "review": [],
        "done": []
    }

    folders = [base_dir, base_dir / "backlog", base_dir / "archive"]
    for folder in folders:
        if not folder.exists():
            continue
        for file_path in folder.glob("kbn-*.md"):
            try:
                fm, _ = read_frontmatter(file_path)
                status = fm.get("status")
                if status in cards_by_status:
                    cards_by_status[status].append({
                        "id": fm.get("id"),
                        "title": fm.get("title", file_path.stem),
                        "file_path": file_path
                    })
            except Exception:
                pass

    # ID 순 정렬
    for k in cards_by_status:
        cards_by_status[k].sort(key=lambda x: x["id"] or "")

    # 3. README.md 업데이트
    readme_path = base_dir / "README.md"
    if readme_path.exists() and not getattr(args, "dry_run", False):
        content = readme_path.read_text(encoding="utf-8")
        
        headers = ["Backlog", "Todo", "In-Progress", "Review", "Done"]
        status_keys = ["backlog", "todo", "in-progress", "review", "done"]
        max_rows = max(len(cards_by_status[k]) for k in status_keys) if any(cards_by_status[k] for k in status_keys) else 0

        table_lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join([":---"] * len(headers)) + " |"
        ]

        for i in range(max_rows):
            row_cells = []
            for key in status_keys:
                cards = cards_by_status[key]
                if i < len(cards):
                    card = cards[i]
                    rel_path = card["file_path"].relative_to(base_dir).as_posix()
                    row_cells.append(f"[{card['id']}]({rel_path})")
                else:
                    row_cells.append("")
            table_lines.append("| " + " | ".join(row_cells) + " |")

        board_md = "\n".join(table_lines)
        pattern = r"(## Board\s*\n)(.*?)(?=\n## |\Z)"
        replacement = f"## Board\n\n{board_md}\n"
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        if count == 0:
            new_content = content + "\n\n## Board\n\n" + board_md + "\n"
            
        readme_path.write_text(new_content, encoding="utf-8")

    if args.command == "update":
        payload = {
            "status": "updated",
            "path": str(base_dir),
            "cards_count": {k: len(cards_by_status[k]) for k in cards_by_status}
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Unified Kanban CLI Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    parser_init = subparsers.add_parser("init", help="Initialize Kanban workspace")
    parser_init.add_argument("path", help="Kanban root directory")

    # create
    parser_create = subparsers.add_parser("create", help="Create a new card")
    parser_create.add_argument("path", help="Kanban root directory")
    parser_create.add_argument("name", help="Kebab-case card name")
    parser_create.add_argument("--priority", choices=["low", "medium", "high"], default="medium", help="Priority")
    parser_create.add_argument("--assignee", help="Assignee")
    parser_create.add_argument("--description", help="Description")
    parser_create.add_argument("--tags", help="Comma-separated tags")
    parser_create.add_argument("--dry-run", action="store_true", help="Dry run")

    # move
    parser_move = subparsers.add_parser("move", help="Move card and update status")
    parser_move.add_argument("path", help="Kanban root directory")
    parser_move.add_argument("card", help="Card ID, filename or path")
    parser_move.add_argument("status", choices=["backlog", "todo", "in-progress", "review", "done", "rejected"], help="Target status")
    parser_move.add_argument("--assignee", help="Update assignee")
    parser_move.add_argument("--priority", choices=["low", "medium", "high"], help="Update priority")
    parser_move.add_argument("--dry-run", action="store_true", help="Dry run")

    # update
    parser_update = subparsers.add_parser("update", help="Update index files and README.md board")
    parser_update.add_argument("path", help="Kanban root directory")
    parser_update.add_argument("--dry-run", action="store_true", help="Dry run")

    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            return cmd_init(args)
        elif args.command == "create":
            return cmd_create(args)
        elif args.command == "move":
            return cmd_move(args)
        elif args.command == "update":
            return cmd_update(args)
    except Exception as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
