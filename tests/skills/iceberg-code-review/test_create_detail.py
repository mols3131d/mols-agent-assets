import tempfile
import unittest
from pathlib import Path

from _shared import ReviewFileCreationError
from create_detail import create_detail


class CreateDetailTest(unittest.TestCase):
    def test_create_and_reject_invalid_or_duplicate_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            review_dir = Path(directory) / "review"
            destination = create_detail(review_dir, "auth", "null-user")

            self.assertEqual(destination, review_dir / "auth-null-user.md")
            self.assertEqual(destination.read_text(), _template().read_text())
            with self.assertRaises(ReviewFileCreationError):
                create_detail(review_dir, "auth", "null-user")
            with self.assertRaises(ReviewFileCreationError):
                create_detail(review_dir, "../auth", "null-user")


def _template() -> Path:
    root = Path(__file__).resolve().parents[3]
    src_template = (
        root
        / "src"
        / "skills"
        / "iceberg-code-review"
        / "assets"
        / "templates"
        / "{{domain}}-{{detail}}.md"
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
        / "{{domain}}-{{detail}}.md"
    )


if __name__ == "__main__":
    unittest.main()
