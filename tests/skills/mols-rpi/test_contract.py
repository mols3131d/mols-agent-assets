from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / "mols-rpi" / "SKILL.md"


def load() -> tuple[dict[str, object], str]:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end >= 0
    frontmatter = yaml.safe_load(text[4:end])
    assert isinstance(frontmatter, dict)
    return frontmatter, text[end + 5 :]


def compact(text: str) -> str:
    return " ".join(text.split())


def test_activation_keeps_method_intent_but_excludes_generic_repeat() -> None:
    frontmatter, body = load()
    description = frontmatter["description"]
    assert isinstance(description, str)
    body = compact(body)

    assert "requests RPI" in description
    assert "asks to loop" in description
    assert "recursive loop/재귀 루프" in description
    assert "complex multi-step" in description
    assert "generic content repetition" in description
    assert "asks to loop, repeat" not in description
    assert "only asks to repeat content without iterative work" in body


def test_run_has_one_global_hard_loop_ceiling() -> None:
    _, body = load()
    body = compact(body)
    assert "max_total_loops: 30" in body
    assert "loops_used" in body
    assert "Parent and recursive child Loops share `loops_used`" in body
    assert "no separate per-scope Loop limit" in body
    assert "no fixed recursion-depth limit" in body
    assert "Never hide a reset" in body


def test_recursion_is_review_gated_and_authority_cannot_expand() -> None:
    _, body = load()
    body = compact(body)
    assert "Push a child scope only from Review" in body
    assert "every recursive descent" in body
    assert "preceded by a counted substantive Loop" in body
    assert "A child may narrow these boundaries, never expand them." in body


def test_artifact_order_and_permission_boundary_are_explicit() -> None:
    _, body = load()
    body = compact(body)
    assert "Research precedes Plan" in body
    assert "Plan precedes Work" in body
    assert "Review precedes acceptance" in body
    assert "Retrospective Research or Plan" in body
    assert "A Plan is methodological authorization, not operational permission." in body


def test_loop_exhaustion_is_a_handoff_boundary() -> None:
    _, body = load()
    body = compact(body)
    assert "continuation boundary" in body
    assert "start no new Loop" in body
    assert "preserve `loops_used`, the effective ceiling, the active scope path" in body
    assert "mark the Run as handed off, not complete" in body
    assert "Handoff does not itself authorize or auto-start another Run" in body
    assert "**HANDOFF**" in body
