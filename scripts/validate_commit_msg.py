from __future__ import annotations

import re
import sys
from pathlib import Path

HEADER_RE = re.compile(
    r"^(feat|fix|refactor|perf|docs|test|style|chore)(\([^)]+\))?: .+$"
)
MAX_SUBJECT_LENGTH = 72
GENERATED_PREFIXES = ("Merge ", 'Revert "')


def validate_subject(subject: str) -> str | None:
    if not subject:
        return "commit subject must not be empty"

    if subject.startswith(GENERATED_PREFIXES):
        return None

    if len(subject) > MAX_SUBJECT_LENGTH:
        return f"commit subject must be at most {MAX_SUBJECT_LENGTH} characters"

    if not HEADER_RE.fullmatch(subject):
        return (
            "commit subject must match "
            "<type>(optional-scope): <description>; "
            "allowed types: feat, fix, refactor, perf, docs, test, style, chore"
        )

    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_commit_msg.py <commit-message-file>", file=sys.stderr)
        return 2

    message_path = Path(argv[1])
    subject = message_path.read_text(encoding="utf-8").partition("\n")[0].strip()
    error = validate_subject(subject)

    if error is None:
        return 0

    print(f"Invalid commit message: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
