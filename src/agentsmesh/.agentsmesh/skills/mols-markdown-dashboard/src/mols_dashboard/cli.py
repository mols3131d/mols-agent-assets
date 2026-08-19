from __future__ import annotations

import argparse
import os
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from jinja2 import TemplateError

from .loader import DashboardInputError, load_dashboard
from .render import DEFAULT_TEMPLATE_DIRECTORY, DEFAULT_TEMPLATE_NAME, render_dashboard
from .validate import (
    DashboardValidationError,
    validate_dashboard_consistency,
    validate_markdown,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mols-dashboard",
        description="Render evidence-backed Markdown development dashboards from YAML.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    render = subparsers.add_parser(
        "render",
        help="validate YAML and render Markdown",
    )
    render.add_argument("input", type=Path, help="dashboard YAML")
    render.add_argument(
        "-o",
        "--output",
        required=True,
        help="output Markdown path or '-' for stdout",
    )
    render.add_argument(
        "--template-directory",
        type=Path,
        default=DEFAULT_TEMPLATE_DIRECTORY,
    )
    render.add_argument("--template-name", default=DEFAULT_TEMPLATE_NAME)
    render.add_argument(
        "--no-markdown-check",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    validate = subparsers.add_parser(
        "validate",
        help="validate YAML and rendered Markdown",
    )
    validate.add_argument("input", type=Path, help="dashboard YAML")
    validate.add_argument(
        "--markdown",
        type=Path,
        help="existing Markdown; otherwise render in memory",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        dashboard = load_dashboard(args.input)
        validate_dashboard_consistency(dashboard)

        if args.command == "render":
            markdown = render_dashboard(
                dashboard,
                template_directory=args.template_directory,
                template_name=args.template_name,
            )
            if not args.no_markdown_check:
                validate_markdown(markdown, dashboard=dashboard)
            _write_output(args.output, markdown)
            if args.output != "-":
                print(f"rendered: {args.output}")
            return 0

        markdown = (
            args.markdown.read_text(encoding="utf-8")
            if args.markdown
            else render_dashboard(dashboard)
        )
        validate_markdown(markdown, dashboard=dashboard)
        print(f"valid: {args.input}")
        return 0
    except (
        DashboardInputError,
        DashboardValidationError,
        TemplateError,
        OSError,
        ValueError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _write_output(output: str, markdown: str) -> None:
    if output == "-":
        sys.stdout.write(markdown)
        return

    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(markdown)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
