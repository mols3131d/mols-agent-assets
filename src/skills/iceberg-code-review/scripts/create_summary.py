#!/usr/bin/env python3
"""Generates a code review summary file from a template."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from _shared import ReviewFileCreationError, copy_template

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create code review summary file")
    parser.add_argument("--review-dir", required=True, type=Path)
    return parser.parse_args()


def create_summary(review_dir: Path) -> Path:
    if not review_dir.is_dir():
        raise ReviewFileCreationError(f"REVIEW_DIR_NOT_FOUND: {review_dir}")
    if not any(path.name != "__summary__.md" for path in review_dir.glob("*.md")):
        raise ReviewFileCreationError(f"DETAIL_FILES_NOT_FOUND: {review_dir}")

    destination = review_dir / "__summary__.md"
    return copy_template("__summary__.md", destination)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()

    try:
        destination = create_summary(args.review_dir)
    except ReviewFileCreationError as error:
        LOGGER.error("Fail: %s", error, extra={"reason": str(error)})
        return 1

    LOGGER.info("OK: %s", destination.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
