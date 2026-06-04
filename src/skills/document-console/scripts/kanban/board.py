from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from core import (
    DocStatus,
    Document,
)

class KanbanBoard:
    """칸반 보드 디렉터리 및 카드 자산들을 총괄 관리하는 도메인 모델."""
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir.resolve()
        self.backlog_dir = self.base_dir / "backlog"
        self.archive_dir = self.base_dir / "archive"

    def exists(self) -> bool:
        """칸반 디렉터리가 활성화되어 있는지 여부를 체크한다."""
        return self.base_dir.exists()

    def get_status_folder(self, status: DocStatus) -> Path:
        """상태에 따른 카드 보관 디렉터리를 매핑한다."""
        if status in (DocStatus.BACKLOG, DocStatus.TODO):
            return self.backlog_dir
        elif status in (DocStatus.IN_PROGRESS, DocStatus.REVIEW):
            return self.base_dir
        else:
            return self.archive_dir

    def get_next_card_id(self) -> str:
        """모든 폴더를 스캔하여 중복되지 않는 다음 kbn 일련번호 ID를 결정한다."""
        max_id = 0
        folders = [self.base_dir, self.backlog_dir, self.archive_dir]
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

    def locate_card(self, ident: str) -> Document | None:
        """ID, 파일명 또는 경로로부터 카드 문서를 찾아 로드한다."""
        # 1. 직접 파일 경로 매칭 확인
        paths = [
            self.base_dir / ident,
            self.backlog_dir / ident,
            self.archive_dir / ident,
        ]
        for p in paths:
            if p.is_file():
                return Document.load(p)

        # 2. ID 식별자 패딩 정규화
        card_id = ident.strip()
        if card_id.isdigit():
            card_id = f"kbn-{int(card_id):03d}"

        # 3. 전체 카드 디렉터리 패턴 스캔
        for folder in [self.base_dir, self.backlog_dir, self.archive_dir]:
            if not folder.exists():
                continue
            for p in folder.glob("kbn-*.md"):
                name = p.name
                parts = name.split(".", 1)[0].split("-", 2)
                if len(parts) >= 2:
                    current_id = f"{parts[0]}-{parts[1]}"
                    if current_id.lower() == card_id.lower():
                        return Document.load(p)
        return None

    def update_indices(self) -> None:
        """모든 폴더 내 INDEX.csv 메타데이터 파일을 동기화한다."""
        for folder in [self.base_dir, self.backlog_dir, self.archive_dir]:
            if not folder.exists():
                continue
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

    def render_board(self) -> None:
        """README.md 파일 내 칸반 보드 테이블 레이아웃을 다시 렌더링한다."""
        readme_path = self.base_dir / "README.md"
        if not readme_path.exists():
            return

        cards_by_status: dict[str, list[dict[str, Any]]] = {
            "backlog": [],
            "todo": [],
            "in-progress": [],
            "review": [],
            "done": [],
        }

        # 1. 모든 활성 상태 카드 스캔 및 분류
        for folder in [self.base_dir, self.backlog_dir, self.archive_dir]:
            if not folder.exists():
                continue
            for file_path in folder.glob("kbn-*.md"):
                try:
                    doc = Document.load(file_path)
                    status = doc.frontmatter.status
                    if status in cards_by_status:
                        cards_by_status[status].append({
                            "id": doc.frontmatter.id,
                            "title": doc.frontmatter.title or file_path.stem,
                            "file_path": file_path,
                        })
                except Exception:
                    pass

        # 2. 상태별 카드 정렬 (ID 순)
        for k in cards_by_status:
            cards_by_status[k].sort(key=lambda x: x["id"] or "")

        # 3. 보드 테이블 생성
        headers = ["Backlog", "Todo", "In-Progress", "Review", "Done"]
        status_keys = ["backlog", "todo", "in-progress", "review", "done"]
        max_rows = max(len(cards_by_status[k]) for k in status_keys) if any(cards_by_status[k] for k in status_keys) else 0

        table_lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join([":---"] * len(headers)) + " |",
        ]

        for i in range(max_rows):
            row_cells = []
            for key in status_keys:
                cards = cards_by_status[key]
                if i < len(cards):
                    card = cards[i]
                    rel_path = card["file_path"].relative_to(self.base_dir).as_posix()
                    row_cells.append(f"[{card['id']}]({rel_path})")
                else:
                    row_cells.append("")
            table_lines.append("| " + " | ".join(row_cells) + " |")

        board_md = "\n".join(table_lines)
        content = readme_path.read_text(encoding="utf-8")

        pattern = r"(## Board\s*\n)(.*?)(?=\n## |\Z)"
        replacement = f"## Board\n\n{board_md}\n"
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        if count == 0:
            new_content = content + "\n\n## Board\n\n" + board_md + "\n"
            
        readme_path.write_text(new_content, encoding="utf-8")
