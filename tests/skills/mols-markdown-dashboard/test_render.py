from __future__ import annotations

from pathlib import Path

from mols_dashboard.loader import load_dashboard
from mols_dashboard.render import render_dashboard

SKILL_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "rulesync"
    / ".rulesync"
    / "skills"
    / "mols-markdown-dashboard"
)


def test_domain_example_renders_core_tables_and_resets_gap_numbers() -> None:
    dashboard = load_dashboard(SKILL_ROOT / "examples/domain-dashboard.yml")
    markdown = render_dashboard(dashboard)

    assert "| Capability | Implementation Status" in markdown
    assert "| Grain Alignment | 1 | Raw aggregate" in markdown
    assert "| Notebook Runtime | 1 | Valid input" in markdown
    assert "| Notebook Runtime | 2 | Malformed input" in markdown
    assert "🔴 dbt mart aggregate 비교 실패" in markdown
    assert "{{" not in markdown


def test_project_example_uses_domain_row_label() -> None:
    dashboard = load_dashboard(SKILL_ROOT / "examples/project-dashboard.yml")
    markdown = render_dashboard(dashboard)

    assert "| Domain | Implementation Status" in markdown
    assert "| **Total**" in markdown


def test_table_cells_escape_pipe_and_newline(tmp_path: Path) -> None:
    yaml_path = tmp_path / "dashboard.yml"
    yaml_path.write_text(
        """version: 1

dashboard:
  level: domain
  title: Demo
  snapshot: v1
  current_focus: Focus

items:
  - name: A | B
    implementation:
      status: in_progress
      progress: 0/1
      gaps:
        - |-
          first line
          second | line
    verification:
      status: unverified
      progress: 0/1
      gaps:
        - missing | target
""",
        encoding="utf-8",
    )

    markdown = render_dashboard(load_dashboard(yaml_path))

    assert "A \\| B" in markdown
    assert "first line<br>second \\| line" in markdown
    assert "missing \\| target" in markdown


def test_empty_optional_sections_are_omitted() -> None:
    dashboard = load_dashboard(SKILL_ROOT / "examples/project-dashboard.yml")
    markdown = render_dashboard(dashboard)

    assert "## Risks / Blockers" not in markdown
    assert "## References" not in markdown
