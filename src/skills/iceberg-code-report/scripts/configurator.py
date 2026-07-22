#!/usr/bin/env python3
"""iceberg-code-report 사용자 설정을 생성하고 관리한다."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

LOGGER = logging.getLogger(__name__)
SKILL_CONFIG_PATH = Path("iceberg-code-report/user_data/config.json")
DEFAULT_CONFIG: dict[str, str] = {
    "timezone": "Asia/Seoul",
    "default_output_dir": "reports/",
    "default_output_format": "%Y-%m%d/%H%M-{title_slug}",
}
CONFIG_KEYS = frozenset(DEFAULT_CONFIG)


class ConfigError(ValueError):
    """설정이 없거나 유효하지 않을 때 발생한다."""


def config_candidates(
    project_root: Path,
    *,
    project_configs_directory: Path | None = None,
    project_agent_skills_directory: Path | None = None,
    global_agent_skills_directory: Path | None = None,
) -> tuple[Path, ...]:
    """우선순위대로 중복 없는 config 후보를 반환한다."""
    directories = [
        project_configs_directory,
        project_root / ".configs",
        project_agent_skills_directory or project_root / ".agents" / "skills",
        global_agent_skills_directory or Path.home() / ".agents" / "skills",
    ]
    candidates: list[Path] = []
    for directory in directories:
        if directory is None:
            continue
        candidate = directory / SKILL_CONFIG_PATH
        if candidate not in candidates:
            candidates.append(candidate)
    return tuple(candidates)


def find_config(
    project_root: Path,
    **directories: Path | None,
) -> Path:
    """우선순위가 가장 높은 기존 config 경로를 반환한다."""
    candidates = config_candidates(project_root, **directories)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise ConfigError(f"config file not found; searched: {searched}")


def _validate_relative_path(value: str, key: str) -> None:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise ConfigError(f"{key} must be a non-empty relative path: {value!r}")


def validate_config(config: dict[str, Any]) -> None:
    """필수 키와 각 설정값을 검증한다."""
    missing = CONFIG_KEYS - config.keys()
    unknown = config.keys() - CONFIG_KEYS
    if missing or unknown:
        raise ConfigError(
            f"invalid config keys: missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    if not all(isinstance(config[key], str) for key in CONFIG_KEYS):
        raise ConfigError("all config values must be strings")

    try:
        ZoneInfo(config["timezone"])
    except ZoneInfoNotFoundError as error:
        raise ConfigError(f"unknown IANA timezone: {config['timezone']!r}") from error

    _validate_relative_path(config["default_output_dir"], "default_output_dir")
    _validate_relative_path(config["default_output_format"], "default_output_format")
    if config["default_output_format"].count("{title_slug}") != 1:
        raise ConfigError("default_output_format must contain one {title_slug}")


def _write_config(config: dict[str, str], config_file: Path) -> None:
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def initialize_config(
    config_file: Path | None = None,
    *,
    overwrite: bool = False,
    project_root: Path | None = None,
    project_configs_directory: Path | None = None,
) -> dict[str, str]:
    """기본 설정 파일을 생성하고 현재 설정을 반환한다."""
    if config_file is None:
        config_file = config_candidates(
            project_root or Path.cwd(),
            project_configs_directory=project_configs_directory,
        )[0]
    if config_file.exists() and not overwrite:
        return check_config(config_file)

    config = DEFAULT_CONFIG.copy()
    _write_config(config, config_file)
    return config


def check_config(
    config_file: Path | None = None,
    *,
    project_root: Path | None = None,
    project_configs_directory: Path | None = None,
    project_agent_skills_directory: Path | None = None,
    global_agent_skills_directory: Path | None = None,
) -> dict[str, str]:
    """설정 파일을 읽고 검증한 뒤 반환한다."""
    if config_file is None:
        config_file = find_config(
            project_root or Path.cwd(),
            project_configs_directory=project_configs_directory,
            project_agent_skills_directory=project_agent_skills_directory,
            global_agent_skills_directory=global_agent_skills_directory,
        )
    elif not config_file.is_file():
        raise ConfigError(f"config file not found: {config_file}")
    try:
        config = json.loads(config_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ConfigError(f"could not read config: {config_file}") from error
    if not isinstance(config, dict):
        raise ConfigError("config root must be an object")
    validate_config(config)
    return config


def update_config(
    updates: dict[str, str],
    config_file: Path | None = None,
    **search: Path | None,
) -> dict[str, str]:
    """지정한 값만 수정하고 검증된 전체 설정을 반환한다."""
    unknown = updates.keys() - CONFIG_KEYS
    if unknown:
        raise ConfigError(f"unknown config keys: {sorted(unknown)}")
    if config_file is None:
        config_file = find_config(
            search.pop("project_root", None) or Path.cwd(), **search
        )
    config = check_config(config_file)
    config.update(updates)
    validate_config(config)
    _write_config(config, config_file)
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure iceberg-code-report")
    parser.add_argument("--config", type=Path, help="Use one explicit config file")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--project-configs-dir", type=Path)
    parser.add_argument("--project-agent-skills-dir", type=Path)
    parser.add_argument("--global-agent-skills-dir", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create default config")
    init_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing config"
    )
    subparsers.add_parser("show", help="Validate and show config")

    set_parser = subparsers.add_parser("set", help="Update config")
    set_parser.add_argument("--timezone")
    set_parser.add_argument("--output-dir")
    set_parser.add_argument("--output-format")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()
    search = {
        "project_configs_directory": args.project_configs_dir,
        "project_agent_skills_directory": args.project_agent_skills_dir,
        "global_agent_skills_directory": args.global_agent_skills_dir,
    }
    try:
        if args.command == "init":
            config_file = (
                args.config
                or config_candidates(
                    args.project_root,
                    project_configs_directory=args.project_configs_dir,
                )[0]
            )
            config = initialize_config(
                config_file,
                overwrite=args.force,
                project_root=args.project_root,
                project_configs_directory=args.project_configs_dir,
            )
        else:
            config_file = args.config or find_config(args.project_root, **search)
            if args.command == "show":
                config = check_config(config_file)
            else:
                updates = {
                    key: value
                    for key, value in {
                        "timezone": args.timezone,
                        "default_output_dir": args.output_dir,
                        "default_output_format": args.output_format,
                    }.items()
                    if value is not None
                }
                if not updates:
                    raise ConfigError("set requires at least one option")
                config = update_config(updates, config_file)
    except ConfigError as error:
        LOGGER.error("Configuration failed: %s", error)
        return 1

    LOGGER.info(
        "Configuration file: %s", config_file, extra={"config_file": str(config_file)}
    )
    LOGGER.info(
        "Configuration: %s", json.dumps(config, ensure_ascii=False, sort_keys=True)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
