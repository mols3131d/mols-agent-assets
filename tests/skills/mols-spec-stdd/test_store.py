"""Deterministic tests for change promotion into hierarchical domain specifications."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/rulesync/.rulesync/skills/mols-spec-stdd/scripts/store.py"
OLD = """# payments/refunds/validation Specification

## Purpose

Validate refunds.

## Requirements

### Requirement: Check amount
The system MUST reject negative amounts.

#### Scenario: Negative input
- WHEN amount is negative
- THEN validation fails

### Requirement: Keep history
The system SHALL retain audit history.

#### Scenario: History lookup
- WHEN history is requested
- THEN records are returned

## Notes

This extra canonical note must survive.
"""
DOMAIN = "payments/refunds/validation"


def invoke(store: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(store), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def review(tmp_path: Path, result: str = "pass", evidence: list[str] | None = None) -> Path:
    path = tmp_path / "review.json"
    path.write_text(json.dumps({
        "result": result,
        "evidence": ["tests/ci#passed"] if evidence is None else evidence,
        "findings": [],
    }), encoding="utf-8")
    return path


def main_spec(store: Path, domain: str = DOMAIN) -> Path:
    return store / "specs" / domain / "spec.md"


def write_delta(store: Path, change: str, domain: str, operations: str,
                existing: str | None = None, *, purpose: str = "") -> Path:
    digest = ("absent" if existing is None
              else hashlib.sha256(existing.encode("utf-8")).hexdigest())
    path = store / "changes" / change / "specs" / domain / "spec.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Delta for {domain}\n\n<!-- base-sha256: {digest} -->\n\n"
        + (f"## Purpose\n\n{purpose}\n\n" if purpose else "")
        + operations + "\n",
        encoding="utf-8",
    )
    return path


def test_preview_is_read_only_and_deep_domain_archive_preserves_context(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    current.write_text(OLD, encoding="utf-8")
    change = store / "changes" / "refund-validation"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text("# Why refunds need validation\n", encoding="utf-8")
    write_delta(store, "refund-validation", DOMAIN, """## MODIFIED Requirements

### Requirement: Check amount
The system MUST reject negative and over-limit amounts.

#### Scenario: Invalid input
- WHEN the amount is negative or too large
- THEN validation fails

## ADDED Requirements

### Requirement: Validate currency
The system SHALL accept only configured currencies.

#### Scenario: Unknown currency
- WHEN currency is unknown
- THEN validation fails
""", OLD)
    record = review(tmp_path)
    args = ("archive", "refund-validation", "--review", str(record),
            "--date", "2026-11-03")
    preview = invoke(store, *args)
    assert preview.returncode == 0, preview.stderr
    result = json.loads(preview.stdout)
    assert result["status"] == "ready_to_archive"
    assert result["updated_specs"] == [f"specs/{DOMAIN}/spec.md"]
    assert result["archive"] == "changes/archive/2026-11-03-refund-validation"
    assert current.read_text(encoding="utf-8") == OLD
    assert change.is_dir()

    apply = invoke(store, *args, "--apply")
    assert apply.returncode == 0, apply.stderr
    applied = json.loads(apply.stdout)
    assert applied["status"] == "archived"
    assert applied["updated_specs"] == result["updated_specs"]
    assert applied["archive"] == result["archive"]
    merged = current.read_text(encoding="utf-8")
    assert "negative and over-limit amounts" in merged
    assert "Validate currency" in merged
    assert "Keep history" in merged
    assert "## Notes\n\nThis extra canonical note must survive." in merged
    assert "## MODIFIED Requirements" not in merged
    archived = store / "changes" / "archive" / "2026-11-03-refund-validation"
    assert (archived / "proposal.md").exists()
    assert (archived / "specs" / DOMAIN / "spec.md").exists()
    assert not change.exists()


def test_new_deep_subdomain_from_absent_baseline(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    domain = "accounts/security/sessions/tokens"
    write_delta(store, "add-tokens", domain, """## ADDED Requirements

### Requirement: Token expiry
The system MUST expire tokens.

#### Scenario: Expired token
- WHEN a token expires
- THEN access is rejected
""", purpose="Keep sessions secure.")
    record = review(tmp_path)
    result = invoke(store, "archive", "add-tokens", "--review", str(record),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 0, result.stderr
    text = main_spec(store, domain).read_text(encoding="utf-8")
    assert "## Purpose\n\nKeep sessions secure." in text
    assert "## Requirements" in text and "Token expiry" in text


def test_removal_only_preserves_other_requirements(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    current.write_text(OLD, encoding="utf-8")
    write_delta(store, "remove-old-check", DOMAIN, """## REMOVED Requirements

### Requirement: Check amount
Obsolete behavior is retired.
""", OLD)
    result = invoke(store, "archive", "remove-old-check", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 0, result.stderr
    merged = current.read_text(encoding="utf-8")
    assert "### Requirement: Check amount" not in merged
    assert "### Requirement: Keep history" in merged


def test_multiple_domains_preflight_failure_writes_nothing(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    current.write_text(OLD, encoding="utf-8")
    write_delta(store, "mixed-change", "accounts/signin", """## ADDED Requirements

### Requirement: Login success
The system SHALL authenticate credentials.
""", purpose="Sign users in.")
    write_delta(store, "mixed-change", DOMAIN, """## MODIFIED Requirements

### Requirement: Does not exist
Wrong baseline target.
""", OLD)
    result = invoke(store, "archive", "mixed-change", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 2
    assert "cannot modify missing requirement" in result.stderr
    assert current.read_text(encoding="utf-8") == OLD
    assert not main_spec(store, "accounts/signin").exists()
    assert (store / "changes" / "mixed-change").exists()


def test_stale_baseline_rejects_concurrent_modification(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    current.write_text(OLD, encoding="utf-8")
    write_delta(store, "modify-amount", DOMAIN, """## MODIFIED Requirements

### Requirement: Check amount
The system MUST reject all negative amounts and unknown currencies.
""", OLD)
    changed = OLD.replace("Validate refunds.", "Validate refunds and chargebacks.")
    current.write_text(changed, encoding="utf-8")
    result = invoke(store, "archive", "modify-amount", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 2
    assert "stale base" in result.stderr
    assert current.read_text(encoding="utf-8") == changed


@pytest.mark.parametrize(("section", "expected"), [
    ("""## ADDED Requirements

### Requirement: Check amount
The system SHALL permit negatives.
""", "cannot add existing"),
    ("""## REMOVED Requirements

### Requirement: Unknown
No such requirement.
""", "cannot remove missing"),
])
def test_conflicting_operations_rejected(tmp_path: Path, section: str, expected: str) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    current.write_text(OLD, encoding="utf-8")
    write_delta(store, "conflict", DOMAIN, section, OLD)
    result = invoke(store, "archive", "conflict", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 2 and expected in result.stderr
    assert current.read_text(encoding="utf-8") == OLD


def test_cannot_remove_last_domain_requirement(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    current = main_spec(store)
    current.parent.mkdir(parents=True)
    original = """# Accounts Specification

## Requirements

### Requirement: Only rule
The system SHALL support one rule.
"""
    current.write_text(original, encoding="utf-8")
    write_delta(store, "remove-domain", DOMAIN, """## REMOVED Requirements

### Requirement: Only rule
No longer needed.
""", original)
    result = invoke(store, "archive", "remove-domain", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 2
    assert "retiring a whole domain" in result.stderr
    assert current.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("result,evidence", [("blocked", ["some link"]), ("pass", []), ("rework", ["some link"])])
def test_review_gate_rejects_incomplete_changes(tmp_path: Path, result: str, evidence: list[str]) -> None:
    store = tmp_path / "spec"
    write_delta(store, "new-domain", "orders/checkouts", """## ADDED Requirements

### Requirement: Checkout
The system SHALL check out orders.
""", purpose="Handle checkouts.")
    status = invoke(store, "archive", "new-domain",
                    "--review", str(review(tmp_path, result, evidence)), "--apply")
    assert status.returncode == 2
    assert not main_spec(store, "orders/checkouts").exists()


def test_existing_archive_name_blocks_change_without_mutation(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    write_delta(store, "duplicate", "orders/checkouts", """## ADDED Requirements

### Requirement: Checkout
The system SHALL check out orders.
""", purpose="Handle checkouts.")
    occupied = store / "changes" / "archive" / "2026-11-03-duplicate"
    occupied.mkdir(parents=True)
    result = invoke(store, "archive", "duplicate", "--review", str(review(tmp_path)),
                    "--date", "2026-11-03", "--apply")
    assert result.returncode == 2 and "already exists" in result.stderr
    assert not main_spec(store, "orders/checkouts").exists()
    assert (store / "changes" / "duplicate").is_dir()


def test_baseline_absent_and_existing(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    absent = invoke(store, "baseline", "accounts/security/sessions")
    assert absent.returncode == 0
    assert json.loads(absent.stdout)["base_sha256"] == "absent"
    existing = main_spec(store)
    existing.parent.mkdir(parents=True)
    existing.write_text(OLD, encoding="utf-8")
    result = invoke(store, "baseline", DOMAIN)
    assert result.returncode == 0
    assert json.loads(result.stdout)["base_sha256"] == hashlib.sha256(OLD.encode()).hexdigest()


def test_non_delta_files_and_invalid_domain_rejected(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    write_delta(store, "bad-input", "accounts/security", """## ADDED Requirements

### Requirement: Login
The system SHALL authenticate.
""", purpose="Login.")
    (store / "changes" / "bad-input" / "specs" / "accounts" / "security" / "notes.md").write_text(
        "Not a domain spec", encoding="utf-8"
    )
    result = invoke(store, "archive", "bad-input", "--review", str(review(tmp_path)))
    assert result.returncode == 2 and "unexpected file" in result.stderr
    invalid = invoke(store, "baseline", "../outside")
    assert invalid.returncode == 2 and "domain must be" in invalid.stderr


def test_symlink_domain_writes_are_rejected(tmp_path: Path) -> None:
    store = tmp_path / "spec"
    outside = tmp_path / "outside"
    outside.mkdir()
    target = store / "specs"
    store.mkdir()
    try:
        target.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable")
    result = invoke(store, "baseline", DOMAIN)
    assert result.returncode == 2
    assert "symlink path" in result.stderr
