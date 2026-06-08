---
name: asset-doc-maker
description: Creates and updates developer-facing documentation (README.md, details.md) for skills in src/skills/ under docs/skills/. Use when documenting new skills or updating existing skill explanations.
---

# Asset Document Maker (asset-doc-maker)

Creates and maintains developer-facing explanations for agent skills.

## Triggers

- Explicit request to document a skill.
- New skill added in `src/skills/`.
- Existing skill behavior, variables, or guidelines updated.

## Exclusions

- Implementing or fixing code logic (use `coder` skill).
- Creating global agent rules in `/.agents/rules/` or coder references in `src/skills/coder/references/`.

## Constraints

1. **Symmetrical Structure**: Documents must map from `src/` to `docs/`:
   - Target: `src/skills/<skill-name>/`
   - Output: `docs/skills/<skill-name>/`
2. **README & Splitting**:
   - `README.md` is mandatory for each documented skill.
   - Split complex or long topics (e.g., >200 lines, troubleshooting, config) into separate files (e.g., `details.md`, `troubleshooting.md`) and link them relatively from `README.md`.
3. **No Absolute Paths**: Use relative path links only; do not write `file://` links.

---

## Folder Structure

```text
workspace/
├── src/skills/<skill-name>/SKILL.md    (Agent instructions)
└── docs/skills/<skill-name>/
    ├── README.md                       (Mandatory: Overview, usage, entry point)
    └── [details].md                    (Optional: Split detailed pages)
```

---

## Workflow

1. **Analyze Target**: Read `src/skills/<skill-name>/SKILL.md` and related code to understand trigger/exclusion/procedures.
2. **Plan Structure**: Determine if a single `README.md` is sufficient or if multi-file splitting is needed.
3. **Write Documentation**: Create `docs/skills/<skill-name>/README.md` containing:
   - **Overview**: Purpose and description.
   - **Key Features**: Mechanism and capabilities.
   - **Usage**: Invocation format, inputs, parameters, and outputs.
   - **Examples**: Clean, runnable scenarios.
4. **Validate**: Verify markdown formatting and ensure all links are valid relative paths.
