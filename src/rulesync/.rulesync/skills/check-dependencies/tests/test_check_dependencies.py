import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "check_dependencies.py"
spec = importlib.util.spec_from_file_location("check_dependencies", SOURCE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class DependencyChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def add_npm_lock(self):
        (self.root / "package-lock.json").write_text(json.dumps({
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "example"},
                "node_modules/example": {"version": "1.2.3"},
                "node_modules/@private/secret": {"version": "2.3.4"},
                "node_modules/example/node_modules/child": {"version": "4.5.6"},
                "node_modules/local": {"version": "file:../local", "link": True},
            },
        }), encoding="utf-8")

    def test_inventory_offline_never_queries_network(self):
        self.add_npm_lock()
        (self.root / "package.json").write_text('{"dependencies": {"example":"^9.0.0"}}')
        (self.root / "requirements.txt").write_text("Requests==2.32.0\nunknown>=2\n-r private.txt\n")
        with patch.object(audit, "request_json", side_effect=AssertionError("network called")):
            packages, warnings = audit.inventory(self.root)
        self.assertEqual(len(packages), 6)
        self.assertEqual(next(p for p in packages if p["name"] == "example")["version"], "1.2.3")
        self.assertEqual(next(p for p in packages if p["name"] == "local")["version_status"], "UNRESOLVED")
        self.assertEqual(next(p for p in packages if p["name"] == "requests")["version_status"], "PINNED")
        self.assertEqual(next(p for p in packages if p["name"] == "unknown")["version_status"], "UNRESOLVED")
        self.assertTrue(any("Unparsed requirements.txt" in warning for warning in warnings))
        self.assertTrue(all(p["registry"] == "NOT_CHECKED" for p in packages))

    def test_manifest_only_does_not_assert_pinned(self):
        (self.root / "package.json").write_text('{"dependencies":{"direct":"1.2.3"}}')
        packages, _ = audit.inventory(self.root)
        self.assertEqual(packages[0]["version_status"], "UNRESOLVED")

    def test_online_404_and_osv_found_and_private_exclusion(self):
        self.add_npm_lock()
        packages, warnings = audit.inventory(self.root)
        calls = []

        def fake(url, payload=None, timeout=10):
            calls.append((url, payload))
            if url == "https://api.osv.dev/v1/querybatch":
                return {"results": [{"vulns": ([{"id": "GHSA-1234"}] if q["package"]["name"] == "example" else [])}
                                    for q in payload["queries"]]}, None
            if "example" in url:
                return None, "HTTP 404"
            return {"name": "child"}, None

        with patch.object(audit, "request_json", side_effect=fake):
            queried = audit.verify_online(packages, warnings, 50, 10, False)
        self.assertEqual(queried, 2)
        package = next(p for p in packages if p["name"] == "example")
        self.assertEqual(package["registry"], "NOT_FOUND_PUBLIC")
        self.assertEqual(package["osv"], "FOUND")
        self.assertEqual(package["advisory_ids"], ["GHSA-1234"])
        scoped = next(p for p in packages if p["name"].startswith("@"))
        self.assertEqual(scoped["registry"], "SKIPPED")
        self.assertEqual(scoped["osv"], "NOT_CHECKED")
        self.assertFalse(any("@private" in url for url, _ in calls))

    def test_osv_error_remains_error(self):
        packages = [audit.record("PyPI", "requests", "2.32.0", "requirements.txt:1", True)]
        with patch.object(audit, "request_json", return_value=(None, "HTTP 503")):
            audit.query_osv(packages, 5)
        self.assertEqual(packages[0]["osv"], "ERROR")
        self.assertIn("HTTP 503", " ".join(packages[0]["errors"]))

    def test_osv_pagination(self):
        packages = [audit.record("PyPI", "demo", "1.0.0", "requirements.txt:1", True)]
        pages = []

        def fake(url, payload=None, timeout=10):
            token = payload["queries"][0].get("page_token")
            pages.append(token)
            if not token:
                return {"results": [{"vulns": [{"id": "VULN-1"}], "next_page_token": "more"}]}, None
            return {"results": [{"vulns": [{"id": "VULN-2"}]}]}, None

        with patch.object(audit, "request_json", side_effect=fake):
            audit.query_osv(packages, 10)
        self.assertEqual(pages, [None, "more"])
        self.assertEqual(packages[0]["advisory_ids"], ["VULN-1", "VULN-2"])
        self.assertEqual(packages[0]["osv"], "FOUND")

    def test_nonpublic_npm_origin_never_leaves_machine(self):
        (self.root / "package-lock.json").write_text(json.dumps({
            "lockfileVersion": 3,
            "packages": {
                "node_modules/internal-service": {
                    "version": "1.2.3",
                    "resolved": "https://packages.example.internal/internal-service-1.2.3.tgz",
                },
                "node_modules/public-service": {
                    "version": "4.5.6",
                    "resolved": "https://registry.npmjs.org/public-service/-/public-service-4.5.6.tgz",
                },
            },
        }), encoding="utf-8")
        packages, warnings = audit.inventory(self.root)
        self.assertEqual(next(p for p in packages if p["name"] == "internal-service")["public_origin"], "NONPUBLIC_ORIGIN")
        calls = []
        def fake(url, payload=None, timeout=10):
            calls.append((url, payload))
            if url.endswith("querybatch"):
                return {"results": [{"vulns": []}]}, None
            return {"name": "public-service"}, None
        with patch.object(audit, "request_json", side_effect=fake):
            self.assertEqual(audit.verify_online(packages, warnings, 50, 5, False), 1)
        internal = next(p for p in packages if p["name"] == "internal-service")
        self.assertEqual((internal["registry"], internal["osv"]), ("SKIPPED", "NOT_CHECKED"))
        self.assertTrue(all("internal-service" not in str(arg) for call in calls for arg in call))

    def test_python_custom_index_skips_public_api(self):
        (self.root / "requirements.txt").write_text(
            "--index-url https://repo.example.internal/simple\ninternal-lib==9.8.7\n", encoding="utf-8")
        packages, warnings = audit.inventory(self.root)
        self.assertEqual(packages[0]["public_origin"], "NONPUBLIC_ORIGIN")
        self.assertTrue(any("Custom Python package index" in x for x in warnings))
        with patch.object(audit, "request_json", side_effect=AssertionError("network called")):
            self.assertEqual(audit.verify_online(packages, warnings, 50, 5, False), 0)
        self.assertEqual(packages[0]["registry"], "SKIPPED")
        self.assertEqual(packages[0]["osv"], "NOT_CHECKED")

    def test_unknown_origin_requires_manual_review_warning(self):
        (self.root / "package-lock.json").write_text(json.dumps({
            "lockfileVersion": 3,
            "packages": {"node_modules/unknown-origin": {"version": "1.0.0"}},
        }), encoding="utf-8")
        packages, _ = audit.inventory(self.root)
        self.assertEqual(packages[0]["public_origin"], "UNKNOWN")

    def test_max_packages_leave_others_unchecked(self):
        packages = [audit.record("PyPI", f"public-{i}", "1.0.0", f"req:{i}", True) for i in range(3)]
        warnings = []
        with patch.object(audit, "request_json", return_value=({"results": [{"vulns": []}]}, None)):
            audit.verify_online(packages, warnings, 1, 5, False)
        self.assertEqual(packages[1]["registry"], "NOT_CHECKED")
        self.assertTrue(any("limited" in s for s in warnings))


if __name__ == "__main__":
    unittest.main()
