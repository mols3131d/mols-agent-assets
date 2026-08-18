#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "scenarios"
RESULTS = ROOT / "tests" / "results"

REQUIRED_PACKAGE_FILES = {
    "SKILL.md",
    "README.md",
    "references/inspection-rules.md",
    "references/rule-sources.md",
    "references/report-format.md",
    "references/example-report.md",
    "tests/README.md",
    "tests/run_tests.py",
}
REQUIRED_REPORT_KEYS = [
    "title", "description", "created", "updated", "author", "type",
    "repository", "target", "coverage", "snapshot",
]
REMOVED_REPORT_KEYS = {"artifact_type", "result", "generator", "schema_version", "test_fixture"}
GAP_TYPES = {"contradiction", "omission", "drift", "stale-reference", "revision-mismatch", "handoff-gap", "validation-gap"}
RESULT_STATES = {"findings", "incomplete", "no-verified-findings"}
COVERAGE_STATES = {"bounded-complete", "partial", "blocked"}
ROOT_CAUSE_TO_GAP = {
    "revision-context": "revision-mismatch",
    "reference-target": "stale-reference",
    "implementation-validation": "validation-gap",
    "handoff-transfer": "handoff-gap",
    "required-counterpart-absence": "omission",
    "asymmetric-change": "drift",
    "simultaneous-assertion": "contradiction",
}

@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str = ""


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("front matter opening delimiter is missing")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("front matter closing delimiter is missing")
    values: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1].isspace():
            continue
        if ":" not in raw:
            raise AssertionError(f"invalid front matter line: {raw}")
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def expected_gap_type(data: dict[str, Any]) -> str | None:
    cause = data.get("root_cause")
    if cause is None:
        return None
    return ROOT_CAUSE_TO_GAP[cause]


def expected_status(data: dict[str, Any]) -> str | None:
    if data.get("root_cause") is None:
        return None
    if data.get("root_cause") == "required-counterpart-absence":
        if data.get("zero_result_only") or not data.get("bounded_absence"):
            return "unresolved"
    if data.get("direct_evidence") and data.get("counterevidence_checked"):
        return "verified"
    return "unresolved"


def expected_result(data: dict[str, Any]) -> str:
    if data.get("verified_findings", 0) > 0:
        return "findings"
    if data.get("unresolved_candidates", 0) > 0 or data.get("material_blocker"):
        return "incomplete"
    return "no-verified-findings"


def expected_coverage(data: dict[str, Any]) -> str:
    if not data.get("primary_access", False):
        return "blocked"
    if data.get("repository_wide_sampling") or data.get("material_blocker") or data.get("zero_result_only"):
        return "partial"
    if data.get("root_cause") is not None and not data.get("counterevidence_checked"):
        return "partial"
    return "bounded-complete"


def resolve_rule_sources(rule_sources: Any, auto_candidates: list[str]) -> list[str]:
    items = ["auto"] if rule_sources == "auto" else list(rule_sources)
    if items.count("auto") > 1:
        raise AssertionError("auto may appear at most once")
    expanded: list[str] = []
    for item in items:
        candidates = auto_candidates if item == "auto" else [item]
        for source in candidates:
            if source not in expanded:
                expanded.append(source)
    return expanded


def output_filename(repository: str, target: str | None, stamp: str, revision: int = 1, ext: str = "md") -> str:
    repo = re.sub(r"[^a-z0-9]+", "-", repository.lower()).strip("-")
    target_part = ""
    if target:
        target_part = "-" + re.sub(r"[^a-z0-9]+", "-", target.lower()).strip("-")
    revision_part = "" if revision == 1 else f"-r{revision}"
    return f"{repo}-artifact-consistency-report{target_part}{revision_part}-{stamp}.{ext}"


def run_case(name: str, fn) -> TestResult:
    try:
        fn()
        return TestResult(name, True)
    except Exception as exc:  # noqa: BLE001
        return TestResult(name, False, str(exc))


def test_package_structure() -> None:
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
    missing = REQUIRED_PACKAGE_FILES - actual
    assert not missing, f"missing package files: {sorted(missing)}"
    assert not any(part == ".docs" for p in ROOT.rglob("*") for part in p.relative_to(ROOT).parts)


def test_skill_front_matter() -> None:
    fm = parse_front_matter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    assert fm.get("name") == "artifact-consistency-inspector"
    assert fm.get("description")


def test_reference_integrity() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for rel in ["references/inspection-rules.md", "references/rule-sources.md", "references/report-format.md", "references/example-report.md"]:
        assert rel in skill, f"SKILL.md does not reference {rel}"
        assert (ROOT / rel).exists(), f"referenced file missing: {rel}"
    assert "tests/" in skill and "development-facing" in skill


def test_no_coding_agent_defaults() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    forbidden = ["report_root", "arguments.paths", "openspec/specs/", "target: vscode", "tools: [read, search, execute, edit]"]
    for token in forbidden:
        assert token not in skill, f"coding-agent residue found: {token}"
    assert "Do not use a fixed directory list" in skill
    assert "remote evidence source" in skill


def test_read_only_contract() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for phrase in [
        "Use read-only repository and web retrieval only",
        "Never create, edit, delete, commit, comment on, label, merge",
        "Never invoke repository write actions",
    ]:
        assert phrase in skill, f"read-only phrase missing: {phrase}"


def test_rule_sources_contract() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    doc = (ROOT / "references" / "rule-sources.md").read_text(encoding="utf-8")
    assert "rule_sources: auto" in skill
    assert "ordered list" in skill
    assert "expands in place" in skill
    assert "universal category order" in skill
    assert "universal precedence" in doc
    forbidden_fixed_orders = [
        "policy documents always outrank",
        "configuration always outrank",
        "specification always outrank",
    ]
    for phrase in forbidden_fixed_orders:
        assert phrase not in (skill + doc).lower()


def test_report_front_matter() -> None:
    fm = parse_front_matter((ROOT / "references" / "example-report.md").read_text(encoding="utf-8"))
    assert list(fm.keys()) == REQUIRED_REPORT_KEYS, list(fm.keys())
    assert fm["author"] == "<author>"
    assert fm["type"] == "artifact-consistency-report"
    assert not (REMOVED_REPORT_KEYS & set(fm))
    assert fm["coverage"] in COVERAGE_STATES
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", fm["created"])
    assert fm["created"] == fm["updated"]


def test_report_schema_contract() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fmt = (ROOT / "references" / "report-format.md").read_text(encoding="utf-8")
    example = (ROOT / "references" / "example-report.md").read_text(encoding="utf-8")
    for key in REQUIRED_REPORT_KEYS:
        assert f"{key}:" in fmt, f"report-format missing {key}"
    for key in REMOVED_REPORT_KEYS:
        assert f"{key}:" not in fmt, f"removed field remains: {key}"
    assert "| Result |" in fmt and "| Coverage |" in fmt
    assert "Resolved rule sources:" in fmt
    assert "Rule-source conflicts:" in fmt
    assert "front matter" in skill.lower()
    for heading in ["#### Observed difference", "#### References", "#### Potential impact"]:
        assert heading in fmt and heading in example, f"compact heading missing: {heading}"
    assert "#### Why unresolved" in fmt and "#### Why unresolved" in example
    for legacy in ["**Expected:**", "**Actual:**", "**Evidence:**", "**Counterevidence checked:**", "**Impact:**"]:
        assert legacy not in fmt + example, f"legacy detailed field remains: {legacy}"


def test_compact_report_example() -> None:
    text = (ROOT / "references" / "example-report.md").read_text(encoding="utf-8")
    assert "| Result | `findings` |" in text
    assert "| Coverage | `bounded-complete` |" in text
    sections = text.split("\n### CON-")[1:]
    assert len(sections) >= 3
    unresolved_count = 0
    for section in sections:
        assert section.count("#### Observed difference") == 1
        assert section.count("#### References") == 1
        assert section.count("#### Potential impact") == 1
        if "**Status:** `unresolved`" in section:
            unresolved_count += 1
            assert section.count("#### Why unresolved") == 1
        else:
            assert "#### Why unresolved" not in section
    assert unresolved_count >= 1


def test_filename_rules() -> None:
    stamp = "202608042327"
    base = output_filename("refund-service", "refund-processing-v2", stamp)
    dup = output_filename("refund-service", "refund-processing-v2", stamp, revision=2)
    zipped = output_filename("refund-service", "refund-processing-v2", stamp, ext="zip")
    assert base == "refund-service-artifact-consistency-report-refund-processing-v2-202608042327.md"
    assert dup == "refund-service-artifact-consistency-report-refund-processing-v2-r2-202608042327.md"
    assert zipped.endswith("-202608042327.zip")
    pattern = re.compile(r"^[a-z0-9-]+(?:-r[2-9][0-9]*)?-\d{12}\.(?:md|zip)$")
    assert pattern.fullmatch(base) and pattern.fullmatch(dup) and pattern.fullmatch(zipped)


def test_gap_scenarios() -> None:
    files = sorted(SCENARIOS.glob("*.json"))
    count = 0
    for path in files:
        scenario = json.loads(path.read_text(encoding="utf-8"))
        if "input" not in scenario:
            continue
        count += 1
        data = scenario["input"]
        actual = {
            "gap_type": expected_gap_type(data),
            "status": expected_status(data),
            "result": expected_result(data),
            "coverage": expected_coverage(data),
        }
        assert actual == scenario["expected"], f"{scenario['id']}: {actual}"
        if actual["gap_type"] is not None:
            assert actual["gap_type"] in GAP_TYPES
        assert actual["result"] in RESULT_STATES
        assert actual["coverage"] in COVERAGE_STATES
    assert count >= 8


def test_rule_source_scenarios() -> None:
    files = sorted(SCENARIOS.glob("rule-sources-*.json"))
    assert len(files) >= 3
    for path in files:
        scenario = json.loads(path.read_text(encoding="utf-8"))
        resolved = resolve_rule_sources(scenario["rule_sources"], scenario["auto_candidates"])
        assert resolved == scenario["expected_resolved"], f"{scenario['id']}: {resolved}"
        conflict = "none"
        pairs = scenario.get("conflicting_pairs", [])
        tiers = scenario.get("authority_tiers", {})
        if any(tiers.get(a) == tiers.get(b) for a, b in pairs):
            conflict = "unresolved-tier"
        assert conflict == scenario["expected_conflict"]


def test_inferred_convention_scenario() -> None:
    scenario = json.loads((SCENARIOS / "inferred-convention-unresolved.json").read_text(encoding="utf-8"))
    status = "verified" if scenario["mandatory_established"] and scenario["direct_evidence"] and scenario["counterevidence_checked"] else "unresolved"
    assert status == scenario["expected_status"]


def test_zip_shape() -> None:
    tmp = RESULTS / ".package-shape-test.zip"
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(ROOT.rglob("*")):
                if p.is_file() and p != tmp:
                    zf.write(p, Path(ROOT.name) / p.relative_to(ROOT))
        with zipfile.ZipFile(tmp) as zf:
            names = zf.namelist()
            assert f"{ROOT.name}/SKILL.md" in names
            assert f"{ROOT.name}/README.md" in names
            assert f"{ROOT.name}/references/rule-sources.md" in names
            assert any(n.startswith(f"{ROOT.name}/tests/scenarios/") for n in names)
            assert not any("/.docs/" in n for n in names)
            assert all(not n.startswith("/") for n in names)
            assert zf.testzip() is None
    finally:
        tmp.unlink(missing_ok=True)


def write_report(results: list[TestResult]) -> Path:
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).replace(second=0, microsecond=0)
    stamp = now.strftime("%Y%m%d%H%M")
    iso = now.isoformat()
    passed = sum(r.passed for r in results)
    failed = len(results) - passed
    path = RESULTS / f"artifact-consistency-inspector-test-report-{stamp}.md"
    lines = [
        "---",
        'title: "Artifact Consistency Inspector Test Report"',
        'description: "Deterministic package and scenario contract test results."',
        f'created: "{iso}"',
        f'updated: "{iso}"',
        'author: "<author>"',
        'type: "skill-test-report"',
        f'package: "{ROOT.name}"',
        f'status: "{"passed" if failed == 0 else "failed"}"',
        "---", "", "# Artifact Consistency Inspector Test Report", "", "## Summary", "",
        f"- Tests: `{len(results)}`", f"- Passed: `{passed}`", f"- Failed: `{failed}`",
        "- Scope: package structure, references, report contract, filename rules, rule-source resolution, and deterministic decision scenarios",
        "- Limitation: live ChatGPT repository retrieval and model reasoning are not executed", "", "## Results", "",
    ]
    for result in results:
        marker = "PASS" if result.passed else "FAIL"
        suffix = f" — {result.detail}" if result.detail else ""
        lines.append(f"- **{marker}** `{result.name}`{suffix}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    tests = [
        ("package-structure", test_package_structure),
        ("skill-front-matter", test_skill_front_matter),
        ("reference-integrity", test_reference_integrity),
        ("no-coding-agent-defaults", test_no_coding_agent_defaults),
        ("read-only-contract", test_read_only_contract),
        ("rule-sources-contract", test_rule_sources_contract),
        ("report-front-matter", test_report_front_matter),
        ("report-schema-contract", test_report_schema_contract),
        ("compact-report-example", test_compact_report_example),
        ("filename-rules", test_filename_rules),
        ("gap-scenarios", test_gap_scenarios),
        ("rule-source-scenarios", test_rule_source_scenarios),
        ("inferred-convention-scenario", test_inferred_convention_scenario),
        ("zip-shape", test_zip_shape),
    ]
    results = [run_case(name, fn) for name, fn in tests]
    report = write_report(results)
    for result in results:
        print(f"{'PASS' if result.passed else 'FAIL'} {result.name}{': ' + result.detail if result.detail else ''}")
    print(f"REPORT {report}")
    return 0 if all(r.passed for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())
