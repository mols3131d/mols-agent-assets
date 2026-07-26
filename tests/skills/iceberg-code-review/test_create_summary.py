import tempfile
import unittest
from pathlib import Path

from _shared import ReviewFileCreationError
from create_summary import create_summary


class CreateSummaryTest(unittest.TestCase):
    def test_create_and_reject_invalid_or_duplicate_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            review_dir = Path(directory) / "review"
            review_dir.mkdir()

            destination = create_summary(review_dir)

            self.assertEqual(destination, review_dir / "__summary__.md")
            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                _template().read_text(encoding="utf-8"),
            )
            with self.assertRaises(ReviewFileCreationError):
                create_summary(review_dir)

    def test_reject_missing_review_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ReviewFileCreationError):
                create_summary(Path(directory) / "review")


def _template() -> Path:
    root = Path(__file__).resolve().parents[3]
    src_template = (
        root
        / "src"
        / "skills"
        / "iceberg-code-review"
        / "assets"
        / "templates"
        / "__summary__.md"
    )
    if src_template.exists():
        return src_template
    return (
        root
        / "release"
        / "skills"
        / "iceberg-code-review"
        / "assets"
        / "templates"
        / "__summary__.md"
    )


if __name__ == "__main__":
    unittest.main()
