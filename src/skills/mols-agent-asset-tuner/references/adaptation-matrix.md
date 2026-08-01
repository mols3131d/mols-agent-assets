# Adaptation Matrix

Classify every behavior-bearing or execution-bearing source component.

| Decision | Meaning |
| --- | --- |
| `Keep` | Compatible and useful without change |
| `Adapt` | Preserve purpose while changing terminology, paths, tools, or workflow |
| `Replace` | Project-native mechanism provides the same required outcome |
| `Drop` | Not needed, unsafe, redundant, or conflicts with project policy |
| `Defer` | Decision depends on unavailable evidence or capability |

## Required Columns

| Component | Source behavior | Project evidence | Decision | Target implementation | Risk | Validation |
| --- | --- | --- | --- | --- | --- | --- |

## Rules

- Do not preserve source structure merely because it exists.
- Do not drop behavior without recording whether it was required.
- Use `Replace` rather than `Adapt` when the project has a canonical equivalent.
- Use `Defer`, not guessing, for decision-critical unknowns.
- Keep portable behavior separate from runtime adapters.
