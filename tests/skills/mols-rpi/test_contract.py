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


def test_rpi_is_orchestration_not_domain_replacement() -> None:
    _, body = load()
    body = compact(body)
    assert "orchestration method, not the task-domain capability" in body
    assert "Keep applicable task-specific Skills, tools, and governing procedures in force" in body
    assert "does not replace more specific task authority" in body


def test_arguments_are_auto_first_and_invariant_bounded() -> None:
    _, body = load()
    body = compact(body)
    required = [
        "## Arguments",
        "target: <auto> goal: <auto> terminal: <auto> scope: <auto> scope_policy: <auto>",
        "research: <auto> recursion: <auto> max_total_loops: <auto> progress: <auto> output: <auto>",
        "Explicit values win over `<auto>`",
        "`scope_policy` — `adaptive`, `narrow-only`, `fixed`, or `<auto>`",
        "`research` — `internal`, `external`, `mixed`, or `<auto>`",
        "`recursion` — `prefer`, `off`, or `<auto>`",
        "`max_total_loops` — integer `1..30` or `<auto>`",
        "no argument may raise the hard cap above 30",
        "Arguments may narrow behavior, but they never authorize side effects",
    ]
    for phrase in required:
        assert phrase in body


def test_heading_hierarchy_is_grouped_by_responsibility() -> None:
    _, body = load()
    headings = [
        "# Interface",
        "# Runtime",
        "# Execution",
        "# Adaptive Control",
        "# Reporting and Output",
    ]
    positions = [body.index(heading) for heading in headings]
    assert positions == sorted(positions)

    interface = body[positions[0] : positions[1]]
    runtime = body[positions[1] : positions[2]]
    execution = body[positions[2] : positions[3]]
    control = body[positions[3] : positions[4]]

    assert "## Arguments" in interface
    assert "## Activation" in interface
    assert "## Core Lifecycle" in runtime
    assert "## Run and Loop" in runtime
    assert "## Scope Control" in runtime
    assert "## Artifacts" in execution
    assert "## Stages" in execution
    assert "### Research" in execution
    assert "### Plan" in execution
    assert "### Implementation" in execution
    assert "### Review" in execution
    assert "## Goal-State Convergence" in control
    assert "## Recursive Resolution" in control
    assert "## Run Boundary and Handoff" in control


def test_run_has_one_global_hard_loop_ceiling() -> None:
    _, body = load()
    body = compact(body)
    assert "max_total_loops: 30" in body
    assert "loops_used" in body
    assert "Parent and recursive child Loops share `loops_used`" in body
    assert "no separate per-scope Loop limit" in body
    assert "no fixed recursion-depth limit" in body
    assert "Never hide a reset" in body


def test_scope_is_explicit_dynamic_and_bounded() -> None:
    _, body = load()
    body = compact(body)
    required = [
        "## Scope Control",
        "Active Scope - Goal - In scope - Out of scope - Acceptance conditions",
        "At Run start, establish a provisional Active Scope",
        "infer the smallest scope sufficient to pursue the Goal",
        "Work stays inside the Active Scope",
        "Out-of-scope findings may inform Research or Review",
        "Narrowing is adaptive",
        "Expansion is consequential",
        "the proposal does not change the Active Scope",
        "Research must validate the need and boundary",
        "smallest justified boundary delta",
        "Explicit boundaries are not silently mutable",
        "new authority from the source that set that boundary",
        "Scope change never resets controls",
        "Recursive Scope only narrows",
        "strict subset of its parent Scope",
        "do not expand the child locally",
    ]
    for phrase in required:
        assert phrase in body


def test_diagrams_are_split_by_control_concern() -> None:
    _, body = load()
    assert body.count("```mermaid") == 4
    assert "## Model" not in body

    headings = [
        "## Core Lifecycle",
        "## Scope Control",
        "## Recursive Resolution",
        "## Run Boundary and Handoff",
    ]
    positions = [body.index(heading) for heading in headings]
    assert positions == sorted(positions)

    core = body[positions[0] : body.index("## Run and Loop")]
    scope = body[positions[1] : body.index("# Execution")]
    recursion = body[positions[2] : positions[3]]
    boundary = body[positions[3] : body.index("# Reporting and Output")]

    for section in (core, scope, recursion, boundary):
        assert section.count("```mermaid") == 1

    assert "Expansion proposal" not in core
    assert "Child RPI" not in core
    assert "HANDOFF" not in core
    assert "Child RPI" not in scope
    assert "HANDOFF" not in scope
    assert "Expand Active Scope" not in recursion
    assert "HANDOFF" not in recursion
    assert "Child RPI" not in boundary
    assert "Expand Active Scope" not in boundary


def test_recursion_is_review_gated_and_authority_cannot_expand() -> None:
    _, body = load()
    body = compact(body)
    assert "push a child scope only from Review" in body
    assert "every recursive descent" in body
    assert "preceded by a counted substantive Loop" in body
    assert "A child may narrow these boundaries, never expand or replace them." in body


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
    required = [
        "continuation boundary",
        "start no new Loop",
        "preserve `loops_used`, the effective ceiling, the active scope path",
        "current Active Scope definition",
        "pending Scope proposals",
        "validating inherited Research, Active Scope, pending Scope proposals, Plan",
        "mark the Run as handed off, not complete",
        "Handoff does not itself authorize or auto-start another Run",
        "**HANDOFF**",
    ]
    for phrase in required:
        assert phrase in body
