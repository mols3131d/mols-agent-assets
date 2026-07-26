#!/usr/bin/env python3
"""Generates a code review detail file from a template."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from _shared import ReviewFileCreationError, copy_template, validate_slug

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create code review detail file")
    parser.add_argument("--review-dir", required=True, type=Path)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--detail", required=True)
    return parser.parse_args()


def create_detail(review_dir: Path, domain: str, detail: str) -> Path:
    for name, value in (("domain", domain), ("detail", detail)):
        validate_slug(name, value)

    if review_dir.exists() and not review_dir.is_dir():
        raise ReviewFileCreationError(f"REVIEW_DIR_NOT_DIRECTORY: {review_dir}")

    destination = review_dir / f"{domain}-{detail}.md"
    return copy_template("{{domain}}-{{detail}}.md", destination)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args()

    try:
        destination = create_detail(args.review_dir, args.domain, args.detail)
    except ReviewFileCreationError as error:
        LOGGER.error("Fail: %s", error, extra={"reason": str(error)})
        return 1

    LOGGER.info("OK: %s", destination.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
