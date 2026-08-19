from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "agentsmesh"
    / "skills"
    / "mols-agent-asset-validator"
)
sys.path.insert(0, str(ROOT / "scripts"))

from scan_assets import ScanError, extract_zip_safely, scan_directory  # noqa: E402


class ScanAssetsTests(unittest.TestCase):
    def test_valid_minimal_skill_passes_deterministic_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Example.\n---\n\n# Example\n",
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "cases.json").write_text(
                json.dumps({"cases": []}) + "\n", encoding="utf-8"
            )
            result = scan_directory(root)
            self.assertEqual(result["summary"]["critical"], 0)
            self.assertEqual(result["summary"]["major"], 0)
            self.assertEqual(result["summary"]["disposition"], "pass")

    def test_broken_markdown_link_is_major(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "SKILL.md").write_text(
                "---\nname: broken-skill\ndescription: Broken.\n---\n\n[Missing](references/nope.md)\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            messages = [item["message"] for item in result["findings"]]
            self.assertTrue(any("broken relative link" in message for message in messages))
            self.assertEqual(result["summary"]["disposition"], "revise")

    def test_invalid_json_is_major(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "config.json").write_text("{not-json}\n", encoding="utf-8")
            result = scan_directory(root)
            self.assertTrue(any(item["category"] == "json" for item in result["findings"]))

    def test_possible_secret_is_critical(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "prompt.md").write_text(
                "token: " + "sk-" + "abcdefghijklmnopqrstuvwx" + "\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            self.assertEqual(result["summary"]["critical"], 1)

    def test_duplicate_frontmatter_name_is_major(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "agents").mkdir()
            for name in ("a.agent.md", "b.agent.md"):
                (root / "agents" / name).write_text(
                    "---\nname: duplicate\ndescription: Example.\n---\n\n# Agent\n",
                    encoding="utf-8",
                )
            result = scan_directory(root)
            self.assertTrue(any(item["category"] == "identity" for item in result["findings"]))

    def test_declared_missing_asset_path_is_major(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "SKILL.md").write_text(
                "---\nname: declared-path-skill\ndescription: Example.\n---\n\nRead `references/missing.md`.\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            self.assertTrue(any(item["category"] == "reference" for item in result["findings"]))

    def test_invalid_toml_is_major(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "config.toml").write_text("key = [\n", encoding="utf-8")
            result = scan_directory(root)
            self.assertTrue(any(item["category"] == "toml" for item in result["findings"]))

    def test_nested_skill_declared_paths_resolve_from_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package = root / "nested-skill"
            (package / "references").mkdir(parents=True)
            (package / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (package / "SKILL.md").write_text(
                "---\nname: nested-skill\ndescription: Example.\n---\n\nRead `references/guide.md`.\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            self.assertFalse(any(item["category"] == "reference" for item in result["findings"]))

    def test_suspicious_zip_compression_ratio_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "compressed.zip"
            destination = Path(temp_dir) / "out"
            destination.mkdir()
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
                handle.writestr("zeros.txt", b"0" * (2 * 1024 * 1024))
            with self.assertRaises(ScanError):
                extract_zip_safely(archive, destination)

    def test_zip_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "unsafe.zip"
            destination = Path(temp_dir) / "out"
            destination.mkdir()
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("../escape.txt", "no")
            with self.assertRaises(ScanError):
                extract_zip_safely(archive, destination)

    def test_heading_depth_jump_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "SKILL.md").write_text(
                "---\nname: heading-skill\ndescription: Example.\n---\n\n# Root\n\n### Skipped\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            self.assertTrue(
                any(item["category"] == "human-comprehension" for item in result["findings"])
            )

    def test_repeated_normative_instruction_across_three_files_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "SKILL.md").write_text(
                "---\nname: repeated-skill\ndescription: Example.\n---\n\n# Root\n\n- Always preserve the explicit approval boundary before destructive actions.\n",
                encoding="utf-8",
            )
            (root / "agents").mkdir()
            for name in ("a.agent.md", "b.agent.md"):
                (root / "agents" / name).write_text(
                    f"---\nname: {name.split('.')[0]}\ndescription: Example.\n---\n\n# Agent\n\n- Always preserve the explicit approval boundary before destructive actions.\n",
                    encoding="utf-8",
                )
            result = scan_directory(root)
            self.assertTrue(any(item["category"] == "context-noise" for item in result["findings"]))
            self.assertEqual(result["analysis_signals"]["duplicate_normative_groups"], 1)

    def test_relationship_and_analysis_signals_are_emitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "references").mkdir()
            (root / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "SKILL.md").write_text(
                "---\nname: relation-skill\ndescription: Example.\n---\n\n# Root\n\nRead `references/guide.md`.\n",
                encoding="utf-8",
            )
            result = scan_directory(root)
            self.assertGreaterEqual(result["analysis_signals"]["relationship_count"], 1)
            self.assertTrue(
                any(item["to"] == "references/guide.md" for item in result["relationships"])
            )


if __name__ == "__main__":
    unittest.main()
