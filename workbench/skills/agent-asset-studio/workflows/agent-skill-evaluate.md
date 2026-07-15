# Evaluate Agent Skill

## Goal

Evaluate one existing agent skill's effectiveness and report actionable findings without modifying it.

## Required Inputs

- Existing skill path
- Evaluation scope, or full quality review when no narrower scope is given

## Procedure

1. List the target files with `rg --files <skill-dir>`.
2. Read the frontmatter and only the files needed to assess the requested scope.
3. Check trigger precision, near-miss exclusions, output contract, instruction clarity, context cost, and resource boundaries.
4. For routing skills, read `references/routing-skill-structure.md` and assess whether requests select the minimum correct workflow.
5. Report findings by severity with file locations, evidence, and the smallest corrective action. State explicitly when no findings remain.

## Validation

- The report covers the requested quality scope and separates findings from skipped checks.
- Each finding includes evidence, impact, and a minimal correction.
- Structural conformance requests route to `agent-skill-validate` instead.

## Resources

- Read `references/routing-skill-structure.md` only when evaluating a routing skill.

## Stop Conditions

- Do not edit files during evaluation unless the user also requests fixes.
- Stop and report any check requiring unavailable tools, permissions, or external state.
