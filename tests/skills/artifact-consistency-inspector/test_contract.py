from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/agentsmesh/skills/artifact-consistency-inspector"
SCENARIOS = Path(__file__).resolve().parent / "scenarios"

REQUIRED_PACKAGE_FILES = {
    "SKILL.md",
    "references/inspection-rules.md",
    "references/rule-sources.md",
    "references/report-format.md",
    "references/example-report.md",
}
REQUIRED_REPORT_KEYS = [
    "title",
    "description",
    "created",
    "updated",
    "author",
    "type",
    "repository",
    "target",
    "coverage",
    "snapshot",
]
REMOVED_REPORT_KEYS = {
    "artifact_type",
    "result",
    "generator",
    "schema_version",
    "test_fixture",
}
GAP_TYPES = {
    "contradiction",
    "omission",
    "drift",
    "stale-reference",
    "revision-mismatch",
    "handoff-gap",
    "validation-gap",
}
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


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("front matter opening delimiter is missing")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("front matter closing delimiter is missing")
    values: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw[:1].isspace():
            continue
        if ":" not in raw:
            raise AssertionError(f"invalid front matter line: {raw}")
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def expected_gap_type(data: dict[str, Any]) -> str | None:
    cause = data.get("root_cause")
    return None if cause is None else ROOT_CAUSE_TO_GAP[cause]


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
    if (
        data.get("repository_wide_sampling")
        or data.get("material_blocker")
        or data.get("zero_result_only")
    ):
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


def output_filename(
    repository: str,
    target: str | None,
    stamp: str,
    revision: int = 1,
    ext: str = "md",
) -> str:
    repo = re.sub(r"[^a-z0-9]+", "-", repository.lower()).strip("-")
    target_part = ""
    if target:
        target_part = "-" + re.sub(r"[^a-z0-9]+", "-", target.lower()).strip("-")
    revision_part = "" if revision == 1 else f"-r{revision}"
    return f"{repo}-artifact-consistency-report{target_part}{revision_part}-{stamp}.{ext}"


def test_package_structure() -> None:
    actual = {str(path.relative_to(SKILL)) for path in SKILL.rglob("*") if path.is_file()}
    missing = REQUIRED_PACKAGE_FILES - actual
    assert not missing, f"missing package files: {sorted(missing)}"
    for name in ("tests", "evals", "scenarios", "results"):
        assert not (SKILL / name).exists(), name


def test_skill_front_matter() -> None:
    fm = parse_front_matter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
    assert fm.get("name") == "artifact-consistency-inspector"
    assert fm.get("description")


def test_reference_integrity() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for rel in [
        "references/inspection-rules.md",
        "references/rule-sources.md",
        "references/report-format.md",
        "references/example-report.md",
    ]:
        assert rel in skill, f"SKILL.md does not reference {rel}"
        assert (SKILL / rel).exists(), f"referenced file missing: {rel}"
    assert "tests/" not in skill


def test_no_coding_agent_defaults() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    forbidden = [
        "report_root",
        "arguments.paths",
        "openspec/specs/",
        "target: vscode",
        "tools: [read, search, execute, edit]",
    ]
    for token in forbidden:
        assert token not in skill, f"coding-agent residue found: {token}"
    assert "Do not use a fixed directory list" in skill
    assert "remote evidence source" in skill


def test_read_only_contract() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in [
        "Use read-only repository and web retrieval only",
        "Never create, edit, delete, commit, comment on, label, merge",
        "Never invoke repository write actions",
    ]:
        assert phrase in skill, f"read-only phrase missing: {phrase}"


def test_rule_sources_contract() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    doc = (SKILL / "references/rule-sources.md").read_text(encoding="utf-8")
    assert "rule_sources: auto" in skill
    assert "ordered list" in skill
    assert "expands in place" in skill
    assert "universal category order" in skill
    assert "universal precedence" in doc
    for phrase in [
        "policy documents always outrank",
        "configuration always outrank",
        "specification always outrank",
    ]:
        assert phrase not in (skill + doc).lower()


def test_report_front_matter() -> None:
    fm = parse_front_matter(
        (SKILL / "references/example-report.md").read_text(encoding="utf-8")
    )
    assert list(fm.keys()) == REQUIRED_REPORT_KEYS
    assert fm["author"] == "<author>"
    assert fm["type"] == "artifact-consistency-report"
    assert not (REMOVED_REPORT_KEYS & set(fm))
    assert fm["coverage"] in COVERAGE_STATES
    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}",
        fm["created"],
    )
    assert fm["created"] == fm["updated"]


def test_report_schema_contract() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fmt = (SKILL / "references/report-format.md").read_text(encoding="utf-8")
    example = (SKILL / "references/example-report.md").read_text(encoding="utf-8")
    for key in REQUIRED_REPORT_KEYS:
        assert f"{key}:" in fmt
    for key in REMOVED_REPORT_KEYS:
        assert f"{key}:" not in fmt
    assert "| Result |" in fmt and "| Coverage |" in fmt
    assert "Resolved rule sources:" in fmt
    assert "Rule-source conflicts:" in fmt
    assert "front matter" in skill.lower()
    for heading in [
        "#### Observed difference",
        "#### References",
        "#### Potential impact",
    ]:
        assert heading in fmt and heading in example
    assert "#### Why unresolved" in fmt and "#### Why unresolved" in example


def test_compact_report_example() -> None:
    text = (SKILL / "references/example-report.md").read_text(encoding="utf-8")
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
    duplicate = output_filename(
        "refund-service", "refund-processing-v2", stamp, revision=2
    )
    zipped = output_filename(
        "refund-service", "refund-processing-v2", stamp, ext="zip"
    )
    assert base == "refund-service-artifact-consistency-report-refund-processing-v2-202608042327.md"
    assert duplicate == "refund-service-artifact-consistency-report-refund-processing-v2-r2-202608042327.md"
    assert zipped.endswith("-202608042327.zip")


def test_gap_scenarios() -> None:
    count = 0
    for path in sorted(SCENARIOS.glob("*.json")):
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
        resolved = resolve_rule_sources(
            scenario["rule_sources"], scenario["auto_candidates"]
        )
        assert resolved == scenario["expected_resolved"], scenario["id"]
        conflict = "none"
        pairs = scenario.get("conflicting_pairs", [])
        tiers = scenario.get("authority_tiers", {})
        if any(tiers.get(a) == tiers.get(b) for a, b in pairs):
            conflict = "unresolved-tier"
        assert conflict == scenario["expected_conflict"]


def test_inferred_convention_scenario() -> None:
    scenario = json.loads(
        (SCENARIOS / "inferred-convention-unresolved.json").read_text(encoding="utf-8")
    )
    status = (
        "verified"
        if scenario["mandatory_established"]
        and scenario["direct_evidence"]
        and scenario["counterevidence_checked"]
        else "unresolved"
    )
    assert status == scenario["expected_status"]


def test_zip_shape(tmp_path: Path) -> None:
    archive = tmp_path / "package-shape-test.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file():
                handle.write(path, Path(SKILL.name) / path.relative_to(SKILL))

    with zipfile.ZipFile(archive) as handle:
        names = handle.namelist()
        assert f"{SKILL.name}/SKILL.md" in names
        assert f"{SKILL.name}/references/rule-sources.md" in names
        assert not any(
            f"/{name}/" in entry
            for entry in names
            for name in ("tests", "evals", "scenarios", "results")
        )
        assert handle.testzip() is None
