"""Run the bundled portable regression suite in the repository PR Gate."""

import io
import unittest
from pathlib import Path


def test_bundled_check_dependencies_regressions():
    tests_dir = (
        Path(__file__).resolve().parents[3]
        / "src/rulesync/.rulesync/skills/check-dependencies/tests"
    )
    suite = unittest.defaultTestLoader.discover(
        str(tests_dir), pattern="test_check_dependencies.py"
    )
    assert suite.countTestCases() > 0, "Bundled dependency tests were not discovered"

    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output).run(suite)
    assert result.wasSuccessful(), output.getvalue()
