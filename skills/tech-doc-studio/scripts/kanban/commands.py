from __future__ import annotations

# ruff: noqa: E501
from abc import ABC, abstractmethod
from typing import Any

from core import (
    DocStatus,
    Document,
    TaskPriority,
    format_yaml_list,
    normalize_kebab_case,
    title_case_name,
)
from templates import KANBAN_DOCUMENT_TEMPLATE

from kanban.board import KanbanBoard


class KanbanCommand(ABC):
    """모든 칸반 세부 명령들이 구현해야 할 공통 커맨드 인터페이스."""

    @abstractmethod
    def execute(self) -> dict[str, Any]:
        """명령을 수행하고 결과를 반환한다."""
        pass


class KanbanInitCommand(KanbanCommand):
    """칸반 보드 구조 및 문서를 초기화한다."""

    def __init__(self, board: KanbanBoard) -> None:
        self.board = board

    def execute(self) -> dict[str, Any]:
        self.board.base_dir.mkdir(parents=True, exist_ok=True)
        self.board.backlog_dir.mkdir(exist_ok=True)
        self.board.archive_dir.mkdir(exist_ok=True)

        # 인덱스 초기화
        self.board.update_indices()
        created = ["INDEX.csv", "backlog/INDEX.csv", "archive/INDEX.csv"]

        return {
            "status": "initialized",
            "path": str(self.board.base_dir),
            "created": created,
        }


class KanbanCreateCommand(KanbanCommand):
    """새로운 백로그 카드를 생성한다."""

    def __init__(
        self,
        board: KanbanBoard,
        name: str,
        priority: TaskPriority,
        assignee: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        dry_run: bool = False,
    ) -> None:
        self.board = board
        self.name = name
        self.priority = priority
        self.assignee = assignee
        self.description = description
        self.tags = tags or []
        self.dry_run = dry_run

    def execute(self) -> dict[str, Any]:
        if not self.board.exists():
            raise FileNotFoundError(
                f"칸반 디렉터리가 존재하지 않습니다. 먼저 init을 실행하세요: {self.board.base_dir}"
            )

        id_num = self.board.get_next_card_id()
        card_id = f"kbn-{id_num}"
        doc_name = normalize_kebab_case(self.name)
        filename = f"{card_id}-{doc_name}.md"

        dest_path = self.board.backlog_dir / filename

        if dest_path.exists():
            raise FileExistsError(f"카드 파일이 이미 존재합니다: {dest_path}")

        title = title_case_name(doc_name)
        tags_yaml = format_yaml_list(self.tags)
        doc_content = KANBAN_DOCUMENT_TEMPLATE.format(
            card_id=card_id,
            title=title,
            status=DocStatus.BACKLOG.value,
            priority=self.priority.value,
            description=self.description or "",
            assignee=self.assignee or "",
            tags=tags_yaml,
        )

        if not self.dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(doc_content, encoding="utf-8")
            self.board.update_indices()

        return {
            "status": "created",
            "card_id": card_id,
            "filename": filename,
            "path": str(dest_path),
        }


class KanbanMoveCommand(KanbanCommand):
    """카드를 이동시키고 상태 및 담당자, 우선순위를 변경한다."""

    def __init__(
        self,
        board: KanbanBoard,
        card_ident: str,
        status: DocStatus,
        assignee: str | None = None,
        priority: TaskPriority | None = None,
        dry_run: bool = False,
    ) -> None:
        self.board = board
        self.card_ident = card_ident
        self.status = status
        self.assignee = assignee
        self.priority = priority
        self.dry_run = dry_run

    def execute(self) -> dict[str, Any]:
        doc = self.board.locate_card(self.card_ident)
        if not doc or not doc.path:
            raise FileNotFoundError(
                f"지정된 카드를 찾을 수 없습니다: {self.card_ident}"
            )

        old_status = doc.frontmatter.status
        old_path = doc.path

        # 1. 프론트매터 정보 업데이트
        doc.frontmatter.set("status", self.status.value)
        if self.assignee is not None:
            doc.frontmatter.set("assignee", self.assignee)
        if self.priority is not None:
            doc.frontmatter.set("priority", self.priority.value)

        # 2. 이동 경로 계산
        dest_folder = self.board.get_status_folder(self.status)
        dest_path = dest_folder / doc.path.name

        if not self.dry_run:
            if doc.path != dest_path:
                if dest_path.exists():
                    raise FileExistsError(
                        f"이동하려는 위치에 파일이 이미 존재합니다: {dest_path}"
                    )
                doc.path.unlink()

            doc.save(dest_path)
            self.board.update_indices()

        return {
            "status": "moved",
            "card_id": doc.frontmatter.id,
            "old_status": old_status,
            "new_status": self.status.value,
            "old_path": str(old_path),
            "new_path": str(dest_path),
        }


class KanbanUpdateCommand(KanbanCommand):
    def __init__(self, board: KanbanBoard, dry_run: bool = False) -> None:
        self.board = board
        self.dry_run = dry_run

    def execute(self) -> dict[str, Any]:
        if not self.dry_run:
            self.board.update_indices()

        # 각 폴더별 상태 요약 집계
        cards_count = {
            "backlog": 0,
            "todo": 0,
            "in-progress": 0,
            "review": 0,
            "done": 0,
        }

        for folder in [
            self.board.base_dir,
            self.board.backlog_dir,
            self.board.archive_dir,
        ]:
            if not folder.exists():
                continue
            for file_path in folder.glob("kbn-*.md"):
                try:
                    doc = Document.load(file_path)
                    status = doc.frontmatter.status
                    if status in cards_count:
                        cards_count[status] += 1
                except Exception:
                    pass

        return {
            "status": "updated",
            "path": str(self.board.base_dir),
            "cards_count": cards_count,
        }
