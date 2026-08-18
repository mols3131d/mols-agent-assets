from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .derive import (
    aggregate_dashboard,
    implementation_gap_rows,
    progress_bar,
    verification_gap_rows,
)
from .model import Dashboard

DEFAULT_TEMPLATE_DIRECTORY = Path(__file__).resolve().parents[2] / "templates"
DEFAULT_TEMPLATE_NAME = "dashboard.md.j2"


def markdown_cell(value: object) -> str:
    """Preserve lightweight Markdown while preventing table-shape corruption."""
    return (
        str(value)
        .replace("|", "\\|")
        .replace("\r\n", "<br>")
        .replace("\r", "<br>")
        .replace("\n", "<br>")
    )


def markdown_inline(value: object) -> str:
    """Normalize a scalar for one-line prose without altering Markdown links."""
    return " ".join(str(value).replace("\r", "\n").splitlines())


def render_dashboard(
    dashboard: Dashboard,
    *,
    template_directory: Path = DEFAULT_TEMPLATE_DIRECTORY,
    template_name: str = DEFAULT_TEMPLATE_NAME,
) -> str:
    environment = _create_environment(template_directory)
    template = environment.get_template(template_name)
    rendered = template.render(
        dashboard=dashboard,
        total=aggregate_dashboard(dashboard),
        row_label=dashboard.level.row_label,
        implementation_gap_rows=implementation_gap_rows(dashboard),
        verification_gap_rows=verification_gap_rows(dashboard),
    )
    return f"{rendered.rstrip()}\n"


def _create_environment(template_directory: Path) -> Environment:
    environment = Environment(
        loader=FileSystemLoader(template_directory),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters.update(
        markdown_cell=markdown_cell,
        markdown_inline=markdown_inline,
        progress_bar=progress_bar,
    )
    return environment
