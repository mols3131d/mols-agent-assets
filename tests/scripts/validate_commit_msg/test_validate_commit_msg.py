import pytest

from scripts.validate_commit_msg import main, validate_subject


@pytest.mark.parametrize(
    "subject",
    [
        "feat: add hook validation",
        "fix(hooks): handle staged files",
        "docs: 문서 규칙 정리",
        'Revert "feat: add hook validation"',
        "Merge branch 'main' into feature/hook",
    ],
)
def test_validate_subject_accepts_valid_subjects(subject: str) -> None:
    assert validate_subject(subject) is None


@pytest.mark.parametrize(
    "subject",
    [
        "",
        "build: unsupported type",
        "feat:",
        "feat missing separator",
        "feat: " + "a" * 67,
    ],
)
def test_validate_subject_rejects_invalid_subjects(subject: str) -> None:
    assert validate_subject(subject) is not None


def test_main_rejects_empty_message_file(tmp_path) -> None:
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text("", encoding="utf-8")

    assert main(["validate_commit_msg.py", str(message)]) == 1
