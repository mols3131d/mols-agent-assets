#!/usr/bin/env python3
"""검증된 config로 code report directory를 생성한다."""

from __future__ import annotations

import argparse
import logging
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from configurator import ConfigError, check_config

LOGGER = logging.getLogger(__name__)
TITLE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ReportDirectoryError(ValueError):
    """Report directory를 안전하게 생성할 수 없을 때 발생한다."""


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def create_report_dir(
    title_slug: str,
    *,
    project_root: Path,
    output_path: Path | None = None,
    config_file: Path | None = None,
    project_configs_directory: Path | None = None,
    project_agent_skills_directory: Path | None = None,
    global_agent_skills_directory: Path | None = None,
    now: datetime | None = None,
) -> Path:
    """Report directory를 생성하고 절대 경로를 반환한다."""
    if not TITLE_SLUG.fullmatch(title_slug):
        raise ReportDirectoryError("title_slug must be lowercase kebab-case")

    root = project_root.resolve()
    if output_path is None:
        config = check_config(
            config_file,
            project_root=root,
            project_configs_directory=project_configs_directory,
            project_agent_skills_directory=project_agent_skills_directory,
            global_agent_skills_directory=global_agent_skills_directory,
        )
        timestamp = now or datetime.now(ZoneInfo(config["timezone"]))
        try:
            relative = timestamp.strftime(config["default_output_format"]).format(
                title_slug=title_slug,
            )
        except (KeyError, ValueError) as error:
            raise ReportDirectoryError(
                "could not render default_output_format"
            ) from error
        destination = root / config["default_output_dir"] / relative
    else:
        destination = output_path if output_path.is_absolute() else root / output_path

    destination = destination.resolve()
    if not _inside(destination, root):
        raise ReportDirectoryError(
            f"report directory escapes project root: {destination}"
        )
    if destination.exists() and not destination.is_dir():
        raise ReportDirectoryError(
            f"report directory path is not a directory: {destination}"
        )

    destination.mkdir(parents=True, exist_ok=True)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an iceberg-code-report directory"
    )
    parser.add_argument("--title-slug", required=True)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-path", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--project-configs-dir", type=Path)
    parser.add_argument("--project-agent-skills-dir", type=Path)
    parser.add_argument("--global-agent-skills-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()
    try:
        report_dir = create_report_dir(
            args.title_slug,
            project_root=args.project_root,
            output_path=args.output_path,
            config_file=args.config,
            project_configs_directory=args.project_configs_dir,
            project_agent_skills_directory=args.project_agent_skills_dir,
            global_agent_skills_directory=args.global_agent_skills_dir,
        )
    except (ConfigError, ReportDirectoryError, OSError) as error:
        LOGGER.error("Report directory creation failed: %s", error)
        return 1

    LOGGER.info(
        "Report directory: %s", report_dir, extra={"report_dir": str(report_dir)}
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
