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


def section(body: str, start: str, end: str | None = None) -> str:
    begin = body.index(start)
    finish = body.index(end, begin + len(start)) if end else len(body)
    return body[begin:finish]


def test_description_owns_discovery_without_body_trigger_duplication() -> None:
    frontmatter, body = load()
    description = frontmatter["description"]
    assert isinstance(description, str)

    required = [
        "requests RPI",
        "RPI(R)",
        "loop/loops/loop it/루프",
        "recursive loop/재귀 루프",
        "improvement loop/개선 루프",
        "deep loop/심층 루프",
        "equivalent repeated research/planning/work/review or recursive improvement",
        "evidence gathering or reconciliation before consequential decisions",
        "an explicit Plan before consequential Work",
        "multiple acceptance conditions or coupled workstreams",
        "repeated verification or likely replanning",
        "narrower subproblem resolution",
        "costly rework from hidden assumptions or uncertainty",
        "loop is merely the topic, identifier, or code concept",
        "only asks to repeat content without iterative work",
        "merely because a task is long",
        "trivial work where explicit prerequisite artifacts add no meaningful control",
    ]
    for phrase in required:
        assert phrase in description

    assert "## Activation" not in body
    assert "### Explicit method intent" not in body
    assert "### Complexity intent" not in body
    assert "Use this Skill when the user asks" not in body


def test_rpi_is_orchestration_not_domain_replacement() -> None:
    _, body = load()
    body = compact(body)
    assert "orchestration method, not the task-domain capability" in body
    assert "Keep applicable task-specific Skills, tools, and governing procedures in force" in body
    assert "does not replace more specific task authority" in body


def test_arguments_own_choices_not_runtime_semantics() -> None:
    _, body = load()
    arguments = compact(section(body, "# Arguments", "# Runtime"))

    required = [
        "target: <auto> goal: <auto> terminal: <auto> scope: <auto> scope_policy: <auto>",
        "research: <auto> recursion: <auto> max_total_loops: <auto> progress: <auto> output: <auto>",
        "| `scope_policy` | `adaptive`, `narrow-only`, `fixed` | Scope Control |",
        "| `research` | `internal`, `external`, `mixed` | Research |",
        "| `recursion` | `prefer`, `off` | Recursive Resolution |",
        "| `max_total_loops` | integer `1..30` | Run and Loop |",
        "Arguments choose behavior; their owning sections define it.",
        "Arguments never authorize side effects",
    ]
    for phrase in required:
        assert phrase in arguments

    forbidden = [
        "permits bounded narrowing",
        "pushes a qualifying narrower child",
        "reports material transitions",
        "uses the hard Run ceiling of `30` while still stopping early",
    ]
    for phrase in forbidden:
        assert phrase not in arguments


def test_heading_hierarchy_is_grouped_by_responsibility() -> None:
    _, body = load()
    headings = [
        "# Arguments",
        "# Runtime",
        "# Execution",
        "# Adaptive Control",
        "# Reporting and Output",
    ]
    positions = [body.index(heading) for heading in headings]
    assert positions == sorted(positions)

    runtime = section(body, "# Runtime", "# Execution")
    execution = section(body, "# Execution", "# Adaptive Control")
    control = section(body, "# Adaptive Control", "# Reporting and Output")

    for heading in ("## Core Lifecycle", "## Run and Loop", "## Scope Control"):
        assert heading in runtime
    for heading in ("## Artifacts", "## Stages", "### Research", "### Plan", "### Implementation", "### Review"):
        assert heading in execution
    for heading in ("## Goal-State Convergence", "## Recursive Resolution", "## Run Boundary and Handoff"):
        assert heading in control


def test_run_has_one_global_hard_loop_ceiling() -> None:
    _, body = load()
    run = compact(section(body, "## Run and Loop", "## Scope Control"))
    required = [
        "max_total_loops: 30",
        "loops_used",
        "Parent and recursive child Loops share `loops_used`",
        "no separate per-scope Loop limit",
        "no fixed recursion-depth limit",
        "Never hide a reset",
    ]
    for phrase in required:
        assert phrase in run


def test_scope_control_owns_current_scope_changes_only() -> None:
    _, body = load()
    scope = compact(section(body, "## Scope Control", "# Execution"))
    required = [
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
        "Scope changes preserve controls",
        "Recursive child boundaries are owned by `Recursive Resolution`",
    ]
    for phrase in required:
        assert phrase in scope

    assert "strict subset of its parent Scope" not in scope
    assert "do not expand the child locally" not in scope


def test_review_classifies_and_dispatches_without_reimplementing_controls() -> None:
    _, body = load()
    review = compact(section(body, "### Review", "# Adaptive Control"))
    required = [
        "Review **classifies and dispatches**",
        "| evidence, plan, or bounded Work gap | Core Lifecycle |",
        "| Scope boundary change | Scope Control |",
        "| saturation or no credible gain | Goal-State Convergence |",
        "| narrower material blocker | Recursive Resolution |",
        "| accepted terminal, blocking boundary, or Loop ceiling | Run Boundary and Handoff |",
    ]
    for phrase in required:
        assert phrase in review

    forbidden = [
        "propose smallest justified expansion → Research → Plan",
        "Push a recursive child only when",
        "Finish Review and hand off",
        "Change source/method/perspective",
    ]
    for phrase in forbidden:
        assert phrase not in review


def test_diagrams_are_split_by_control_concern() -> None:
    _, body = load()
    assert body.count("```mermaid") == 4
    assert "## Model" not in body

    core = section(body, "## Core Lifecycle", "## Run and Loop")
    scope = section(body, "## Scope Control", "# Execution")
    recursion = section(body, "## Recursive Resolution", "## Run Boundary and Handoff")
    boundary = section(body, "## Run Boundary and Handoff", "# Reporting and Output")

    for concern in (core, scope, recursion, boundary):
        assert concern.count("```mermaid") == 1

    assert "Expansion proposal" not in core
    assert "Child RPI" not in core
    assert "HANDOFF" not in core
    assert "Child RPI" not in scope
    assert "HANDOFF" not in scope
    assert "Expand Active Scope" not in recursion
    assert "HANDOFF" not in recursion
    assert "Child RPI" not in boundary
    assert "Expand Active Scope" not in boundary


def test_recursion_owns_child_scope_and_reuses_run_accounting() -> None:
    _, body = load()
    recursion = compact(section(body, "## Recursive Resolution", "## Run Boundary and Handoff"))
    required = [
        "push a child scope only from Review",
        "strict subset of the parent Active Scope",
        "A child may narrow these boundaries, never expand or replace them.",
        "Every recursive descent is Review-gated and uses the existing `Run and Loop` accounting",
        "it never creates or resets a Run",
        "do not expand the child locally",
    ]
    for phrase in required:
        assert phrase in recursion

    assert "There is no separate per-scope Loop limit" not in recursion
    assert "run-wide Loop ceiling keeps" not in recursion


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
    boundary = compact(section(body, "## Run Boundary and Handoff", "# Reporting and Output"))
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
        assert phrase in boundary
