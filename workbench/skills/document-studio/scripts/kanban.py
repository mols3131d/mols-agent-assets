#!/usr/bin/env python3
"""Unified Kanban board and card manager script entry point."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

# Add current scripts directory to sys.path to allow importing from packages
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from core import DocStatus, TaskPriority
from kanban import (
    KanbanBoard,
    KanbanCreateCommand,
    KanbanInitCommand,
    KanbanMoveCommand,
    KanbanUpdateCommand,
)


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
    parser_create.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Priority",
    )
    parser_create.add_argument("--assignee", help="Assignee")
    parser_create.add_argument("--description", help="Description")
    parser_create.add_argument("--tags", help="Comma-separated tags")
    parser_create.add_argument("--dry-run", action="store_true", help="Dry run")

    # move
    parser_move = subparsers.add_parser("move", help="Move card and update status")
    parser_move.add_argument("path", help="Kanban root directory")
    parser_move.add_argument("card", help="Card ID, filename or path")
    parser_move.add_argument(
        "status",
        choices=["backlog", "todo", "in-progress", "review", "done", "rejected"],
        help="Target status",
    )
    parser_move.add_argument("--assignee", help="Update assignee")
    parser_move.add_argument(
        "--priority", choices=["low", "medium", "high"], help="Update priority"
    )
    parser_move.add_argument("--dry-run", action="store_true", help="Dry run")

    # update
    parser_update = subparsers.add_parser(
        "update", help="Update index files and README.md board"
    )
    parser_update.add_argument("path", help="Kanban root directory")
    parser_update.add_argument("--dry-run", action="store_true", help="Dry run")

    args = parser.parse_args(argv)
    board = KanbanBoard(Path(args.path))

    try:
        if args.command == "init":
            cmd = KanbanInitCommand(board)
        elif args.command == "create":
            tags_list = (
                [t.strip() for t in args.tags.split(",") if t.strip()]
                if args.tags
                else []
            )
            cmd = KanbanCreateCommand(
                board=board,
                name=args.name,
                priority=TaskPriority(args.priority),
                assignee=args.assignee,
                description=args.description,
                tags=tags_list,
                dry_run=args.dry_run,
            )
        elif args.command == "move":
            priority_val = TaskPriority(args.priority) if args.priority else None
            cmd = KanbanMoveCommand(
                board=board,
                card_ident=args.card,
                status=DocStatus(args.status),
                assignee=args.assignee,
                priority=priority_val,
                dry_run=args.dry_run,
            )
        elif args.command == "update":
            cmd = KanbanUpdateCommand(board, dry_run=args.dry_run)
        else:
            raise ValueError(f"Unknown command: {args.command}")

        payload = cmd.execute()

    except Exception as exc:
        payload = {"status": "error", "message": str(exc)}
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1

    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
